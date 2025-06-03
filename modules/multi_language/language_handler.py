import os
import deepl
from bs4 import BeautifulSoup
from modules.multi_language.language_detector import detect_input_language_with_label, extract_requested_languages

# ✅ DeepL API 密钥
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY") or "your-deepl-api-key-here"
translator = deepl.Translator(DEEPL_API_KEY)

# 语言显示前缀
language_prefix = {
    "zh": "[中文]",
    "en": "[English]",
    "ja": "[日本語]"
}

# DeepL 接收的语言代码
deepl_lang_map = {
    "zh": "ZH",
    "en": "EN-US",  # 必须用 EN-US 或 EN-GB
    "ja": "JA"
}

def normalize_lang_code(lang: str) -> str:
    """标准化语言代码"""
    lang = lang.lower()
    if lang.startswith("zh"):
        return "zh"
    if lang.startswith("en"):
        return "en"
    if lang.startswith("ja"):
        return "ja"
    return lang

def deepl_translate(html: str, target_lang: str) -> str:
    """使用 DeepL 翻译 HTML 内容，保留结构"""
    try:
        normalized = normalize_lang_code(target_lang)
        deepl_target = deepl_lang_map.get(normalized)
        if not deepl_target:
            return f"[Unsupported language: {target_lang}]"

        def translate_text(text):
            return translator.translate_text(text, target_lang=deepl_target).text

        soup = BeautifulSoup(html, "html.parser")

        for elem in soup.find_all(text=True):
            parent = elem.parent.name
            if parent not in ["script", "style"] and elem.strip():
                try:
                    translated = translate_text(elem.strip())
                    elem.replace_with(translated)
                except Exception as e:
                    print(f"[翻译失败片段] {elem}: {e}")

        prefix = language_prefix.get(normalized, f"[{target_lang}]")
        return f"{prefix}<br>{str(soup)}"

    except Exception as e:
        return f"[翻译失败: {e}]"

def generate_multilingual_response(original_response: str, user_input: str) -> str:
    """根据用户输入内容生成语言适配回答"""
    requested_langs = extract_requested_languages(user_input)

    if not requested_langs:
        # 自动识别语言
        lang_code, lang_label = detect_input_language_with_label(user_input)
        translated = deepl_translate(original_response, lang_code)
        print(f"[DEBUG] 系统识别语言：{lang_label}")
        return f"{translated}"
    else:
        # 用户明确要求多语言回答
        responses = [deepl_translate(original_response, lang) for lang in requested_langs]
        return "<hr>".join(responses)
