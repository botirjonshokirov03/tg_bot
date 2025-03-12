import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    async def generate_response(self, chat_messages):
        """ Generate AI response from OpenAI API """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat_messages
            )
            return response["choices"][0]["message"]["content"]
        except openai.error.OpenAIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
