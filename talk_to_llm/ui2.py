"""
Description: 
Author: haichun feng
Date: 2024-04-01 14:31:06
LastEditor: haichun feng
LastEditTime: 2024-04-01 14:41:58
"""

import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder(
    energy_threshold=(-1.0, 1.0),
    pause_threshold=5.0,
)
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
