from llama_cpp import Llama

# LLMの準備
# model_path = "./llama-2-7b-chat.Q4_K_M.gguf"
model_path = './llama-2-13b-chat.Q2_K.gguf'
llm = Llama(model_path=model_path, n_gpu_layers=32)

# プロンプトの準備
prompt = """[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible.
<</SYS>>
What is the meaning of vamp?[/INST]
"""

# 推論の実行
output = llm(
    prompt,
    temperature=0.1,
    echo=True,
)
print(output["choices"][0]["text"])
