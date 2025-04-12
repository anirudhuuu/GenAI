# Automation
import os
import json
from google import genai
from google.genai import types

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "ooutput", "validate", and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next intput
3. Carefully analyse the user query

Output Format:
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2
Output: {{ step: "analyse", content: "Alright! The user is interested in maths query and he is asking a basic arthematic oepration" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct answer for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

"""

messages = []

query = input("> ")
messages.append(query)

while True:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
        contents=messages,
    )

    clean_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
    parsed_response = json.loads(clean_text)
    messages.append(clean_text)

    if parsed_response.get("step") != "result":
        print(f"🧠: {parsed_response.get("content")}")
        continue

    print(f"🤖: {parsed_response.get("content")}")
    break
