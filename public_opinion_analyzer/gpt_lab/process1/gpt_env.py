import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI


def get_openai_client():
    # Access the API key using the variable name defined in the .env file
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("API key is not set")

    client = OpenAI(api_key=api_key)
    return client
