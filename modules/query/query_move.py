from typing import List, Optional

def format_move_html(data: dict, fields: Optional[List[str]] = None) -> str:
    name_zh = data.get("name", "未知")
    name_jp = data.get("name_jp", "-")
    name_en = data.get("name_en", "-")

    blocks = []
    
    # 检查是否展示所有字段
    show_all = fields is None

    # 标题
    blocks.append(f"<b>🧬 发现了一个技能：{name_zh}（{name_jp} / {name_en}）✨</b><br><br>")

    # 世代
    if show_all or "generation" in fields:
        generation = data.get("generation", "未知世代")
        blocks.append(f"📅 <b>登场世代：</b>{generation}<br>")

    # 属性 & 类别
    if show_all or "category" in fields:
        move_type = data.get("type", "—")
        category = data.get("category", "—")
        blocks.append(f"🔰 <b>属性：</b>{move_type}　📦 <b>类别：</b>{category}<br>")

    # 威力 命中 PP
    if show_all or "accuracy" in fields:
        power = data.get("power", "—")
        accuracy = data.get("accuracy", "—")
        pp = data.get("pp", "—")
        blocks.append(f"⚡ <b>威力：</b>{power}　🎯 <b>命中：</b>{accuracy}　⏳ <b>PP：</b>{pp}<br>")

    # 攻击范围
    if show_all or "attack_range" in fields:
        attack_range = data.get("range", "—")
        blocks.append(f"🎯 <b>攻击范围：</b>{attack_range}<br>")

    # 简介
    if show_all or "text" in fields:
        text = data.get("text", "无介绍")
        blocks.append(f"<br>📝 <b>技能简介：</b><br>{text}")

    # 实战效果
    if show_all or "effect" in fields:
        effect = data.get("effect", "").replace("\n", "<br>")
        blocks.append(f"<br>🎈 <b>实际效果：</b><br>{effect or '暂无说明'}")

    # 机制说明
    if show_all or "info" in fields:
        info_list = data.get("info", [])
        if info_list:
            info_html = "<ul style='margin-left:1em;'>" + "".join(f"<li>{item}</li>" for item in info_list) + "</ul>"
        else:
            info_html = "暂无机制说明"
        blocks.append(f"<br>📚 <b>机制说明：</b><br>{info_html}")

    # 可学习宝可梦
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

        blocks.append(f"<br>📖 <b>可学习宝可梦：</b><br>{learn_html}")

    # 拼接输出
    return f'''
<div align="left">
<span style="padding: 10px; display:block;">
{''.join(blocks)}
</span></div><br>
'''
