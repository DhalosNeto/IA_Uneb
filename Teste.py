from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Carregar o modelo
model_id = "deepseek-ai/deepseek-coder-6.7b-base"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

# Gerar uma resposta
prompt = "Escreva uma função Python que calcule a soma de uma lista."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
