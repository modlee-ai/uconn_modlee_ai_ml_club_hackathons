# 🧠 SQL Coach CLI — Powered by Modlee Agents

**SQL Coach CLI** is a command-line tool that transforms natural language questions into executable SQL queries using Modlee's advanced `data_operator_agent_sql`. It's perfect for analysts, developers, or anyone who wants to query databases without writing raw SQL.

---

## 🚀 What This Project Does

- Converts user questions into SQL using a Modlee Agent.
- Runs the SQL against a mock SQLite database.
- Displays query results in the terminal.
- Logs every question, query, result count, and feedback score.
- Provides a schema file for AI-guided query construction.

---

## 🧩 Modlee Agent Used

This project uses:

### ✅ `data_operator_agent_sql`

- **Role**: Converts natural language questions into SQL.
- **How it's used**:
  - Receives your question and the database schema.
  - Returns an SQL query and parameters.
  - Example usage payload:
    ```json
    {
      "user_question": "What are the top 5 products by sales?",
      "schema": { ... }
    }
    ```

---

## 💡 Example Usage
Your question: Which region has the highest total sales?

1. Contacting Modlee agent...
2. SQL Generated: SELECT region, SUM(total_cost) as revenue FROM sales_data GROUP BY region ORDER BY revenue DESC LIMIT 1;
3. Results:
  ('West', 20232.15)
4. Rate this answer from 1–5 🌟:

## 📷 Screenshots
Prompting and Response

![image](https://github.com/user-attachments/assets/5eb61322-625f-451d-af57-e502422508dd)

## 🎥 Demo
If you’d like to see SQL Coach CLI in action, check out the following demo:

Watch the demo video here (https://www.loom.com/share/595defbfabbf4e68ab8a583bada727d8?sid=169d139d-8d44-4312-8a41-d0a836297769)

