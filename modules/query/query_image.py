from modules.query.config import IMAGE_DIR
from urllib.parse import quote
import os

def get_all_form_images(index: str, name: str, extra_images: list = None) -> str:
    img_html = ""
    index_fmt = f"{int(index):04}"
    prefix = f"{index_fmt}-{name}"

    if os.path.isdir(IMAGE_DIR):
        for file in sorted(os.listdir(IMAGE_DIR)):
            if not file.startswith(prefix) or not file.endswith(".png"):
                continue

            file_path = os.path.abspath(os.path.join(IMAGE_DIR, file))
            file_url = f"file:///{quote(file_path.replace(os.sep, '/'))}"

            label = file[len(prefix):].replace(".png", "").lstrip("-") or "默认形态"
            label = label.replace("shiny", "✨ Shiny 版").replace("--", "-")
            if "Shiny 版" not in label:
                label = f"🎨 {label}"

            img_html += f"<div><b>{label}</b><br><img src='{file_url}' style='max-width:200px; border-radius:10px;'></div><br>"

    if extra_images:
        for form in extra_images:
            for key, label in [("image", "🎨 默认形态"), ("shiny", "✨ Shiny 版")]:
                file = form.get(key)
                if not file:
                    continue
                file_path = os.path.abspath(os.path.join(IMAGE_DIR, file))
                file_url = f"file:///{quote(file_path.replace(os.sep, '/'))}"
                img_html += f"<div><b>{form['name']} - {label}</b><br><img src='{file_url}' style='max-width:200px; border-radius:10px;'></div><br>"

    return img_html