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


        /* Hide the default empty Streamlit sidebar header */
        [data-testid="stSidebarHeader"] {
            display: none;
        }

        .sidebar-content {
            display: flex;
            align-items: top;
            gap: 0.5rem;
            
        }
        .sidebar-profile{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            bottom: 0;
            width: 100%;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )