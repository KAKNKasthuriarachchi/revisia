from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
load_dotenv()

class MongoDB:
    def __init__(self):
        print("Connecting to MongoDB...", os.getenv("DATABASE_URL"), os.getenv("DB_NAME"))
        self.client = MongoClient(os.getenv("DATABASE_URL"), server_api=ServerApi('1'))
        self.db = self.client[os.getenv("DB_NAME")]
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    # -------- Collections --------
    def get_users_collection(self):
        return self.db["users"]

    def get_chats_collection(self):
        return self.db["chats"]

    def get_chat_history_collection(self):
        return self.db["chat_history"]

    def close_connection(self):
        self.client.close()

mongo = MongoDB()
def get_chat_history():
    return mongo.get_chat_history_collection()

def save_chat(message: str):
    collection = mongo.get_chat_history_collection()
    collection.insert_one({"message": message})