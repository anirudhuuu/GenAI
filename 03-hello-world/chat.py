import os
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

"""
Simple chat with AI
=====================
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "user", "content": "Hey, there"}
    ]
)
"""

"""
No access to real-time data
==============================
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "user", "content": "What is the weather today?"}
    ]
)
"""

"""
Stateless responses
==============================
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "user", "content": "Hey, my name is Anirudh"}
    ]
)

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "user", "content": "Whats my name?"}
    ]
)

No access to your history, unless provided
"""

"""
Provide with history and context
====================================
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "user", "content": "Hey, my name is Anirudh"},
        {"role": "assistant",
            "content": "Hi Anirudh, it's nice to meet you! How can I help you today?"},
        {"role": "user", "content": "Whats my name?"}
    ]
)
"""

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "user", "content": "Hey, my name is Anirudh"},
        {"role": "assistant",
            "content": "Hi Anirudh, it's nice to meet you! How can I help you today?"},
        {"role": "user", "content": "Whats my name?"},
        {"role": "assistant", "content": "Your name is Anirudh."},
        {"role": "user", "content": "How are you?"},
    ]
)

print(response.choices[0].message.content)
