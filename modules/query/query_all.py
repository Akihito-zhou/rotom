# query_all.py
import os
import json
from typing import List, Tuple, Optional
import unicodedata
from urllib.parse import quote
from modules.query.query_ability import format_ability_html
from modules.query.query_move import format_move_html
from modules.query.query_pokemon import format_pokemon_html
from modules.query.config import POKEMON_DIR, MOVE_DIR, ABILITY_DIR

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

# def query_local(name: str, category: str) -> Tuple[bool, str]:
#     dir_path = {
#         "pokemon": POKEMON_DIR,
#         "move": MOVE_DIR,
#         "ability": ABILITY_DIR
#     }.get(category)

#     if not dir_path or not os.path.isdir(dir_path):
#         return False, f"図鑑データのフォルダが見つかりませんでした。"

#     for file in os.listdir(dir_path):
#         if not file.endswith(".json"):
#             continue

#         file_path = os.path.join(dir_path, file)
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 if match_name(name, data):
#                     if category == "pokemon":
#                         return True, format_pokemon_html(data)
#                     elif category == "move":
#                         return True, format_move_html(data)
#                     elif category == "ability":
#                         return True, format_ability_html(data)
#         except Exception:
#             continue

#     return False, f"「{name}」の情報は見つかりませんでした。"

# def ask_gpt(prompt: str) -> str:
#     keyword = prompt.strip()

#     # 优先查宝可梦
#     success, content = query_local(keyword, "pokemon")
#     if success:
#         return content + f"<div style='color:gray;'>（来自宝可梦图鉴）</div>"

#     # 再查技能
#     success, content = query_local(keyword, "move")
#     if success:
#         return content + f"<div style='color:gray;'>（来自技能图鉴）</div>"

#     # 最后查特性
#     success, content = query_local(keyword, "ability")
#     if success:
#         return content + f"<div style='color:gray;'>（来自特性图鉴）</div>"

#     return f"<div>すみません，「{keyword}」についてはまだ図鑑に登録されていません。</div>"

def query_local(name: str, category: str, fields: Optional[List[str]] = None) -> Tuple[bool, str]:
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
                        return True, format_pokemon_html(data, fields=fields)
                    elif category == "move":
                        return True, format_move_html(data, fields=fields)
                    elif category == "ability":
                        return True, format_ability_html(data, fields=fields)
        except Exception:
            continue

    return False, f"「{name}」の情報は見つかりませんでした。"

