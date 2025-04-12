from google import genai
from google.genai import types
import os

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    config=types.GenerateContentConfig(
        system_instruction='You are an ai assistant whose name is ChaiCode'
    ),
    contents='Hey there, what is your name? I am Anirudh',
)

print(response.text)
