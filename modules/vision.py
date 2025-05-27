import os
from modules.pokemon_images_detection.find_match import find_best_match
from .chat import query_local

def describe_image(image_path: str) -> str:
    try:
        result = find_best_match(image_path, topk=1)

        if not result:
            return "❌ 无法识别图像中宝可梦。"

        matched_path, score = result[0]
        matched_name = os.path.basename(os.path.dirname(matched_path))
        print(f"[DEBUG] Matched Pokémon: {matched_name}, Score: {score:.4f}")

        # 查图鉴
        found, html = query_local(matched_name, "pokemon")
        if found:
            return f"✅ 与图像最相似的是：<b>{matched_name}</b>（相似度：{score:.2f}）<br>{html}"
        else:
            return f"⚠️ 找到最相似的宝可梦：<b>{matched_name}</b>（相似度：{score:.2f}），但未能查询到其图鉴信息。"
    
    except Exception as e:
        return f"❌ 识别图像时出错：{str(e)}"