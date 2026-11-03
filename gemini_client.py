import os
from dotenv import load_dotenv
from google import genai

def get_client():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if key is None or key == "":
        return None
    return genai.Client(api_key=key)

                         
