import os

# 修改为你的项目图像路径
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pokemon-dataset-zh", "data"))
IMAGE_DIR = os.path.join(BASE_DIR, "images", "home")


def get_all_forms_images(index: str, name: str):
    index_fmt = f"{int(index):04}"
    prefix = f"{index_fmt}-{name}"
    found_images = []

    for file in os.listdir(IMAGE_DIR):
        if not file.endswith(".png") or not file.startswith(prefix):
            continue

        # 去掉.png后按-分隔
        parts = file[:-4].split('-')
        form_parts = parts[2:]  # 去掉编号和中文名
        form_name = "-".join(form_parts).replace("-shiny", "")
        is_shiny = "shiny" in file.lower()

        label = f"{form_name or '默认形态'} {'(Shiny)' if is_shiny else '(普通)'}"
        image_path = os.path.abspath(os.path.join(IMAGE_DIR, file))
        found_images.append((label, image_path))

    return found_images


if __name__ == "__main__":
    # 👇 测试目标
    test_cases = [
        ("0003", "妙蛙花"),
        ("0006", "喷火龙"),
        ("0020", "拉达")
    ]

    for index, name in test_cases:
        print(f"\n=== 📘 {name}（No.{index}）的所有图像形态 ===")
        results = get_all_forms_images(index, name)
        if not results:
            print("⚠️ 未找到任何图像")
        for label, path in results:
            print(f"{label}：{path}")