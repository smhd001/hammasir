import streamlit as st
from streamlit_mic_recorder import speech_to_text
from elastic_query import search
from slot_filing import slot_filing

state = st.session_state

if "text_received" not in state:
    state.text_received = ""

if "slots" not in state:
    state.slots = {}

if "search_result" not in state:
    state.search_result = []

st.markdown(
    """
<style>
summary, input{
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}
</style>
""",
    unsafe_allow_html=True,
)


text = speech_to_text(
    language="fa", use_container_width=True, just_once=True, key="STT"
)

if text:
    state.text_received = text
    print("result of asr", text)
    slots = slot_filing(text)
    print(slots)
    state.slots = slots
    search_result = search("")
    print(search_result)
    state.search_result = search_result


state.text_received

"slots", state.slots

for res in state.search_result:
    title, descripotion = res
    with st.expander(title):
        st.code(descripotion)
