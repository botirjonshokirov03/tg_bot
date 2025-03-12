from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")

app = FastAPI(
    title="Telegram AI Chatbot API",
    description="This API manages user registration, chat history, and integrates with OpenAI for NLP responses.",
    version="1.0.0",
    contact={
        "name": "Botirjon Shokirov",
        "url": "https://github.com/botirjonshokirov03",
        "email": "shokirovbotirjon2003@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)


# Database Setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String)

# Message Model
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)

# Create tables if they don’t exist
Base.metadata.create_all(bind=engine)

# Pydantic Schema for Messages
class MessageData(BaseModel):
    telegram_id: int = Field(..., example=123456789)
    text: str = Field(..., example="Hello, how are you?")


# Pydantic Schema
class RegisterUser(BaseModel):
    telegram_id: int = Field(..., example=987654321)
    username: str = Field(..., example="john_doe")


# Store messages in the database
@app.post(
    "/save_message",
    summary="Save user message",
    description="Stores a user's message in the database, linking it to their Telegram ID.",
    responses={
        200: {
            "description": "Message successfully saved",
            "content": {
                "application/json": {
                    "example": {"message": "Message saved successfully"}
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
def save_message(message: MessageData):
    user = db.query(User).filter(User.telegram_id == message.telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_message = Message(user_id=user.id, text=message.text)
    db.add(new_message)
    db.commit()
    
    return {"message": "Message saved successfully"}


@app.post(
    "/register",
    summary="Register a new user",
    description="Registers a user with their Telegram ID and username.",
    responses={
        200: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {"message": "User registered successfully"}
                }
            }
        },
        409: {
            "description": "User already exists",
            "content": {
                "application/json": {
                    "example": {"message": "Welcome back, john_doe!"}
                }
            }
        }
    }
)
def register_user(user: RegisterUser):
    existing_user = db.query(User).filter(User.telegram_id == user.telegram_id).first()
    if existing_user:
        return {"message": f"Welcome back, {existing_user.username}!"}

    new_user = User(telegram_id=user.telegram_id, username=user.username)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}



# Retrieve chat history
@app.get(
    "/history/{telegram_id}",
    summary="Retrieve chat history",
    description="Fetches the chat history of a user by their Telegram ID.",
    responses={
        200: {
            "description": "User chat history retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "history": [
                            {"id": 1, "text": "Hello, how are you?"},
                            {"id": 2, "text": "What is my name?"}
                        ]
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
def get_chat_history(telegram_id: int):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    messages = db.query(Message).filter(Message.user_id == user.id).all()
    return {"history": [{"id": msg.id, "text": msg.text} for msg in messages]}


