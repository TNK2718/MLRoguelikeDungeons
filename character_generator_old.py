import os
from llama_cpp import Llama


# Load prompts
prompt_path = './prompts'
with open(os.path.join(prompt_path, 'system_message.txt')) as f:
    system_message = f.read()
with open(os.path.join(prompt_path, 'prompt.txt')) as f:
    prompt = f.read()

starting = "Monster Name:"

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = Llama(
  model_path="./tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",  # Download the model file first
  n_ctx=2048,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=35         # The number of layers to offload to GPU, if you have GPU acceleration available
)

output = llm(
  "<|system|>\n" + system_message + "</s>\n<|user|>\n" + prompt + "</s>\n<|assistant|>" + starting, # Prompt
  max_tokens=2048,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=False        # Whether to echo the prompt
)
print(output["choices"][0]["text"])