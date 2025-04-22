import os
import json
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate

from rest_places_api_example import query_google_places,load_saved_schema

# ✅ Define API Endpoints
API_BASE_URL = "https://agentsserver.modlee.ai:5000"
SCHEMA_ENDPOINT = f"{API_BASE_URL}/data_operator_agent_rest_schema"
QUERY_ENDPOINT = f"{API_BASE_URL}/data_operator_agent_rest"

# ✅ Get API Keys
MODLEE_AGENTS_API_KEY = os.getenv("MODLEE_AGENTS_API_KEY")  # Modlee Agent API Key
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Google Places API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API Key for GPT-4o Mini

# ✅ File paths
SCHEMA_OUTPUT_PATH = "places_api_schema.json"  # Saved schema


def process_with_gpt4o(user_request, google_data):
    """Generate a response using GPT-4o Mini based only on structured Google Places data."""

    llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY"))

    # ✅ Define prompt with structured format
    prompt_message = HumanMessage(
        content=(
            "Based on the following structured data from Google Places, answer the user's question strictly using this data.\n\n"
            "**User Query:** {user_request}\n"
            "**Retrieved Data:** {google_data}\n\n"
            "Answer concisely, avoiding any hallucination."
        ).format(
            user_request=user_request,
            google_data=json.dumps(google_data, indent=2)
        )
    )

    # ✅ Get AI-generated response
    response = llm([prompt_message]).content.strip()
    
    return response

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.memory import VectorStoreRetrieverMemory
from langchain.docstore.in_memory import InMemoryDocstore
import faiss
import json


# # ✅ Initialize OpenAI Embedding Function
# embedding_function = OpenAIEmbeddings()

# # ✅ Create an Empty FAISS Index
# dimension = 1536  # OpenAI Embedding dimension
# index = faiss.IndexFlatL2(dimension)  # L2 Distance Index
# docstore = InMemoryDocstore()  # In-memory document store
# index_to_docstore_id = {}

# # ✅ Create FAISS Vector Store
# vector_db = FAISS(
#     index=index,
#     docstore=docstore,
#     index_to_docstore_id=index_to_docstore_id,
#     embedding_function=embedding_function,
# )

# # ✅ Create Memory for Storing History
# memory = VectorStoreRetrieverMemory(retriever=vector_db.as_retriever(search_kwargs={"k": 3}))


# def store_history(query: str, google_data: list, response: str):
#     """
#     Store user query, Google API response, and AI-generated response in the VDB.
#     """
#     google_data_str = json.dumps(google_data, indent=2)  # Convert API response to a string
#     document_content = (
#         f"User Query: {query}\n"
#         f"Google API Response:\n{google_data_str}\n"
#         f"AI Response: {response}"
#     )
    
#     document = Document(page_content=document_content)
#     vector_db.add_documents([document])

# def retrieve_history(query: str, top_n: int = 3):
#     """Retrieve the top N most relevant past interactions."""
#     similar_docs = memory.load_memory_variables(query)
#     return "\n\n".join([doc.page_content for doc in similar_docs[:top_n]])


if __name__ == "__main__":
    print("\n🔍 Google Places CLI with GPT-4o Integration")

    while True:

        print("\n\nExample questions ---- ")
        print("📌 What are the closest hotels to times square, and whch has the top rating?")
        print("📌 What is the google places id for the hotel Hotel Riu Plaza Manhattan Times Square?")
        print("📌 Give me the reviews for the hotel hotel Hotel Riu Plaza Manhattan Times Square with places id ChIJNcZg81VYwokRIcQV-JL4Ewc?")
        print("🔴 Type 'exit' to stop.\n\n")

        user_request = input("📝 Enter your query: ")
        if user_request.lower() == "exit":
            print("👋 Exiting...")
            break

        # ✅ Retrieve top 3 relevant past queries from history
        past_history = ""#retrieve_history(user_request, top_n=3)

        # ✅ Construct query with historical context
        user_request_with_history = f"{user_request}\n\n**Relevant User Conversation History for Context**\n{past_history}"

        # ✅ Retrieve data from Google Places API
        api_schema = load_saved_schema()
        google_data = query_google_places(api_schema, user_request_with_history)

        if google_data:
            # ✅ Process response with GPT-4o Mini
            ai_response = process_with_gpt4o(user_request, google_data)

            # ✅ Store query, Google data, and AI response in the vector DB for future retrieval
            #store_history(user_request, google_data, ai_response)

            print("\n🤖 AI Response:\n", ai_response)
        else:
            print("⚠️ No valid data retrieved. Try again.")

# if __name__ == "__main__":
#     print("\n🔍 Google Places CLI with GPT-4o Integration")
#     print("📌 Type a location-based query (e.g., 'Find coffee shops near Times Square')")
#     print("🔴 Type 'exit' to stop.\n")

#     history = []

#     while True:
#         user_request = input("📝 Enter your query: ")
#         if user_request.lower() == "exit":
#             print("👋 Exiting...")
#             break

#         history.append(f"user_request = {user_request}")

#         # ✅ Retrieve data from Google Places API
#         api_schema = load_saved_schema()  # Use saved schema if available


#         user_request = f"user_request = {user_request}\n\n**conversation history - which may include important details for determining query for user request**\n\n{history[-3:]}"

#         google_data = [data for data in query_google_places(api_schema,user_request)]

#         history.append(f"google_data = {google_data}")


#         if google_data:
#             # ✅ Process response with GPT-4o Mini
#             ai_response = process_with_gpt4o(user_request, google_data)

#             history.append(f"google_data = {google_data}")

#             print("\n🤖 AI Response:\n", ai_response)
#         else:
#             print("⚠️ No valid data retrieved. Try again.")
