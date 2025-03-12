import aiohttp
import os
from dotenv import load_dotenv
import logging

load_dotenv()
NLP_URL = os.getenv("NLP_URL", "http://localhost:8001")

class NLPClient:
    def __init__(self):
        self.nlp_url = NLP_URL

    async def get_ai_response(self, user_id: int, text: str):
        # Get AI-generated response from NLP Service
        logging.info(f"Sending request to NLP Service: user_id={user_id}, text={text}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.nlp_url}/generate", json={"user_id": user_id, "text": text}) as response:
                logging.info(f"NLP service response status: {response.status}")

                if response.status == 200:
                    data = await response.json()
                    logging.info(f"NLP service response data: {data}")
                    return data.get("response", "No AI response received.")

                error_message = f"Error: Unable to connect to NLP Service, status {response.status}"
                logging.error(error_message)
                return error_message
