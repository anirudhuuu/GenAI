from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

text = "Eiffel Tower is in Paris and is a famous landmark, it is 324 meters tall"

response = client.models.embed_content(
    model = "gemini-embedding-exp-03-07",
    contents = text
)

print("Vector Embeddings : ", response.embeddings)
