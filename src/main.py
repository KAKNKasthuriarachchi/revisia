import streamlit as st
from auth import auth_ui
from chat import chat_ui
from styles import load_styles

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Revisia",
    layout="wide"
)

# -------------------------------
# Load custom CSS / styles
# -------------------------------
load_styles()

# -------------------------------
# Initialize session state defaults
# -------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Reset chats data when authentication changes
if "last_user_id" not in st.session_state:
    st.session_state.last_user_id = None

current_user_id = st.session_state.get("user_id")
if current_user_id != st.session_state.last_user_id:
    # User changed, reset all chat-related state
    st.session_state.chats = {}
    st.session_state.chat_messages = {}
    st.session_state.active_chat = None
    st.session_state.chats_loaded = False
    st.session_state.last_user_id = current_user_id

if "chats" not in st.session_state or not isinstance(st.session_state.chats, dict):
    st.session_state.chats = {}  # Will be initialized in chat.py per user

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None  # Will be set in chat.py

if st.session_state.authenticated:
    chat_ui()
else:
    auth_ui()
