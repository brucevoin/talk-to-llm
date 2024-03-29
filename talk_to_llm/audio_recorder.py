'''
Description: 
Author: haichun feng
Date: 2024-03-22 17:59:19
LastEditor: haichun feng
LastEditTime: 2024-03-29 10:42:05
'''

import pyaudio
import wave
import time
import os
import threading
import queue

from config_reader import ConfigManager


class AudioRecorder(threading.Thread):

    def __init__(self,config,control_event,work_queue):
        super(AudioRecorder, self).__init__()

        self.control_event = control_event

        self.work_queue = work_queue

        self.config = config
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5

        self.audio = pyaudio.PyAudio()
        self.stream = pyaudio.Stream
        self.FILE_COUNT_LIMIT = 100
        self.AUDIO_FILES_DIRECTORY = config.get_config('AUDIO_FILES_DIRECTORY')
        self.stop = False

    def run(self):
        try:
            self.Listening()
        except KeyboardInterrupt:
            print("Recorder interrupted by the user.")
        finally:
            self.shutdown()

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
            self.control_event.wait()
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

                self.work_queue.put(file_path)
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
            self.control_event.clear()


    def shutdown(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

if __name__ == "__main__":
    config = ConfigManager()
    instance = AudioRecorder(config=config)
    instance.Listening()