from aiogram.filters import CommandStart
from aiogram.types import Message
from services.api_client import APIClient
import logging

api_client = APIClient()

async def start(message: Message):
    # Handle /start command: Register user and greet them
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"

    logging.info(f"Registering user {user_id} with username: {username}")

    # Register user only when the /start command is sent
    registration_response = await api_client.register_user(user_id, username)
    
    welcome_message = f"Hello {username}! {registration_response['message']}"
    await message.answer(welcome_message)
