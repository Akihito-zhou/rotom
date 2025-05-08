import requests
from bs4 import BeautifulSoup
import re

def detect_language(text: str) -> str:
    if re.search(r'[\u4e00-\u9fff]', text):
        return 'zh'
    elif re.search(r'[ぁ-んァ-ン]', text):
        return 'ja'
    elif re.search(r'[A-Za-z]', text):  # 改为检测是否“包含”英文字符
        return 'en'
    return 'unknown'

def clean_text(text: str) -> str:
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def search_pokemon_wiki(keyword: str) -> str:
    lang = detect_language(keyword)
    headers = { "User-Agent": "Mozilla/5.0" }

    try:
        if lang == 'zh':
            url = f"https://wiki.52poke.com/wiki/{keyword}"
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            p_tags = soup.select("#mw-content-text > div > p")
            for p in p_tags:
                text = clean_text(p.get_text(strip=True))
                if len(text) > 30:
                    return text[:300]

        elif lang == 'ja':
            url = f"https://wiki.xn--rckteqa2e.com/wiki/{keyword}"
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            p_tags = soup.select("#mw-content-text > div > p")
            for p in p_tags:
                text = clean_text(p.get_text(strip=True))
                if len(text) > 30:
                    return text[:300]

        elif lang == 'en':
            keyword_fixed = keyword.replace(" ", "_")
            url = f"https://bulbapedia.bulbagarden.net/wiki/{keyword_fixed}"
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            p = soup.select_one("table + p") or soup.select_one("p")
            return clean_text(p.get_text(strip=True))[:300] if p else ""

        return f"{keyword} に関する情報は見つからなかったロト…"

    except Exception as e:
        print(f"[Wiki Error] {e}")
        return "情報を取得する際にエラーが発生したロト。"