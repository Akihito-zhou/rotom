import json
import re
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


# ========= 1. 实体索引器 ========= #
def build_entity_index(pokemon_list, move_list, ability_list):
    def extract_names(item):
        return set([item.get("name"), item.get("name_en"), item.get("name_jp")])

    index = {
        "宝可梦": set(),
        "技能": set(),
        "特性": set(),
    }

    for p in pokemon_list:
        index["宝可梦"].update(extract_names(p))
    for m in move_list:
        index["技能"].update(extract_names(m))
    for a in ability_list:
        index["特性"].update(extract_names(a))

    return index


def classify_entity(name, entity_index):
    for category, name_set in entity_index.items():
        if name in name_set:
            return category
    return "未知"


# ========= 2. 意图识别器（Qwen） ========= #
class QwenIntentParser:
    def __init__(self, model_path="Qwen/Qwen1.5-7B-Chat", device="cuda"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
        
    def build_prompt(self, user_input: str) -> str:
        return f"""
你是一个宝可梦图鉴助手。

请从用户提问中提取以下两个字段：
- target：用户提到的实体名（如“皮卡丘”、“Stench”、“十万伏特”）
- intent：用户想查询的内容，如 查询、进化、技能、介绍、属性等

请以如下 JSON 格式输出：
{{"target": "实体名称", "intent": "意图"}}

用户：{user_input}
助手：
"""

    def extract(self, user_input: str) -> dict:
        prompt = self.build_prompt(user_input)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=False,
            temperature=0.1,
            eos_token_id=self.tokenizer.eos_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        match = re.search(r'\{.*?\}', response)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass

        return {"target": "未知", "intent": "查询"}


# ========= 3. 主控制器 ========= #
def handle_query(user_input, pokemon_list, move_list, ability_list, qwen_parser):
    entity_index = build_entity_index(pokemon_list, move_list, ability_list)
    parsed = qwen_parser.extract(user_input)
    target = parsed.get("target", "")
    intent = parsed.get("intent", "查询")
    entity_type = classify_entity(target, entity_index)

    if entity_type == "未知":
        return f"我不太确定“{target}”是宝可梦、技能还是特性，可以再确认一下吗？"

    # 响应逻辑（演示）
    return f"'{target}' 是一个{entity_type}，用户意图为：{intent}。系统将在此基础上查询详细信息。"


# ========= ✅ 示例测试 ========= #
# ========= 🔁 批量读取文件夹中所有 JSON ========= #
def load_all_json_from_folder(folder_path):
    all_data = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            try:
                with open(os.path.join(folder_path, file), encoding="utf-8") as f:
                    all_data.append(json.load(f))
            except Exception as e:
                print(f"[WARN] 无法读取 {file}：{e}")
    return all_data


# ========= ✅ 示例测试 ========= #
if __name__ == "__main__":
    # 请根据你的路径结构修改下面路径（相对路径或绝对路径皆可）
    base_dir = "pokemon-dataset-zh/data"
    pokemon_data = load_all_json_from_folder(os.path.join(base_dir, "pokemon"))
    move_data = load_all_json_from_folder(os.path.join(base_dir, "move"))
    ability_data = load_all_json_from_folder(os.path.join(base_dir, "ability"))

    parser = QwenIntentParser()

    print("✅ 宝可梦图鉴意图识别系统已启动（输入 exit 可退出）")
    while True:
        q = input("\n💬 请输入问题：")
        if q.strip().lower() == "exit":
            break
        result = handle_query(q, pokemon_data, move_data, ability_data, parser)
        print("📤 系统答复：", result)
