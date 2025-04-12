from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

result = client.chat.completions.create(
    model='gpt-4',
    messages=[
        # System prompt
        {'role': 'system', 'content': 'You are an ai assistant whose name is ChaiCode'},
        {'role': 'user', 'content': 'Hey there'}
    ]
)

print(result.choices[0].message.content)
