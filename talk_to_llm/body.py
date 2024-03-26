'''
Description: r
Author: haichun feng
Date: 2024-03-22 17:42:13
LastEditor: haichun feng
LastEditTime: 2024-03-26 11:13:28
'''
"""
Description: 
Author: haichun feng
Date: 2024-03-22 17:42:13
LastEditor: haichun feng
LastEditTime: 2024-03-25 17:48:24
"""

from voice_recorder2 import AudioInput
from asr import ASR
import threading
import time
import logging

logging.basicConfig(level=logging.ERROR)


def audio_input():
    audioInput_instance = AudioInput()
    audioInput_instance.Listening()


def asr():
    asr_instance = ASR()
    asr_instance.Scan_and_asr()


audio_input_thread = threading.Thread(target=audio_input)
audio_input_thread.start()

asr_thread = threading.Thread(target=asr)
asr_thread.start()

## 考虑将Recorder与ASR合并