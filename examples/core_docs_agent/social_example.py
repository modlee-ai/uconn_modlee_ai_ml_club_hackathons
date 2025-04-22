import os
import json
import requests
import time

# ✅ Define API Endpoint
API_URL = "https://agentsserver.modlee.ai:5000/core_docs_agent_social"  # Adjust if needed

# ✅ Get API Key from environment variable
API_KEY = os.getenv("MODLEE_AGENTS_API_KEY")  # Ensure API key is set in environment

# ✅ Step 1: Define mock user input (simplified version of `USER_SOCIAL_INPUT_FORM`)
USER_SOCIAL_INPUT_FORM = {
    "preferences": {
        "audience": "Software developers, QA professionals, and IT managers integrating AI into testing.",
        "flowNotes": "The post highlights AI's role in testing, its challenges, Modlee's solutions, and ends with a call to action.",
        "tone": "Professional yet approachable, with clear explanations and industry terminology.",
        "length": 500
    },
    "strategy": {
        "seo": "AI-driven testing, Agentic AI, Autonomous test generation, AI-powered QA, Software testing innovation.",
        "referencePost": "AI is transforming software testing by enabling proactive, adaptive, and intelligent automation."
    },
    "sources": {
        "text": "AI in testing has evolved from machine learning to generative AI and now Agentic AI, enhancing automation, decision-making, and compliance."
    }
}

# ✅ Step 2: Ping the API with a test request
def test_social_api():
    """Test sending a request to the core_docs_agent_social endpoint."""

    # Ensure Flask app is running before making a request
    print("⏳ Waiting for Flask API to be available...")
    time.sleep(2)  # Adjust if necessary

    # ✅ Define request headers with API Key
    headers = {
        "X-API-KEY": API_KEY
    }

    # ✅ Make API request
    response = requests.post(API_URL, json=USER_SOCIAL_INPUT_FORM, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("\n✅ API Response Received!\n")
        print("Generated Social Media Post:\n")
        print(data["response"])  # Print generated post content

    else:
        print(f"❌ API Request Failed: {response.status_code}")
        print("Response:", response.text)


if __name__ == "__main__":
    test_social_api()
