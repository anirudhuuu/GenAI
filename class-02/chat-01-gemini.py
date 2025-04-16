from openai import OpenAI
import os

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

result = client.chat.completions.create(
    model='gemini-2.0-flash',
    messages=[
        {'role': 'user', 'content': 'Hey there'} # Zero shot prompting
    ]
)

print(result.choices[0].message.content)
