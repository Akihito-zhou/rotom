import os
import sys
import unicodedata

# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.pokemon_query import query_local

# 输入清洗函数：去除空格、统一字符、降重全角
def normalize_text(text: str) -> str:
    text = text.strip().replace("　", " ")  # 替换全角空格为半角
    text = unicodedata.normalize("NFKC", text)  # 全角转半角
    return text

def extract_keyword_type(prompt: str) -> dict:
    prompt = normalize_text(prompt)

    for category in ["pokemon", "move", "ability"]:
        found, _ = query_local(prompt, category)
        if found:
            print(f"[DEBUG] 类型判断成功：{prompt} ➜ {category}")
            return {"name": prompt, "type": category}

    print(f"[DEBUG] 类型判断失败：{prompt} ➜ unknown")
    return {"name": prompt, "type": "unknown"}

def ask_gpt(prompt: str) -> str:
    keyword_data = extract_keyword_type(prompt)
    name = keyword_data["name"]
    category = keyword_data["type"]

    if category in ["pokemon", "move", "ability"]:
        _, html = query_local(name, category)
        return html
    else:
        return f"<div><b>ロトム：</b> すみません，「{name}」についてはまだ図鑑に登録されていません。</div>"