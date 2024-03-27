'''
Description: 
Author: haichun feng
Date: 2024-03-26 16:06:49
LastEditor: haichun feng
LastEditTime: 2024-03-27 14:33:27
'''

from playsound import playsound
from TTS.api import TTS

from config_reader import get_AUDIO_FILES_DIRECTORY


class AudioOutput:
    def __init__(self):
        print("loading TTS model")
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        self.AUDIO_FILES_DIRECTORY = get_AUDIO_FILES_DIRECTORY()

    def speak(self, text_str):

        output = f"{self.AUDIO_FILES_DIRECTORY}/audio_output.wav"
        print("saving tts to file")
        # speaker_wav用以指定克隆对象的声音样本
        self.tts.tts_to_file(
            text=text_str,
            file_path=output,
            speaker_wav=["test_data/voice_clone_sample.wav"],
            language="zh-cn",
            split_sentences=True,
            emotion="angry",
        )
        print("playing audio")
        playsound(output)


if __name__ == "__main__":
    mouth = AudioOutput()
    mouth.speak(
        "我是一个聊天机器人。我是一个根据自然语言处理的技术开发的语言模型。我能够理解和生成人类语言，并可以用于多种任务，例如对话、作文、翻译等。"
    )
