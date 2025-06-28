import os
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

text = "dog chases cat"

response = client.embeddings.create(
    model="text-embedding-004",
    input=text
)

print("Vector Embeddings", response)

# Indicator for no. of dimensions for vector embedding
print("Length", len(response.data[0].embedding))
