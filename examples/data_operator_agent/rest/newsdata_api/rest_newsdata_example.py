import os
import json
import requests
import time
from typing import Dict, List, Any

# Define API endpoints
API_BASE_URL = "https://agentsserver.modlee.ai:5000"
SCHEMA_ENDPOINT = f"{API_BASE_URL}/data_operator_agent_rest_schema"
QUERY_ENDPOINT = f"{API_BASE_URL}/data_operator_agent_rest"

# NewsData.io API configuration
NEWSDATA_API_KEY = os.getenv("NEWDATA_IO_API_KEY")
NEWSDATA_BASE_URL = "https://newsdata.io/api/1/news"

# Get Modlee API Key from environment variable
MODLEE_AGENTS_API_KEY = os.getenv("MODLEE_AGENTS_API_KEY")

def read_api_docs() -> str:
    """Read API documentation from a local text file."""
    try:
        with open("/Users/nnigam/modlee/modlee_agents_server/examples/data_operator_agent/rest/newsdata_api/newsdata_api_docs.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"❌ API documentation file 'newsdata_api_docs.txt' not found.")
        return None

def generate_api_schema(api_text: str) -> Dict[str, Any]:
    """Send the API documentation to generate a structured schema."""
    headers = {"X-API-KEY": MODLEE_AGENTS_API_KEY}
    payload = {"api_text": api_text}

    print("\n⏳ Sending API documentation to generate schema...")
    try:
        response = requests.post(SCHEMA_ENDPOINT, json=payload, headers=headers, timeout=180)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ API Schema Received!")

            # Save schema locally
            with open("newsdata_api_schema.json", "w", encoding="utf-8") as schema_file:
                json.dump(data["api_schema"], schema_file, indent=4)
                print(f"📁 Schema saved to newsdata_api_schema.json")

            return data["api_schema"]
        else:
            print(f"❌ API Schema Request Failed: {response.status_code}")
            print("Response:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during schema generation: {e}")
        return None

def query_newsdata_api(api_schema: Dict[str, Any], user_request: str) -> List[Dict[str, Any]]:
    """Send a user question and retrieve relevant data using the structured schema."""
    headers = {"X-API-KEY": MODLEE_AGENTS_API_KEY}
    
    payload = {
        "api_schema": api_schema,
        "user_request": user_request
    }

    print("\n⏳ Sending query request to NewsData.io...")
    try:
        response = requests.post(QUERY_ENDPOINT, json=payload, headers=headers, timeout=300)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Modlee Agents Query Response Received!")
            
            # Extract and print API configuration
            if "query_configs" in data:
                print("\n📜 API Config Used:\n", json.dumps(data["query_configs"], indent=4))

            news_response_data = []

            # Execute generated API queries
            for query in data["queries"]:
                # Handle both string URLs and dictionary queries
                if isinstance(query, dict):
                    url = query.get("url")
                    method = query.get("method", "GET")
                else:
                    url = query
                    method = "GET"

                if not url:
                    print("❌ Invalid query format received")
                    continue

                # Remove page parameter from initial request
                if "page=" in url:
                    url = url.split("page=")[0].rstrip("&")

                # Add API key to the URL
                separator = "&" if "?" in url else "?"
                url_with_key = f"{url}{separator}apikey={NEWSDATA_API_KEY}"

                print(f"\n⏳ Executing NewsData.io API call: {url_with_key}")
                try:
                    if method.upper() == "GET":
                        api_response = requests.get(url_with_key, timeout=30)
                    else:
                        print(f"❌ Unsupported HTTP method: {method}")
                        continue

                    api_response_data = api_response.json()
                    print("\n🔹 NewsData.io API Response Data:", json.dumps(api_response_data, indent=4))

                    # Check for error response
                    if api_response_data.get("status") == "error":
                        print(f"❌ NewsData.io API Error: {api_response_data.get('results', {}).get('message')}")
                        continue

                    # Ensure API response contains expected data
                    assert api_response.status_code == 200
                    assert isinstance(api_response_data, dict)

                    news_response_data.append(api_response_data)
                except requests.exceptions.RequestException as e:
                    print(f"❌ NewsData.io API Request Failed: {e}")

            return news_response_data
        else:
            print(f"❌ Modlee Query Request Failed: {response.status_code}")
            print("Response:", response.text)
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during query execution: {e}")
        return []

def load_saved_schema() -> Dict[str, Any]:
    """Load the previously saved API schema if it exists."""
    if os.path.exists("newsdata_api_schema.json"):
        print(f"\n📂 Loading saved schema from newsdata_api_schema.json...")
        with open("newsdata_api_schema.json", "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return None

def main():
    # Step 1: Read API documentation from file
    api_text = read_api_docs()
    
    if api_text:
        # Step 2: Generate and save the API schema
        api_schema = load_saved_schema()
        if not api_schema:
            api_schema = generate_api_schema(api_text)

        if api_schema:
            while True:
                print("\n📰 NewsData.io API Example")
                print("1. Search for news articles")
                print("2. Exit")
                
                choice = input("\nEnter your choice (1-2): ")
                
                if choice == "1":
                    user_request = input("Enter your news search query: ")
                    news_response_data = query_newsdata_api(api_schema, user_request)
                    
                    # Save results to a file
                    if news_response_data:
                        output_file = f"newsdata_results_{int(time.time())}.json"
                        with open(output_file, "w", encoding="utf-8") as f:
                            json.dump(news_response_data, f, indent=4)
                        print(f"\n📁 Results saved to {output_file}")
                
                elif choice == "2":
                    print("👋 Exiting...")
                    break
                
                else:
                    print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 