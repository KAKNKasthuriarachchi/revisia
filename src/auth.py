import streamlit as st
from database.mongodb import MongoDB
from werkzeug.security import generate_password_hash, check_password_hash
from streamlit_cookies_manager import EncryptedCookieManager
import re

# -------------------------------
# MongoDB connection
# -------------------------------
db = MongoDB()
users_collection = db.get_users_collection()

# -------------------------------
# Email validation helper
# -------------------------------
def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# -------------------------------
# Authentication UI
# -------------------------------
def auth_ui():
    # -------------------------------
    # Initialize cookies for persistent login
    # -------------------------------
    cookies = EncryptedCookieManager(
        prefix="revisia_",
        password="supersecretpassword123!"
    )
    if not cookies.ready():
        st.stop()
    
    # -------------------------------
    # Load auth state from cookie
    # -------------------------------
    if "authenticated" not in st.session_state:
        user_id_cookie = cookies.get("user_id")
        if user_id_cookie:
            st.session_state.authenticated = True
            st.session_state.user_id = user_id_cookie
        else:
            st.session_state.authenticated = False
            st.session_state.user_id = None
    
    # Center content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>📚 Revisia</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            if st.button("Login", key="login_btn", use_container_width=True):
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    user = users_collection.find_one({"username": username})
                    if user and check_password_hash(user["password"], password):
                        st.session_state.authenticated = True
                        st.session_state.user_id = str(user["_id"])
                        cookies["user_id"] = st.session_state.user_id
                        cookies.save()
                        st.success("Logged in successfully! ✅")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
        
        with tab2:
            new_username = st.text_input("Username", key="register_username", placeholder="Choose a username")
            email = st.text_input("Email", key="register_email", placeholder="Enter your email address")
            new_password = st.text_input("Password", type="password", key="register_password", placeholder="Choose a password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Re-enter your password")
            
            if st.button("Register", key="register_btn", use_container_width=True):
                if not new_username or not email or not new_password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif users_collection.find_one({"username": new_username}):
                    st.error("Username already exists.")
                elif users_collection.find_one({"email": email}):
                    st.error("Email already registered.")
                else:
                    hashed_password = generate_password_hash(new_password)
                    users_collection.insert_one({
                        "username": new_username,
                        "email": email,
                        "password": hashed_password
                    })
                    st.success("Registered successfully! You can now log in. ✅")
