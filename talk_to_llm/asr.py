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
import threading
from collections import deque
import queue

# For unit test
#from talk_to_llm.config_reader import ConfigManager
from config_reader import ConfigManager
from audio_recorder import AudioRecorder

class ASR(threading.Thread):
    def __init__(self,config,control_event,work_queue):
        super(ASR,self).__init__()
        self.work_queue = work_queue
        self.config = config
        self.model = whisper.load_model("base")
        self.AUDIO_FILES_DIRECTORY = config.get_config('AUDIO_FILES_DIRECTORY')
        self.segment_queue = CircularQueue(size=30)
        self.control_event = control_event

    def run(self):
        self.Scan_and_asr()

    def Scan_and_asr(self):
        while True:
            self.control_event.set()

            file_path = self.work_queue.get()
            if(file_path) is None:
                time.sleep(5)
                continue
            if os.path.exists(file_path) and os.access(file_path, os.R_OK):
                print(f"detect audio file:{file_path}")
                asr_input = self.Asr(file_path)
                ## 测试时不删除文件
                ## os.remove(file_path)
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
            if self.is_a_break(s):
                ## 之前的是一段
                print('---------------This is a break---------------')
                ## todo 调用模型服务
                self.control_event.clear()
                print(self.segment_queue.dequeue_all())
                self.recorder.continue_listen()
                print('---------------------------------------------')
                ## 之后的是下一段
                self.segment_queue.enqueue(s)
            else:
                self.segment_queue.enqueue(s)

    def is_a_break(self, segment):
        if segment.no_speech_prob >0.5:
            return True
        # if segment.calculate_no_speech_time() >= 3:
        #     return True
        if self.segment_queue.last_item is not None and (segment.start) + (5 - self.segment_queue.last_item.end) >= 3:
            return True
        return False


class Segment:
    def __init__(self, text, start, end, no_speech_prob):
        self.text = text
        self.start = start
        self.end = end
        self.no_speech_prob = no_speech_prob


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
    recorder = AudioRecorder(config=config)
    asr = ASR(config=config,recorder=recorder)
    asr.Scan_and_asr()
