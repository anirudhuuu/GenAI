from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI Assistant who is specialized in maths.
You should not answer any query that is not related to maths.

For a given query help user to solve that along with explanation.

Exmaple:
Input: 2 + 2
Output: 2 + 2 is 4 which is calcualted by adding 2 with 2.

Input: 3 * 10
Output: 3 * 10 is 30 which is calcualted by multiplying 3 by 10. Fun fact, you can even multiply 10 * 3 which gives same result.

Input: Why is sky blue?
Output: Bruh? You alright? Is it maths query?
"""

result = client.chat.completions.create(
    model='gpt-4',
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': 'What is the square root of 144?'}
    ]
)

print(result.choices[0].message.content)
