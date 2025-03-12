from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import get_db
from repositories.user_repository import UserRepository
from repositories.message_repository import MessageRepository

app = FastAPI(
    title="Telegram AI Chatbot API",
    description="This API manages user registration, chat history, and integrates with OpenAI for NLP responses.",
    version="1.0.0"
)

# Pydantic Schemas
class RegisterUser(BaseModel):
    telegram_id: int = Field(..., example=987654321)
    username: str = Field(..., example="john_doe")

class MessageData(BaseModel):
    telegram_id: int = Field(..., example=123456789)
    text: str = Field(..., example="Hello, how are you?")

@app.post("/register", summary="Register a new user")
def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    existing_user = user_repo.get_user_by_telegram_id(user.telegram_id)

    if existing_user:
        return {"message": f"Welcome back, {existing_user.username}!"}

    user_repo.create_user(user.telegram_id, user.username)
    return {"message": "User registered successfully"}

@app.post("/save_message", summary="Save user message")
def save_message(message: MessageData, db: Session = Depends(get_db)):
    message_repo = MessageRepository(db)
    saved_message = message_repo.save_message(message.telegram_id, message.text)

    if not saved_message:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Message saved successfully"}

@app.get("/history/{telegram_id}", summary="Retrieve chat history")
def get_chat_history(telegram_id: int, db: Session = Depends(get_db)):
    message_repo = MessageRepository(db)
    history = message_repo.get_chat_history(telegram_id)

    if history is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"history": [{"id": msg.id, "text": msg.text} for msg in history]}
