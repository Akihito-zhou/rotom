import os
import json
from typing import Tuple
import unicodedata
from urllib.parse import quote

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pokemon-dataset-zh", "data"))
IMAGE_DIR = os.path.join(BASE_DIR, "images", "home")

POKEMON_DIR = os.path.join(BASE_DIR, "pokemon")
MOVE_DIR = os.path.join(BASE_DIR, "move")
ABILITY_DIR = os.path.join(BASE_DIR, "ability")

def get_all_form_images(index: str, name: str, extra_images: list = None) -> str:
    img_html = ""
    index_fmt = f"{int(index):04}"
    prefix = f"{index_fmt}-{name}"

    if os.path.isdir(IMAGE_DIR):
        for file in sorted(os.listdir(IMAGE_DIR)):
            if not file.startswith(prefix) or not file.endswith(".png"):
                continue

            file_path = os.path.abspath(os.path.join(IMAGE_DIR, file))
            file_url = f"file:///{quote(file_path.replace(os.sep, '/'))}"

            label = file[len(prefix):].replace(".png", "").lstrip("-") or "默认形态"
            label = label.replace("shiny", "✨ Shiny 版").replace("--", "-")
            if "Shiny 版" not in label:
                label = f"🎨 {label}"

            img_html += f"<div><b>{label}</b><br><img src='{file_url}' style='max-width:200px; border-radius:10px;'></div><br>"

    if extra_images:
        for form in extra_images:
            for key, label in [("image", "🎨 默认形态"), ("shiny", "✨ Shiny 版")]:
                file = form.get(key)
                if not file:
                    continue
                file_path = os.path.abspath(os.path.join(IMAGE_DIR, file))
                file_url = f"file:///{quote(file_path.replace(os.sep, '/'))}"
                img_html += f"<div><b>{form['name']} - {label}</b><br><img src='{file_url}' style='max-width:200px; border-radius:10px;'></div><br>"

    return img_html

def normalize(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)
    return text.strip().lower().replace("・", "").replace("－", "-").replace("—", "-").replace(" ", "")

def match_name(input_name: str, data: dict) -> bool:
    name_pool = set()

    for key in ["name", "name_jp", "name_en"]:
        val = data.get(key)
        if isinstance(val, str):
            name_pool.add(val)

    names_dict = data.get("names")
    if isinstance(names_dict, dict):
        for val in names_dict.values():
            if isinstance(val, str):
                name_pool.add(val)

    aliases = data.get("aliases")
    if isinstance(aliases, list):
        for alias in aliases:
            if isinstance(alias, str):
                name_pool.add(alias)

    norm_input = normalize(input_name)
    return any(normalize(candidate) == norm_input for candidate in name_pool)

def query_local(name: str, category: str) -> Tuple[bool, str]:
    dir_path = {
        "pokemon": POKEMON_DIR,
        "move": MOVE_DIR,
        "ability": ABILITY_DIR
    }.get(category)

    if not dir_path or not os.path.isdir(dir_path):
        return False, f"図鑑データのフォルダが見つかりませんでした。"

    for file in os.listdir(dir_path):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(dir_path, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if match_name(name, data):
                    if category == "pokemon":
                        return True, format_pokemon_html(data)
                    elif category == "move":
                        return True, format_move_html(data)
                    elif category == "ability":
                        return True, format_ability_html(data)
        except Exception:
            continue

    return False, f"「{name}」の情報は見つかりませんでした。"

def format_pokemon_html(data: dict) -> str:
    name = data.get("name", "未知")
    name_jp = data.get("name_jp", "-")
    name_en = data.get("name_en", "-")
    index = data.get("index", "0000")
    profile = data.get("profile", "").replace("\n", "<br>")
    form = data.get("forms", [{}])[0]

    types = " / ".join(form.get("types", [])) or "不明"
    genus = form.get("genus", "未知种类")
    shape = form.get("shape", "-")
    color = form.get("color", "-")
    gender_rate = form.get("gender_rate")
    if isinstance(gender_rate, dict):
        male = gender_rate.get("male", "？")
        female = gender_rate.get("female", "？")
    else:
        male = female = "？"
    catch_rate = form.get("catch_rate", {}).get("rate", "？")

    ability_list = form.get("ability", [])
    ability_html = ", ".join(
        f"{a['name']}<span style='color:gray;'>（隐藏）</span>" if a.get("is_hidden") else a["name"]
        for a in ability_list
    )

    img_html = get_all_form_images(index, name, data.get("home_images"))

    # 能力值展示
    stats = data.get("stats", [{}])[0].get("data", {})
    if stats:
        stat_html = "<ul style='margin-left:1em;'>"
        stat_map = {
            "hp": "💗 HP",
            "attack": "🗡️ 攻击",
            "defense": "🛡️ 防御",
            "sp_attack": "🔥 特攻",
            "sp_defense": "🧊 特防",   
            "speed": "💨 速度"        
        }
        for key, label in stat_map.items():
            value = stats.get(key, "-")
            stat_html += f"<li>{label}：{value}</li>"
        stat_html += "</ul>"
    else:
        stat_html = "暂无能力值数据"

    # 自动推断世代
    generation = data.get("generation")
    if not generation:
        index_int = int(data.get("index", "0000"))
        if index_int <= 151:
            generation = "第一世代"
        elif index_int <= 251:
            generation = "第二世代"
        elif index_int <= 386:
            generation = "第三世代"
        elif index_int <= 493:
            generation = "第四世代"
        elif index_int <= 649:
            generation = "第五世代"
        elif index_int <= 721:
            generation = "第六世代"
        elif index_int <= 809:
            generation = "第七世代"
        elif index_int <= 905:
            generation = "第八世代"
        else:
            generation = "第九世代"

    return f'''
<div align="left">
<span style="padding: 6px; border-radius: 12px; display:block; line-height: 1.2;">
<br>
📡 我来啦～这是 No.{index} <b>{name}</b>（{name_jp} / {name_en}）的图鉴信息～📘<br><br>
{img_html}
🔢 <b>世代：</b>{generation}<br>
🌱 <b>种类：</b>{genus}<br>
🎨 <b>体色：</b>{color}　🐾 <b>外形：</b>{shape}<br>
🧬 <b>属性：</b>{types}<br>
👫 <b>性别比：</b> ♂{male} / ♀{female}<br>
🎯 <b>捕获率：</b>{catch_rate}<br>
🧠 <b>特性：</b>{ability_html}<br><br>
📝 <b>简介：</b><br>{profile}<br><br>
📊 <b>基础能力值：</b>{stat_html}
</span></div><br>
'''

def format_ability_html(data: dict) -> str:
    name_zh = data.get("name", "未知")
    name_jp = data.get("name_jp", "-")
    name_en = data.get("name_en", "-")
    generation = data.get("generation", "-")
    text = data.get("text", "无介绍")
    effect = data.get("effect", "").replace("\n", "<br>")

    info_list = data.get("info", [])
    info_html = "<ul>" + "".join(f"<li>{item}</li>" for item in info_list) + "</ul>" if info_list else "无"

    pokemon_list = data.get("pokemon", [])
    if pokemon_list:
        table_rows = ""
        for p in pokemon_list:
            p_types = " / ".join(p.get("types", []))
            row = (
                f"<tr>"
                f"<td>{p.get('index', '-')}</td>"
                f"<td>{p.get('name', '-')}</td>"
                f"<td>{p_types}</td>"
                f"<td>第一：{p.get('first') or '-'}</td>"
                f"<td>第二：{p.get('second') or '-'}</td>"
                f"<td>隐藏：{p.get('hidden') or '-'}</td>"
                f"</tr>"
            )
            table_rows += row
        pokemon_table = (
            f"<table border='1' cellpadding='4' cellspacing='0'>"
            f"<tr><th>编号</th><th>宝可梦</th><th>属性</th><th>第一特性</th><th>第二特性</th><th>隐藏特性</th></tr>"
            f"{table_rows}</table>"
        )
    else:
        pokemon_table = "暂无资料"

    return f'''
<div align="left">
<span style="padding: 10px; display:block;">
<br>
🧬 发现了一个特性：<b>{name_zh}</b>（{name_jp} / {name_en}）✨<br><br>
📅 <b>首次登场世代：</b>{generation}<br><br>
📝 <b>特性描述：</b>{text}<br>
🎯 <b>实战效果：</b><br>{effect or '无'}<br>
📘 <b>机制说明：</b>{info_html}<br><br>
👥 <b>拥有这个特性的宝可梦一览：</b><br>{pokemon_table}
</span></div><br>
'''
def format_move_html(data: dict) -> str:
    name_zh = data.get("name", "未知")
    name_jp = data.get("name_jp", "-")
    name_en = data.get("name_en", "-")
    generation = data.get("generation", "未知世代")
    move_type = data.get("type", "—")
    category = data.get("category", "—")
    power = data.get("power", "—")
    accuracy = data.get("accuracy", "—")
    pp = data.get("pp", "—")
    text = data.get("text", "无介绍")
    effect = data.get("effect", "").replace("\n", "<br>")
    attack_range = data.get("range", "—")

    info_list = data.get("info", [])
    info_html = (
        "<ul style='margin-left: 1em;'>"
        + "".join(f"<li>{i}</li>" for i in info_list)
        + "</ul>"
    ) if info_list else "暂无机制说明"

    return f'''
<div align="left">
<span style="padding: 10px; display:block;">
<b>ロトム：</b><br>
🔥 收到！这是技能 <b>{name_zh}</b>（{name_jp} / {name_en}）的完整记录～📒<br><br>
📅 <b>登场世代：</b>{generation}<br>
🔰 <b>属性：</b>{move_type}　📦 <b>类别：</b>{category}<br>
⚡ <b>威力：</b>{power}　🎯 <b>命中：</b>{accuracy}　⏳ <b>PP：</b>{pp}<br>
🎯 <b>攻击范围：</b>{attack_range}<br><br>
📝 <b>技能简介：</b>{text}<br>
🎈 <b>实际效果：</b><br>{effect or '暂无说明'}<br>
📚 <b>机制说明：</b><br>{info_html}
</span></div><br>
'''

def ask_gpt(prompt: str) -> str:
    keyword = prompt.strip()

    # 优先查宝可梦
    success, content = query_local(keyword, "pokemon")
    if success:
        return content + f"<div style='color:gray;'>（来自宝可梦图鉴）</div>"

    # 再查技能
    success, content = query_local(keyword, "move")
    if success:
        return content + f"<div style='color:gray;'>（来自技能图鉴）</div>"

    # 最后查特性
    success, content = query_local(keyword, "ability")
    if success:
        return content + f"<div style='color:gray;'>（来自特性图鉴）</div>"

    return f"<div>すみません，「{keyword}」についてはまだ図鑑に登録されていません。</div>"