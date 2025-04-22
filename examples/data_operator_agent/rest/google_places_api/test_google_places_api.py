import requests
import json
import os

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Google Places API Key

# Define Place ID
place_id = "ChIJjXMc60FZwokR1UaXTvtlLks"

# Define the API URL
query_url = f"https://places.googleapis.com/v1/places/{place_id}?key={GOOGLE_PLACES_API_KEY}"

# Headers (fieldMask should be here)
google_headers = {
    "Content-Type": "application/json",
    "X-Goog-FieldMask": "displayName,id,formattedAddress,rating,reviews,currentOpeningHours"
}

print(f"\n⏳ Executing Google Places API GET request: {query_url}")

try:
    api_response = requests.get(query_url, headers=google_headers)
    
    # Check if response is empty
    if api_response.status_code != 200:
        print(f"❌ API Request Failed: {api_response.status_code} - {api_response.text}")
    else:
        api_response_data = api_response.json()
        print("\n🔹 Google Places API Response Data:", json.dumps(api_response_data, indent=4))

except requests.exceptions.RequestException as e:
    print(f"❌ Google Places API Request Failed: {e}")
