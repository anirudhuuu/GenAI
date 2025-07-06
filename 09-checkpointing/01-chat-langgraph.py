import os

from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END

api_key = os.getenv("GEMINI_API_KEY")


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = init_chat_model(
    model_provider="google_genai",
    model="gemini-2.0-flash",
    api_key=api_key,
)


def chat_node(state: State):
    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


graph_builder = StateGraph(State)

graph_builder.add_node("chat_node", chat_node)
graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)

graph = graph_builder.compile()


def main():
    query = input("> ")

    _state = {
        "messages": [
            {"role": "user", "content": query}
        ]
    }

    # This creates a fresh new state for each invocation
    result = graph.invoke(_state)
    # And the state is deleted after the invocation

    print("result:", result)


main()
