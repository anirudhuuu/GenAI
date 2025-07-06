import os

from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END

from pydantic import BaseModel

from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


class State(TypedDict):
    user_query: str
    llm_result: str | None
    accuracy_percentage: str | None
    is_coding_question: bool | None


class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool


class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: str


def classify_message(state: State):
    print("⚠️ Classifying message...")

    # Read user message from the state
    query = state['user_query']

    # OpenAI LLM call for classification
    SYSTEM_PROMPT = """
     You are an AI assistant whose job is to detect if the user's query is related
     to coding question or not.

     Return the response in specified JSON boolean only.
    """

    # Structured Output / Responses

    response = client.beta.chat.completions.parse(
        model="gemini-2.0-flash",
        response_format=ClassifyMessageResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    # Extract the classification result
    is_coding_question = response.choices[0].message.parsed.is_coding_question

    # Update the state with the classification result
    state['is_coding_question'] = is_coding_question

    return state


def route_query(state: State) -> Literal["general_query", "coding_query"]:
    print("🔄 Routing query...")

    is_coding = state['is_coding_question']

    if is_coding:
        return "coding_query"

    return "general_query"


def general_query(state: State):
    print("💬 Handling general query...")

    query = state['user_query']

    # To use OpenAI mini model or equivalent in Gemini
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "user", "content": query},
        ]
    )

    result = response.choices[0].message.content

    state['llm_result'] = result

    return state


def coding_query(state: State):
    print("💻 Handling coding query...")

    query = state['user_query']

    SYSTEM_PROMPT = """
        You are an AI assistant whose job is to answer coding questions.
        You will be given a coding question and you need to provide a detailed answer.
    """

    # To use OpenAI 4.1 model or equivalent in Gemini
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
    )

    result = response.choices[0].message.content

    state['llm_result'] = result

    return state


def coding_validate_query(state: State):
    print("✅ Validating coding query...")

    query = state['user_query']
    llm_result = state['llm_result']

    SYSTEM_PROMPT = f"""
        You are an expert in calculating the accuracy of a code according to the question.
        Return the percentage of accuracy of the code.

        User Query: {query}
        Code: {llm_result}
    """

    # To use Gemini or Claude
    response = client.beta.chat.completions.parse(
        model="gemini-2.0-flash",
        response_format=CodeAccuracyResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
    )

    accuracy = response.choices[0].message.parsed.accuracy_percentage

    state['accuracy_percentage'] = accuracy

    return state


graph_builder = StateGraph(State)

# Define the nodes in the graph
graph_builder.add_node("classify_message", classify_message)
graph_builder.add_node("route_query", route_query)
graph_builder.add_node("general_query", general_query)
graph_builder.add_node("coding_query", coding_query)
graph_builder.add_node("coding_validate_query", coding_validate_query)

# Add the edges to connect the nodes
graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", route_query)
graph_builder.add_edge("general_query", END)
graph_builder.add_edge("coding_query", "coding_validate_query")
graph_builder.add_edge("coding_validate_query", END)

graph = graph_builder.compile()


def main():
    user = input("> ")

    # Invoke the graph
    _state: State = {
        "user_query": user,
        "accuracy_percentage": None,
        "is_coding_question": False,
        "llm_result": None
    }

    for event in graph.stream(_state):
        print("Event: ", event)


main()
