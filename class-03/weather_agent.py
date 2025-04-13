import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

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
    model='gpt-4o',
    response_format={"type": "json_object"},
    messages=[
        { 'role': 'system', 'content': system_prompt },
        { 'role': 'user', 'content': 'What is the current weather of Hyderabad?' },

        # Manual addition
        { 'role': 'assistant', 'content': json.dumps({ 'steps': 'plan', 'content': 'The user is asking for the current weather in Hyderabad.' }) },
        { 'role': 'assistant', 'content': json.dumps({ 'steps': 'plan', 'content': 'From the available tools, I should call get_weather to obtain the weather information for Hyderabad.' }) },
        { 'role': 'assistant', 'content': json.dumps({ 'steps': 'action', 'function': 'get_weather', 'input': 'Hyderabad' }) },
        { 'role': 'assistant', 'content': json.dumps({ 'steps': 'observe', 'output': '32 degree celcius' }) },
    ]
)

print(response.choices[0].message.content)
