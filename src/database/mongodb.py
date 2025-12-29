from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from bson import ObjectId
from datetime import datetime

load_dotenv()

class MongoDB:
    def __init__(self):
        # Use consistent environment variable names
        mongodb_uri = os.getenv("MONGODB_URI") or os.getenv("DATABASE_URL")
        db_name = os.getenv("DATABASE_NAME") or os.getenv("DB_NAME")
        
        print(f"Connecting to MongoDB: {db_name}")
        self.client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        
        try:
            self.client.admin.command('ping')
            print("✅ Successfully connected to MongoDB!")
        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
    
    # -------- Collections --------
    def get_users_collection(self):
        return self.db["users"]
    
    def get_chats_collection(self):
        return self.db["chats"]
    
    def get_chat_history_collection(self):
        return self.db["chat_history"]
    
    # -------- Chat Management Methods --------
    def create_chat(self, user_id: str, title: str = "New Chat"):
        """Create a new chat session"""
        chat = {
            "user_id": user_id,
            "title": title,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = self.get_chats_collection().insert_one(chat)
        return str(result.inserted_id)
    
    def get_user_chats(self, user_id: str):
        """Get all chats for a user"""
        chats = self.get_chats_collection().find(
            {"user_id": user_id}
        ).sort("updated_at", -1)
        return list(chats)
    
    def update_chat_title(self, chat_id: str, title: str):
        """Update chat title"""
        self.get_chats_collection().update_one(
            {"_id": ObjectId(chat_id)},
            {"$set": {"title": title, "updated_at": datetime.utcnow()}}
        )
    
    def delete_chat(self, chat_id: str):
        """Delete a chat and all its messages"""
        self.get_chats_collection().delete_one({"_id": ObjectId(chat_id)})
        self.get_chat_history_collection().delete_many({"chat_id": chat_id})
    
    def add_message(self, chat_id: str, role: str, message: str):
        """Add a message to a chat"""
        msg = {
            "chat_id": chat_id,
            "role": role,  # "user" or "assistant"
            "message": message,
            "timestamp": datetime.utcnow()
        }
        self.get_chat_history_collection().insert_one(msg)
        
        # Update chat's updated_at timestamp
        self.get_chats_collection().update_one(
            {"_id": ObjectId(chat_id)},
            {"$set": {"updated_at": datetime.utcnow()}}
        )
    
    def get_chat_messages(self, chat_id: str):
        """Get all messages for a specific chat"""
        messages = self.get_chat_history_collection().find(
            {"chat_id": chat_id}
        ).sort("timestamp", 1)
        return list(messages)
    
    def close_connection(self):
        self.client.close()