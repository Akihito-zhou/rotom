import os
import clip
import torch
from PIL import Image
import numpy as np
import pickle

# 设备选择
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 路径设置
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "train_data")
IMAGE_DIR = os.path.join(DATA_DIR, "train")
SAVE_PATH = os.path.join(BASE_DIR, "checkpoints", "image_features.pkl")

# 保证保存目录存在
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

# 提取特征
features = {}
for root, _, files in os.walk(IMAGE_DIR):
    for file in files:
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        path = os.path.join(root, file)
        try:
            image = Image.open(path).convert("RGB")
            image_tensor = preprocess(image).unsqueeze(0).to(device)

            with torch.no_grad():
                feature = model.encode_image(image_tensor).float()
                feature = feature / feature.norm(dim=-1, keepdim=True)

            features[path] = feature.cpu().numpy()
            print(f"✅ Processed: {path}")
        except Exception as e:
            print(f"⚠️ Failed: {path} → {e}")

# 保存为指定路径
with open(SAVE_PATH, "wb") as f:
    pickle.dump(features, f)

print(f"🎉 所有图像特征已保存到 {SAVE_PATH}")