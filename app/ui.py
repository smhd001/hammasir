import config
import streamlit as st
import streamlit.components.v1 as components
from elastic_query import search
from streamlit_mic_recorder import speech_to_text

# from slot_filing import slot_filing

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
summary, input, .stMarkdown {
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
text = "دکتر قلب خوش اخلاق وکیل آباد مشهد"

if text:
    state.text_received = text
    print("result of asr", text)
    # slots = slot_filing(text)
    # print("slotl", slots)
    # state.slots = slots
    search_result = search("")
    print("search", search_result)
    state.search_result = search_result


state.text_received

st.html('<p style="direction:LTR">slots<p>')
state.slots

for res in state.search_result:
    title, url, description = res
    with st.expander(title):
        json_view, site_view = st.tabs(["json", "site"])
        with json_view:
            description
        with site_view:
            col1, col2 = st.columns(2)
            with col1:
                st.image(config.P24_BASE_IMAGE_URL + description["image"])
            with col2:
                f"[مشاهده در پزشک 24]({config.p24_BASE_URL}{description["url"]})"
                f"[مسیر یابی در نشان]({config.NESHAN_BASE_URL}/{description["lat"]},{description["lon"]})"
