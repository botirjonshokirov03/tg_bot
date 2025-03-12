import logging
import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://localhost:8000"
NLP_URL = "http://localhost:8001"

# Initialize bot & dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def save_message(telegram_id: int, text: str):
    """ Save user message to API Service """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/save_message", json={"telegram_id": telegram_id, "text": text}) as response:
            return await response.json()

async def register_user(telegram_id: int, username: str):
    """ Register user in API Service """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/register", json={"telegram_id": telegram_id, "username": username}) as response:
            return await response.json()

async def get_ai_response(user_id: int, text: str):
    """ Get AI-generated response from NLP Service """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{NLP_URL}/generate", json={"user_id": user_id, "text": text}) as response:
            return await response.json()

@dp.message(CommandStart())
async def start(message: Message):
    """ Handle /start command: Register user and greet them """
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"

    registration_response = await register_user(user_id, username)
    await message.answer(f"Hello {username}! {registration_response['message']}")

@dp.message()
async def handle_message(message: Message):
    """ Handle user messages: Save history & get AI response """
    await save_message(message.from_user.id, message.text)

    reply = await get_ai_response(message.from_user.id, message.text)
    await message.answer(reply["response"])

async def main():
    """ Start the bot """
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
