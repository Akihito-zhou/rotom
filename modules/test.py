import os
import sys

# 加入项目根路径，确保可以 import modules 下的文件
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.pokemon_query import query_local


def test_query(keyword: str, category: str):
    print(f"\n🧪 正在测试 query_local('{keyword}', '{category}')\n")

    if category not in ["pokemon", "move", "ability"]:
        print("❌ 无效的类别，只能是 'pokemon'、'move' 或 'ability'")
        return

    try:
        result = query_local(keyword, category)
        if "找不到" in result or "未登録" in result or "図鑑データのフォルダが見つかりません" in result:
            print("❌ 查询失败")
        else:
            print("✅ 查询成功，结果片段如下：\n")
            # 输出前300字符，避免刷屏
            print(result[:300] + "...\n")
    except Exception as e:
        print(f"❌ 程序异常：{e}")


if __name__ == "__main__":
    # 可以自由修改下列测试内容
    test_query("妙蛙种子", "pokemon")
    test_query("恶臭", "ability")
    test_query("超极巨百火焚野", "move")