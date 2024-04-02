"""
Description: 
Author: haichun feng
Date: 2024-04-02 10:37:22
LastEditor: haichun feng
LastEditTime: 2024-04-02 11:35:17
"""

# pip install transformers torch accelerate
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

timeStart = time.time()
tokenizer = AutoTokenizer.from_pretrained(
    "google/gemma-2b", token="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"
)
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2b",
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    token="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",
)

print("加载模型时间: ", -timeStart + time.time())
max_new_token_length = 50
while True:
    input_str = input("输入: ")
    # input_token_length = input('输入长度: ')
    if input_str == "exit":
        break
    timeStart = time.time()
    inputs = tokenizer.encode(input_str, return_tensors="pt")
    outputs = model.generate(inputs, max_new_tokens=int(max_new_token_length))
    output_str = tokenizer.decode(outputs[0])
    print(output_str)
    print("耗时: ", -timeStart + time.time())
