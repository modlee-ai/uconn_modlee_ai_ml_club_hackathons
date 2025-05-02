import os
import json
import random
import sqlite3
import requests
from datetime import datetime

# ==== CONFIG ====
API_URL = "https://agentsserver.modlee.ai:5000/data_operator_agent_sql"
API_KEY = "f3d8415e3c347c01a45e7743ff7f0f87"  # 🔐 Explicit API key as requested

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

# ==== SCHEMA CREATION ====
def create_mock_schema():
    schema = {
        "database": {
            "name": "mock_database.db",
            "human_context": {
                "description": "A simple database for tracking sales transactions."
            }
        },
        "tables": {
            "sales_data": {
                "human_context": {
                    "description": "Stores sales transactions including product details, payment methods, and customer regions."
                },
                "columns": {
                    "id": {"data_type": "INTEGER", "is_primary_key": True},
                    "customer_name": {"data_type": "TEXT"},
                    "product": {"data_type": "TEXT"},
                    "quantity": {"data_type": "INTEGER"},
                    "price": {"data_type": "FLOAT"},
                    "total_cost": {"data_type": "FLOAT"},
                    "purchase_date": {"data_type": "TEXT"},
                    "payment_method": {"data_type": "TEXT"},
                    "region": {"data_type": "TEXT"},
                    "discount_applied": {"data_type": "FLOAT"},
                    "feedback_score": {"data_type": "INTEGER"}
                },
                "aggregations": {
                    "allowed_functions": ["SUM", "AVG", "COUNT", "MIN", "MAX"],
                    "applicable_data_types": {
                        "SUM": ["FLOAT", "INTEGER"],
                        "AVG": ["FLOAT", "INTEGER"],
                        "COUNT": ["ANY"],
                        "MIN": ["FLOAT", "INTEGER"],
                        "MAX": ["FLOAT", "INTEGER"]
                    }
                },
                "filters": {
                    "allowed_filter_types": ["exact", "range"],
                    "applicable_data_types": {
                        "exact": ["TEXT", "INTEGER", "FLOAT"],
                        "range": ["INTEGER", "FLOAT", "TEXT"]
                    }
                },
                "group_by_options": {
                    "human_context": {
                        "description": "AI Agent Guidance: Defines which columns should be grouped.",
                        "qa_section": {
                            "Which columns make the most sense to group by in typical reports?": "Grouping by `product`, `payment_method`, and `region` provides valuable insights.",
                            "Are there key categorical fields that drive analytical insights?": "Yes, `product` and `region` often segment sales effectively.",
                            "Should grouping be avoided for any specific columns?": "Yes, unique identifiers like `id` should not be grouped."
                        }
                    },
                    "programmatically_obtained": {
                        "allowed": True,
                        "recommended_columns": []
                    }
                },
                "order_by_options": {
                    "human_context": {
                        "description": "AI Agent Guidance: Defines which columns can be sorted.",
                        "qa_section": {
                            "Which fields do users typically sort by in reports?": "Users often sort by `total_cost`, `quantity`, and `purchase_date`.",
                            "Are there specific sorting orders that provide better insights?": "Sorting `total_cost` DESC highlights the highest revenue sales.",
                            "Should sorting be avoided on any fields?": "Yes, `description` and `customer_name` are not useful for sorting."
                        }
                    },
                    "programmatically_obtained": {
                        "allowed": True,
                        "applicable_data_types": ["INTEGER", "FLOAT", "TEXT"]
                    }
                },
                "pagination": {
                    "human_context": {
                        "description": "AI Agent Guidance: Defines pagination behavior.",
                        "qa_section": {
                            "What is a reasonable default result limit for performance?": "A default limit of 10 ensures fast query performance.",
                            "Is deep pagination (high offset values) required?": "Deep pagination is rarely needed beyond the top 100 results.",
                            "Should limits be different for different types of queries?": "Yes, large summary reports may need higher limits."
                        }
                    },
                    "programmatically_obtained": {
                        "default_limit": 10,
                        "max_limit": 1000,
                        "supports_offset": True
                    }
                }
            }
        }
    }

    with open(SCHEMA_PATH, "w") as f:
        json.dump(schema, f, indent=4)

    print("📄 Schema file created!")

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

# ==== SQL EXPLAINER (Placeholder) ====
def explain_sql(query):
    return f"🤖 This SQL query is attempting to: **{query[:100]}...**"

# ==== MAIN INTERFACE ====
def test_sql_api():
    print("\n🧠 Welcome to SQL Coach CLI!")
    if not os.path.exists(SCHEMA_PATH):
        create_mock_schema()
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

        payload = {"user_question": user_question, "schema": schema}

        print("📡 Contacting Modlee agent...")
        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ API error: {e}")
            continue

        data = response.json()
        query = data.get("query")
        params = data.get("params", [])

        if not query:
            print("⚠️ No query returned. Try a simpler question.")
            continue

        print("\n✅ SQL Generated:\n", query)
        print("📥 Params:", params)
        print("💡 Explanation:", explain_sql(query))

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

            print("\n📊 Results:")
            if results:
                for row in results:
                    print("  ", row)
            else:
                print("  (No results returned.)")

        except Exception as e:
            print("❌ Error executing SQL:", e)
            results = []

        finally:
            cursor.close()
            conn.close()

        feedback = input("\n🌟 Rate this answer from 1–5 (or press Enter to skip): ").strip()
        try:
            rating = int(feedback)
            assert 1 <= rating <= 5
        except:
            rating = None

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
    if not os.path.exists(DB_PATH):
        create_mock_database()
    test_sql_api()
    
