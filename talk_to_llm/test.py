import streamlit as st
import time

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