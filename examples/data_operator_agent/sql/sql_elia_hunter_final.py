import os
import json
import random
import sqlite3
import requests
import time
from datetime import datetime

# ==== CONFIG ====
API_URL = "https://agentsserver.modlee.ai:5000/data_operator_agent_sql"
API_KEY = "f3d8415e3c347c01a45e7743ff7f0f87"

# ==== PATHS ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mock_database.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "mock_schema.json")
LOG_PATH = os.path.join(BASE_DIR, "query_log.json")

# ==== DATABASE SETUP ====
def create_mock_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS sales_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        product TEXT,
        quantity INTEGER,
        price FLOAT,
        total_cost FLOAT,
        purchase_date TEXT,
        payment_method TEXT,
        region TEXT,
        discount_applied FLOAT,
        feedback_score INTEGER
    )""")

    products = ["Laptop", "Phone", "Tablet", "Monitor", "Headphones"]
    payment_methods = ["Credit Card", "PayPal", "Bitcoin"]
    regions = ["North", "South", "East", "West"]

    for _ in range(100):
        quantity = random.randint(1, 5)
        price = round(random.uniform(50, 2000), 2)
        total_cost = round(quantity * price, 2)
        discount = round(random.uniform(0, 0.2) * total_cost, 2)
        cursor.execute("""INSERT INTO sales_data (
            customer_name, product, quantity, price, total_cost,
            purchase_date, payment_method, region, discount_applied, feedback_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            f"Customer_{random.randint(1, 1000)}",
            random.choice(products),
            quantity,
            price,
            total_cost,
            f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d} {random.randint(10, 23):02d}:00:00",
            random.choice(payment_methods),
            random.choice(regions),
            discount,
            random.randint(1, 5)
        ))

    conn.commit()
    conn.close()
    print("✅ Mock database created!")

def create_mock_schema():
    # Use your existing JSON schema creation code
    with open(SCHEMA_PATH, "r") as f:
        schema = json.load(f)
    return schema

# ==== LOGGING ====
def log_session_entry(entry):
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=4)

# ==== SQL EXPLAINER (GPT-style) ====
def explain_sql(query):
    return f"🤖 This SQL query is attempting to: **{query[:100]}...**\n\n(Explanation not yet AI-generated — you could integrate GPT-4 for that.)"

# ==== MAIN INTERFACE ====
def test_sql_api():
    print("\n🧠 Welcome to SQL Coach CLI!")
    with open(SCHEMA_PATH, "r") as f:
        schema = json.load(f)

    headers = {"X-API-KEY": API_KEY}

    while True:
        print("\n--- Example questions ---")
        print("1. What is the total sales amount for each product?")
        print("2. Which region has the highest total sales revenue?")
        print("3. What are the top 5 highest-value transactions?")
        print("Type 'exit' to quit.\n")

        user_question = input("🔎 Your question: ").strip()
        if user_question.lower() == "exit":
            print("👋 Goodbye!")
            break

        payload = {
            "user_question": user_question,
            "schema": schema
        }

        print("📡 Contacting Modlee agent...")
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code != 200:
            print(f"❌ API Error ({response.status_code}): {response.text}")
            continue

        data = response.json()
        query = data.get("query")
        params = data.get("params", [])

        print("\n✅ SQL Generated:\n", query)
        print("📥 Params:", params)
        print("💡 Explanation:", explain_sql(query))

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            print("\n📊 Results:")
            for row in results:
                print("  ", row)

        except Exception as e:
            print("❌ Error executing SQL:", e)
            results = []

        finally:
            cursor.close()
            conn.close()

        # Ask for feedback
        feedback = input("\n🌟 Rate this answer from 1–5 (or press Enter to skip): ").strip()
        try:
            rating = int(feedback)
            assert 1 <= rating <= 5
        except:
            rating = None

        # Log session
        log_session_entry({
            "timestamp": datetime.now().isoformat(),
            "question": user_question,
            "query": query,
            "params": params,
            "results_count": len(results),
            "feedback": rating
        })

        print("📝 Session logged!\n")

# ==== RUN ====
if __name__ == "__main__":
    create_mock_database()
    create_mock_schema()
    test_sql_api()
