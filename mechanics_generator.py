from llama_cpp import Llama
import os
import random

# LLMの準備
# model_path = './llama-2-7b-chat.Q4_K_M.gguf'
# model_path = './llama-2-13b-chat.Q4_K_M.gguf'
model_path = './llama-2-13b-chat.Q2_K.gguf'

# Load llama2
seed = random.randint(0, 1e8)
print(seed)
llm = Llama(model_path=model_path, n_gpu_layers=-1,
            n_ctx=2048 + 512, seed=seed)

# Load prompt
# prompt_path = './prompt_8.txt'
# prompt_path = './prompt_9.txt'
prompt_path = './prompt_10.txt'

with open(prompt_path) as f:
    prompt = f.read()

# 推論の実行
output = llm(
    prompt,
    temperature=0.8,
    # stop=["]\n"],
    echo=False,
    max_tokens=-1)
print(output["choices"][0]["text"])
