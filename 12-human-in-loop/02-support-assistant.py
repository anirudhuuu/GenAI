import os
import json

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langgraph.types import Command, interrupt
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver

from pymongo import MongoClient

api_key = os.getenv("GEMINI_API_KEY")


def append_admin_message(config, solution):
    client = MongoClient("mongodb://admin:admin@localhost:27017")
    db = client["checkpointing_db"]
    collection = db["checkpoints"]

    thread_id = config["configurable"]["thread_id"]

    collection.update_one(
        {"configurable.thread_id": thread_id},
        {"$push": {"messages": {"role": "assistant", "content": solution}}}
    )


@tool()
def human_assistance(query: str) -> str:
    """
    Request assistance from a human.
    """

    # This saves the state in DB and kills the graph execution.
    human_response = interrupt({"query": query})
    return human_response["data"]


tools = [human_assistance]


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


def user_chat():
    # MongoDB connection details
    DB_URI = "mongodb://admin:admin@localhost:27017"

    # Config for thread_id
    config = {
        "configurable": {
            "thread_id": "9",
        }
    }

    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_checkpointer = create_chat_graph(mongo_checkpointer)

        while True:
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


# user_chat()


def admin_call():
    # MongoDB connection details
    DB_URI = "mongodb://admin:admin@localhost:27017"

    # Config for thread_id
    config = {
        "configurable": {
            "thread_id": "9",
        }
    }

    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_checkpointer = create_chat_graph(mongo_checkpointer)

        state = graph_with_checkpointer.get_state(config=config)
        last_message = state.values['messages'][-1]

        tool_calls = getattr(last_message, "tool_calls", [])

        user_query = None

        for call in tool_calls:
            if call.get("function", {}).get("name") == "human_assistance" or call.get("name") == "human_assistance":
                args_json = None
                if call.get("function", {}).get("arguments"):
                    args_json = call["function"]["arguments"]
                elif call.get("args"):
                    args_json = call["args"]

                if isinstance(args_json, dict):
                    user_query = args_json.get("query")
                elif isinstance(args_json, str):
                    try:
                        args_dict = json.loads(args_json)
                        user_query = args_dict.get("query")
                    except Exception:
                        print("Failed to decode tool arguments.")
                        user_query = None
                else:
                    user_query = None

        print("User has a query:", user_query)
        solution = input("> ")

        resume_command = Command(resume={"data": solution})

        for event in graph_with_checkpointer.stream(resume_command, config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()

        append_admin_message(config, solution)


# admin_call()
user_chat()
