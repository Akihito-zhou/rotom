import re
import csv

with open('/Users/aki/Desktop/ninjyoukon/rotom/datasets/move/move_list.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 改用 re.DOTALL 支持跨行匹配，修正 pattern
pattern = r"\{\{Movelist/gen/ex\|(\d+)\|([^\|]*)\|([^\|]*)\|([^\|]*)\|([^\|]*)\|([^\|]*)\|([^\|]*)\|([^\|]*)\|([^\}]*)\}\}"

matches = re.findall(pattern, content, re.DOTALL)

with open('/Users/aki/Desktop/ninjyoukon/rotom/datasets/move/move_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['No.', 'Chinese Name', 'Japanese Name', 'English Name', 'Type', 'Category', 'Power', 'Accuracy', 'PP'])

    for m in matches:
        writer.writerow([s.strip() for s in m])

print("✅ CSV 文件已生成：move_list.csv")

