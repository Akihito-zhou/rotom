# import os
# import json
# from pokemon_query import query_local

# POKEMON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pokemon-dataset-zh", "data", "ability"))

# def test_all_pokemon_entries():
#     print(f"[INFO] 正在测试图鉴目录：{POKEMON_DIR}\n")

#     failed_cases = []
#     total = 0
#     success_count = 0

#     for file in sorted(os.listdir(POKEMON_DIR)):
#         if not file.endswith(".json"):
#             continue

#         file_path = os.path.join(POKEMON_DIR, file)
#         total += 1

#         try:
#             with open(file_path, encoding="utf-8") as f:
#                 data = json.load(f)
#         except Exception as e:
#             print(f"❌ 无法读取文件 {file}: {e}")
#             failed_cases.append((file, "JSON 解析失败"))
#             continue

#         name = data.get("name")
#         if not name:
#             print(f"⚠️  文件 {file} 缺少 name 字段，跳过")
#             failed_cases.append((file, "缺少 name 字段"))
#             continue

#         try:
#             success, _ = query_local(name, "pokemon")
#             if success:
#                 print(f"✅ 匹配成功：{file}（{name}）")
#                 success_count += 1
#             else:
#                 print(f"❌ 匹配失败：{file}（{name}）")
#                 failed_cases.append((file, name))
#         except Exception as e:
#             print(f"🔥 匹配出错：{file}（{name}） -> {e}")
#             failed_cases.append((file, f"异常: {e}"))

#     print("\n📋 测试完成：共 {}/{} 条匹配成功".format(success_count, total))
#     print("❌ 无法匹配的文件数量：", len(failed_cases))

#     if failed_cases:
#         print("\n🔍 匹配失败列表：")
#         for file, reason in failed_cases:
#             print(f" - {file} 👉 原因：{reason}")

# if __name__ == "__main__":
#     test_all_pokemon_entries()

# import os
# import json

# # ✅ 修改为你的实际 JSON 文件夹路径
# POKEMON_DIR = "C:\\Users\\12730\\Desktop\\pokemon_VQA\\rotom\\pokemon-dataset-zh\\data\\pokemon"

# # 📌 粘贴你提供的156个宝可梦中文名
# failed_names = [
#     "小磁怪", "三合一磁怪", "霹雳电球", "顽皮雷弹", "海星星", "宝石海星", "百变怪", "多边兽", "急冻鸟",
#     "闪电鸟", "火焰鸟", "超梦", "梦幻", "未知图腾", "多边兽Ⅱ", "电击怪", "雷公", "炎帝", "水君", "洛奇亚",
#     "凤王", "时拉比", "脱壳忍者", "月石", "太阳岩", "天秤偶", "念力土偶", "铁哑铃", "金属怪", "巨金怪",
#     "雷吉洛克", "雷吉艾斯", "雷吉斯奇鲁", "盖欧卡", "固拉多", "烈空坐", "基拉祈", "代欧奇希斯", "铜镜怪",
#     "青铜钟", "自爆磁怪", "多边兽Ｚ", "洛托姆", "由克希", "艾姆利多", "亚克诺姆", "帝牙卢卡", "帕路奇亚",
#     "雷吉奇卡斯", "骑拉帝纳", "霏欧纳", "玛纳霏", "达克莱伊", "谢米", "阿尔宙斯", "比克提尼", "齿轮儿",
#     "齿轮组", "齿轮怪", "几何雪花", "泥偶小人", "泥偶巨人", "勾帕路翁", "代拉基翁", "毕力吉翁", "莱希拉姆",
#     "捷克罗姆", "酋雷姆", "凯路迪欧", "美洛耶塔", "盖诺赛克特", "小碎钻", "哲尔尼亚斯", "伊裴尔塔尔",
#     "基格尔德", "蒂安希", "胡帕", "波尔凯尼恩", "属性：空", "银伴战兽", "小陨星", "破破舵轮", "卡璞・鸣鸣",
#     "卡璞・蝶蝶", "卡璞・哞哞", "卡璞・鳍鳍", "科斯莫古", "科斯莫姆", "索尔迦雷欧", "露奈雅拉", "虚吾伊德",
#     "爆肌蚊", "费洛美螂", "电束木", "铁火辉夜", "纸御剑", "恶食大王", "奈克洛兹玛", "玛机雅娜", "玛夏多",
#     "毒贝比", "四颚针龙", "垒磊石", "砰头小丑", "捷拉奥拉", "美录坦", "美录梅塔", "来悲茶", "怖思壶",
#     "列阵兵", "雷鸟龙", "雷鸟海兽", "鳃鱼龙", "鳃鱼海兽", "苍响", "藏玛然特", "无极汰那", "萨戮德",
#     "雷吉艾勒奇", "雷吉铎拉戈", "雪暴马", "灵幽马", "蕾冠王", "一对鼠", "一家鼠", "雄伟牙", "吼叫尾",
#     "猛恶菇", "振翼发", "爬地翅", "沙铁皮", "铁辙迹", "铁包袱", "铁臂膀", "铁脖颈", "铁毒蛾", "铁荆棘",
#     "索财灵", "赛富豪", "古简蜗", "古剑豹", "古鼎鹿", "古玉鱼", "轰鸣月", "铁武者", "故勒顿", "密勒顿",
#     "波荡水", "铁斑叶", "斯魔茶", "来悲粗茶", "破空焰", "猛雷鼓", "铁磐岩", "铁头壳", "桃歹郎"
# ]

# # 🔍 加载所有 JSON 中的 name 字段
# name_to_file = {}
# for file in os.listdir(POKEMON_DIR):
#     if file.endswith(".json"):
#         path = os.path.join(POKEMON_DIR, file)
#         try:
#             with open(path, encoding="utf-8") as f:
#                 data = json.load(f)
#                 name = data.get("name")
#                 if name:
#                     name_to_file[name] = file
#         except Exception as e:
#             print(f"❌ 错误读取文件 {file}: {e}")

# # ✅ 检查匹配情况
# print("\n=== 匹配检查结果 ===")
# not_found = []
# for name in failed_names:
#     if name in name_to_file:
#         print(f"✅ {name} -> {name_to_file[name]}")
#     else:
#         print(f"❌ {name} -> 未找到")
#         not_found.append(name)

# print(f"\n总计：{len(failed_names)} 个测试名")
# print(f"匹配成功：{len(failed_names) - len(not_found)} 个")
# print(f"匹配失败：{len(not_found)} 个")

import os
import json
from modules.query.query_all import query_local

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pokemon-dataset-zh", "data"))
POKEMON_DIR = os.path.join(BASE_DIR, "pokemon")
MOVE_DIR = os.path.join(BASE_DIR, "move")
ABILITY_DIR = os.path.join(BASE_DIR, "ability")

def test_category(category, dir_path):
    print(f"\n[TEST] 正在测试类别：{category} ({dir_path})")
    total = 0
    failed = []

    for file in os.listdir(dir_path):
        if not file.endswith(".json"):
            continue
        path = os.path.join(dir_path, file)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            name = data.get("name")
            if not name:
                print(f"⚠️ 缺少 name 字段：{file}")
                failed.append(file)
                continue

            success, _ = query_local(name, category)
            if success:
                print(f"✅ 匹配成功：{file} - {name}")
            else:
                print(f"❌ 匹配失败：{file} - {name}")
                failed.append(file)
            total += 1
        except Exception as e:
            print(f"🔥 错误读取文件 {file}: {e}")
            failed.append(file)

    print(f"\n📊 共测试 {total} 条，失败 {len(failed)} 条")
    if failed:
        print("❌ 失败列表:")
        for f in failed:
            print(f" - {f}")

def test_all():
    test_category("pokemon", POKEMON_DIR)
    # test_category("move", MOVE_DIR)
    # test_category("ability", ABILITY_DIR)

if __name__ == "__main__":
    test_all()
