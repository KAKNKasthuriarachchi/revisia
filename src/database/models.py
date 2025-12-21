from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

# ---------------------------
# ObjectId handler for Pydantic
# ---------------------------
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# ---------------------------
# User Model
# ---------------------------
class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True


# ---------------------------
# Chat Model (Chat session)
# ---------------------------
class Chat(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True


# ---------------------------
# Chat History Model (Messages)
# ---------------------------
class ChatMessage(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    chat_id: PyObjectId
    sender: str  # "user" or "assistant"
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True


# ---------------------------
# Serializers (MongoDB → JSON)
# ---------------------------
def user_serializer(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"]
    }


def chat_serializer(chat: dict) -> dict:
    return {
        "id": str(chat["_id"]),
        "user_id": str(chat["user_id"]),
        "title": chat["title"],
        "created_at": chat["created_at"]
    }


def chat_message_serializer(message: dict) -> dict:
    return {
        "id": str(message["_id"]),
        "chat_id": str(message["chat_id"]),
        "sender": message["sender"],
        "message": message["message"],
        "timestamp": message["timestamp"]
    }
