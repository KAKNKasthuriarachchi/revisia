import streamlit as st
from auth import auth_ui
from chat import chat_ui
from styles import load_styles

st.set_page_config(
    page_title="Revisia",
    layout="wide"
)

load_styles()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "chats" not in st.session_state:
    st.session_state.chats = []

if not st.session_state.authenticated:
    auth_ui()
else:
    chat_ui()