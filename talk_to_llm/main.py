'''
Description: r
Author: haichun feng
Date: 2024-03-22 17:42:13
LastEditor: haichun feng
LastEditTime: 2024-03-27 14:58:05
'''



import threading
import time
import logging

from audio_recorder import AudioRecorder
from asr import ASR
from config_reader import ConfigManager

def audio_input(config):
    audioInput_instance = AudioRecorder(config=config)
    audioInput_instance.Listening()


def asr(config):
    asr_instance = ASR(config=config)
    asr_instance.Scan_and_asr()


## 考虑将Recorder与ASR合并

if __name__ == "__main__":
    config = ConfigManager()

    audio_input_thread = threading.Thread(target=audio_input,args=config)
    audio_input_thread.start()

    asr_thread = threading.Thread(target=asr,args=config)
    asr_thread.start()