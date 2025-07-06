import os
import requests

from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode, tools_condition

api_key = os.getenv("GEMINI_API_KEY")

todos = []


@tool()
def add_todo(task: str):
    """Adds the input task to database."""
    todos.append(task)
    return True


@tool()
def get_all_todos():
    """Returns all the todos from the database."""
    return todos


@tool()
def add_two_numbers(a: int, b: int) -> int:
    """This tool adds two numbers."""
    return a + b


@tool()
def get_weather(city: str) -> str:
    """This tool returns the weather data about the given city."""
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    else:
        return "Sorry, I couldn't get the weather data for the city"


tools = [get_weather, add_two_numbers, add_todo, get_all_todos]


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = init_chat_model(
    model_provider="google_genai",
    model="gemini-2.0-flash",
    api_key=api_key,
)

# Bind the tools to the LLM
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    return {"messages": [message]}


tool_node = ToolNode(tools=tools)

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")

# Add a condition to check if the tool is needed
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


def main():
    user_query = input("> ")

    state = State(
        messages=[
            {"role": "user", "content": user_query}
        ]
    )

    for event in graph.stream(state, stream_mode="values"):
        if "messages" in event:
            event["messages"][-1].pretty_print()


main()
