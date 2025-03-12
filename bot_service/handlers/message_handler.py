from aiogram.types import Message
from services.api_client import APIClient
from services.nlp_client import NLPClient
import logging

api_client = APIClient()
nlp_client = NLPClient()

async def handle_message(message: Message):
    # Handle user messages: Save history & get AI response
    user_id = message.from_user.id
    text = message.text

    logging.info(f"Received message from Telegram user {user_id}: {text}")

    # Save message to API service
    save_response = await api_client.save_message(user_id, text)
    logging.info(f"Save message response: {save_response}")

    # Get AI-generated response from NLP service
    ai_response = await nlp_client.get_ai_response(user_id, text)
    logging.info(f"NLP response for user {user_id}: {ai_response}")

    # Send AI-generated response back to the user
    await message.answer(ai_response)
