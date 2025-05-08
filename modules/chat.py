from shutil import move
import sys
import os
import csv
import re

from torch import is_deterministic_algorithms_warn_only_enabled

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

# 加载所有词库

def load_keywords(csv_path: str) -> set:
    keywords = set()
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            # 只提取第2~4列（中文、日文、英文）
            for lang in row[1:4]:
                keywords.add(lang.strip())
    return keywords

# 读取 CSV 文件，获取所有关键词
dataset_dir = os.path.join(os.path.dirname(__file__), "/Users/aki/Desktop/ninjyoukon/rotom/datasets")
pokemon_list_path = os.path.join(dataset_dir, 'pokemon/pokemon_list.csv')
move_list_path = os.path.join(dataset_dir, 'move/move_list.csv')
item_list_path = os.path.join(dataset_dir, 'item/item_list.csv')
ability_list_path = os.path.join(dataset_dir, 'ability/ability_list.csv')

pokemon_set = load_keywords(pokemon_list_path)
move_set = load_keywords(move_list_path)
item_set = load_keywords(item_list_path)
ability_set = load_keywords(ability_list_path)

# 建立反向映射
keyword_category_map = {}
for word in pokemon_set:
    keyword_category_map[word] = "pokemon"
for word in move_set:
    keyword_category_map[word] = "move"
for word in item_set:
    keyword_category_map[word] = "item"
for word in ability_set:
    keyword_category_map[word] = "ability"

# 高级关键词提取器
def extract_keyword(prompt: str) -> dict:
    """
    从用户输入中提取关键词，并返回 {'name': ..., 'type': ...}
    """
    for keyword in keyword_category_map:
        if keyword in prompt:
            return {"name": keyword, "type": keyword_category_map[keyword]}
    return {"name": prompt.strip().split()[0], "type": "unknown"}

# 主函数
def ask_gpt(prompt: str) -> str:
    """
    使用 Elyza 指令模型进行日语对话生成，接入 Wiki 知识 + 洛托姆风格。
    """

    keyword_data = extract_keyword(prompt)
    keyword = keyword_data["name"]
    use_wiki = keyword_data["type"] in ["pokemon", "ability", "move", "item"]

    if use_wiki:
        wiki_info = search_pokemon_wiki(keyword)
    else:
        wiki_info = ""

    system_prompt = (
        "名前はロトム。"
        "短くて可愛い言葉を使う。"
        "電子図鑑のポケモン。"
        "専門情報を知ってたら、それに基づいてちゃんと教えるんだ。"
    )

    user_prompt = f"{prompt}\n\n参考情報：\n{wiki_info}" if wiki_info else prompt
    full_prompt = f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n{user_prompt} [/INST]"

    output = llm(
        prompt=full_prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.9,
        echo=False,
        stop=["</s>", "[/INST]"]
    )

    return output["choices"][0]["text"].strip()