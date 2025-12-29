import streamlit as st
from database.mongodb import MongoDB
from utils.helpers import format_chat_message
from rag.retriever import generate_dummy_response
from config import Config
from bson import ObjectId
import time

# -------------------------------
# MongoDB connection
# -------------------------------
db = MongoDB()

# -------------------------------
# Initialize session state safely
# -------------------------------
def init_session_state():
    """Initialize session state with user's chats from database"""
    user_id = st.session_state.get("user_id")
    
    if not user_id:
        st.error("Please log in to use the chat feature.")
        return
    
    # Initialize chats dict if not exists (ensure it's always a dict)
    if "chats" not in st.session_state or not isinstance(st.session_state.chats, dict):
        st.session_state.chats = {}
    
    # Initialize chat_messages dict to store messages per chat
    if "chat_messages" not in st.session_state or not isinstance(st.session_state.chat_messages, dict):
        st.session_state.chat_messages = {}
    
    # Initialize vector store selection if not exists
    if "selected_vector_store" not in st.session_state:
        st.session_state.selected_vector_store = Config.DEFAULT_VECTOR_STORE
    
    # Load user's chats from database (only on first load)
    if "chats_loaded" not in st.session_state or st.session_state.chats_loaded == False:
        user_chats = db.get_user_chats(user_id)
        
        if user_chats:
            # Load existing chats
            for chat in user_chats:
                chat_id = str(chat["_id"])
                st.session_state.chats[chat_id] = {
                    "title": chat["title"],
                    "created_at": chat["created_at"]
                }
                # Load messages for this chat
                messages = db.get_chat_messages(chat_id)
                st.session_state.chat_messages[chat_id] = [
                    {"role": msg["role"], "message": msg["message"]}
                    for msg in messages
                ]
        else:
            # Create first chat for new user
            chat_id = db.create_chat(user_id, "New Chat")
            st.session_state.chats[chat_id] = {
                "title": "New Chat",
                "created_at": None
            }
            st.session_state.chat_messages[chat_id] = [
                {"role": "assistant", "message": "Hello! Ask me about Grade 10 or 11 History."}
            ]
            # Save welcome message to DB
            db.add_message(chat_id, "assistant", "Hello! Ask me about Grade 10 or 11 History.")
        
        st.session_state.chats_loaded = True
    
    # Set active_chat if not set or if it's invalid
    if (not st.session_state.get("active_chat") or 
        st.session_state.active_chat not in st.session_state.chats):
        if st.session_state.chats:
            st.session_state.active_chat = list(st.session_state.chats.keys())[0]
        else:
            # Emergency: create a new chat if none exists
            chat_id = db.create_chat(user_id, "New Chat")
            st.session_state.chats[chat_id] = {
                "title": "New Chat",
                "created_at": None
            }
            st.session_state.chat_messages[chat_id] = [
                {"role": "assistant", "message": "Hello! Ask me about Grade 10 or 11 History."}
            ]
            db.add_message(chat_id, "assistant", "Hello! Ask me about Grade 10 or 11 History.")
            st.session_state.active_chat = chat_id

# -------------------------------
# Generate chat title from first message
# -------------------------------
def generate_chat_title(message: str) -> str:
    """Generate a short title from the first user message"""
    # Take first 30 characters and add ellipsis if longer
    title = message[:40].strip()
    if len(message) > 40:
        title += "..."
    return title

# -------------------------------
# Sidebar UI
# -------------------------------
def sidebar_ui():
    st.sidebar.title("💬 Chats")
    
    # Vector Store Selection
    st.sidebar.divider()
    st.sidebar.subheader("📚 Content Selection")
    
    # Get available vector stores
    available_stores = Config.list_available_vector_stores()
    store_options = {desc: key for key, desc in available_stores}
    
    # Get current selection description
    current_info = Config.get_vector_store_info(st.session_state.selected_vector_store)
    current_desc = current_info.get("description", "Default Vector Store")
    
    selected_desc = st.sidebar.selectbox(
        "Select content:",
        options=list(store_options.keys()),
        index=list(store_options.keys()).index(current_desc) if current_desc in store_options.keys() else 0,
        key="vector_store_selector"
    )
    
    # Update session state if selection changed
    new_store_key = store_options[selected_desc]
    if new_store_key != st.session_state.selected_vector_store:
        st.session_state.selected_vector_store = new_store_key
        st.sidebar.success(f"Switched to: {selected_desc}")
    
    st.sidebar.divider()
    
    # Ensure chats is a dictionary before proceeding
    if not isinstance(st.session_state.get("chats"), dict):
        st.session_state.chats = {}
    
    # New chat button
    if st.sidebar.button("➕ New Chat", use_container_width=True):
        user_id = st.session_state.get("user_id")
        # Create new chat in database
        chat_id = db.create_chat(user_id, "New Chat")
        st.session_state.chats[chat_id] = {
            "title": "New Chat",
            "created_at": None
        }
        st.session_state.chat_messages[chat_id] = [
            {"role": "assistant", "message": "Hello! How can I help you today?"}
        ]
        # Save welcome message to DB
        db.add_message(chat_id, "assistant", "Hello! How can I help you today?")
        st.session_state.active_chat = chat_id
        st.rerun()
    
    st.sidebar.divider()
    
    # Display chat list (only if chats exist and it's a dict)
    if isinstance(st.session_state.chats, dict):
        for chat_id, chat_info in st.session_state.chats.items():
            col1, col2 = st.sidebar.columns([4, 1])
            
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
                    # Delete chat from database
                    db.delete_chat(chat_id)
                    # Remove from session state
                    del st.session_state.chats[chat_id]
                    del st.session_state.chat_messages[chat_id]
                    # Set active chat to another one
                    if st.session_state.chats:
                        st.session_state.active_chat = list(st.session_state.chats.keys())[0]
                    else:
                        # Create a new chat if all deleted
                        user_id = st.session_state.get("user_id")
                        new_chat_id = db.create_chat(user_id, "New Chat")
                        st.session_state.chats[new_chat_id] = {"title": "New Chat", "created_at": None}
                        st.session_state.chat_messages[new_chat_id] = [
                            {"role": "assistant", "message": "Hello! How can I help you today?"}
                        ]
                        db.add_message(new_chat_id, "assistant", "Hello! How can I help you today?")
                        st.session_state.active_chat = new_chat_id
                    st.rerun()

# -------------------------------
# Main chat UI
# -------------------------------
def chat_ui():
    init_session_state()
    sidebar_ui()
    
    active_chat_id = st.session_state.active_chat
    chat_title = st.session_state.chats[active_chat_id]["title"]
    
    st.title(f"📘 {chat_title}")
    
    # Get chat messages
    chat_history = st.session_state.chat_messages[active_chat_id]
    
    # Display chat messages
    for chat in chat_history:
        st.markdown(format_chat_message(chat))
    
    # Input area
    user_input = st.chat_input("Type your message here...")
    
    if user_input and user_input.strip():
        # Add user message to chat
        chat_history.append({"role": "user", "message": user_input})
        
        # Save user message to database
        db.add_message(active_chat_id, "user", user_input)
        
        # Update chat title if this is the first user message (title is still "New Chat")
        if chat_title == "New Chat" and len(chat_history) <= 2:
            new_title = generate_chat_title(user_input)
            st.session_state.chats[active_chat_id]["title"] = new_title
            db.update_chat_title(active_chat_id, new_title)
        
        # Display user message immediately
        st.markdown(format_chat_message({"role": "user", "message": user_input}))
        
        # Generate and stream assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_text = ""
            
            # Generate response using selected vector store
            full_response = generate_dummy_response(
                user_input, 
                vector_store_key=st.session_state.selected_vector_store
            )
            
            # Simulate token streaming
            for token in full_response.split():
                response_text += token + " "
                response_placeholder.markdown(response_text + "▌")
                time.sleep(0.05)
            
            # Display final response
            response_placeholder.markdown(full_response)
        
        # Save assistant response to chat history and database
        chat_history.append({"role": "assistant", "message": full_response})
        db.add_message(active_chat_id, "assistant", full_response)
        
        # Rerun to refresh the UI
        st.rerun()
