import os
import shutil
import random
import re


# ===== 配置路径 =====
BASE_DIR = os.path.dirname(__file__)
SOURCE_DIRS = [
    "pokemon-dataset-zh/data/images/home",
    "pokemon-dataset-zh/data/images/official",
    "pokemon-dataset-zh/data/images/dream"
]
TARGET_DIR = os.path.join(BASE_DIR, "train_data")
SPLIT_RATIO = (0.8, 0.1, 0.1)

# ===== 主类名提取函数 =====
def extract_main_name(filename):
    name = os.path.splitext(filename)[0]  # 去掉扩展名

    # Case 1：中文宝可梦名，如 0003.2-超级妙蛙花.png 或 0003-妙蛙种子.png
    match_cn = re.match(r"\d{3,4}(?:\.\d)?-([^-]+)", name)
    if match_cn:
        return match_cn.group(1)

    # Case 2：英文名，如 1008Miraidon_Dream.png
    match_en = re.match(r"\d{3,4}([A-Za-z]+)", name)
    if match_en:
        return match_en.group(1)

    return None

# ===== 收集所有图片并按类名归组 =====
def collect_images():
    images = {}
    for src_dir in SOURCE_DIRS:
        if not os.path.isdir(src_dir):
            continue
        for file in os.listdir(src_dir):
            if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            label = extract_main_name(file)
            if not label:
                print(f"⚠️ 跳过无法解析：{file}")
                continue
            full_path = os.path.join(src_dir, file)
            images.setdefault(label, []).append(full_path)
    return images

# ===== 拆分并复制 =====
def split_and_copy(images):
    for subset in ["train", "val", "test"]:
        os.makedirs(os.path.join(TARGET_DIR, subset), exist_ok=True)

    for label, file_list in images.items():
        if len(file_list) < 3:
            # 如果图像太少，直接全部放到 train
            subset = "train"
            target_class_dir = os.path.join(TARGET_DIR, subset, label)
            os.makedirs(target_class_dir, exist_ok=True)
            for fpath in file_list:
                shutil.copy2(fpath, os.path.join(target_class_dir, os.path.basename(fpath)))
            continue

        random.shuffle(file_list)
        n = len(file_list)
        n_train = max(1, int(n * SPLIT_RATIO[0]))
        n_val = max(1, int(n * SPLIT_RATIO[1]))
        n_test = n - n_train - n_val

        # 如果总和 > n，就从 test 扣
        while n_train + n_val + n_test > n:
            n_test = max(0, n_test - 1)

        splits = {
            "train": file_list[:n_train],
            "val": file_list[n_train:n_train + n_val],
            "test": file_list[n_train + n_val:]
        }

        for subset, files in splits.items():
            if not files:
                continue
            target_class_dir = os.path.join(TARGET_DIR, subset, label)
            os.makedirs(target_class_dir, exist_ok=True)
            for fpath in files:
                shutil.copy2(fpath, os.path.join(target_class_dir, os.path.basename(fpath)))

# ===== 主程序入口 =====
if __name__ == "__main__":
    all_images = collect_images()
    if not all_images:
        print("❌ 未找到可用图像，检查目录或命名格式")
        exit(1)

    split_and_copy(all_images)
    total = sum(len(v) for v in all_images.values())
    print(f"✅ 成功拆分并整理 {total} 张图像，共 {len(all_images)} 个类别到 {TARGET_DIR}/ 中")