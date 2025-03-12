import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from handlers.command_handler import start
from handlers.message_handler import handle_message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize bot & dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.message.register(start, Command("start")) 
dp.message.register(handle_message) 

async def main():
    # Start the bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
