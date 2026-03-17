import streamlit as st
from auth import auth_ui, get_cookie_manager
from chat import chat_ui
from styles import load_styles

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Revisia",
    layout="wide",
    initial_sidebar_state="expanded"
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
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Restore auth from cookie if available
cookies = get_cookie_manager()
if cookies.ready():
    pending_cookie_user_id = st.session_state.get("pending_cookie_user_id")
    if pending_cookie_user_id:
        cookies["user_id"] = pending_cookie_user_id
        cookies.save()
        st.session_state.pending_cookie_user_id = None

    user_id_cookie = cookies.get("user_id")
    if user_id_cookie:
        st.session_state.authenticated = True
        st.session_state.user_id = user_id_cookie
    elif not st.session_state.get("authenticated"):
        st.session_state.user_id = None

if not st.session_state.get("user_id"):
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

if st.session_state.authenticated and st.session_state.get("user_id"):
    chat_ui()
else:
    auth_ui()
