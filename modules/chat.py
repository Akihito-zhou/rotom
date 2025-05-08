import sys
import os
# 让你可以导入 modules.wiki_query
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

def ask_gpt(prompt: str) -> str:
    """
    使用 Elyza 指令模型进行日语对话生成，接入 Wiki 知识 + 洛托姆风格。
    """

    # 简单判断是否是宝可梦相关问题
    keywords = ["ポケモン", "特性", "進化", "種族値", "ピカチュウ", "御三家"]
    use_wiki = any(word in prompt for word in keywords)

    # 如果需要，从 wiki 中爬取补充信息
    if use_wiki:
        pokemon_name = extract_keyword(prompt)  # TODO: 简易关键词提取
        wiki_info = search_pokemon_wiki(pokemon_name)
    else:
        wiki_info = ""

    # 系统设定
    system_prompt = (
        "名前はロトム。"
        "短くて可愛い言葉を使う。"
        "電子図鑑のポケモン。"
        "専門情報を知ってたら、それに基づいてちゃんと教えるんだ。"
    )

    if wiki_info:
        user_prompt = f"{prompt}\n\n参考情報：\n{wiki_info}"
    else:
        user_prompt = prompt

    full_prompt = f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n{user_prompt} [/INST]"

    # 生成回复
    output = llm(
        prompt=full_prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.9,
        echo=False,
        stop=["</s>", "[/INST]"]
    )

    return output["choices"][0]["text"].strip()

# 简易关键词提取器
def extract_keyword(prompt: str) -> str:
    """
    从用户输入中简单提取宝可梦名字（默认提取第一个词或硬编码关键词）
    """
    for word in ["ピカチュウ", "ヒトカゲ", "フシギダネ", "ミュウツー", "イーブイ"]:
        if word in prompt:
            return word
    return prompt.strip().split()[0]  # 默认提取第一个词