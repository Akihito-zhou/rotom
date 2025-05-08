import re
import csv

with open('/Users/aki/Desktop/ninjyoukon/rotom/datasets/ability/ability_list.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 正则提取所有特性
pattern = r"\{\{特性列表\|(\d+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|(\d+)\|(\d+)\}\}"
matches = re.findall(pattern, content)

# 写入 CSV 文件
with open('/Users/aki/Desktop/ninjyoukon/rotom/datasets/ability/ability_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['No.', 'Chinese Name', 'Japanese Name', 'English Name', 'Description (Simplified)', 'Description (Traditional)', 'Common', 'Hidden'])

    for m in matches:
        writer.writerow([s.strip() for s in m])

print("✅ 特性 CSV 文件已生成：ability_list.csv")