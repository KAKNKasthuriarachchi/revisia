import streamlit as st

def load_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

        /* ── Global ── */
        * { font-family: 'Inter', sans-serif; }

        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0f0f0f;
            color: #e4e4e7;
        }

        /* ── Main content ── */
        .main {
            background-color: #0f0f0f;
            height: 100vh;
            overflow-y: auto;
        }

        .main .block-container {
            background-color: #0f0f0f;
            max-width: 860px;
            padding: 2rem 2rem 80px 2rem;
        }

        /* ── Headings ── */
        h1, h2, h3, p, span, label, div { color: #e4e4e7 !important; }
        h1 { font-size: 1.4rem !important; font-weight: 600; margin-bottom: 1.5rem; }

        /* ── Chat messages ── */
        .stChatMessage {
            background: transparent !important;
            border: none !important;
            padding: 0.25rem 0;
            margin: 0.1rem 0;
        }

        [data-testid="stChatMessageContent"] {
            background: #1c1c1e !important;
            border-radius: 12px;
            padding: 0.65rem 1rem;
            color: #e4e4e7 !important;
            border: 1px solid #27272a;
        }

        [data-testid="stChatMessageContent"] p { color: #e4e4e7 !important; }

        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
            background: #27272a !important;
        }

        /* ── Chat input - fixed at bottom ── */
        .stChatFloatingInputContainer {
            position: fixed !important;
            bottom: 0 !important;
            left: var(--sidebar-width, 240px) !important;
            right: 0 !important;
            background: #0f0f0f !important;
            border-top: 1px solid #27272a !important;
            padding: 0.5rem 2rem !important;
            z-index: 999 !important;
        }

        .stChatInput textarea {
            background: #1c1c1e !important;
            border: 1px solid #3f3f46 !important;
            border-radius: 8px !important;
            color: #e4e4e7 !important;
            padding: 0.45rem 0.85rem !important;
            font-size: 13px !important;
            min-height: 38px !important;
            max-height: 38px !important;
            resize: none !important;
            line-height: 1.4 !important;
            overflow: hidden !important;
        }

        .stChatInput textarea::placeholder { color: #71717a !important; }
        .stChatInput textarea:focus {
            border-color: #71717a !important;
            outline: none !important;
            max-height: 100px !important;
            overflow-y: auto !important;
        }

        .stChatInput button {
            background: #3f3f46 !important;
            border: none !important;
            border-radius: 6px !important;
            color: #e4e4e7 !important;
            padding: 0.3rem 0.6rem !important;
            height: 32px !important;
        }

        .stChatInput button:hover { background: #52525b !important; }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background-color: #111111 !important;
            border-right: 1px solid #27272a;
        }

        section[data-testid="stSidebar"] > div {
            overflow-y: auto;
            max-height: 100vh;
            padding: 1rem 0.75rem;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #e4e4e7 !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label { color: #a1a1aa !important; }

        section[data-testid="stSidebar"] hr {
            border-color: #27272a !important;
            margin: 0.75rem 0 !important;
        }

        /* ── Sidebar toggle button ── */
        [data-testid="collapsedControl"],
        button[kind="header"] {
            background: #1c1c1e !important;
            border: 1px solid #3f3f46 !important;
            border-radius: 6px !important;
            color: #e4e4e7 !important;
        }

        /* ── Buttons ── */
        .stButton > button {
            background: #1c1c1e;
            color: #e4e4e7;
            border: 1px solid #3f3f46;
            border-radius: 8px;
            font-size: 10px;
            padding: 0.25rem 0.25rem;
            width: 100%;
            transition: all 0.15s ease;
        }

        .stButton > button:hover { background: #27272a; border-color: #52525b; }

        button[kind="primary"] {
            background: #3f3f46 !important;
            color: #fff !important;
            border-color: #52525b !important;
        }

        button[kind="secondary"] {
            background: transparent !important;
            color: #a1a1aa !important;
            border-color: #27272a !important;
        }

        /* ── Inputs ── */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: #1c1c1e !important;
            border: 1px solid #3f3f46 !important;
            border-radius: 8px !important;
            color: #e4e4e7 !important;
            padding: 0.65rem 1rem !important;
        }

        .stTextInput label, .stTextArea label { color: #a1a1aa !important; font-size: 13px !important; }

        /* ── Selectbox ── */
        .stSelectbox > div > div {
            background: #1c1c1e !important;
            border: 1px solid #3f3f46 !important;
            border-radius: 8px !important;
            color: #e4e4e7 !important;
        }

        .stSelectbox label { color: #a1a1aa !important; font-size: 13px !important; }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #27272a; gap: 8px; }
        .stTabs [data-baseweb="tab"] { color: #71717a !important; }
        .stTabs [aria-selected="true"] { color: #e4e4e7 !important; border-bottom: 2px solid #e4e4e7; }

        /* ── Alerts ── */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px;
            border: 1px solid #27272a;
            background: #1c1c1e !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 6px; }
        ::-webkit-scrollbar-thumb:hover { background: #52525b; }
        * { scrollbar-width: thin; scrollbar-color: #3f3f46 transparent; }
        </style>
        """,
        unsafe_allow_html=True
    )