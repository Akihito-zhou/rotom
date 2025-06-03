# chat.py
import os
import sys
import unicodedata

# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.query.query_all import query_local
from modules.llm.chatgpt_rotom import ask_chatgpt
from modules.llm.chatgpt_rotom import extract_entity_name

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
    prompt = normalize_text(prompt)

    keyword = extract_entity_name(prompt)
    if keyword:
        for category in ["pokemon", "move", "ability"]:
            found, html = query_local(keyword, category)
            if found:
                print(f"[DEBUG] 命中本地实体：{keyword} ➜ {category}")
                return html

    # fallback to chatgpt
    print(f"[DEBUG] 未找到实体，调用 ChatGPT 自由回答 ➜ {prompt}")
    answer = ask_chatgpt(prompt)
    return f"<div>{answer}</div>"