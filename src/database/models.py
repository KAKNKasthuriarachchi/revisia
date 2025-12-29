from pydantic import BaseModel, Field
from typing import Optional, List
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
    email: Optional[str] = None
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
    user_id: str
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True


# ---------------------------
# Chat Message Model
# ---------------------------
class ChatMessage(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    chat_id: str
    role: str  # "user" or "assistant"
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
        "email": user.get("email", ""),
        "created_at": user["created_at"]
    }


def chat_serializer(chat: dict) -> dict:
    return {
        "id": str(chat["_id"]),
        "user_id": chat["user_id"],
        "title": chat["title"],
        "created_at": chat["created_at"],
        "updated_at": chat.get("updated_at", chat["created_at"])
    }


def chat_message_serializer(message: dict) -> dict:
    return {
        "id": str(message["_id"]),
        "chat_id": message["chat_id"],
        "role": message["role"],
        "message": message["message"],
        "timestamp": message["timestamp"]
    }
