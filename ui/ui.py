import streamlit as st
from streamlit_mic_recorder import mic_recorder, speech_to_text
import time

state = st.session_state

def pars(text):
    return f"text is {text} and time minut is {time.strftime('%H:%M:%S')}"

if 'text_received' not in state:
    state.text_received = []

text = speech_to_text(language='fa', use_container_width=True, just_once=True, key='STT')

if text:
    state.text_received.append(text)

for text in state.text_received:
    st.text(text)

print(text)

st.text(pars(text))