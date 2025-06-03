from typing import Optional, List

def format_ability_html(data: dict, fields: Optional[List[str]] = None) -> str:
    name_zh = data.get("name", "未知")
    name_jp = data.get("name_jp", "-")
    name_en = data.get("name_en", "-")

    blocks = []

    # 检查是否展示所有字段
    show_all = fields is None

    # 标题
    blocks.append(f"<b>🧬 发现了一个特性：{name_zh}（{name_jp} / {name_en}）✨</b><br><br>")

    # 世代
    if show_all or "generation" in fields:
        generation = data.get("generation", "-")
        blocks.append(f"📅 <b>首次登场世代：</b>{generation}<br>")

    # 数量统计
    if show_all or "count" in fields:
        common_count = data.get("common_count")
        hidden_count = data.get("hidden_count")
        if isinstance(common_count, int) or isinstance(hidden_count, int):
            blocks.append(f"🎯 <b>常规特性数量：</b>{common_count or 0}　🕵️ <b>隐藏特性数量：</b>{hidden_count or 0}<br>")

    # 描述
    if show_all or "text" in fields:
        text = data.get("text", "无介绍")
        blocks.append(f"<br>📝 <b>特性描述：</b><br>{text}")

    # 效果
    if show_all or "effect" in fields:
        effect = data.get("effect", "").replace("\n", "<br>")
        blocks.append(f"<br>🎯 <b>实战效果：</b><br>{effect or '无'}")

    # 机制说明
    if show_all or "info" in fields:
        info_list = data.get("info", [])
        if info_list:
            info_html = "<ul style='margin-left:1em;'>" + "".join(f"<li>{item}</li>" for item in info_list) + "</ul>"
        else:
            info_html = "无"
        blocks.append(f"<br>📘 <b>机制说明：</b><br>{info_html}")

    # 拥有宝可梦表格
    if "pokemon" in fields:
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
                    f"<td>{p.get('first') or '-'}</td>"
                    f"<td>{p.get('second') or '-'}</td>"
                    f"<td>{p.get('hidden') or '-'}</td>"
                    f"</tr>"
                )
                table_rows += row
            pokemon_table = (
                f"<table border='1' cellpadding='4' cellspacing='0' style='border-collapse: collapse;'>"
                f"<tr><th>编号</th><th>宝可梦</th><th>属性</th><th>第一特性</th><th>第二特性</th><th>隐藏特性</th></tr>"
                f"{table_rows}</table>"
            )
        else:
            pokemon_table = "暂无资料"
        blocks.append(f"<br>👥 <b>拥有这个特性的宝可梦一览：</b><br>{pokemon_table}")

    # 拼接 HTML
    return f'''
<div align="left">
<span style="padding: 10px; display:block;">
{''.join(blocks)}
</span></div><br>
'''