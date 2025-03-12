from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.openai_client import OpenAIClient
from services.api_client import APIClient
import logging

router = APIRouter()

class Message(BaseModel):
    user_id: int
    text: str

openai_client = OpenAIClient()
api_client = APIClient()

@router.post("/generate", summary="Generate AI response")
async def generate_response(message: Message):
    """ Generate response using OpenAI with chat history """
    logging.info(f"Received request for AI response: {message.user_id}, {message.text}")

    # Fetch chat history
    history = await api_client.get_chat_history(message.user_id)

    # Convert history into OpenAI-friendly format
    chat_messages = [{"role": "user", "content": msg["text"]} for msg in history]

    # Add the new user message to history
    chat_messages.append({"role": "user", "content": message.text})

    try:
        ai_response = await openai_client.generate_response(chat_messages)
        logging.info(f"AI Response Generated: {ai_response}")
        return {"response": ai_response}
    except Exception as e:
        logging.error(f"Error generating AI response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
