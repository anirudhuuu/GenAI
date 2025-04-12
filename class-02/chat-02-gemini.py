from google import genai
from google.genai import types

client = genai.Clent(api_key='')

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Why is the sky blue?'
)

print(response.text)
