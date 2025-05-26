import os
import json
from pokemon_query import query_local

POKEMON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pokemon-dataset-zh", "data", "pokemon"))

def test_all_pokemon_entries():
    print(f"[INFO] 正在测试图鉴目录：{POKEMON_DIR}\n")

    failed_cases = []
    total = 0
    success_count = 0

    for file in sorted(os.listdir(POKEMON_DIR)):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(POKEMON_DIR, file)
        total += 1

        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ 无法读取文件 {file}: {e}")
            failed_cases.append((file, "JSON 解析失败"))
            continue

        name = data.get("name")
        if not name:
            print(f"⚠️  文件 {file} 缺少 name 字段，跳过")
            failed_cases.append((file, "缺少 name 字段"))
            continue

        try:
            success, _ = query_local(name, "pokemon")
            if success:
                print(f"✅ 匹配成功：{file}（{name}）")
                success_count += 1
            else:
                print(f"❌ 匹配失败：{file}（{name}）")
                failed_cases.append((file, name))
        except Exception as e:
            print(f"🔥 匹配出错：{file}（{name}） -> {e}")
            failed_cases.append((file, f"异常: {e}"))

    print("\n📋 测试完成：共 {}/{} 条匹配成功".format(success_count, total))
    print("❌ 无法匹配的文件数量：", len(failed_cases))

    if failed_cases:
        print("\n🔍 匹配失败列表：")
        for file, reason in failed_cases:
            print(f" - {file} 👉 原因：{reason}")

if __name__ == "__main__":
    test_all_pokemon_entries()