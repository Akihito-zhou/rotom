from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import json

# 设置OpenAI API 密钥
load_dotenv()  # 加载 .env 文件
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "your-openai-api-key-here"

# 初始化客户端（使用 gpt-4o 模型）
client = OpenAI(api_key=OPENAI_API_KEY)
def extract_entity_name(user_input: str) -> str:
    prompt = f"""
你是一个宝可梦图鉴助手，帮我从以下用户问题中提取他们想要了解的关键词（宝可梦、技能或特性名），
请只返回该关键词本身，不要多余解释。

问题：「{user_input}」

只返回关键词字符串。
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=20
        )
        keyword = response.choices[0].message.content.strip()
        return keyword
    except Exception as e:
        print(f"[ERROR] ChatGPT 关键词提取失败: {e}")
        return ""

def extract_fields(user_input: str) -> list:
    prompt = f"""
你是一个宝可梦图鉴助手，专门用于信息提取任务。
请根据下方的字段说明，从用户的问题中识别他们想要了解的具体信息类型。
**只返回字段对应的英文关键词列表，按照以下字段列表限定输出**，无需解释、注释或其他额外文字。

根据问题的上下文推断出该问题指的是宝可梦（pokemon）、技能（move）或特性（ability），然后只输出该类型下的字段关键词。

宝可梦字段（pokemon）：
["basic",         // 名称、编号、种类、属性、性别比等基础资料
 "profile",       // 简介文本
 "types",         // 属性，如火、草等
 "ability",       // 特性，包括隐藏特性
 "stats",         // 能力值（HP、攻击、防御等）
 "moves",         // 技能（等级学习／招式机）
 "flavor",        // 图鉴描述（世代版本）
 "evolution",     // 进化链
 "images"]        // 图片：包括形态图、插画、样子、图片展示、图片长什么样、正面图等

技能字段（move）：
["generation", "category", "accuracy", "attack_range", "text", "effect", "info", "pokemon"]

特性字段（ability）：
["generation", "count", "text", "effect", "info", "pokemon"]

例如：
问题：「飞翔有什么效果？」 → 返回：["effect", "text"]
问题：「妙蛙种子会什么技能？」→ 返回：["moves"]
（这只是例子，请不要直接使用，不要每次都返回这几个字段。请根据用户问题来精准判断。）

请根据以下用户问题，判断他们最关心哪些字段：
用户问题：「{user_input}」
"""


    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100
        )
        content = response.choices[0].message.content.strip()

        # 尝试从返回中解析字段列表
        match = re.search(r"\[.*?\]", content)
        if match:
            return json.loads(match.group())
        return []
    except Exception as e:
        print(f"[ERROR] ChatGPT 字段提取失败: {e}")
        return []
    
    