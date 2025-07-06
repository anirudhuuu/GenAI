import os
import requests

from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

api_key = os.getenv("GEMINI_API_KEY")


@tool()
def get_weather(city: str) -> str:
    """This tool returns the weather data about the given city."""
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    else:
        return "Sorry, I couldn't get the weather data for the city"


tools = [get_weather]


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


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

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
