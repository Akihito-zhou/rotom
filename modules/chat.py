import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("elyza/ELYZA-japanese-Llama-2-7b")
model = AutoModelForCausalLM.from_pretrained("elyza/ELYZA-japanese-Llama-2-7b")
model.eval()  # 推理模式

def ask_gpt(prompt: str) -> str:
    system_prompt = "あなたはポケモンのロトムのようなアシスタントです。明るくて、ツンデレな性格で、ちょっと調子に乗っています。"
    input_text = f"{system_prompt}\nユーザー: {prompt}\nロトム:"

    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # 去掉前面的prompt，只保留回复内容
    return response.replace(input_text, "").strip()