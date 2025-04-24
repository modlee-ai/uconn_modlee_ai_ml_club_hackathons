# Self-contained example to call the /data_aggregator_agent API endpoint
# Simulates a user sending meeting notes and a schema, and prints the structured output.
import os
import json
import requests
import sqlite3

# Endpoint URL (adjust as needed)
API_URL = "http://127.0.0.1:4000/data_aggregator_agent"

# Optionally load API key from environment
API_KEY = os.getenv("MODLEE_API_KEY", "your-default-api-key")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mock_meeting_data.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "mock_meeting_data_schema.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "structured_output.json")

# Sample natural language input (meeting notes)
SAMPLE_TEXT = """
On April 5th, 2025, a Marketing meeting was held. Alice and Bob attended.
They discussed Q1 campaign performance and made adjustments to the Instagram ad strategy.
Alice was assigned to draft new ad copy by April 10th.
"""

# Create a mock SQLite database with relevant tables
def create_mock_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE meetings (
        meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        meeting_type TEXT,
        topics_covered TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE participants (
        participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE meeting_attendees (
        meeting_id INTEGER,
        participant_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE marketing_adjustments (
        adjustment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        meeting_id INTEGER,
        campaign_or_channel TEXT,
        change_details TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE action_items (
        action_id INTEGER PRIMARY KEY AUTOINCREMENT,
        meeting_id INTEGER,
        assigned_to TEXT,
        task_description TEXT,
        deadline TEXT,
        status TEXT
    )
    """)

    conn.commit()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Database created at:", DB_PATH)
    print("Tables in database:", [t[0] for t in tables])

    conn.close()

def call_data_aggregator_agent_with_db():
    create_mock_db()

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }

    payload = {
        "context": SAMPLE_TEXT,
        "db_path": DB_PATH
    }

    print("Sending request to /data_aggregator_agent with db_path...")
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print("\nStructured Output:")
        response_json = response.json()
        print(json.dumps(response_json, indent=2))
        with open(OUTPUT_PATH, "w") as f:
            json.dump(response_json, f, indent=2)
        print("Structured output saved to:", OUTPUT_PATH)

        insert_structured_data(response_json)

    else:
        print(f"\nRequest failed with status {response.status_code}")
        print("Response body:")
        print(response.text)

def insert_structured_data(response_json):
    queries = response_json.get("input_queries", [])
    if not queries:
        print("No input_queries found in the response.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for query in queries:
        if isinstance(query, list) and len(query) == 2:
            sql, values = query
            try:
                cursor.execute(sql, values)
                print(f"Executed: {sql} with {values}")
            except Exception as e:
                print(f"Failed to execute: {sql} with {values}")
                print("Error:", e)
        else:
            print("Invalid query format:", query)

    conn.commit()
    conn.close()
    print("All input_queries executed and committed.")

if __name__ == "__main__":
    call_data_aggregator_agent_with_db()
    print('done')