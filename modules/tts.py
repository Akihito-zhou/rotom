import os
import json

# 数据目录
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pokemon-dataset-zh", "data"))
POKEMON_PATH = os.path.join(BASE_DIR, "pokemon_full_list.json")
MOVE_PATH = os.path.join(BASE_DIR, "move_list.json")
ABILITY_PATH = os.path.join(BASE_DIR, "ability_list.json")

# 加载三类数据
with open(POKEMON_PATH, 'r', encoding='utf-8') as f:
    POKEMON_DATA = json.load(f)

with open(MOVE_PATH, 'r', encoding='utf-8') as f:
    MOVE_DATA = json.load(f)

with open(ABILITY_PATH, 'r', encoding='utf-8') as f:
    ABILITY_DATA = json.load(f)

# === 公共函数：文本匹配 ===
def match_entry_by_name(name: str, data: list) -> dict:
    for entry in data:
        if name in (entry.get("name"), entry.get("name_jp"), entry.get("name_en")):
            return entry
    return None

# === 主查询函数 ===
def query_local(name: str, category: str) -> str:
    if category == "pokemon":
        entry = match_entry_by_name(name, POKEMON_DATA)
        return format_pokemon(entry, name)
    elif category == "move":
        entry = match_entry_by_name(name, MOVE_DATA)
        return format_move(entry, name)
    elif category == "ability":
        entry = match_entry_by_name(name, ABILITY_DATA)
        return format_ability(entry, name)
    else:
        return f"<div><b>ロトム：</b>对不起，暂不支持该类别「{category}」的查询。</div>"

# === 格式化输出函数 ===
def format_pokemon(entry: dict, name: str) -> str:
    if not entry:
        return f"<div><b>ロトム：</b>对不起，没有找到宝可梦「{name}」。</div>"
    types = " / ".join(entry.get("types", []))
    return f"""
<div style='background-color:#f0f8ff; padding:10px; border-radius:10px;'>
<b>宝可梦：</b>{entry['name']}（{entry['name_jp']} / {entry['name_en']}）<br>
<b>编号：</b>{entry['index']}<br>
<b>世代：</b>{entry.get('generation', '—')}<br>
<b>属性：</b>{types}<br>
</div><br>
"""

def format_move(entry: dict, name: str) -> str:
    if not entry:
        return f"<div><b>ロトム：</b>对不起，没有找到技能「{name}」。</div>"
    return f"""
<div style='background-color:#d8f9ff; padding:10px; border-radius:10px;'>
<b>技能：</b>{entry['name']}（{entry['name_jp']} / {entry['name_en']}）<br>
<b>世代：</b>{entry.get('generation', '—')}<br>
<b>属性：</b>{entry.get('type', '—')}　<b>类别：</b>{entry.get('category', '—')}<br>
<b>威力：</b>{entry.get('power', '—')}　<b>命中：</b>{entry.get('accuracy', '—')}　<b>PP：</b>{entry.get('pp', '—')}<br>
<b>描述：</b>{entry.get('text', '')}
</div><br>
"""

def format_ability(entry: dict, name: str) -> str:
    if not entry:
        return f"<div><b>ロトム：</b>对不起，没有找到特性「{name}」。</div>"
    return f"""
<div style='background-color:#fff2cc; padding:10px; border-radius:10px;'>
<b>特性：</b>{entry['name']}（{entry['name_jp']} / {entry['name_en']}）<br>
<b>世代：</b>{entry.get('generation', '—')}<br>
<b>常见宝可梦数量：</b>{entry.get('common_count', '—')}　<b>隐藏特性数：</b>{entry.get('hidden_count', '—')}<br>
<b>效果：</b>{entry.get('text', '')}
</div><br>
"""