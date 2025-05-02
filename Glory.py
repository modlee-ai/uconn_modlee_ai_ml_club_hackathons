import streamlit as st
import requests
import os
import json

API_KEY = "327c4567ec5bf1cf928f421fae12bada"
BASE_URL = "https://agentsserver.modlee.ai:5000"
HEADERS = {"X-API-KEY": API_KEY}

st.set_page_config(page_title="Modlee Multi-Agent Tool", layout="centered")
st.title("✨ Modlee Magic Deck")
st.markdown("""This tool allows you to interact with Modlee's working endpoints:
- Blog Generator
- Social Media Post Generator
- SQL Query Generator
""")

option = st.selectbox("Choose a tool to use:", [
    "📝 Blog Generator",
    "📣 Social Media Post Generator",
    "🧮 SQL Query Generator"
])

# ------------------------- BLOG GENERATOR -------------------------
if option == "📝 Blog Generator":
    st.header("📝 Generate a Technical Blog")
    blog_text = st.text_area("Provide background text for the blog:", height=150)
    audience = st.text_input("Target Audience:", value="Tech leads and product managers")
    tone = st.selectbox("Tone:", ["Insightful", "Authoritative", "Conversational"], index=0)
    length = st.selectbox("Length:", ["short", "medium", "long"], index=2)

    if st.button("Generate Blog"):
        payload = {
            "sources": [{"name": "Blog Context", "text": blog_text}],
            "preferences": {
                "authorNotes": "",
                "flowNotes": "",
                "tone": tone,
                "audienceDescription": audience,
                "length": length
            },
            "strategy": {
                "seo": "AI blog, generative AI, machine learning blog",
                "companyContext": "",
                "referenceBlog": ""
            }
        }
        st.info("Sending request to Modlee Blog Agent...")
        res = requests.post(f"{BASE_URL}/core_docs_agent_blog", json=payload, headers=HEADERS, timeout=300)
        if res.status_code == 200:
            result = res.json().get("response")
            st.success("✅ Blog Generated!")
            st.markdown(result)
            st.download_button("📥 Download Blog", result, file_name="blog.txt")
            st.write(f"✍️ **Word Count:** {len(result.split())} words")
        else:
            st.error(f"❌ Error {res.status_code}")
            st.text(res.text)

# ------------------------- SOCIAL MEDIA POST -------------------------
elif option == "📣 Social Media Post Generator":
    st.header("📣 Generate a LinkedIn-style Post")
    post_text = st.text_area("Provide the main content:", height=150)
    audience = st.text_input("Target Audience:", value="Startup Founders")
    tone = st.selectbox("Tone:", ["Professional", "Friendly", "Witty"], index=0)
    length = st.slider("Length (approx characters):", 100, 500, 300)

    if st.button("Generate Post"):
        payload = {
            "preferences": {
                "audience": audience,
                "flowNotes": "Summarize insights and add a call to action.",
                "tone": tone,
                "length": length
            },
            "strategy": {
                "seo": "generative AI, productivity tools",
                "referencePost": "Explore how AI is changing the way we communicate."
            },
            "sources": {
                "text": post_text
            }
        }
        st.info("Sending request to Modlee Social Agent...")
        res = requests.post(f"{BASE_URL}/core_docs_agent_social", json=payload, headers=HEADERS)
        if res.status_code == 200:
            result = res.json().get("response")
            st.success("✅ Social Post Generated!")
            st.markdown(result)
            st.download_button("📥 Download Post", result, file_name="social_post.txt")
            st.write(f"✍️ **Word Count:** {len(result.split())} words")
        else:
            st.error(f"❌ Error {res.status_code}")
            st.text(res.text)

# ------------------------- SQL GENERATOR -------------------------
elif option == "🧮 SQL Query Generator":
    st.header("🧮 Generate SQL from Natural Language")
    schema = st.text_area("📜 Enter your schema (JSON format):", height=200)
    user_question = st.text_input("📝 What do you want to query?")

    if st.button("Generate SQL Query"):
        try:
            schema_json = json.loads(schema)
            payload = {
                "user_question": user_question,
                "schema": schema_json
            }
            st.info("Sending request to Modlee SQL Agent...")
            res = requests.post(f"{BASE_URL}/data_operator_agent_sql", json=payload, headers=HEADERS)
            if res.status_code == 200:
                result = res.json()
                st.success("✅ SQL Query Generated!")
                st.code(result.get("query"), language="sql")
            else:
                st.error(f"❌ Error {res.status_code}")
                st.text(res.text)
        except Exception as e:
            st.error("Invalid JSON schema.")
            st.text(str(e))
