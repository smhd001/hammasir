import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time

from .elastic_query import search
from slot_filing import slot_filing

state = st.session_state

def pars(text):
    return f"text is {text} and time minut is {time.strftime('%H:%M:%S')}"

if 'text_received' not in state:
    state.text_received = []

if 'slots' not in state:
    state.slots = []

if 'search_result' not in state:
    state.search_result = []

text = speech_to_text(language='fa', use_container_width=True, just_once=True, key='STT')

if text:
    state.text_received.append(text)
    slots = slot_filing(text)
    print(slots)
    state.slots.append(slots)
    search_result = search(slots)
    print(search_result)
    state.search_result.append(search_result)


for text in state.text_received:
    st.text(text)

st.text(state.slots[-1])

st.text(state.search_result[-1])

print(text)

st.text(pars(text))