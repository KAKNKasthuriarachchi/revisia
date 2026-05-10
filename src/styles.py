import streamlit as st

def load_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

        /* Minimal global styling */
        * { font-family: 'Inter', sans-serif; }

        /* Auth header helpers */
        .auth-hero { text-align: center; margin: -2rem 0 2.5rem 0; }
        .auth-hero-title { font-size: 2.5rem; font-weight: 600; margin: 0 0 0.5rem 0; }
        .auth-hero-subtitle { color: #6c6f75; font-size: 0.95rem; margin: 0; }
        .auth-spacer-sm { height: 0.4rem; }
        .auth-spacer-md { height: 0.75rem; }
        .auth-spacer-lg { height: 1rem; }

        /* Sidebar profile bar */
        .sidebar-profile {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 18rem;
            background-color: #ffffff;
            border-top: 1px solid #e5e7eb;
            padding: 0.3rem 0.75rem;
            z-index: 999;
        }
        </style>
        """,
        unsafe_allow_html=True
    )