# test_find.py
import sys
import os

# 获取 rotom 项目的根目录
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT_DIR)

# 然后再正常导入模块
from modules.pokemon_images_detection.find_match import find_best_match

query_path = "/Users/aki/Desktop/ninjyoukon/rotom/modules/pokemon_images_detection/train_data/test/阿尔宙斯/0493-阿尔宙斯-龙属性.png"  # 换成你想测试的图片路径

matches = find_best_match(query_path)  # 默认 topk=1
best_match_path, score = matches[0]
print(f"🔍 最相似的图像是: {best_match_path}")
print(f"💡 相似度分数: {score:.4f}")