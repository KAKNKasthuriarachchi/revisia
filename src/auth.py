def auth_ui():
    import streamlit as st
    from database.mongodb import MongoDB
    from werkzeug.security import generate_password_hash, check_password_hash

    db = MongoDB()
    users_collection = db.get_users_collection()

    st.title("User Authentication")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            user = users_collection.find_one({"username": username})
            if user and check_password_hash(user["password"], password):
                st.session_state.authenticated = True
                st.session_state.user_id = str(user["_id"])
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    elif choice == "Register":
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')

        if st.button("Register"):
            if users_collection.find_one({"username": new_username}):
                st.error("Username already exists.")
            else:
                hashed_password = generate_password_hash(new_password)
                users_collection.insert_one({"username": new_username, "password": hashed_password})
                st.success("Registered successfully! You can now log in.")