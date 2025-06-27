from openai import OpenAI
import os

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

text = "Eiffel Tower is in Paris and is a famous landmark, it is 324 meters tall"

response = client.embeddings.create(
    model="text-embedding-004",
    input=text
)

print("Vector Embeddings : ", response.data[0].embedding)
