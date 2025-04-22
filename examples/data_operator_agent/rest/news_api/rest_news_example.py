import os
import json
import requests

# ✅ Define API Endpoints
API_BASE_URL = "https://agentsserver.modlee.ai:5000"
SCHEMA_ENDPOINT = f"{API_BASE_URL}/data_operator_agent_rest_schema"
QUERY_ENDPOINT = f"{API_BASE_URL}/data_operator_agent_rest"

# ✅ Get API Key from environment variable
MODLEE_AGENTS_API_KEY = os.getenv("MODLEE_AGENTS_API_KEY") # Use default key for local testing
NEWS_API_KEY = os.getenv("NEWS_API_KEY") # Use default key for local testing

# ✅ Define file paths
API_DOCS_PATH = "news_api_docs.txt"  # Path to local API documentation file
SCHEMA_OUTPUT_PATH = "news_api_schema.json"  # Path to save the generated schema


def read_api_docs():
    """Read API documentation from a local text file."""
    try:
        with open(API_DOCS_PATH, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"❌ API documentation file '{API_DOCS_PATH}' not found.")
        return None


def generate_api_schema(api_text):
    """Send the API documentation to generate a structured schema and save it."""
    headers = {"X-API-KEY": MODLEE_AGENTS_API_KEY}
    payload = {"api_text": api_text}

    print("\n⏳ Sending API documentation to generate schema...")
    response = requests.post(SCHEMA_ENDPOINT, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("\n✅ API Schema Received!")

        # ✅ Save schema locally
        with open(SCHEMA_OUTPUT_PATH, "w", encoding="utf-8") as schema_file:
            json.dump(data["api_schema"], schema_file, indent=4)
            print(f"📁 Schema saved to {SCHEMA_OUTPUT_PATH}")

        return data["api_schema"]  # Return the structured schema
    else:
        print(f"❌ API Schema Request Failed: {response.status_code}")
        print("Response:", response.text)
        return None


def query_news_api(api_schema):
    """Send a user question and retrieve relevant data using the structured schema."""
    modlee_headers = {"X-API-KEY": MODLEE_AGENTS_API_KEY}
    
    # ✅ Define a sample user request
    user_request = "What are the news articles about trump in march 2025?"

    payload = {
        "api_schema": api_schema,
        "user_request": user_request
    }

    print("\n⏳ Sending query request to NewsAPI...")
    response = requests.post(QUERY_ENDPOINT, json=payload, headers=modlee_headers)

    if response.status_code == 200:

        data = response.json()
        print("\n✅ Modlee Agents Query Response Received!")
        print(json.dumps(data, indent=4))

        # ✅ Extract and print API configuration
        if "query_configs" in data:
            print("\n📜 API Config Used:\n", json.dumps(data["query_configs"], indent=4))

        news_headers = {"X-API-KEY": NEWS_API_KEY}
        news_response_data = []

        # ✅ Execute generated API queries
        for query_url in data["queries"]:
            print(f"\n⏳ Executing News API call: {query_url}")
            try:
                api_response = requests.get(query_url, headers=news_headers)
                api_response_data = api_response.json()
                print("\n🔹 News API Response Data:", json.dumps(api_response_data, indent=4))

                # ✅ Ensure API response contains expected data
                assert api_response.status_code == 200
                assert isinstance(api_response_data, dict) or isinstance(api_response_data, list)

                news_response_data.append(api_response_data)
            except requests.exceptions.RequestException as e:
                print(f"❌ News API Request Failed: {e}")

    else:
        print(f"❌ Modlee Query Request Failed: {response.status_code}")
        print("Response:", response.text)

    return news_response_data


import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def can_scrape_url(article_url):
    """Check if we are legally allowed to scrape the article's website."""
    parsed_url = urlparse(article_url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            robots_text = response.text.lower()
            # Check if "Disallow: /" exists, meaning scraping is blocked
            return not any(line.strip().startswith("disallow: /") for line in robots_text.split("\n"))
    except requests.RequestException:
        return False  # Assume scraping is not allowed if the check fails

    return True  # Assume scraping is allowed if no robots.txt exists

def scrape_full_text(article_url):
    """Scrape the full article text if allowed."""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            return "\n".join(p.get_text() for p in paragraphs)
    except requests.RequestException:
        return None

    return None

def enhance_news_with_full_text(news_response_data, output_file="news_with_full_text.json"):
    """
    Enhances news data by scraping full text from article URLs (if legally allowed).
    
    Args:
        news_response_data (list): List of news API responses.
        output_file (str): File path to save the enhanced news data.
        
    Returns:
        list: Updated news data with full text included.
    """
    for news_data in news_response_data:
        if isinstance(news_data, dict) and "articles" in news_data:
            for article in news_data["articles"]:
                article_url = article.get("url")
                if article_url and can_scrape_url(article_url):
                    print(f"🔍 Scraping: {article_url}")
                    full_text = scrape_full_text(article_url)
                    if full_text:
                        article["full_text"] = full_text
                        print(f"✅ Full text added for: {article['title']}")
                    else:
                        print(f"⚠️ Failed to scrape: {article_url}")
                else:
                    print(f"🚫 Scraping not allowed for: {article_url}")

    # ✅ Save the updated news data with full text
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(news_response_data, file, indent=4)
        print(f"\n📁 News data with full text saved to {output_file}")

    return news_response_data



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
        # api_schema = generate_api_schema(api_text)
        api_schema = load_saved_schema()#with edits

        if api_schema:
            # Step 3: Query NewsAPI using the generated schema
            news_response_data = query_news_api(api_schema)
            enhance_news_with_full_text(news_response_data)
