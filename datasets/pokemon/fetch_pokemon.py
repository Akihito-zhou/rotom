import re
import csv
from bs4 import BeautifulSoup

# 读取 HTML 文件
with open('/Users/aki/Desktop/ninjyoukon/rotom/datasets/pokemon/pokemon_list.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 用正则匹配所有 {{Rdexe|...}} 模板内容
pattern = r"\{\{Rdexe\|(\d+)\|([^|]+)\|([^|]+)\|([^}]+)\}\}"
matches = re.findall(pattern, html)

# 写入 CSV
with open('/Users/aki/Desktop/ninjyoukon/rotom/datasets/pokemon/pokemon_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['No.', 'Chinese Name', 'Japanese Name', 'English Name'])
    for match in matches:
        writer.writerow(match)

print("✅ CSV 文件已生成：pokemon_list.csv")