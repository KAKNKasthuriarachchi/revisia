import streamlit as st
from utils.helpers import format_chat_message

# Initialize session state
if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": [
            {"role": "assistant", "message": "Hello! Ask me about Grade 10 or 11 History."}
        ]
    }

if "active_chat" not in st.session_state:
    st.session_state.active_chat = list(st.session_state.chats.keys())[0]

# ------------------------------
# Sidebar
# ------------------------------
def sidebar_ui():
    st.sidebar.title("💬 Chats")

    # New chat button
    if st.sidebar.button("➕ New Chat"):
        new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_name] = [
            {"role": "assistant", "message": "New chat started. Ask your question!"}
        ]
        st.session_state.active_chat = new_chat_name
        st.rerun()

    st.sidebar.divider()

    # List all chats
    for chat_name in st.session_state.chats:
        if st.sidebar.button(chat_name):
            st.session_state.active_chat = chat_name
            st.rerun()

# ------------------------------
# Main chat UI
# ------------------------------
def chat_ui():
    sidebar_ui()

    st.title(f"📘 {st.session_state.active_chat}")

    chat_history = st.session_state.chats[st.session_state.active_chat]

    # Display chat messages
    for chat in chat_history:
        st.markdown(format_chat_message(chat))

    # Input
    user_input = st.text_input("You:", key="input_text")

    if st.button("Send"):
        if user_input.strip():
            chat_history.append({"role": "user", "message": user_input})
            chat_history.append({"role": "assistant", "message": "This is a dummy response for now."})

            # Clear input safely using rerun
            st.rerun()
        else:
            st.warning("Please enter a message.")

# ------------------------------
# Run app
# ------------------------------
if __name__ == "__main__":
    chat_ui()
