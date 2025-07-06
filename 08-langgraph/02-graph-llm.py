import os

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


class State(TypedDict):
    query: str
    llm_result: str | None


def chat_bot(state: State):
    # Get the query from the state
    query = state['query']

    # OpenAI LLM call
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "user", "content": query},
        ]
    )

    result = response.choices[0].message.content

    # Update the state with the LLM result
    state['llm_result'] = result

    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

graph = graph_builder.compile()


def main():
    user = input("> ")

    # Invoke the graph
    _state = {
        "query": user,
        "llm_result": None
    }

    graph_result = graph.invoke(_state)

    print("graph_result: ", graph_result)


main()
