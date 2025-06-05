import os
import torch
import clip
import pickle
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ==== 配置路径 ====
BASE_DIR = os.path.dirname(__file__)
FEATURE_PATH = os.path.join(BASE_DIR, "checkpoints", "image_features.pkl")

# ==== 设备 & 模型 ====
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# ==== 加载特征库 ====
with open(FEATURE_PATH, "rb") as f:
    feature_db = pickle.load(f)

# ==== 查找相似图片 ====
def find_best_match(query_image_path, topk=1):
    image = preprocess(Image.open(query_image_path).convert("RGB")).unsqueeze(0).to(device)

    with torch.no_grad():
        query_feature = model.encode_image(image)
        query_feature = query_feature / query_feature.norm(dim=-1, keepdim=True)
        query_feature = query_feature.cpu().numpy()

    sims = []
    for db_path, db_feature in feature_db.items():
        sim = cosine_similarity(query_feature, db_feature)[0][0]
        sims.append((db_path, sim))

    sims.sort(key=lambda x: x[1], reverse=True)

    return sims[:topk]

def find_best_match_from_frame(frame, topk=1):
    from modules.pokemon_images_detection.find_match import find_best_match
    import cv2
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        cv2.imwrite(tmp.name, frame)
        return find_best_match(tmp.name, topk=topk)