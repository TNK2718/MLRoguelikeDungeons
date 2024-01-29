from llama_cpp import Llama

# LLMの準備
# model_path = './llama-2-7b-chat.Q4_K_M.gguf'
# model_path = './llama-2-13b-chat.Q4_K_M.gguf'
model_path = './llama-2-13b-chat.Q2_K.gguf'

llm = Llama(model_path=model_path, n_gpu_layers=50, n_ctx=1024)

"""
\"\"\"
You can ONLY use these words in your answer to express subject node: "self", "enemy", "place".
You can ONLY use these words in your answer to express action node: "attack", "shoot", "punch", "buff", "slash", "heal", "move", "place", "summon", "sneak", "break", "trace", "wait for", "push", "pull", "make do", "create".
You can ONLY use these words in your answer to express modifier node: "in front", "adjacent", "away", "temporary", "for some turns", "in range", "forward", "backward", "designated".
You can ONLY use these words in your answer to express decorator node: "if above", "if below", "if exist", "for x times", "while", "and", "or", "nor", "xor", "if desired".
You can ONLY use these words as noun node: "hp", "strength", "magic power", "flame", "ice", "lightning", "magic", "poison", "obstacle", "wall", "storm", "beam", "cross".
Delete any node else.
\"\"\"
"""

# プロンプトの準備
prompt = """[INST] <<SYS>> \"\"\"
You can ONLY use these words in your answer to express entitys node: "self", "enemy", "place".
You can ONLY use these words in your answer to express action node: "attack", "shoot", "punch", "buff", "slash", "heal", "move", "place", "summon", "sneak", "break", "trace", "wait for", "push", "pull", "make do", "create".
You can ONLY use these words in your answer to express modifier node: "in front", "adjacent", "away", "temporary", "for some turns", "in range", "forward", "backward", "designated".
You can ONLY use these words in your answer to express decorator node: "if above", "if below", "if exist", "for x times", "while", "and", "or", "nor", "xor", "if desired".
You can ONLY use these words as noun node: "hp", "strength", "magic power", "flame", "ice", "lightning", "magic", "poison", "obstacle", "wall", "storm", "beam", "cross".
Delete any node else.
\"\"\"

\"\"\"
Given a input, extrapolate as many relationships as possible from it and provide a list of edges to make a directed graph that expresses given command. Also, name the given command.

Provide an edge as [NODE 1, NODE 2]. The relationship is directed, so the order matters. NODE1 explains how NODE 2 works, like [subject, action], [action, target], [modifier, noun].
\"\"\"

\"\"\"
Example 1:
prompt:
Firely punch to an enemy in front of myself. If my status "hp" is above the half, doubles the damage.
answer:
[["self", "punch"], ["flame", "punch"], ["punch", "enemy], ["self", "in front"], ["in front", "enemy"], ["self", "hp"], ["hp", "if above"], ["if above", "buff"], ["buff", "punch"]]
name: "Blaze punch"
\"\"\"

\"\"\"
Example 2:
prompt:
Perform a shot to an adjacent enemy with mystical flame and fortify magical power for 2 turns.
answer:
[["self", "shoot"], ["shoot", "enemy"], ["self", "adjacent"], ["adjacent", "enemy"], ["flame", "shoot"], ["magic", "flame"], ["self", "buff"], ["magic power", "buff"], ["for some turns", "buff"]]
name:
Growing magical flame
\"\"\"
<</SYS>>
Generate more complex prompts and answers from the examples above.
[/INST]
"""

alt = """
Just complete the following form.
prompt:
Attack an adjacent enemy with mystical flame and fortify my strength for 3 turns.
answer:
"""

# 推論の実行
output = llm(
    prompt,
    temperature=0.8,
    # stop=["Instruction:", "Input:", "Response:", "\n"],
    echo=True,
    max_tokens=2048
)
print(output["choices"][0]["text"])
