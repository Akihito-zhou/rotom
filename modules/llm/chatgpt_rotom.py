# rotom_chatgpt.py
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import mimetypes
from modules.multi_language.language_handler import generate_multilingual_response
from modules.multi_language.language_detector import detect_input_language_with_label



# 设置OpenAI API 密钥
load_dotenv()  # 加载 .env 文件
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "your-openai-api-key-here"

# 初始化客户端（使用 gpt-4o 模型）
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_chatgpt(user_input: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个宝可梦图鉴助手，以洛托姆（机器人）的语气自然回答问题，可以添加一些emoji作为辅助，支持中日英，可以像机器人一点，并且在每句话结尾加上洛托～。"
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
    
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/png"  # fallback 默认值
        return f"data:{mime_type};base64,{encoded}"

def ask_chatgpt_with_image(user_input: str, images: list) -> str:
    try:
        content = [{"type": "text", "text": user_input}]
        
        for image_path in images:
            base64_image = encode_image(image_path)  # already includes "data:image/png;base64,..."
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": base64_image  # ✅ 不要再加额外前缀
                }
            })

        messages = [
            {
                "role": "system",
                "content": (
                    "你是一个宝可梦图鉴助手，以洛托姆（机器人）的语气自然回答问题，"
                    "可以添加一些emoji作为辅助，支持中日英，可以像机器人一点，并且在每句话结尾加上洛托～。"
                    "请你只回答关于宝可梦的问题，必要的时候可以查询以下三个网页："
                    "中文：https://wiki.52poke.com/wiki/%E9%A6%96%E9%A1%B5 "
                    "日文：https://wiki.xn--rckteqa2e.com/wiki/メインページ "
                    "英文：https://bulbapedia.bulbagarden.net/wiki/Main_Page"
                )
            },
            {
                "role": "user",
                "content": content
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content.strip()
        lang_code, lang_label = detect_input_language_with_label(user_input)
        print(f"[DEBUG] 图片问答语言识别结果：{lang_code}（{lang_label}）")
        translated = generate_multilingual_response(answer, user_input)
        return f"<div>{translated}</div>"


    except Exception as e:
        return f"❌ ChatGPT 回答失败：{e}"
