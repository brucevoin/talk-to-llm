"""
Description: 
Author: haichun feng
Date: 2024-03-22 15:22:07
LastEditor: haichun feng
LastEditTime: 2024-03-26 15:24:15
"""

import whisper
import numpy as np
import torch
from typing import Union
from dataclasses import dataclass

import os
import time
from collections import deque


class ASR:
    def __init__(self):
        self.model = whisper.load_model("base")

    def Scan_and_asr(self):
        wav_num = 0
        while True:
            file_path = f"/Users/fhc/Downloads/output_{wav_num}.wav"
            if os.path.exists(file_path) and os.access(file_path, os.R_OK):
                asr_input = self.Asr(file_path)
                os.remove(file_path)
                wav_num += 1
                ## TODO 录音与ASR之间需要同步控制状态信息
                if wav_num == 10:
                    wav_num = 0
            else:
                time.sleep(5)

    def Asr(self, wav_file):
        result = self.model.transcribe(wav_file)
        print(result["text"])
        return result["text"]


class Segment:
    def __init__(self, text, start, end, no_speech_prob):
        self.text = text
        self.start = start
        self.end = end
        self.no_speech_prob = no_speech_prob

    def calculate_no_speech_time(self):
        ## 可配置
        return 5 - self.end


class CircularQueue:
    last_item: Segment

    def __init__(self, size):
        self.queue = deque(maxlen=size)
        self.last_item = None

    def enqueue(self, item):
        self.queue.append(item)
        self.last_item = item

    def dequeue(self):
        return self.queue.popleft() if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return len(self.queue) == self.queue.maxlen

    def __len__(self):
        return len(self.queue)

    def dequeue_all(self):
        text = ""
        if not self.is_empty():
            text += self.dequeue()

        print(text)
        return text

## 以下代码为测试

# 加载模型
model = whisper.load_model("base")

file_path = f"/Users/fhc/Downloads/output_1.wav"
# 进行流式识别
stream = model.transcribe(file_path, initial_prompt="", condition_on_previous_text=True)

print(stream)

queue = CircularQueue(size=30)

for segment in stream["segments"]:
    s = Segment(
        text=segment["text"],
        start=segment["start"],
        end=segment["end"],
        no_speech_prob=segment["no_speech_prob"],
    )
    if s.no_speech_prob > 0.5:
        queue.dequeue_all()
    if (queue.last_item is None):
        queue.enqueue(s)
    elif queue.last_item.calculate_no_speech_time() + s.calculate_no_speech_time() > 3:
        queue.enqueue(s)
        # 触发思考动作
        queue.dequeue_all()
    else:
        queue.enqueue(s)
