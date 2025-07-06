import os
import json
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def get_weather(city: str) -> str:
    # API Call to get the weather
    return "42 degrees C"


SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. And based on the tool selected you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for the next input.
    - Carefully analyse the user query.

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function"
    }}

    Available Tools:
    - "get_weather": Takes a city name as input and returns the weather of the city.

    Example:
    Input: What is the weather in Hyderabad?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of Hyderabad. So I will use the get_weather tool to get the weather data of Hyderabad." }}
    Output: {{ "step": "plan", "content": "From the available tools, I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "Hyderabad" }}
    Output: {{ "step": "observe", "content": "24 degrees C" }}
    Output: {{ "step": "output", "content": "The weather for Hyderabad seems to be 24 degrees C" }}
"""

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is the weather in Hyderabad?"},
        # Chain of thought prompt for weather agent
        {"role": "assistant", "content": json.dumps(
            {"step": "plan", "content": "The user is interested in weather data of Hyderabad. So I will use the get_weather tool to get the weather data of Hyderabad."})},
        {"role": "assistant", "content": json.dumps(
            {"step": "plan", "content": "From the available tools, I should call get_weather"})},
        {"role": "assistant", "content": json.dumps(
            {"step": "action", "function": "get_weather", "input": "Hyderabad"})},
        {"role": "assistant", "content": json.dumps(
            {"step": "observe", "content": "24 degrees C"})},
        # Chain of thought prompt for weather agent ends here
    ]
)

print(response.choices[0].message.content)

"""
{
    "step": "output",
    "content": "The weather for Hyderabad seems to be 24 degrees C"
}
"""
