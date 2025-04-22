# Modlee Agents API Wiki

## Overview

Welcome to the Modlee Agents API! This API gives you access to a variety of AI-powered tools to help with moderation, content creation, data analysis, and more. Whether you're looking to generate a blog post, moderate user reviews, or query a data source using natural language, this API has you covered.

Each API endpoint is listed below along with:
- What it does (in plain English)
- What you need to send (inputs)
- What you’ll get back (outputs)

---

## API Endpoints (Beginner-Friendly)

### 1. `/moderation`
- **What it does**: Analyzes a product review and classifies it as *positive*, *negative*, or *spam* using both AI and a trained machine learning model.
- **Method**: POST
- **Input**:
  ```json
  {
    "review": "Your review text here"
  }
  ```
- **Output**:
  ```json
  {
    "llmPrediction": "positive",
    "dlPrediction": "positive"
  }
  ```
  You get predictions from both the AI (llm) and the distilled machine learning model.

---

### 2. `/moderation_no_save`
- **What it does**: Same as `/moderation`, but it does **not** save the results anywhere. Useful for testing.
- **Method**: POST
- **Input/Output**: Same as `/moderation`.

---

### 3. `/moderation_details`
- **What it does**: Gives you information about the accuracy of the moderation model and how much training data it was trained on.
- **Method**: GET
- **Input**: None
- **Output**:
  ```json
  {
    "final_accuracy_%": 87.5,
    "num_training_examples": 1500
  }
  ```

---

### 4. `/talk_to_wikipedia`
- **What it does**: Ask a question about anything, and the AI uses Wikipedia as its main data source to answer it.
- **Method**: POST
- **Input**:
  ```json
  {
    "question": "Who invented the internet?"
  }
  ```
- **Output**: A natural language response like:
  ```json
  {
    "answer": "The invention of the internet is attributed to multiple researchers, including Vint Cerf and Bob Kahn..."
  }
  ```

---

### 5. `/data_aggregator_agent`
- **What it does**: Converts messy natural language data (e.g., meeting notes) into structured JSON using a provided database schema.
- **Method**: POST
- **Input**:
  ```json
  {
    "input_text": "Meeting with Alice and Bob on 21st March...",
    "schema": {...}
  }
  ```
- **Output**:
  ```json
  {
    "structured_data": {
      "attendees": ["Alice", "Bob"],
      "date": "2025-03-21"
    }
  }
  ```

---

### 6. `/data_operator_agent_sql`
- **What it does**: Ask a question about your SQL data in natural language, and it builds an SQL query for you.
- **Method**: POST
- **Input**:
  ```json
  {
    "question": "What was the total sales last month?",
    "schema": {...}
  }
  ```
- **Output**:
  ```json
  {
    "query": "SELECT SUM(sales) FROM orders WHERE date BETWEEN ...",
    "params": [],
    "config": {...}
  }
  ```

---

### 7. `/data_operator_agent_rest`
- **What it does**: Converts a natural language question into a REST API call based on your API documentation/schema.
- **Method**: POST
- **Input**:
  ```json
  {
    "question": "Get movies directed by Nolan",
    "schema": {...}
  }
  ```
- **Output**:
  ```json
  {
    "queries": ["https://api.example.com/movies?director=Nolan"],
    "query_configs": [...]
  }
  ```

---

### 8. `/data_operator_agent_rest_schema`
- **What it does**: Takes a raw block of API docs and turns it into a structured API schema the agent can use.
- **Method**: POST
- **Input**:
  ```json
  {
    "api_text": "This endpoint returns weather data for a city..."
  }
  ```
- **Output**:
  ```json
  {
    "schema": {...}
  }
  ```

---

### 9. `/generate_blog`
- **What it does**: Automatically writes a full blog post using your company’s style, strategy, and any content you provide.
- **Method**: POST
- **Input**:
  ```json
  {
    "preferences": {...},
    "strategy": {...},
    "sources": [...]
  }
  ```
- **Output**:
  A polished blog in Markdown format with sections and FAQs.

---

### 10. `/core_docs_agent_blog`
- **What it does**: Same as `/generate_blog`, but focused on technical documentation blogs.
- **Method**: POST
- **Input/Output**: Same as `/generate_blog`.

---

### 11. `/core_docs_agent_social`
- **What it does**: Generates a professional LinkedIn post based on your blog or content.
- **Method**: POST
- **Input**:
  ```json
  {
    "tone": "Conversational",
    "audience": "Startup Founders",
    ...
  }
  ```
- **Output**:
  A short and punchy LinkedIn post ready to publish.

---

### 12. `/core_docs_agent_sales`
- **What it does**: Generates a sales message or email template tailored to your input.
- **Method**: POST
- **Input**:
  ```json
  {
    "product_description": "An AI tool that summarizes calls...",
    ...
  }
  ```
- **Output**:
  A personalized sales pitch in plain text.

---

### 13. `/submit_inquiry`
- **What it does**: Used for collecting information (like email, company name, message) during onboarding.
- **Method**: POST
- **Input**:
  ```json
  {
    "email": "someone@example.com",
    "company": "AwesomeAI",
    "message": "We want to use your platform..."
  }
  ```
- **Output**:
  ```json
  {
    "status": "success"
  }
  ```

---

## How To Use This API (Step-by-Step)

1. **Get Your API Key**: You need this to use the endpoints.
2. **Send a Request**:
   - Use Postman, Curl, or your own app.
   - Add this to your headers:
     ```
     Authorization: Bearer YOUR_API_KEY
     ```
3. **Check the Response**: All responses are in JSON. They’re easy to read and use in your app or project.

---

By following this guide, you’ll be able to easily experiment with and use each endpoint. Have fun, and good luck at the hackathon!