# rotom_chatgpt.py
from openai import OpenAI
import os
import re
import json


# 设置OpenAI API 密钥
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

【字段列表说明】
以下是所有可提取的字段，仅可返回以下英文关键词：

宝可梦相关字段（category = "pokemon"）：
- name：名称相关
- types：属性
- ability：特性
- stats：能力值（HP/攻击/防御等）
- moves：技能（包含等级学习与招式机学习）
- profile：宝可梦简介
- flavor_texts：图鉴描述（按世代与版本划分）
- evolution：进化信息（进化阶段及条件）
- generation：登场世代
- image：图像展示

技能（招式）相关字段（category = "move"）：
- name：名称相关
- generation：登场世代
- category：属性 + 类别（如物理/特殊/变化）
- accuracy：威力、命中、PP
- attack_range：攻击范围
- text：简介
- effect：实战效果
- info：机制说明
- pokemon：可学习此技能的宝可梦

特性相关字段（category = "ability"）：
- name：名称相关
- generation：登场世代
- text：简介
- effect：实战效果
- info：机制说明
- count：拥有此特性的宝可梦数量（常规+隐藏）
- pokemon：拥有此特性的宝可梦列表

---

请根据以下用户问题，判断他们最关心哪些字段：
用户问题：「{user_input}」

请只返回字段关键词组成的 **JSON 数组**，格式如下：
["types", "moves", "stats"]
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

def ask_chatgpt(user_input: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个宝可梦图鉴助手，以洛托姆（机器人）的语气自然回答问题，支持中日英，可以像机器人一点，并且在每句话结尾加上洛托～。"
                "请你只回答关于宝可梦的问题，必要的时候可以查询，以下三个网页："
                "中文：https://wiki.52poke.com/wiki/%E9%A6%96%E9%A1%B5"
                "日文：https://wiki.xn--rckteqa2e.com/wiki/メインページ"
                "英文：https://bulbapedia.bulbagarden.net/wiki/Main_Page"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ ChatGPT 回答失败：{e}"

