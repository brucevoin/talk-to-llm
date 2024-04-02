'''
Description: 
Author: haichun feng
Date: 2024-04-01 14:56:17
LastEditor: haichun feng
LastEditTime: 2024-04-01 16:44:01
'''
"""
Description: 
Author: haichun feng
Date: 2024-04-01 14:56:17
LastEditor: haichun feng
LastEditTime: 2024-04-01 14:56:22
"""

from streamlit_mic_recorder import mic_recorder
import streamlit as st
import io

# from openai import OpenAI
# import dotenv
import os
import whisper
import numpy as np


def whisper_stt(
    openai_api_key=None,
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    language=None,
    callback=None,
    args=(),
    kwargs=None,
    key=None,
    whisper_model=None,
):
    # if not 'openai_client' in st.session_state:
    #     dotenv.load_dotenv()
    #     st.session_state.openai_client = OpenAI(api_key=openai_api_key or os.getenv('OPENAI_API_KEY'))
    if not "_last_speech_to_text_transcript_id" in st.session_state:
        st.session_state._last_speech_to_text_transcript_id = 0
    if not "_last_speech_to_text_transcript" in st.session_state:
        st.session_state._last_speech_to_text_transcript = None
    if key and not key + "_output" in st.session_state:
        st.session_state[key + "_output"] = None
    audio = mic_recorder(
        start_prompt=start_prompt,
        stop_prompt=stop_prompt,
        just_once=just_once,
        use_container_width=use_container_width,
        key=key,
        format="wav",
    )
    new_output = False
    if audio is None:
        output = None
    else:
        id = audio["id"]
        new_output = id > st.session_state._last_speech_to_text_transcript_id
        if new_output:
            output = None
            st.session_state._last_speech_to_text_transcript_id = id

            # audio_bio = io.BytesIO(audio["bytes"])
            # audio_bio.name = "audio.wav"

            success = False
            err = 0
            while (
                not success and err < 3
            ):  # Retry up to 3 times in case of OpenAI server error.
                try:
                    # transcript = (
                    #     st.session_state.openai_client.audio.transcriptions.create(
                    #         model="whisper-1", file=audio_bio, language=language
                    #     )
                    # )
                    audio_np = np.frombuffer(audio["bytes"], np.int16).flatten().astype(np.float32) / 32768.0 
                    stream = model.transcribe(audio_np, initial_prompt="", condition_on_previous_text=True)
                    print(stream)
                except Exception as e:
                    print(str(e))  # log the exception in the terminal
                    err += 1
                else:
                    success = True
                    output = stream["text"]
                    st.session_state._last_speech_to_text_transcript = output
        elif not just_once:
            output = st.session_state._last_speech_to_text_transcript
        else:
            output = None

    if key:
        st.session_state[key + "_output"] = output
    if new_output and callback:
        callback(*args, **(kwargs or {}))
    return output


model = whisper.load_model("base")
text = whisper_stt(
    whisper_model=model, language = 'en')  
if text:
    st.write(text)