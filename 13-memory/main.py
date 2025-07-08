import os
import json

from mem0 import Memory
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

config = {
    "version": "v1.1",

    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": api_key,
            "model": "models/text-embedding-004",
        }
    },

    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": api_key,
            "model": "gemini-2.0-flash-001",
        }
    },

    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": "6333",
            "collection_name": "memories",
        }
    }
}

memory_client = Memory.from_config(config)


def chat():
    while True:
        user_query = input("> ")
        # read user input based search and given that memory
        relevant_memories = memory_client.search(
            query=user_query, user_id="anirudh")

        memories = [
            f"ID: {mem.get("id")}, Memory: {mem.get("memory")}" for mem in relevant_memories.get("results")]

        SYSTEM_PROMPT = f"""
            You are a memory aware assistant which responses to user with context.
            You are given with past memories and facts about the user.
            
            Memory of the user:
            {json.dumps(memories)}
        """

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ],
        )

        print(f"🤖: {response.choices[0].message.content}")

        memory_client.add([
            {"role": "user", "content": user_query},
            {"role": "assistant",
                "content": response.choices[0].message.content},
        ], user_id="anirudh")


chat()
