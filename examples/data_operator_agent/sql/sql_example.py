import os
import json
import random
import sqlite3
import requests
import time

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mock_database.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "mock_schema.json")
API_URL = "https://agentsserver.modlee.ai:5000/data_operator_agent_sql"  # Adjust if using a different host/port

# ✅ Get API Key from environment variable
API_KEY = os.getenv("MODLEE_AGENTS_API_KEY")  # Use a default key for local testing if not set

# ✅ Step 1: Create a mock SQLite database
def create_mock_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a sample table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_data (
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
        )
    """)

    # Generate 100 random rows
    products = ["Laptop", "Phone", "Tablet", "Monitor", "Headphones"]
    payment_methods = ["Credit Card", "PayPal", "Bitcoin"]
    regions = ["North", "South", "East", "West"]

    for _ in range(100):
        quantity = random.randint(1, 5)
        price = round(random.uniform(50, 2000), 2)
        total_cost = round(quantity * price, 2)
        discount = round(random.uniform(0, 0.2) * total_cost, 2)
        cursor.execute("""
            INSERT INTO sales_data (customer_name, product, quantity, price, total_cost, purchase_date, payment_method, region, discount_applied, feedback_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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


# ✅ Step 2: Create a mock schema JSON file
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
                        "applicable_data_types": [
                            "INTEGER",
                            "FLOAT",
                            "TEXT"
                        ]
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
    
    print("✅ Mock schema file created!")


# # ✅ Step 3: Ping the API with a test query
# def test_sql_api():
#     # Ensure Flask app is running before making a request
#     print("⏳ Waiting for Flask API to be available...")
#     time.sleep(2)  # Adjust this if needed

#     user_question = "What is the total sales amount for each product?"

#     print(f"user_question = {user_question}")

#     with open(SCHEMA_PATH, "r") as f:
#         schema = json.load(f)

#     # ✅ Define request headers with API Key
#     headers = {
#         "X-API-KEY": API_KEY
#     }

#     payload = {
#         "user_question": user_question,
#         "schema": schema
#     }

#     response = requests.post(API_URL, json=payload, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#         print("\n✅ API Response Received!\n")
#         print("Generated SQL Query:\n", data["query"])
#         print("Query Parameters:\n", data["params"])

#         # ✅ Step 4: Execute query on the SQLite database
#         conn = sqlite3.connect(DB_PATH)
#         cursor = conn.cursor()

#         try:
#             cursor.execute(data["query"], data["params"])
#             results = cursor.fetchall()

#             print("\nQuery Results:\n")
#             for row in results:
#                 print(row)

#         except Exception as e:
#             print(f"❌ Error executing query: {e}")

#         finally:
#             cursor.close()
#             conn.close()

#     else:
#         print(f"❌ API Request Failed: {response.status_code}")
#         print("Response:", response.text)

# ✅ Step 3: CLI for SQL API interaction
def test_sql_api():
    print("\n🔍 SQL API CLI - Ask questions about the database!")

    with open(SCHEMA_PATH, "r") as f:
        schema = json.load(f)

    headers = {"X-API-KEY": API_KEY}

    while True:

        print("\n\n📌 Example questions ----")
        print("  1️⃣ What is the total sales amount for each product?")
        print("  2️⃣ Which region has the highest total sales revenue?")
        print("  3️⃣ What are the top 5 highest-value transactions, and which customers made them?")
        print("  4️⃣ How many purchases were made using each payment method?")
        print("  5️⃣ What is the average feedback score for each product category?")
        print("🔴 Type 'exit' to stop.\n\n")

        user_question = input("📝 Enter your question: ")
        if user_question.lower() == "exit":
            print("👋 Exiting...")
            break

        payload = {"user_question": user_question, "schema": schema}
        
        print("⏳ Sending request to API...")
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ API Response Received!")
            print("Generated SQL Query:\n", data["query"])
            print("Query Parameters:\n", data["params"])

            # ✅ Execute query on the SQLite database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            try:
                cursor.execute(data["query"], data["params"])
                results = cursor.fetchall()

                print("\n📊 Query Results:\n")
                for row in results:
                    print(row)

            except Exception as e:
                print(f"❌ Error executing query: {e}")

            finally:
                cursor.close()
                conn.close()

        else:
            print(f"❌ API Request Failed: {response.status_code}")
            print("Response:", response.text)


if __name__ == "__main__":
    create_mock_database()
    create_mock_schema()
    test_sql_api()
