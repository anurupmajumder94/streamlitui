import streamlit as st


st.set_page_config(layout="wide", page_title="Home", page_icon="favicon.ico")

def local_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
local_css("style.css")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("""
<div class="navbar">
    <a href="#" class="brand">Application Name</a>
    <div>Chat Bot</div>
</div>
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-container'><div class='user-bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-container'><div class='bot-bubble'>{message['content']}</div></div>", unsafe_allow_html=True)

user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    bot_response = f"You said: {user_input}"
    st.session_state.messages.append({"role": "bot", "content": bot_response})

    st.rerun()