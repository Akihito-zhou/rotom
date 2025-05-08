from shutil import move
import sys
import os
import csv
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llama_cpp import Llama
from modules.wiki_query import search_pokemon_wiki

# 初始化模型（Apple Silicon 优化）
llm = Llama.from_pretrained(
    repo_id="mmnga/ELYZA-japanese-Llama-2-7b-fast-instruct-gguf",
    filename="ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4,
    use_mlock=True,
    verbose=False
)

# 加载关键词词库
def load_keywords(csv_path: str) -> set:
    keywords = set()
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            for lang in row[1:4]:  # 中文、日文、英文
                keywords.add(lang.strip())
    return keywords

# 加载数据集路径
dataset_dir = os.path.join(os.path.dirname(__file__), "/Users/aki/Desktop/ninjyoukon/rotom/datasets")
pokemon_list_path = os.path.join(dataset_dir, 'pokemon/pokemon_list.csv')
move_list_path = os.path.join(dataset_dir, 'move/move_list.csv')
item_list_path = os.path.join(dataset_dir, 'item/item_list.csv')
ability_list_path = os.path.join(dataset_dir, 'ability/ability_list.csv')

pokemon_set = load_keywords(pokemon_list_path)
move_set = load_keywords(move_list_path)
item_set = load_keywords(item_list_path)
ability_set = load_keywords(ability_list_path)

# 建立关键词类别映射
keyword_category_map = {}
for word in pokemon_set:
    keyword_category_map[word] = "pokemon"
for word in move_set:
    keyword_category_map[word] = "move"
for word in item_set:
    keyword_category_map[word] = "item"
for word in ability_set:
    keyword_category_map[word] = "ability"

# 精确匹配：最长关键词优先
def extract_keyword(prompt: str) -> dict:
    candidates = [(word, len(word)) for word in keyword_category_map if word in prompt]
    if candidates:
        keyword = sorted(candidates, key=lambda x: x[1], reverse=True)[0][0]
        return {"name": keyword, "type": keyword_category_map[keyword]}
    return {"name": prompt.strip().split()[0], "type": "unknown"}

# 主函数：与 LLM 对话生成
def ask_gpt(prompt: str) -> str:
    keyword_data = extract_keyword(prompt)
    keyword = keyword_data["name"]
    use_wiki = keyword_data["type"] in ["pokemon", "ability", "move", "item"]

    reference_text = ""
    if use_wiki:
        wiki_info = search_pokemon_wiki(keyword)
        if wiki_info:
            reference_text = f"\n参考情報：\n{wiki_info}"
        else:
            reference_text = f"\n参考情報：\n「{keyword}」の情報は見つかりませんでした。"

    system_prompt = (
        "あなたは『ロトム』という名前のAIポケモン図鑑です。\n"
        "ユーザーは毎回ポケモンに関する質問をします。\n"
        "出力は必ず「ロトム：」から始め、「ユーザー：」を含めてはいけません。\n"
        "わかりやすく、可愛く、短く答えてください。\n"
        "ロールプレイは禁止です。"
    )

    user_prompt = f"""ユーザー：{prompt}
    {reference_text}
    ロトム：
    """

    full_prompt = f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n{user_prompt}[/INST]"

    from llama_cpp import Llama
    llm = Llama.from_pretrained(
        repo_id="mmnga/ELYZA-japanese-Llama-2-7b-fast-instruct-gguf",
        filename="ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf",
        n_ctx=2048,
        n_threads=4,
        use_mlock=True,
        verbose=False
    )

    output = llm(
        prompt=full_prompt,
        max_tokens=200,
        temperature=0.5,
        top_p=0.85,
        echo=False,
        stop=["ユーザー：", "</s>", "[/INST]"]
    )

    text = output["choices"][0]["text"].strip()

    # 安全清洗
    for tag in ["ロトム：", "ユーザー：", "ポケモン："]:
        if text.startswith(tag):
            text = text[len(tag):].strip()

    # 限制句数（最多两句）
    lines = text.split("\n")
    text = "\n".join(lines[:10]).strip()

    return f"ロトム：{text}"