import json
import os
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

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

response = client.chat.completions.create(
    model='gemini-2.0-flash',
    response_format={"type": "json_object"},
    messages=[
        { 'role': 'system', 'content': system_prompt },
        { 'role': 'user', 'content': 'What is the current weather of Hyderabad?' },

        # Manual addition
        { 'role': 'assistant', 'content': json.dumps({ "step": "plan", "content": "The user wants to know the current weather in Hyderabad.", "function": None, "input": None }) },
        { 'role': 'assistant', 'content': json.dumps({ "step": "plan", "content": "I should use the 'get_weather' tool to find the weather information for Hyderabad.", "function": None, "input": None }) },
        { 'role': 'assistant', 'content': json.dumps({ "step": "action", "content": "Call get_weather function to get weather details for Hyderabad", "function": "get_weather", "input": "Hyderabad" }) },
        { 'role': 'assistant', 'content': json.dumps({ "step": "observe", "output": "The current weather in Hyderabad is 30 degrees Celsius, with clear skies and a light breeze." }) },
    ]
)

print(response.choices[0].message.content)

# {
#     "step": "output",
#     "content": "The current weather in Hyderabad is 30 degrees Celsius, with clear skies and a light breeze.",
#     "function": null,
#     "input": null
# }
