'''
Description: 
Author: haichun feng
Date: 2024-03-22 17:35:59
LastEditor: haichun feng
LastEditTime: 2024-03-22 17:39:25
'''

import pyaudio
import wave

# 设置音频参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

# 初始化PyAudio对象
audio = pyaudio.PyAudio()

# 打开数据流
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("开始录音,请说话...")

# 创建WAV文件
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录音结束!")

# 停止数据流
stream.stop_stream()
stream.close()
audio.terminate()

# 保存WAV文件
waveFile = wave.open("/Users/fhc/Downloads/input_converted.wav", 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()