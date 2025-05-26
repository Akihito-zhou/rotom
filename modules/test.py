import sys
import os
import json

# 把 rotom 根目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 然后使用无前缀导入
from pokemon_query import format_pokemon_html

# 设置宝可梦编号（例如 1 为妙蛙种子）
POKEMON_INDEX = 1
POKEMON_JSON_PATH = os.path.abspath(
    os.path.join("pokemon-dataset-zh", "data", "pokemon", f"{POKEMON_INDEX:03}.json")
)

if os.path.exists(POKEMON_JSON_PATH):
    with open(POKEMON_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        html = format_pokemon_html(data)

        with open("test_output.html", "w", encoding="utf-8") as out:
            out.write(f"<html><body>{html}</body></html>")

        print("✅ HTML 输出成功，打开 test_output.html 查看渲染效果。")
else:
    print(f"❌ 找不到 JSON 文件：{POKEMON_JSON_PATH}")