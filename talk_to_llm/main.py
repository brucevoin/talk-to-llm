'''
Description: 
Author: haichun feng
Date: 2024-03-26 16:06:49
LastEditor: haichun feng
LastEditTime: 2024-03-28 18:11:30
'''
"""
Description: r
Author: haichun feng
Date: 2024-03-22 17:42:13
LastEditor: haichun feng
LastEditTime: 2024-03-28 17:16:20
"""

import threading
import time
import logging
import queue

from audio_recorder import AudioRecorder
from asr import ASR
from config_reader import ConfigManager

# def audio_input(config):
#     audioInput_instance = AudioRecorder(config=config)
#     audioInput_instance.Listening()


# def asr(config):
#     asr_instance = ASR(config=config)
#     asr_instance.Scan_and_asr()


## 考虑将Recorder与ASR合并

if __name__ == "__main__":

    config = ConfigManager()
    event = threading.Event()
    work_queue = queue.Queue()

    audioInput_instance = AudioRecorder(config=config,control_event=event,work_queue=work_queue)
    
    asr_instance = ASR(config=config, control_event=event, work_queue=work_queue)

    audioInput_instance.run()

    asr_instance.run()

