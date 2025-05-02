# agents.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("MODLEE_AGENTS_API_KEY")

def call_modlee(endpoint, payload):
    headers = {"X-API-KEY": API_KEY}
    url = f"https://agentsserver.modlee.ai:5000{endpoint}"

    print(f"\n🔄 Sending request to: {url}")
    print("📜 Payload:", payload)

    try:
        response = requests.post(url, json=payload, headers=headers)

        print("📬 Status Code:", response.status_code)
        print("📦 Response Body:", response.text)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"{response.status_code} — {response.text}"}

    except Exception as e:
        return {"error": "❌ Exception occurred", "details": str(e)}

if __name__ == "__main__":
    if API_KEY:
        print("🔐 API Key Loaded:", API_KEY[:6], "...")
    else:
        print("❌ API Key NOT FOUND")
