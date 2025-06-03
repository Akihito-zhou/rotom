import re
from langdetect import detect
from modules.llm.chatgpt_rotom import extract_entity_name
from modules.query.query_all import query_local  # 实体判断所需

# 支持的语言映射
language_map = {
    "中文": "zh",
    "汉语": "zh",
    "英文": "en",
    "英语": "en",
    "日语": "ja",
    "日文": "ja"
}

# 显示用标签
LANGUAGE_LABELS = {
    "zh": "中文",
    "en": "English",
    "ja": "日本語"
}

# ----------------------- 判断函数 -----------------------

def is_single_english_word(text: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z\-]+", text.strip()))

def is_mostly_english(text: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9\s\-,.?']+", text.strip()))

def is_single_japanese_word(text: str) -> bool:
    return bool(re.fullmatch(r"[\u3040-\u30FF\u4E00-\u9FAFー]+", text.strip()))

def is_mostly_japanese(text: str) -> bool:
    jp_chars = re.findall(r"[\u3040-\u30FF\u4E00-\u9FAFー]", text)
    return len(jp_chars) >= len(text.strip()) * 0.4

# ----------------------- 主识别逻辑 -----------------------

def detect_input_language(text: str) -> str:
    text = text.strip()

    # 英文实体判断
    entity = extract_entity_name(text)
    if entity and is_single_english_word(entity):
        for category in ["pokemon", "move", "ability"]:
            found, _ = query_local(entity.lower(), category, fields=[])
            if found:
                return "en"

    # 日文实体判断
    entity = extract_entity_name(text)
    if entity and is_mostly_japanese(text):
        for category in ["pokemon", "move", "ability"]:
            found, _ = query_local(entity, category, fields=[])
            if found:
                return "ja"

    # 太短 ➜ 默认中文
    if len(text.split()) < 3:
        return "zh"

    # fallback: 使用 langdetect
    try:
        return detect(text)
    except:
        return "zh"

def detect_input_language_with_label(text: str) -> tuple[str, str]:
    """返回语言代码和可显示语言名"""
    lang_code = detect_input_language(text)
    lang_label = LANGUAGE_LABELS.get(lang_code, lang_code)
    return lang_code, lang_label

# ----------------------- 用户请求语言指令提取 -----------------------

def extract_requested_languages(text: str) -> list:
    """从文本中提取用户指定的回答语言（如“用英语和日语告诉我”）"""
    pattern = r"(?:用|使用)?(中文|汉语|英文|英语|日语|日文)(?:和|与|、)?(中文|汉语|英文|英语|日语|日文)?(?:回答|说明|告诉)?"
    match = re.search(pattern, text)
    if match:
        langs = [language_map.get(lang) for lang in match.groups() if lang]
        return list(set(filter(None, langs)))
    return []
