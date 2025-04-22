import os
import json
import requests
import time

# ✅ Define API Endpoint
API_URL = "https://agentsserver.modlee.ai:5000/core_docs_agent_blog"  # Adjust if needed

# ✅ Get API Key from environment variable
API_KEY = os.getenv("MODLEE_AGENTS_API_KEY")  # Use a default key for local testing if not set

# ✅ Step 1: Define mock user input (simplified version of `user_input_form`)
USER_INPUT_FORM = {
    "sources": [{
        "name": "Sustainability and Corporate Travel",
        "text": "Corporate travel decisions are increasingly driven by sustainability data..."
    }],
    "preferences": {
        "authorNotes": "Greenwashing remains a challenge...",
        "flowNotes": "The blog will open with the rise of ESG in travel...",
        "tone": "insightful, authoritative.",
        "audienceDescription": "corporate travel managers, sustainability officers.",
        "length": "long"
    },
    "strategy": {
        "seo": '"Sustainable corporate travel", "Corporate travel ESG compliance"',
        "companyContext": "Hotels struggle to communicate sustainability efforts...",
        "referenceBlog": "GreenCert Metrics raises funding for ESG hotel tracking..."
    }
}

# ✅ Step 2: Ping the API with a test request
def test_blog_api():
    """Test sending a request to the core_docs_agent_blog endpoint."""

    # Ensure Flask app is running before making a request
    print("⏳ Waiting for Flask API to be available...")
    time.sleep(2)  # Adjust if necessary

    # ✅ Define request headers with API Key
    headers = {
        "X-API-KEY": API_KEY
    }

    # ✅ Make API request
    response = requests.post(API_URL, json=USER_INPUT_FORM, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("\n✅ API Response Received!\n")
        print("Generated Blog Content:\n")
        print(data["response"])  # Print generated blog

    else:
        print(f"❌ API Request Failed: {response.status_code}")
        print("Response:", response.text)


if __name__ == "__main__":
    test_blog_api()
