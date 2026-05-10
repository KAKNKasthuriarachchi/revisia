import streamlit as st
import re
from database.mongodb import MongoDB
from werkzeug.security import generate_password_hash, check_password_hash
from streamlit_cookies_manager import EncryptedCookieManager
from utils import validate_email
from config import Config
from bson import ObjectId

# -------------------------------
# MongoDB connection
# -------------------------------
db = MongoDB()
users_collection = db.get_users_collection()

# -------------------------------
# Grade options
# -------------------------------
GRADE_OPTIONS = ["6", "7", "8", "9", "O/L"]

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
    if cookies.ready():
        cookies["user_id"] = ""
        cookies.save()
    st.session_state.pending_cookie_user_id = None
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.rerun()

# -------------------------------
# Authentication UI
# -------------------------------
def auth_ui():
    cookies = get_cookie_manager()

    # -------------------------------
    # Always restore auth state from cookie on every load/reload
    # -------------------------------
    user_id_cookie = cookies.get("user_id") if cookies.ready() else None
    if user_id_cookie:
        if not st.session_state.get("authenticated"):
            user = users_collection.find_one({"_id": ObjectId(user_id_cookie)})
            stored_grade = user.get("grade") if user else None
            if not stored_grade:
                stored_grade = "O/L"
                if user:
                    users_collection.update_one(
                        {"_id": ObjectId(user_id_cookie)},
                        {"$set": {"grade": stored_grade}}
                    )
            if stored_grade not in GRADE_OPTIONS:
                stored_grade = "O/L"
                if user:
                    users_collection.update_one(
                        {"_id": ObjectId(user_id_cookie)},
                        {"$set": {"grade": stored_grade}}
                    )
            st.session_state.selected_grade = stored_grade
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
            <div class='auth-hero'>
                <h1 class='auth-hero-title'>Revisia</h1>
                <p class='auth-hero-subtitle'>Your AI-powered history tutor</p>
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

        st.markdown("<div class='auth-spacer-lg'></div>", unsafe_allow_html=True)

        # Login Form
        if st.session_state.auth_mode == "login":
            st.markdown("<p style='font-size: 0.875rem; color: #71717a; margin-bottom: 0.75rem;'>Welcome back! Please sign in to continue.</p>", unsafe_allow_html=True)

            email = st.text_input("Email", key="login_email", placeholder="Enter your email", label_visibility="collapsed")
            st.markdown("<div class='auth-spacer-sm'></div>", unsafe_allow_html=True)

            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password", label_visibility="collapsed")
            st.markdown("<div class='auth-spacer-md'></div>", unsafe_allow_html=True)

            if st.button("Sign In", key="login_btn", use_container_width=True, type="primary"):
                login_email = email.strip().lower()
                password_value = password.strip()

                if not login_email or not password_value:
                    st.error("Please fill in all fields.")
                else:
                    user = users_collection.find_one({
                        "email": {"$regex": f"^{re.escape(login_email)}$", "$options": "i"}
                    })

                    stored_password = user.get("password") if user else None
                    if user and not stored_password:
                        stored_password = user.get("password_hash")

                    password_ok = False
                    if user and stored_password:
                        try:
                            password_ok = check_password_hash(stored_password, password_value)
                        except ValueError:
                            password_ok = stored_password == password_value

                    if user and password_ok:
                        stored_grade = user.get("grade") if user else None
                        if not stored_grade or stored_grade not in GRADE_OPTIONS:
                            stored_grade = "O/L"
                            users_collection.update_one(
                                {"_id": user["_id"]},
                                {"$set": {"grade": stored_grade}}
                            )
                        st.session_state.selected_grade = stored_grade
                        st.session_state.authenticated = True
                        st.session_state.user_id = str(user["_id"])
                        if cookies.ready():
                            cookies["user_id"] = st.session_state.user_id
                            cookies.save()
                        else:
                            st.session_state.pending_cookie_user_id = st.session_state.user_id
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        # Register Form
        else:
            st.markdown("<p style='font-size: 0.875rem; color: #71717a; margin-bottom: 0.75rem;'>Create a new account to get started.</p>", unsafe_allow_html=True)

            first_name = st.text_input("First Name", key="register_first_name", placeholder="Enter your first name", label_visibility="collapsed")
            st.markdown("<div class='auth-spacer-sm'></div>", unsafe_allow_html=True)

            last_name = st.text_input("Last Name", key="register_last_name", placeholder="Enter your last name", label_visibility="collapsed")
            st.markdown("<div class='auth-spacer-sm'></div>", unsafe_allow_html=True)

            email = st.text_input("Email", key="register_email", placeholder="Enter your email", label_visibility="collapsed")
            st.markdown("<div class='auth-spacer-sm'></div>", unsafe_allow_html=True)

            selected_grade = st.selectbox("Grade", GRADE_OPTIONS, index=GRADE_OPTIONS.index("O/L"), key="register_grade")
            st.markdown("<div class='auth-spacer-sm'></div>", unsafe_allow_html=True)

            new_password = st.text_input("Password", type="password", key="register_password", placeholder="Create a password (min. 6 characters)", label_visibility="collapsed")
            st.markdown("<div class='auth-spacer-sm'></div>", unsafe_allow_html=True)

            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password", label_visibility="collapsed")
            st.markdown("<div class='auth-spacer-md'></div>", unsafe_allow_html=True)

            if st.button("Create Account", key="register_btn", use_container_width=True, type="primary"):
                normalized_first = " ".join(first_name.split())
                normalized_last = " ".join(last_name.split())
                normalized_email = email.strip().lower()

                if not normalized_first or not normalized_last or not normalized_email or not new_password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif not validate_email(normalized_email):
                    st.error("Please enter a valid email address.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif users_collection.find_one({
                    "email": {"$regex": f"^{re.escape(normalized_email)}$", "$options": "i"}
                }):
                    st.error("User already registered.")
                else:
                    hashed_password = generate_password_hash(new_password)
                    users_collection.insert_one({
                        "first_name": normalized_first,
                        "last_name": normalized_last,
                        "email": normalized_email,
                        "password": hashed_password,
                        "password_hash": hashed_password,
                        "grade": selected_grade,
                    })
                    st.success("Account created! Please sign in.")
                    st.session_state.auth_mode = "login"
                    st.rerun()
