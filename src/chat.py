def chat_ui():
    import streamlit as st
    from database.mongodb import get_chat_history, save_chat
    from utils.helpers import format_chat_message

    st.title("Chat Interface")

    # Display chat history
    chat_history = get_chat_history().find()
    for chat in chat_history:
        st.markdown(format_chat_message(chat))

    # User input for new chat message
    user_input = st.text_input("You:", "")
    
    if st.button("Send"):
        if user_input:
            # Save the chat message to the database
            save_chat(user_input)
            st.success("Message sent!")
            st.experimental_rerun()  # Refresh the chat history
        else:
            st.warning("Please enter a message.")