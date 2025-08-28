import streamlit as st
import pandas as pd
from app import mock_process

st.set_page_config(layout="wide", page_title="Home", page_icon="favicon.ico")

def local_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
local_css("style.css")

if "reset" not in st.session_state:
    st.session_state.reset = False

st.markdown("""
<div class="navbar">
    <a href="#" class="brand">Application Name</a>
    <div>Home</div>
</div>
""", unsafe_allow_html=True)

with st.form(key="input_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=st.session_state.get("name", ""))
    with col2:
        feedback = st.text_area("Feedback", value=st.session_state.get("feedback", ""))

    col3, col4 = st.columns(2)
    with col3:
        category = st.selectbox("Category", ["Bug", "Feature", "Other"], index=["Bug", "Feature", "Other"].index(st.session_state.get("category", "Bug")))
    with col4:
        priority = st.radio("Priority", ["Low", "Medium", "High"], horizontal=True, index=["Low", "Medium", "High"].index(st.session_state.get("priority", "Low")))

    col_submit, col_reset = st.columns([1, 1])
    with col_submit:
        submit_button = st.form_submit_button("Submit")
    with col_reset:
        reset_button = st.form_submit_button("Reset")

if submit_button:
    st.session_state.name = name
    st.session_state.feedback = feedback
    st.session_state.category = category
    st.session_state.priority = priority
    st.session_state.reset = False

    with st.spinner("Processing..."):
        text_response, json_array = mock_process(name, feedback, category, priority)
    st.success("✅ Submission Complete!")

    st.text_input("Response", value=text_response, disabled=True)
    df = pd.DataFrame(json_array)
    st.dataframe(df, use_container_width=True)

if reset_button:
    st.rerun()