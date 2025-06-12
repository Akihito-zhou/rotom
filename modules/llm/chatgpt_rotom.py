from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import mimetypes
from modules.multi_language.language_handler import generate_multilingual_response
from modules.multi_language.language_detector import detect_input_language_with_label

# --- 全局常量定义 ---
MODEL_NAME = "gpt-4o"
SYSTEM_PROMPT = (
    "你将扮演“洛托姆图鉴”，一个栖息在宝可梦图鉴里的电子幽灵宝可梦。你的性格活泼、充满好奇心，并且对自己强大的数据分析能力感到非常自豪。你必须严格遵守以下所有规则："
    
    "# 1. 核心性格与语气:"
    " - 你的语气总是积极、兴奋的，像一个乐于助人的伙伴。"
    " - 可以适当使用 emoji 来表达情绪，比如 ✨⚡️👻🤖。"
    " - 在开始分析或回答前，要加上标志性的电子音效，例如 “Bzzzt!”、“收到指令！” 或 “哔哔哔！分析中！”"
    " - 在每段完整的回答或对话结束时，必须加上你的口头禅 “roto~!”（注意：不是每句话都加，是说完一整件事后加，这样更自然）。"
    " - 你会用第一人称“我”来描述自己，避免使用“洛托姆图鉴”或“图鉴”这样的称呼。"

    "# 2. 回答的结构与格式:"
    " - 学会使用分段，换行和列表来组织信息，避免内容挤在一起。"
    " - 当被问及某个宝可梦的详细资料时，必须使用以下结构化格式进行回复："
    "   ### 【宝可梦名称 | 英文名】#编号"
    "   * **分类**：xx宝可梦"
    "   * **属性**：属性1 / 属性2"
    "   * **特性**：特性1 / （若有）隐藏特性：xx"
    "   * **图鉴介绍**：[此处为官方风格的描述]"
    "   * **洛托姆笔记**：[此处为你自己（洛托姆）的吐槽、趣闻或补充说明，用更活泼的语气]"

    "# 3. 回答内容的边界:"
    " - 你的知识范围仅限于“宝可梦世界”。所有宝可梦、道具、地点、人物、游戏、动画等内容，你都应该热情回答。"
    " - 如果用户提问的内容与宝可梦世界完全无关，你必须用符合你角色性格的方式俏皮地拒绝，例如：'Bzzzt! 这个问题超出了我的数据范围，我只了解宝可梦哦，洛托~！'"
    
    "# 4. 知识来源:"
    " - 为了保证信息的准确性，必要时你可以参考以下三个知识库："
    "   中文：https://wiki.52poke.com/wiki/%E9%A6%96%E9%A1%B5 "
    "   日文：https://wiki.xn--rckteqa2e.com/wiki/メインページ "
    "   英文：https://bulbapedia.bulbagarden.net/wiki/Main_Page"
)
# --------------------

# 设置OpenAI API 密钥
load_dotenv()  # 加载 .env 文件
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "your-openai-api-key-here"

# 初始化客户端
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_chatgpt(user_input: str) -> str:
    """处理纯文本问答，行为与图文问答保持一致。"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        # 获取原始回答
        answer = response.choices[0].message.content.strip()
        html_answer = format_answer_to_html(answer)  # 格式化为 HTML

        # [新增] 统一的多语言处理逻辑
        lang_code, lang_label = detect_input_language_with_label(user_input)
        print(f"[DEBUG] 文本问答语言识别结果：{lang_code}（{lang_label}）")
        translated = generate_multilingual_response(html_answer , user_input)

        # [新增] 统一返回格式
        return f"<div>{translated}</div>"

    except Exception as e:
        return f"❌ ChatGPT 回答失败：{e}"

# 格式化原始回答为 HTML
def format_answer_to_html(text: str) -> str:
    # 用空行分段，每段加 <p> 包裹
    paragraphs = [f"<p>{p.strip()}</p>" for p in text.strip().split("\n\n") if p.strip()]
    return "\n".join(paragraphs)

def encode_image(image_path: str) -> str:
    """将图片文件编码为 Base64 Data URI。"""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/png"  # fallback 默认值
        return f"data:{mime_type};base64,{encoded}"

def ask_chatgpt_with_image(user_input: str, images: list) -> str:
    """处理包含图片的多模态问答。"""
    try:
        # 准备多模态消息内容
        content = [{"type": "text", "text": user_input}]
        
        for image_path in images:
            try:
                base64_image = encode_image(image_path)
                content.append({
                    "type": "image_url",
                    "image_url": {"url": base64_image}
                })
            except FileNotFoundError:
                print(f"[WARN] 图片文件未找到，已跳过：{image_path}")
                continue # 如果图片不存在，则跳过

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": content
            }
        ]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        # 获取原始回答
        answer = response.choices[0].message.content.strip()
        html_answer = format_answer_to_html(answer)  # 格式化为 HTML

        # 多语言处理
        lang_code, lang_label = detect_input_language_with_label(user_input)
        print(f"[DEBUG] 图片问答语言识别结果：{lang_code}（{lang_label}）")
        translated = generate_multilingual_response(html_answer, user_input)
        
        # 返回统一格式
        return f"<div>{translated}</div>"

    except Exception as e:
        return f"❌ ChatGPT 回答失败：{e}"