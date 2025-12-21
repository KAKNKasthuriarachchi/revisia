import streamlit as st

def load_styles():
    st.markdown(
        """
        <style>
        /* Custom styles for the Streamlit app */
        body {
            background-color: #f0f2f5;
            font-family: 'Arial', sans-serif;
        }
        .stButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .stTextInput, .stTextArea {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )