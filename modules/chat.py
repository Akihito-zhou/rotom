# chat.py

from modules.query.query_all import query_local, normalize
from modules.llm.chatgpt_rotom import extract_entity_name, extract_fields, ask_chatgpt
from modules.multi_language.language_handler import generate_multilingual_response

CATEGORY_FIELDS = {
    "pokemon": ["basic", "profile", "types", "ability", "stats", "moves", "flavor", "evolution"],
    "move": ["generation", "category", "accuracy", "attack_range", "text", "effect", "info", "pokemon"],
    "ability": ["generation", "count", "text", "effect", "info", "pokemon"]
}

def ask_gpt(prompt: str) -> str:
    prompt_clean = normalize(prompt)
    keyword = extract_entity_name(prompt_clean)
    fields = extract_fields(prompt_clean)

    if keyword:
        for category in ["pokemon", "move", "ability"]:
            allowed_fields = CATEGORY_FIELDS[category]
            filtered_fields = [f for f in (fields or []) if f in allowed_fields]

            found, html = query_local(keyword, category, fields=filtered_fields)
            if found:
                print(f"[DEBUG] 命中本地实体：{keyword} ➜ {category}，字段：{filtered_fields}")
                translated_html = generate_multilingual_response(html, prompt)
                return translated_html + f"<div style='color:gray;'>（来自{category}图鉴）</div>"

    print(f"[DEBUG] 未找到实体，调用 ChatGPT 自由回答 ➜ {prompt}")
    answer = ask_chatgpt(prompt)
    translated_answer = generate_multilingual_response(answer, prompt)
    return f"<div>{translated_answer}</div>"

