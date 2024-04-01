"""
Description: 
Author: haichun feng
Date: 2024-03-29 14:27:25
LastEditor: haichun feng
LastEditTime: 2024-04-01 14:30:54
"""

"""
Description: 
Author: haichun feng
Date: 2024-03-29 14:27:25
LastEditor: haichun feng
LastEditTime: 2024-04-01 14:27:02
"""

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_mic_recorder import mic_recorder
import json
import requests
import time
import io
import wave

#         ## - streamlit-mic-recorder https://pypi.org/project/streamlit-mic-recorder/
#         ## - streamlit-audio-recorder
#         ## - audio-recorder-streamlit


# Title
st.title("💬 Talk to LLMs")
st.caption("🚀 Click 'Connect' button to connect to LLM and start talking with it")


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


st_lottie(
    load_lottiefile("images/welcome.json"),
    speed=1,
    reverse=False,
    loop=True,
    quality="high",
    height=300,
)


def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output["bytes"]
        st.audio(audio_bytes)
        audio_bio = io.BytesIO(audio_bytes)
        audio_bio.name = "audio.wav"

        audio_bio.seek(0)  # 将指针移动到文件的开头

        # 打开一个.wav文件
        with wave.open("/Users/fhc/Downloads/audio.wav", "wb") as wf:
            wf.setnchannels(1)  # 设置声道数
            wf.setsampwidth(2)  # 设置采样宽度（以字节为单位）
            wf.setframerate(44100)  # 设置采样率
            wf.writeframes(audio_bio.read())  # 写入音频数据

        print("音频已保存到audio.wav文件中。")


audio = mic_recorder(
    start_prompt="Connect ⏺️",
    stop_prompt="Disconnect ⏹️",
    just_once=False,
    use_container_width=False,
    callback=callback,
    args=(),
    kwargs={},
    key="my_recorder",
    format="wav",
)
print(audio)

# Text input for URL
# url = st.text_input("Enter URL", "https://localhost/generate")
url = "backend service URL"

# Help text
st.text("**Script:**")

# 创建一个空容器
text_container = st.empty()

content = ""
# 模拟滚动输出文本
for i in range(10):
    # 更新文本内容
    content += f"  \n这是第 {i+1} 行滚动输出的文本。"
    text_container.write(content)
    # 等待一段时间
    time.sleep(3)
