from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    query: str
    llm_result: str | None


def chat_bot(state: State):
    # Get the query from the state
    # OpenAI LLM call
    # Update the state with the LLM result

    query = state['query']
    result = "Hello, How can I assist you today?"
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
