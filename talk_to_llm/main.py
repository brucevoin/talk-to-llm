'''
Description: r
Author: haichun feng
Date: 2024-03-22 17:42:13
LastEditor: haichun feng
LastEditTime: 2024-03-26 18:06:38
'''


from audio_recorder import AudioRecorder
from asr import ASR
import threading
import time
import logging

logging.basicConfig(level=logging.ERROR)


def audio_input():
    audioInput_instance = AudioRecorder()
    audioInput_instance.Listening()


def asr():
    asr_instance = ASR()
    asr_instance.Scan_and_asr()


## 考虑将Recorder与ASR合并

if __name__ == "__main__":
    audio_input_thread = threading.Thread(target=audio_input)
    audio_input_thread.start()

    asr_thread = threading.Thread(target=asr)
    asr_thread.start()