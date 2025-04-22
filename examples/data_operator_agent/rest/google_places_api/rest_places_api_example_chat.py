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

if __name__ == "__main__":
    print("\n🔍 Google Places CLI with GPT-4o Integration")

    while True:

        print("\n\n📌 Example questions ---- ")
        print("  1️⃣ What are the closest hotels to times square, and whch has the top rating?")
        print("  2️⃣ What is the google places id for the hotel Hotel Riu Plaza Manhattan Times Square?")
        print("  3️⃣ Give me overview of the hotel and highlight some reviews for the hotel Hotel Riu Plaza Manhattan Times Square (places id ChIJNcZg81VYwokRIcQV-JL4Ewc)")
        print("🔴 Type 'exit' to stop.\n\n")

        user_request = input("📝 Enter your question: ")
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

