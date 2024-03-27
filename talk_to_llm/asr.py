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

# For unit test
#from talk_to_llm.config_reader import ConfigManager
from config_reader import ConfigManager


class ASR:
    def __init__(self,config):
        self.config = config
        self.model = whisper.load_model("base")
        self.AUDIO_FILES_DIRECTORY = config.get_config('AUDIO_FILES_DIRECTORY')
        self.queue = CircularQueue(size=30)

    def Scan_and_asr(self):
        wav_num = 0
        while True:
            file_path = f"{self.AUDIO_FILES_DIRECTORY}/output_{wav_num}.wav"
            if os.path.exists(file_path) and os.access(file_path, os.R_OK):
                print(f"detect audio file:{file_path}")
                asr_input = self.Asr(file_path)
                ## 测试时不删除文件
                ## os.remove(file_path)
                wav_num += 1
                ## TODO 录音与ASR之间需要同步控制状态信息
                if wav_num == 10:
                    wav_num = 0
            else:
                time.sleep(5)

    def Asr(self, wav_file):
        stream = self.model.transcribe(
            wav_file, initial_prompt="", condition_on_previous_text=True
        )

        for segment in stream["segments"]:
            s = Segment(
                text=segment["text"],
                start=segment["start"],
                end=segment["end"],
                no_speech_prob=segment["no_speech_prob"],
            )
            print(segment)
            print(f"-------------{s.calculate_no_speech_time()}")
            if self.is_a_break(s):
                ## 之前的是一段
                print(self.queue.dequeue_all())
                ## 之后的是下一段
                self.queue.enqueue(s)
            else:
                self.queue.enqueue(s)

    def is_a_break(self, segment):
        if segment.no_speech_prob >0.5:
            return True
        if segment.calculate_no_speech_time() >= 3:
            return True
        if self.queue.last_item is not None and (5 - segment.start) + (5 - self.queue.last_item.end) >= 3:
            return True
        return False


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
        while not self.is_empty():
            text += self.dequeue().text
        return text


## 以下代码为测试
if __name__ == "__main__":
    config = ConfigManager()
    asr = ASR(config=config)
    asr.Scan_and_asr()
