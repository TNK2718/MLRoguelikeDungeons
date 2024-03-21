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
settings.disallow_tokens(tokenizer, [tokenizer.eos_token_id])

prompt = "Tell me about One Punch Man."
prompt_template=f'''[INST] <<SYS>>
You are a helpful, respectful and honest assistant.
<</SYS>>
{prompt}[/INST]

'''

max_new_tokens = 1024

generator.warmup()
time_begin = time.time()

output = generator.generate_simple(prompt_template, settings, max_new_tokens, seed=1234)

time_end = time.time()
time_total = time_end - time_begin

print(output)
print()
print(
    f"Response generated in {time_total:.2f} seconds, {max_new_tokens} tokens, {max_new_tokens / time_total:.2f} tokens/second")
