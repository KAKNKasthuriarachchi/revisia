def retrieve_relevant_info(query, db):
    # Function to retrieve relevant information from the MongoDB database based on user queries
    results = db.chat_history.find({"$text": {"$search": query}})
    return list(results)

def get_user_chats(user_id, db):
    # Function to get chat history for a specific user
    user_chats = db.chat_history.find({"user_id": user_id})
    return list(user_chats)

def retrieve_user_info(user_id, db):
    # Function to retrieve user information from the database
    user_info = db.users.find_one({"_id": user_id})
    return user_info