import openai
import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "http://localhost:8000"  # API Service for retrieving history

app = FastAPI()
openai.api_key = OPENAI_API_KEY

class Message(BaseModel):
    user_id: int
    text: str

async def get_chat_history(user_id):
    """ Fetch chat history from API service """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/history/{user_id}") as response:
            if response.status == 200:
                data = await response.json()
                return data.get("history", [])
            return []

@app.post("/generate")
async def generate_response(message: Message):
    # Fetch chat history
    history = await get_chat_history(message.user_id)

    # Convert history into OpenAI-friendly format
    chat_messages = [{"role": "user", "content": msg["text"]} for msg in history]
    
    # Add the new user message to history
    chat_messages.append({"role": "user", "content": message.text})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_messages
        )
        return {"response": response["choices"][0]["message"]["content"]}

    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
