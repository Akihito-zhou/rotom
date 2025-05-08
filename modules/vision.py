# modules/vision.py
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from modules.chat import ask_gpt

# 初始化模型
# 禁用 float16，避免 MPS 引发崩溃
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    torch_dtype=torch.float32,   # 强制 float32
)
model.eval()
model.eval()

def describe_image(image_path: str) -> str:
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=50)

        caption_en = processor.tokenizer.decode(output[0], skip_special_tokens=True)

        # 构造 GPT 输入 prompt（风格+日语+情绪）
        prompt = (
            f"画像に写っているのは「{caption_en}」です。"
            f"ロトムのように日本語で短く明して。"
        )

        # 交给 GPT 生成风格化日语回复
        caption_ja = ask_gpt(prompt)

        return caption_ja

    except Exception as e:
        return f"うわっ！画像の処理中にエラーが起きちゃったロト… ({str(e)})"