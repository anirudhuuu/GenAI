import os
import json
from google import genai
from google.genai import types

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_weather(city: str):
    # TODO: Perform an actual API call
    return "32 degree celcius"

system_prompt = """
    You are an helpful AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next intput 
    - Carefully analyse the user query
    - json response values having null must be replaced with None as per python standard

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather

    Example:
    User Query:  What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Celcius" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    config=types.GenerateContentConfig(
        system_instruction=system_prompt
    ),
    contents=[
        'What is the current weather of Hyderabad?',
        # Manual addition
        json.dumps({ "step": "plan", "content": "The user is asking for the current weather of Hyderabad." }),
        json.dumps({ "step": "plan", "content": "I should use the 'get_weather' tool to find the weather information." }),
        json.dumps({ "step": "action", "content": "Call the 'get_weather' tool to fetch the weather information for Hyderabad.", "function": "get_weather", "input": "Hyderabad" }),
        json.dumps({ "step": "observe", "output": "29 degrees Celcius, clear sky" }),
        json.dumps({ "step": "output", "content": "The current weather in Hyderabad is 29 degrees Celcius with a clear sky.", "function": None, "input": None }),
    ],
)

print(response.text)
