from modules.query.query_all import query_local  # 假设你的主函数在 main.py 中

def run_tests():
    test_cases = [
        ("皮卡丘", "pokemon"),
        ("十万伏特", "move"),
        ("压迫感", "ability"),
        ("超梦", "pokemon"),
        ("同步", "ability"),
        ("不存在的名字", "pokemon"),
    ]

    for name, category in test_cases:
        print(f"🔍 测试输入：'{name}' （类别：{category}）")
        success, result = query_local(name, category)
        if success:
            print("✅ 查询成功！")
        else:
            print("❌ 查询失败！")
        print("-" * 60)

if __name__ == "__main__":
    run_tests()