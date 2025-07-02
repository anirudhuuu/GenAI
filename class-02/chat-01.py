from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

result = client.chat.completions.create(
    model='gpt-4',
    messages=[
        {'role': 'user', 'content': 'Hey there'} # Zero shot prompting
    ]
)

print(result.choices[0].message.content)
