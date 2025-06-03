from typing import List, Tuple, Optional

def format_move_html(data: dict, fields: Optional[List[str]] = None) -> str:
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

    show_all = fields is None
    html = f'''<div align="left"><span style="padding: 10px; display:block;">
<b>ロトム：</b><br>
🔥 收到！这是技能 <b>{name_zh}</b>（{name_jp} / {name_en}）的完整记录～📒<br><br>
'''

    if show_all or "generation" in fields:
        html += f"📅 <b>登场世代：</b>{generation}<br>"

    if show_all or "category" in fields:
        html += f"🔰 <b>属性：</b>{move_type}　📦 <b>类别：</b>{category}<br>"

    if show_all or "accuracy" in fields:
        html += f"⚡ <b>威力：</b>{power}　🎯 <b>命中：</b>{accuracy}　⏳ <b>PP：</b>{pp}<br>"

    if show_all or "attack_range" in fields:
        html += f"🎯 <b>攻击范围：</b>{attack_range}<br><br>"

    if show_all or "text" in fields:
        html += f"📝 <b>技能简介：</b>{text}<br>"

    if show_all or "effect" in fields:
        html += f"🎈 <b>实际效果：</b><br>{effect or '暂无说明'}<br>"

    if show_all or "info" in fields:
        info_list = data.get("info", [])
        info_html = (
            "<ul style='margin-left: 1em;'>"
            + "".join(f"<li>{i}</li>" for i in info_list)
            + "</ul>"
        ) if info_list else "暂无机制说明"
        html += f"📚 <b>机制说明：</b><br>{info_html}<br><br>"

    if "pokemon" in fields:
        pokemon_data = data.get("pokemon", {})
        has_pokemon = any(pokemon_data.get(key) for key in ["level", "machine", "egg", "tutor"])
        if has_pokemon:
            learn_html = "<ul style='margin-left: 1em;'>"
            for method, pokelist in pokemon_data.items():
                if not pokelist:
                    continue
                label = {
                    "level": "📘 提升等级",
                    "machine": "🔧 招式学习器",
                    "egg": "🥚 遗传招式",
                    "tutor": "🎓 教学招式"
                }.get(method, method)
                names = "、".join(pokelist)
                learn_html += f"<li>{label}：{names}</li>"
            learn_html += "</ul>"
        else:
            learn_html = "暂无学习此招式的宝可梦。"
        html += f"📖 <b>可学习宝可梦：</b><br>{learn_html}"

    html += "</span></div><br>"
    return html