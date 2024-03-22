from exllamav2 import (
    ExLlamaV2,
    ExLlamaV2Config,
    ExLlamaV2Cache,
    ExLlamaV2Tokenizer,
)

from exllamav2.generator import (
    ExLlamaV2BaseGenerator,
    ExLlamaV2Sampler
)

import time
import os

# Initialize model and cache

# ダウンロードしたモデルのディレクトリを指定
model_directory = "./Llama-2-7b-Chat-GPTQ"

config = ExLlamaV2Config()
config.model_dir = model_directory
config.prepare()

model = ExLlamaV2(config)
print("Loading model: " + model_directory)

# 複数GPUを使う場合、それぞれへのメモリ振り分けを設定。
# シングルGPUの場合は引数指定不要
# model.load([18, 24])
model.load()

tokenizer = ExLlamaV2Tokenizer(config)

cache = ExLlamaV2Cache(model)

# Initialize generator

generator = ExLlamaV2BaseGenerator(model, cache, tokenizer)

# Generate some text

settings = ExLlamaV2Sampler.Settings()
settings.temperature = 0.85
settings.top_k = 50
settings.top_p = 0.8
settings.token_repetition_penalty = 1.15

prompt_path = './prompts'
with open(os.path.join(prompt_path, 'character_system_message.txt')) as f:
    system_message = f.read()
with open(os.path.join(prompt_path, 'character_prompt.txt')) as f:
    prompt = f.read()

prompt_template = f'''[INST] <<SYS>>
{system_message}
<</SYS>>
{prompt}[/INST]
''' + "{"

max_new_tokens = 1024

generator.warmup()
time_begin = time.time()

# output = generator.generate_simple(
#     prompt_template, settings, max_new_tokens, seed=1234)
output = generator.generate_simple(
    prompt_template, settings, max_new_tokens)

time_end = time.time()
time_total = time_end - time_begin

print(output)
print()
print(f"Response generated in {time_total:.2f} seconds")

