# NL-to-SQL for Mock Healthcare Claims Database

This project demonstrates a Natural Language to SQL (NL-to-SQL) workflow using a mock healthcare claims database. It allows users to ask questions in natural language, which are then translated into SQL queries to retrieve insights from the data.

## Features

* **Mock Database:** A SQLite database (`mock_healthcare.db`) is created with sample healthcare claims data, including patient demographics, diagnoses, procedures, and financial information.
* **JSON Schema:** A JSON file (`schema_healthcare.json`) defines the database schema, providing a structured representation of the data.
* **NL-to-SQL API:** The core functionality is provided by an API that takes natural language questions and generates corresponding SQL queries.
* **CLI Interface:** A command-line interface allows users to interact with the system by typing questions.
* **SQL Execution:** Generated SQL queries are executed against the mock database, and results are displayed to the user.

## How it Works

1. **Database and Schema Creation:** The project initializes by creating the mock database and schema files.
2. **API Interaction:** The CLI prompts the user to enter a question in natural language.
3. **SQL Generation:** The question is sent to the NL-to-SQL API, which processes it and generates an SQL query along with any necessary parameters.
4. **Query Execution:** The generated SQL query is executed against the mock database using SQLite.
5. **Results Display:** The results of the query are presented to the user in a readable format.

## Usage

1. **Clone the Repository:**

2. **Install Dependencies:**

3. 3. **Run the CLI:**

4. **Enter Questions:**
   Type your questions in natural language and press Enter.
   For example:
   * "What is the average claim amount?"
   * "How many claims are there for diagnosis code 'E11.9'?"
   * "Which region has the highest total paid amount?"
5. **View Results:**
   The generated SQL query and the results from the database will be displayed.

## Customization

* **Database Schema:** Modify the `schema_healthcare.json` file to adapt the system to a different database schema.
* **NL-to-SQL API:** You can replace the API endpoint and key in the `main.py` file if you are using a different NL-to-SQL service.
* **CLI Interface:** Customize the prompts and output formatting in the `main.py` file to suit your preferences.


## Note

This project is a demonstration of an NL-to-SQL workflow. The accuracy and capabilities of the system depend on the quality of the NL-to-SQL API used. For real-world applications, consider using a more robust and production-ready NL-to-SQL solution.
