import requests
from bs4 import BeautifulSoup

def search_pokemon_wiki(keyword: str) -> str:
    """
    在 52poke Wiki 上查找宝可梦词条并返回首段文字。
    """
    base_url = "https://wiki.52poke.com/wiki/"
    url = base_url + keyword

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"
        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.select_one("#mw-content-text p")
        if content:
            return content.get_text(strip=True)[:300]
        else:
            return ""
    except Exception as e:
        return ""