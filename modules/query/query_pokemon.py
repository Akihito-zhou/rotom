from query_all import get_all_form_images
from query_all import IMAGE_DIR
from urllib.parse import quote
import os
# def format_pokemon_html(data: dict) -> str:
#     name = data.get("name", "未知")
#     name_jp = data.get("name_jp", "-")
#     name_en = data.get("name_en", "-")
#     index = data.get("index", "0000")
#     profile = data.get("profile", "").replace("\n", "<br>")
#     form = data.get("forms", [{}])[0]

#     types = " / ".join(form.get("types", [])) or "不明"
#     genus = form.get("genus", "未知种类")
#     shape = form.get("shape", "-")
#     color = form.get("color", "-")
#     gender_rate = form.get("gender_rate")
#     if isinstance(gender_rate, dict):
#         male = gender_rate.get("male", "？")
#         female = gender_rate.get("female", "？")
#     else:
#         male = female = "？"
#     catch_rate = form.get("catch_rate", {}).get("rate", "？")

#     ability_list = form.get("ability", [])
#     ability_html = ", ".join(
#         f"{a['name']}<span style='color:gray;'>（隐藏）</span>" if a.get("is_hidden") else a["name"]
#         for a in ability_list
#     )

#     img_html = get_all_form_images(index, name, data.get("home_images"))

#     # 能力值展示
#     stats = data.get("stats", [{}])[0].get("data", {})
#     if stats:
#         stat_html = "<ul style='margin-left:1em;'>"
#         stat_map = {
#             "hp": "💗 HP",
#             "attack": "🗡️ 攻击",
#             "defense": "🛡️ 防御",
#             "sp_attack": "🔥 特攻",
#             "sp_defense": "🧊 特防",   
#             "speed": "💨 速度"        
#         }
#         for key, label in stat_map.items():
#             value = stats.get(key, "-")
#             stat_html += f"<li>{label}：{value}</li>"
#         stat_html += "</ul>"
#     else:
#         stat_html = "暂无能力值数据"

#     # 自动推断世代
#     generation = data.get("generation")
#     if not generation:
#         index_int = int(data.get("index", "0000"))
#         if index_int <= 151:
#             generation = "第一世代"
#         elif index_int <= 251:
#             generation = "第二世代"
#         elif index_int <= 386:
#             generation = "第三世代"
#         elif index_int <= 493:
#             generation = "第四世代"
#         elif index_int <= 649:
#             generation = "第五世代"
#         elif index_int <= 721:
#             generation = "第六世代"
#         elif index_int <= 809:
#             generation = "第七世代"
#         elif index_int <= 905:
#             generation = "第八世代"
#         else:
#             generation = "第九世代"

#     return f'''
# <div align="left">
# <span style="padding: 6px; border-radius: 12px; display:block; line-height: 1.2;">
# <br>
# 📡 我来啦～这是 No.{index} <b>{name}</b>（{name_jp} / {name_en}）的图鉴信息～📘<br><br>
# {img_html}
# 🔢 <b>世代：</b>{generation}<br>
# 🌱 <b>种类：</b>{genus}<br>
# 🎨 <b>体色：</b>{color}　🐾 <b>外形：</b>{shape}<br>
# 🧬 <b>属性：</b>{types}<br>
# 👫 <b>性别比：</b> ♂{male} / ♀{female}<br>
# 🎯 <b>捕获率：</b>{catch_rate}<br>
# 🧠 <b>特性：</b>{ability_html}<br><br>
# 📝 <b>简介：</b><br>{profile}<br><br>
# 📊 <b>基础能力值：</b>{stat_html}
# </span></div><br>
# '''
from typing import List, Tuple, Optional
def format_pokemon_html(data: dict, fields: Optional[List[str]] = None) -> str:
    fields = set(fields or ["basic", "profile", "stats"])  # 默认展示基本信息、简介和能力值
    name = data.get("name", "未知")
    name_jp = data.get("name_jp", "-")
    name_en = data.get("name_en", "-")
    index = data.get("index", "0000")
    form = data.get("forms", [{}])[0]
    output = []

    # 是否展示所有字段
    show_all = fields is None

    # 获取世代
    generation = data.get("generation")
    if not generation:
        index_int = int(index)
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

    # 📌 基本信息
    if show_all or "basic" in fields:
        types = " / ".join(form.get("types", [])) or "不明"
        genus = form.get("genus", "未知种类")
        shape = form.get("shape", "-")
        color = form.get("color", "-")
        gender_rate = form.get("gender_rate", {})
        male = gender_rate.get("male", "？")
        female = gender_rate.get("female", "？")
        catch_rate = form.get("catch_rate", {}).get("rate", "？")
        ability_html = ", ".join(
            f"{a['name']}<span style='color:gray;'>（隐藏）</span>" if a.get("is_hidden") else a["name"]
            for a in form.get("ability", [])
        )
        img_html = get_all_form_images(index, name, data.get("home_images"))

        output.append(f"""
📡 我来啦～这是 No.{index} <b>{name}</b>（{name_jp} / {name_en}）的图鉴信息～📘<br><br>
{img_html}
🔢 <b>世代：</b>{generation}<br>
🌱 <b>种类：</b>{genus}<br>
🎨 <b>体色：</b>{color}　🐾 <b>外形：</b>{shape}<br>
🧬 <b>属性：</b>{types}<br>
👫 <b>性别比：</b> ♂{male} / ♀{female}<br>
🎯 <b>捕获率：</b>{catch_rate}<br>
🧠 <b>特性：</b>{ability_html}<br>
""")

    # 📝 简介
    if show_all or "profile" in fields:
        profile = data.get("profile", "").replace("\n", "<br>")
        output.append(f"<br>📝 <b>简介：</b><br>{profile}<br>")

    # 📊 能力值
    if show_all or "stats" in fields:
        stats = data.get("stats", [{}])[0].get("data", {})
        if stats:
            stat_html = "<ul style='margin-left:1em;'>"
            stat_map = {
                "hp": "💗 HP", "attack": "🗡️ 攻击", "defense": "🛡️ 防御",
                "sp_attack": "🔥 特攻", "sp_defense": "🧊 特防", "speed": "💨 速度"
            }
            for key, label in stat_map.items():
                stat_html += f"<li>{label}：{stats.get(key, '-')}</li>"
            stat_html += "</ul>"
        else:
            stat_html = "暂无能力值数据"
        output.append(f"<br>📊 <b>基础能力值：</b>{stat_html}")

    # 🧬 进化链
    if show_all or "evolution" in fields:
        chains = data.get("evolution_chains", [])
        evo_html = ""
        for chain in chains:
            evo_html += "<div style='margin: 0.5em 0;'>"
            for stage in chain:
                img = stage.get("image", "")
                img_path = os.path.abspath(os.path.join(IMAGE_DIR, img))
                img_url = f"file:///{quote(img_path.replace(os.sep, '/'))}"
                name = stage["name"]
                evo_html += f"<img src='{img_url}' style='height:48px'> → <b>{name}</b> "
            evo_html += "</div>"
        output.append(f"<br>🌱 <b>进化链：</b><br>{evo_html}")

    # 🎯 招式
    if "moves" in fields:
        move_data = data.get("moves", {})
        move_sections = []
        for source in ["learned", "machine"]:
            for group in move_data.get(source, []):
                moves = group.get("data", [])
                if not moves:
                    continue
                section = f"<details><summary><b>{'等级学习' if source == 'learned' else '招式机学习'}</b></summary><ul>"
                for move in moves[:10]:  # ⚠️ 只显示前10个，避免太长
                    name = move.get("name", "未知")
                    type_ = move.get("type", "？")
                    category = move.get("category", "？")
                    power = move.get("power", "—")
                    pp = move.get("pp", "—")
                    section += f"<li>{name}（{type_}／{category}／威力 {power}／PP {pp}）</li>"
                section += "</ul></details>"
                move_sections.append(section)
        output.append(f"<br>📘 <b>技能一览：</b><br>{''.join(move_sections)}")

    # 📖 世代描述
    if "flavor" in fields:
        flavors = data.get("flavor_texts", [])
        flavor_html = ""
        for gen in flavors:
            flavor_html += f"<details><summary><b>{gen['name']}</b></summary><ul>"
            for v in gen["versions"]:
                flavor_html += f"<li>{v['name']}：{v['text']}</li>"
            flavor_html += "</ul></details>"
        output.append(f"<br>📖 <b>图鉴描述：</b><br>{flavor_html}")

    return "<div align='left'><span style='padding:6px; display:block; line-height: 1.6;'>" + "".join(output) + "</span></div>"