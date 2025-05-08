import re
import csv

def clean_description(desc):
    # 提取 zh-hans 的部分（简体中文）
    zh_match = re.search(r'zh-hans:([^;]+);', desc)
    return zh_match.group(1).strip() if zh_match else desc.strip()

with open('/Users/aki/Desktop/ninjyoukon/rotom/datasets/item/item_list.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 正则提取：{{I|中文}} | 日文 | 英文 | 描述
pattern = r"\{\{I\|([^}]+)\}\}\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*(.*?)(?:\n|\r|\|-)"
matches = re.findall(pattern, content)

with open('/Users/aki/Desktop/ninjyoukon/rotom/datasets/item/item_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['No.', 'Chinese Name', 'Japanese Name', 'English Name'])

    for idx, (zh, jp, en, desc) in enumerate(matches, start=1):
        desc_clean = clean_description(desc)
        writer.writerow([idx, zh.strip(), jp.strip(), en.strip(), desc_clean])

print("✅ CSV 文件已生成：item_list.csv")