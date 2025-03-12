import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

class APIClient:
    def __init__(self):
        self.api_url = API_URL

    async def register_user(self, telegram_id: int, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}/register", json={"telegram_id": telegram_id, "username": username}) as response:
                return await response.json()

    async def save_message(self, telegram_id: int, text: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}/save_message", json={"telegram_id": telegram_id, "text": text}) as response:
                return await response.json()
