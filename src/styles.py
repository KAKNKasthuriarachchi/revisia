import streamlit as st

def load_styles():
    st.markdown(
        """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* Remove default padding and make auth pages non-scrollable */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 900px;
        }
        
        /* Auth page specific - center content and prevent scrolling */
        section[data-testid="stSidebar"] + div .block-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 80vh;
            overflow: hidden;
        }
        
        /* Smooth fade-in animation */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Slide-in animation for sidebar items */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* Apply fade-in to main content */
        .main {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Modern Button Styles */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.65rem 1.5rem;
            font-size: 15px;
            font-weight: 500;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
            width: 100%;
            cursor: pointer;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        }
        
        /* Secondary buttons (for chat list) */
        button[kind="secondary"] {
            background: #ffffff !important;
            color: #4a5568 !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        }
        
        button[kind="secondary"]:hover {
            background: #f7fafc !important;
            border-color: #cbd5e0 !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
        }
        
        /* Primary buttons (active chat) */
        button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25) !important;
        }
        
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #5568d3 0%, #653a8b 100%) !important;
            box-shadow: 0 3px 12px rgba(102, 126, 234, 0.35) !important;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.75rem 1rem;
            font-size: 15px;
            transition: all 0.3s ease;
            background-color: #ffffff;
            color: #1a202c !important;
        }
        
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: #a0aec0 !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            outline: none;
        }
        
        /* Input Labels */
        .stTextInput label,
        .stTextArea label {
            color: #4a5568 !important;
            font-weight: 500;
        }
        
        /* Chat Input */
        .stChatInput > div > div > textarea {
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            padding: 1rem 1.25rem;
            font-size: 15px;
            transition: all 0.3s ease;
            background-color: #ffffff;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            color: #1a202c !important;
        }
        
        .stChatInput > div > div > textarea::placeholder {
            color: #a0aec0 !important;
        }
        
        .stChatInput > div > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
        }
        
        /* Sidebar Styling - More Compact */
        section[data-testid="stSidebar"] {
            background-color: #f8f9fa;
            border-right: 1px solid #e2e8f0;
            padding: 0.5rem 0.75rem !important;
        }
        
        section[data-testid="stSidebar"] > div {
            animation: slideIn 0.4s ease-out;
            padding-top: 1rem;
        }
        
        /* Compact sidebar content */
        section[data-testid="stSidebar"] .block-container {
            padding: 0.5rem 0 !important;
        }
        
        /* Sidebar Title - More Compact */
        section[data-testid="stSidebar"] h1 {
            font-size: 1.3rem !important;
            margin-bottom: 0.5rem !important;
            padding: 0.5rem 0 !important;
        }
        
        /* Sidebar Subheader - More Compact */
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-size: 0.95rem !important;
            margin: 0.5rem 0 0.3rem 0 !important;
            padding: 0 !important;
        }
        
        /* Sidebar Text Color Fix */
        section[data-testid="stSidebar"] * {
            color: #1a202c !important;
        }
        
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6 {
            color: #1a202c !important;
        }
        
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: #4a5568 !important;
        }
        
        /* Sidebar button text color override for primary buttons */
        section[data-testid="stSidebar"] button[kind="primary"] p,
        section[data-testid="stSidebar"] button[kind="primary"] span {
            color: white !important;
        }
        
        /* Sidebar Buttons - More Compact */
        section[data-testid="stSidebar"] .stButton > button {
            border-radius: 8px;
            font-size: 13px;
            padding: 0.5rem 0.75rem;
            margin: 0.2rem 0;
            transition: all 0.2s ease;
        }
        
        /* New Chat Button */
        section[data-testid="stSidebar"] .stButton:first-of-type > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-weight: 600;
            color: white !important;
            margin-bottom: 0.5rem;
        }
        
        /* Delete Button - More Compact */
        button:has(span:contains("🗑️")) {
            background: transparent !important;
            color: #e53e3e !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            padding: 0.3rem 0.5rem !important;
            font-size: 14px !important;
            transition: all 0.2s ease !important;
            min-width: 32px !important;
        }
        
        button:has(span:contains("🗑️")):hover {
            background: #fff5f5 !important;
            border-color: #fc8181 !important;
        }
        
        /* Selectbox - More Compact */
        section[data-testid="stSidebar"] .stSelectbox {
            margin: 0.3rem 0 0.5rem 0;
        }
        
        .stSelectbox > div > div {
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            transition: all 0.3s ease;
            background-color: #ffffff;
            font-size: 13px;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #cbd5e0;
        }
        
        /* Selectbox text color */
        .stSelectbox label {
            color: #4a5568 !important;
            font-size: 13px !important;
            margin-bottom: 0.25rem !important;
        }
        
        .stSelectbox div[data-baseweb="select"] > div {
            color: #1a202c !important;
        }
        
        /* Divider - More Compact */
        section[data-testid="stSidebar"] hr {
            margin: 0.5rem 0 !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #4a5568 !important;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            color: #667eea !important;
        }
        
        /* Chat Messages - Fix Text Color */
        .stChatMessage {
            animation: fadeIn 0.4s ease-out;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.75rem 0;
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        /* Chat Message Text Color Fix */
        .stChatMessage p,
        .stChatMessage span,
        .stChatMessage div {
            color: #1a202c !important;
        }
        
        /* Assistant message styling */
        [data-testid="stChatMessageContent"] {
            color: #1a202c !important;
        }
        
        /* Streaming cursor fix */
        .stChatMessage span {
            color: #1a202c !important;
        }
        
        /* Title Styling */
        h1 {
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 1.5rem;
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Divider */
        hr {
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 1rem 0;
        }
        
        /* Success/Error Messages */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 10px;
            padding: 1rem;
            animation: fadeIn 0.4s ease-out;
        }
        
        /* Loading Spinner */
        .stSpinner > div {
            border-color: #667eea;
        }
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a0aec0;
        }
        
        /* Remove extra spacing on auth pages */
        .main.css-uf99v8.e1g8pov65 {
            padding: 1rem;
        }
        
        /* Smooth transitions for all interactive elements */
        button, input, textarea, select {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }
            
            .stButton > button {
                padding: 0.6rem 1.2rem;
                font-size: 14px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )