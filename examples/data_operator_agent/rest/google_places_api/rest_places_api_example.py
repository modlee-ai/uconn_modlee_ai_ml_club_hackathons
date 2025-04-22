import os
import json
import requests

# ✅ Define API Endpoints
API_BASE_URL = "https://agentsserver.modlee.ai:5000"
SCHEMA_ENDPOINT = f"{API_BASE_URL}/data_operator_agent_rest_schema"
QUERY_ENDPOINT = f"{API_BASE_URL}/data_operator_agent_rest"

# ✅ Get API Key from environment variables
MODLEE_AGENTS_API_KEY = os.getenv("MODLEE_AGENTS_API_KEY")  # Modlee Agent API Key
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Google Places API Key

# ✅ Define file paths
API_DOCS_PATH = "places_api_docs.txt"  # Local API documentation file
SCHEMA_OUTPUT_PATH = "places_api_schema.json"  # Output path for the generated schema

def read_api_docs():
    """Read API documentation from a local text file."""
    try:
        with open(API_DOCS_PATH, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"❌ API documentation file '{API_DOCS_PATH}' not found.")
        return None

def generate_api_schema(api_text):
    """Send API documentation to generate a structured schema and save it."""
    headers = {"X-API-KEY": MODLEE_AGENTS_API_KEY}
    payload = {"api_text": api_text}

    # print("\n⏳ Sending API documentation to generate schema...")
    response = requests.post(SCHEMA_ENDPOINT, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # print("\n✅ API Schema Received!")

        # ✅ Save schema locally
        with open(SCHEMA_OUTPUT_PATH, "w", encoding="utf-8") as schema_file:
            json.dump(data["api_schema"], schema_file, indent=4)
            # print(f"📁 Schema saved to {SCHEMA_OUTPUT_PATH}")

        return data["api_schema"]  # Return structured schema
    else:
        # print(f"❌ API Schema Request Failed: {response.status_code}")
        # print("Response:", response.text)
        return None

def query_google_places(api_schema,user_request):
    """Send a user request and retrieve data using the structured schema."""
    modlee_headers = {"X-API-KEY": MODLEE_AGENTS_API_KEY}
    
    payload = {
        "api_schema": api_schema,
        "user_request": user_request
    }

    print("\n⏳ Sending query request to Google Places API...")
    response = requests.post(QUERY_ENDPOINT, json=payload, headers=modlee_headers)

    google_response_data = []

    if response.status_code == 200:
        data = response.json()
        print("\n✅ Modlee Agents Query Response Received!")
        # print(json.dumps(data, indent=4))

        # ✅ Extract and print API configuration
        if "query_configs" in data:
            query_configs = data["query_configs"]
            print("\n📜 API Config Used:\n", json.dumps(query_configs, indent=4))

        google_headers = {
            "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
            "Content-Type": "application/json"
        }

        # ✅ Execute generated API queries
        for i,query_info in enumerate(data["queries"]):
            query_config = query_configs[i]
            method = query_info.get("method", "GET").upper()
            query_url = query_info.get("url")

            # if method == "GET":
            #     query_url_with_key = f"{query_url}?key={GOOGLE_PLACES_API_KEY}"
            #     print(f"\n⏳ Executing Google Places API call: {query_url_with_key}")
            #     try:
            #         api_response = requests.get(query_url_with_key)
            #         api_response_data = api_response.json()
            #         print("\n🔹 Google Places API Response Data:", json.dumps(api_response_data, indent=4))

            #         google_response_data.append(api_response_data)
            #     except requests.exceptions.RequestException as e:
            #         print(f"❌ Google Places API GET Request Failed: {e}")
            if method == "GET":

                # Define Place ID

                # print(query_url)

                query_url = query_url.split('?')[0]#"ChIJjXMc60FZwokR1UaXTvtlLks"

                # Define the API URL
                query_url = f"{query_url}?key={GOOGLE_PLACES_API_KEY}"

                # Headers (fieldMask should be here)
                # google_headers = {
                #     "Content-Type": "application/json",
                #     "X-Goog-FieldMask": "displayName,id,formattedAddress,rating,reviews,currentOpeningHours"
                # }

                google_headers = {
                    "Content-Type": "application/json",
                }

                for url_param in query_config["url_params"]:
                    key,value = url_param.split("=")
                    google_headers[key] = value

                print(f"\n⏳ Executing Google Places API GET request: {query_url}")

                try:
                    api_response = requests.get(query_url, headers=google_headers)
                    
                    # Check if response is empty
                    if api_response.status_code != 200:
                        print(f"❌ API Request Failed: {api_response.status_code} - {api_response.text}")
                    else:
                        api_response_data = api_response.json()
                        print("\n🔹 Google Places API Response Data:", json.dumps(api_response_data, indent=4))

                        google_response_data.append(api_response_data)

                except requests.exceptions.RequestException as e:
                    print(f"❌ Google Places API Request Failed: {e}")

            elif method == "POST":

                for key,value in query_config['headers'].items():
                    google_headers[key]=value

                json_body = query_info.get("json_body", {})
                print(f"\n⏳ Executing Google Places API POST request: {query_url}")
                print(f"🔹 Request Body: {json.dumps(json_body, indent=4)}")
                
                try:
                    api_response = requests.post(query_url, headers=google_headers, json=json_body)
                    api_response_data = api_response.json()
                    print("\n🔹 Google Places API Response Data:", json.dumps(api_response_data, indent=4))

                    google_response_data.append(api_response_data)
                except requests.exceptions.RequestException as e:
                    print(f"❌ Google Places API POST Request Failed: {e}")

    else:
        print(f"❌ Modlee Query Request Failed: {response.status_code}")
        print("Response:", response.text)

    return google_response_data

def load_saved_schema():
    """Load the previously saved API schema if it exists."""
    if os.path.exists(SCHEMA_OUTPUT_PATH):
        print(f"\n📂 Loading saved schema from {SCHEMA_OUTPUT_PATH}...")
        with open(SCHEMA_OUTPUT_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return None

if __name__ == "__main__":
    # Step 1: Read API documentation from file
    api_text = read_api_docs()
    
    if api_text:
        # Step 2: Generate and save the API schema
        api_schema = load_saved_schema()  # Use saved schema if available
        if not api_schema:
            api_schema = generate_api_schema(api_text)

        if api_schema:
            # Step 3: Query Google Places API using the generated schema
            # ✅ Define a sample user request
            user_request = "Find restaurants near Times Square, New York."

            google_places_response_data = query_google_places(api_schema,user_request)
            # print(google_places_response_data)
