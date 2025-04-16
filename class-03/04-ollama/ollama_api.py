from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

client = Client(
    host="http://localhost:11434",
)

client.pull('gemma3:1b')

@app.post("/chat")
def chat(message: str = Body(..., description="Chat Message")):
    response = client.chat(
        model='gemma3:1b',
        messages=[
            # { 'role': 'user', 'content': 'hey there' }
            { 'role': 'user', 'content': message }
        ]
    )

    return response['message']['content']
