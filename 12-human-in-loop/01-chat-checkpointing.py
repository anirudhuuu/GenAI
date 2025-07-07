import os

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

from langchain.chat_models import init_chat_model
# from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver

api_key = os.getenv("GEMINI_API_KEY")

tools = []


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = init_chat_model(
    model_provider="google_genai",
    model="gemini-2.0-flash",
    api_key=api_key,
)
llm_with_tools = llm.bind_tools(tools=tools)


def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    return {"messages": [message]}


tool_node = ToolNode(tools=tools)

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)


def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


def main():
    # MongoDB connection details
    DB_URI = "mongodb://admin:admin@localhost:27017"

    # Config for thread_id
    config = {
        "configurable": {
            "thread_id": 1,
        }
    }

    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_checkpointer = create_chat_graph(mongo_checkpointer)

        user_input = input("> ")

        state = State(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        )

        for event in graph_with_checkpointer.stream(state, config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()


main()
