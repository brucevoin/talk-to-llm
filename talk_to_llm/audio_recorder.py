'''
Description: 
Author: haichun feng
Date: 2024-03-22 17:59:19
LastEditor: haichun feng
LastEditTime: 2024-03-26 18:17:47
'''

import pyaudio
import wave
import time
import os

from config_reader import Get_AUDIO_FILES_DIRECTORY


class AudioRecorder:

    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5

        self.audio = pyaudio.PyAudio()
        self.stream = pyaudio.Stream
        self.FILE_COUNT_LIMIT = 10
        self.AUDIO_FILES_DIRECTORY = Get_AUDIO_FILES_DIRECTORY()

    def Listening(self):
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )
        print("开始持续录音,请说话...")
        frames = []
        wav_num = 0
        start_time = time.time()

        # 持续录音并生成WAV文件
        while True:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            frames.append(data)
            elapsed_time = time.time() - start_time

            # 每隔RECORD_SECONDS秒写入一个WAV文件
            if elapsed_time >= self.RECORD_SECONDS:
                # 保存WAV文件
                file_path = f"{self.AUDIO_FILES_DIRECTORY}/output_{wav_num}.wav"
                waveFile = wave.open(file_path, "wb")
                waveFile.setnchannels(self.CHANNELS)
                waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                waveFile.setframerate(self.RATE)
                waveFile.writeframes(b"".join(frames))
                waveFile.close()

                # 重置frames和开始时间
                frames = []
                start_time = time.time()

                wav_num += 1
                if wav_num  >= self.FILE_COUNT_LIMIT:
                    file_path0 = f"{self.AUDIO_FILES_DIRECTORY}/output_0.wav"
                    if (os.path.exists(file_path0)):
                        self.FILE_COUNT_LIMIT *= 2
                    else:
                        wav_num = 0

    def Stop_Listen(self):
        # 停止数据流
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

if __name__ == "__main__":
    instance = AudioRecorder()
    instance.Listening()