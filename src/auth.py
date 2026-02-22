import streamlit as st
from database.mongodb import MongoDB
from werkzeug.security import generate_password_hash, check_password_hash
from streamlit_cookies_manager import EncryptedCookieManager
from utils import validate_email
from config import Config

# -------------------------------
# MongoDB connection
# -------------------------------
db = MongoDB()
users_collection = db.get_users_collection()

# -------------------------------
# Cookie manager as module-level singleton (avoids CachedWidgetWarning)
# -------------------------------
_cookie_manager = None

def get_cookie_manager():
    global _cookie_manager
    if _cookie_manager is None:
        _cookie_manager = EncryptedCookieManager(
            prefix="revisia_",
            password=Config.SECRET_KEY,
        )
    return _cookie_manager

# -------------------------------
# Logout helper
# -------------------------------
def logout():
    cookies = get_cookie_manager()
    cookies["user_id"] = ""
    cookies.save()
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.rerun()

# -------------------------------
# Authentication UI
# -------------------------------
def auth_ui():
    cookies = get_cookie_manager()

    if not cookies.ready():
        st.stop()

    # -------------------------------
    # Always restore auth state from cookie on every load/reload
    # -------------------------------
    user_id_cookie = cookies.get("user_id")
    if user_id_cookie:
        if not st.session_state.get("authenticated"):
            st.session_state.authenticated = True
            st.session_state.user_id = user_id_cookie
            st.rerun()
    else:
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
            st.session_state.user_id = None

    # Modern centered auth layout
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2.5rem; margin-top: -2rem;'>
                <h1 style='font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem; color: #FFFFFF;'>Revisia</h1>
                <p style='color: #71717a; font-size: 0.95rem;'>Your AI-powered history tutor</p>
            </div>
        """, unsafe_allow_html=True)

        if "auth_mode" not in st.session_state:
            st.session_state.auth_mode = "login"

        mode_col1, mode_col2 = st.columns(2)
        with mode_col1:
            if st.button("Sign In", key="mode_login", use_container_width=True,
                        type="primary" if st.session_state.auth_mode == "login" else "secondary"):
                st.session_state.auth_mode = "login"
                st.rerun()
        with mode_col2:
            if st.button("Sign Up", key="mode_register", use_container_width=True,
                        type="primary" if st.session_state.auth_mode == "register" else "secondary"):
                st.session_state.auth_mode = "register"
                st.rerun()

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Login Form
        if st.session_state.auth_mode == "login":
            st.markdown("<p style='font-size: 0.875rem; color: #71717a; margin-bottom: 0.75rem;'>Welcome back! Please sign in to continue.</p>", unsafe_allow_html=True)

            username = st.text_input("Username", key="login_username", placeholder="Enter your username", label_visibility="collapsed")
            st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password", label_visibility="collapsed")
            st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

            if st.button("Sign In", key="login_btn", use_container_width=True, type="primary"):
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    user = users_collection.find_one({"username": username})
                    if user and check_password_hash(user["password"], password):
                        st.session_state.authenticated = True
                        st.session_state.user_id = str(user["_id"])
                        cookies["user_id"] = st.session_state.user_id
                        cookies.save()
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        # Register Form
        else:
            st.markdown("<p style='font-size: 0.875rem; color: #71717a; margin-bottom: 0.75rem;'>Create a new account to get started.</p>", unsafe_allow_html=True)

            new_username = st.text_input("Username", key="register_username", placeholder="Choose a username", label_visibility="collapsed")
            st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

            email = st.text_input("Email", key="register_email", placeholder="Enter your email", label_visibility="collapsed")
            st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

            new_password = st.text_input("Password", type="password", key="register_password", placeholder="Create a password (min. 6 characters)", label_visibility="collapsed")
            st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password", label_visibility="collapsed")
            st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

            if st.button("Create Account", key="register_btn", use_container_width=True, type="primary"):
                if not new_username or not email or not new_password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif not validate_email(email):
                    st.error("Please enter a valid email address.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
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
                    st.success("Account created! Please sign in.")
                    st.session_state.auth_mode = "login"
                    st.rerun()
