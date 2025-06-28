import os
from openai import OpenAI
from datetime import datetime

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant

    Today is {datetime.now().strftime("%A, %B %d, %Y")} and the time is {datetime.now().strftime("%I:%M %p")} IST
"""

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is the date and time today?"}
    ]
)

print(response.choices[0].message.content)
