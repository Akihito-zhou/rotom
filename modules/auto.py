import os
import shutil
import random

SOURCE_DIR = "pokemon-dataset-zh/data/images/home"
TARGET_DIR = "train_data"
SPLIT_RATIO = (0.8, 0.1, 0.1)  # train/val/test

def parse_name(filename):
    parts = filename.split("-")
    if len(parts) < 2:
        return None
    name = parts[1].split(".")[0]  # 提取“妙蛙种子”部分
    return name

def collect_images():
    images = {}
    for file in os.listdir(SOURCE_DIR):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        name = parse_name(file)
        if not name:
            continue
        images.setdefault(name, []).append(file)
    return images

def split_and_copy(images):
    for subset in ["train", "val", "test"]:
        os.makedirs(os.path.join(TARGET_DIR, subset), exist_ok=True)

    for name, files in images.items():
        random.shuffle(files)
        n = len(files)
        n_train = int(n * SPLIT_RATIO[0])
        n_val = int(n * SPLIT_RATIO[1])
        n_test = n - n_train - n_val

        subsets = {
            "train": files[:n_train],
            "val": files[n_train:n_train+n_val],
            "test": files[n_train+n_val:]
        }

        for subset, subset_files in subsets.items():
            target_dir = os.path.join(TARGET_DIR, subset, name)
            os.makedirs(target_dir, exist_ok=True)
            for fname in subset_files:
                shutil.copy2(os.path.join(SOURCE_DIR, fname), os.path.join(target_dir, fname))

if __name__ == "__main__":
    imgs = collect_images()
    split_and_copy(imgs)
    print("✅ 图片已拆分到 train_data/ 中，结构符合分类任务要求。")