import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

class APIClient:
    def __init__(self):
        self.api_url = API_URL

    async def get_chat_history(self, user_id: int):
        """ Fetch chat history from API Service """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/history/{user_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("history", [])
                return []
