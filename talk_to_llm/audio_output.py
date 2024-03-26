'''
Description: 
Author: haichun feng
Date: 2024-03-26 16:06:49
LastEditor: haichun feng
LastEditTime: 2024-03-26 17:43:17
'''
"""
Description: 
Author: haichun feng
Date: 2024-03-22 10:53:58
LastEditor: haichun feng
LastEditTime: 2024-03-26 17:27:56
"""

from playsound import playsound
from TTS.api import TTS


class AudioOutput:
    def __init__(self):
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

    def speak(self, text_str):

        output = "/Users/fhc/Downloads/output.wav"
        self.tts.tts_to_file(
            text=text_str,
            file_path=output,
            speaker_wav=["/Users/fhc/Downloads/Untitled.wav"],
            language="zh-cn",
            split_sentences=True,
            emotion="angry",
        )
        playsound(output)


if __name__ == "__main__":
    AudioOutput = Mouth()
    AudioOutput.speak(
        "我是一个聊天机器人。我是一个根据自然语言处理的技术开发的语言模型。我能够理解和生成人类语言，并可以用于多种任务，例如对话、作文、翻译等。"
    )
