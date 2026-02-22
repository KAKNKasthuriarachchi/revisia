import streamlit as st
import streamlit.components.v1 as components
from database.mongodb import MongoDB
from rag.retriever import generate_response
from config import FallbackResponse, Grade, Language
from auth import logout
from bson import ObjectId
import time

# -------------------------------
# MongoDB connection
# -------------------------------
db = MongoDB()

# -------------------------------
# Grade / Language mappings
# -------------------------------
GRADE_MAP = {
    "6": Grade.GRADE_6, "7": Grade.GRADE_7, "8": Grade.GRADE_8,
    "9": Grade.GRADE_9, "O/L": Grade.O_LEVEL,
}
LANGUAGE_MAP = {
    "English": Language.ENGLISH,
    "Sinhala": Language.SINHALA,
    "Tamil": Language.TAMIL,
}

def get_grade_enum() -> Grade:
    return GRADE_MAP.get(st.session_state.selected_grade, Grade.O_LEVEL)

def get_language_enum() -> Language:
    return LANGUAGE_MAP.get(st.session_state.selected_language, Language.ENGLISH)

def get_welcome_message() -> str:
    messages = {
        Language.ENGLISH: "Hello! I'm your History tutor. Select your grade and language from the sidebar to get started.",
        Language.SINHALA: "ආයුබෝවන්! මම ඔබේ ඉතිහාස ගුරුතුමා. ආරම්භ කිරීමට sidebar එකෙන් ශ්‍රේණිය සහ භාෂාව තෝරන්න.",
        Language.TAMIL:   "வணக்கம்! நான் உங்கள் வரலாற்று ஆசிரியர். தொடங்க பக்கப்பட்டியில் இருந்து தரம் மற்றும் மொழியை தேர்ந்தெடுக்கவும்.",
    }
    return messages.get(get_language_enum(), messages[Language.ENGLISH])

def generate_chat_title(message: str) -> str:
    title = message[:40].strip()
    return title + "..." if len(message) > 40 else title

# -------------------------------
# Session state init
# -------------------------------
def init_session_state():
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("Please log in to use the chat feature.")
        return

    if "chats" not in st.session_state or not isinstance(st.session_state.chats, dict):
        st.session_state.chats = {}
    if "chat_messages" not in st.session_state or not isinstance(st.session_state.chat_messages, dict):
        st.session_state.chat_messages = {}
    if "selected_grade" not in st.session_state:
        st.session_state.selected_grade = "O/L"
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "English"

    if not st.session_state.get("chats_loaded"):
        user_chats = db.get_user_chats(user_id)
        if user_chats:
            for chat in user_chats:
                chat_id = str(chat["_id"])
                st.session_state.chats[chat_id] = {"title": chat["title"], "created_at": chat["created_at"]}
                st.session_state.chat_messages[chat_id] = [
                    {"role": m["role"], "message": m["message"]}
                    for m in db.get_chat_messages(chat_id)
                ]
        else:
            _create_new_chat(user_id)
        st.session_state.chats_loaded = True

    if not st.session_state.get("active_chat") or st.session_state.active_chat not in st.session_state.chats:
        if st.session_state.chats:
            st.session_state.active_chat = list(st.session_state.chats.keys())[0]
        else:
            _create_new_chat(user_id)

def _create_new_chat(user_id: str) -> str:
    chat_id = db.create_chat(user_id, "New Chat")
    welcome = get_welcome_message()
    st.session_state.chats[chat_id] = {"title": "New Chat", "created_at": None}
    st.session_state.chat_messages[chat_id] = [{"role": "assistant", "message": welcome}]
    db.add_message(chat_id, "assistant", welcome)
    st.session_state.active_chat = chat_id
    return chat_id

# -------------------------------
# Sidebar
# -------------------------------
def sidebar_ui():
    with st.sidebar:
        st.title("💬 Chats")
        st.divider()

        # Study settings
        st.subheader("📚 Study Settings")
        grade_options = list(GRADE_MAP.keys())
        selected_grade = st.selectbox(
            "Grade",
            grade_options,
            index=grade_options.index(st.session_state.selected_grade),
            key="grade_selector"
        )
        language_options = list(LANGUAGE_MAP.keys())
        selected_language = st.selectbox(
            "Language",
            language_options,
            index=language_options.index(st.session_state.selected_language),
            key="language_selector"
        )
        if selected_grade != st.session_state.selected_grade or selected_language != st.session_state.selected_language:
            st.session_state.selected_grade = selected_grade
            st.session_state.selected_language = selected_language
            st.success(f"Grade {selected_grade} · {selected_language}")

        st.divider()

        # New chat
        if st.button("➕ New Chat", use_container_width=True):
            _create_new_chat(st.session_state.get("user_id"))
            st.rerun()

        st.divider()

        # Chat list
        for chat_id, chat_info in list(st.session_state.chats.items()):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    chat_info["title"],
                    key=f"chat_{chat_id}",
                    use_container_width=True,
                    type="primary" if chat_id == st.session_state.active_chat else "secondary"
                ):
                    st.session_state.active_chat = chat_id
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    db.delete_chat(chat_id)
                    del st.session_state.chats[chat_id]
                    del st.session_state.chat_messages[chat_id]
                    if st.session_state.chats:
                        st.session_state.active_chat = list(st.session_state.chats.keys())[0]
                    else:
                        _create_new_chat(st.session_state.get("user_id"))
                    st.rerun()

        # Sticky profile bar at bottom
        st.markdown("""
            <style>
                section[data-testid="stSidebar"] > div { padding-bottom: 1rem !important; }
                .profile-wrap {
                    position: fixed; bottom: 0; left: 0;
                    width: 18rem;
                    background-color: #0e1117;
                    border-top: 1px solid #27272a;
                    padding: 0.3rem 0.75rem;
                    z-index: 999;
                }
            </style>
            <div class="profile-wrap">
        """, unsafe_allow_html=True)

        username = _get_username()
        with st.popover(f"👤 {username}", use_container_width=True):
            st.caption(f"Signed in as **{username}**")
            if st.button("🚪 Log out", use_container_width=True, type="secondary", key="logout_btn"):
                logout()

        st.markdown("</div>", unsafe_allow_html=True)

def _get_username() -> str:
    user_id = st.session_state.get("user_id")
    if user_id:
        try:
            user = db.get_users_collection().find_one({"_id": ObjectId(user_id)})
            if user:
                return user.get("username", "User")
        except Exception:
            pass
    return "User"

# -------------------------------
# Main chat UI
# -------------------------------
def chat_ui():
    init_session_state()
    sidebar_ui()

    active_chat_id = st.session_state.active_chat
    chat_title = st.session_state.chats[active_chat_id]["title"]
    chat_history = st.session_state.chat_messages[active_chat_id]

    st.title(f"📘 {chat_title}")

    for msg in chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["message"])

    components.html("""
        <script>
            function scrollToBottom() {
                const main = window.parent.document.querySelector('.main');
                if (main) main.scrollTop = main.scrollHeight;
            }
            scrollToBottom();
            setTimeout(scrollToBottom, 300);
        </script>
    """, height=0)

    user_input = st.chat_input("Type your message here...")
    if user_input and user_input.strip():
        chat_history.append({"role": "user", "message": user_input})
        db.add_message(active_chat_id, "user", user_input)

        if chat_title == "New Chat" and len(chat_history) <= 2:
            new_title = generate_chat_title(user_input)
            st.session_state.chats[active_chat_id]["title"] = new_title
            db.update_chat_title(active_chat_id, new_title)

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            response_text = ""
            full_response = generate_response(user_input, grade=get_grade_enum(), language=get_language_enum())
            for token in full_response.split():
                response_text += token + " "
                placeholder.markdown(response_text + "▌")
                time.sleep(0.05)
            placeholder.markdown(full_response)

        chat_history.append({"role": "assistant", "message": full_response})
        db.add_message(active_chat_id, "assistant", full_response)
        st.rerun()
