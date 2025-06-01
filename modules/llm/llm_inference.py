from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re


class LLMParser:
    def __init__(self, model_path="01-ai/Yi-1.5-9B-Chat", device="auto"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map=device,
            attn_implementation="eager"
        )

    def build_prompt(self, user_input: str) -> str:
        """构造提示词"""
        return f"""你是一个宝可梦图鉴助手，请根据用户的问题，提取意图和目标实体。

【任务说明】
请严格提取以下三个字段：
1. target：用户提到的实体名称（如“皮卡丘”、“恶臭”、“十万伏特”）
2. target_type：该实体的类型（宝可梦 / 技能 / 特性）
3. intent：用户想了解的内容（如 查询、进化、属性）

【输出格式】
请仅输出一行 JSON，不要添加解释：
{{"target": "实体名称", "target_type": "宝可梦/技能/特性", "intent": "意图"}}

【示例】
用户：皮卡丘是技能还是宝可梦？
助手：{{"target": "皮卡丘", "target_type": "宝可梦", "intent": "查询"}}

用户：{user_input}
助手："""

    def extract_intent_entities(self, user_input: str) -> dict:
        """执行意图识别任务"""
        prompt = self.build_prompt(user_input)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        try:
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=False,
                temperature=0.1,
                eos_token_id=self.tokenizer.eos_token_id
            )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"[DEBUG] 模型原始输出:\n{response}")

            # 尝试匹配 JSON 格式
            match = re.search(r'\{.*?\}', response)
            if match:
                data = json.loads(match.group(0))
                return {
                    "target": data.get("target", "未知"),
                    "target_type": data.get("target_type", "未知"),
                    "intent": data.get("intent", "未知")
                }

        except Exception as e:
            print(f"[ERROR] 模型输出或解析失败: {e}")

        # fallback 返回
        return {
            "target": "未知",
            "target_type": "未知",
            "intent": "未知"
        }


# 测试用
if __name__ == "__main__":
    parser = LLMParser()
    print("🔍 LLM 意图识别测试（输入自然语言问题）\n输入 'exit' 退出。")

    while True:
        query = input("\n💬 请输入问题：")
        if query.strip().lower() == "exit":
            break

        result = parser.extract_intent_entities(query)
        print("📤 提取结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
