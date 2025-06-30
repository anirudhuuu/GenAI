# flake8: noqa
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://vector-db:6333",
    collection_name="learning_vectors",
    embedding=embedding_model,
)


def process_query(query: str):
    print("Searching chuncks for:", query)

    search_results = vector_db.similarity_search(
        query=query
    )

    context = "\n\n".join(
        [f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

    SYSTEM_PROMPT = f"""
        You are a helpful AI assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page number.

        You should only answer the user based on the following context and navigate the user to open the right page number to know more.

        Context:
        {context}
    """

    chat_completion = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
    )

    # Save to DB
    print(f"🤖: {query}", {
          chat_completion.choices[0].message.content}, "\n\n\n")

    return chat_completion.choices[0].message.content
