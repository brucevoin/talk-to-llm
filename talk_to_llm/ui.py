'''
Description: 
Author: haichun feng
Date: 2024-03-29 14:27:25
LastEditor: haichun feng
LastEditTime: 2024-03-29 16:02:09
'''
import streamlit as st
import requests
import time

def stop_talking():
    print("Hello")

# Title
st.title("Talk to LLMs")

# Text input for URL
# url = st.text_input("Enter URL", "https://localhost/generate")
url = "backend service URL"

# Button to trigger HTTP request
if st.button("Start Talking"):
    try:
        # Make HTTP request
        button_text = "Stop Talking"
        st.button("Stop Talking", on_click= stop_talking)

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # # Display response data
        # st.success("Request successful!")
        # st.json(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

# Help text
st.text("**Script:**")

# 创建一个空容器
text_container = st.empty()

content = ""
# 模拟滚动输出文本
for i in range(10):
    # 更新文本内容
    content +=  f'  \n这是第 {i+1} 行滚动输出的文本。'
    text_container.write(content)
    # 等待一段时间
    time.sleep(3)