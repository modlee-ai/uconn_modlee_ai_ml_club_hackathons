import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
API_KEY = os.getenv("MODLEE_AGENTS_API_KEY")

# App Config
st.set_page_config(
    page_title="🤱 BumpBridge – Awareness Post Generator",
    page_icon="🤰",
    layout="centered"
)

# Header with image, title, and subtitle (clean version, no extra emojis/images)
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #d6336c;'>🤱 BumpBridge – Awareness Post Generator</h1>
        <h4 style='margin-top: -10px; color: #555;'>Empowering maternal health with community-driven messaging</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
st.header("📝 Enter Your Message Details")

# Form inputs
persona = st.selectbox("Select a Voice (Persona)", [
    "Young Mother", "Health Worker", "Community Leader", "NGO Volunteer", "Nurse"
])

source_info = st.text_area(
    "Post Source Info",
    placeholder="What is this post about? Include facts, statistics, stories, etc."
)

tone = st.selectbox("Post Tone", [
    "Supportive", "Inspirational", "Informative", "Urgent"
])

audience_options = [
    "Young mothers", "Health workers", "Fathers", "Family support groups", "NGO volunteers"
]
audience = st.selectbox("Choose Your Audience", options=audience_options)

cta_options = [
    "Join our community to support maternal health",
    "Share this message to raise awareness",
    "Donate to local maternal clinics",
    "Volunteer to support expecting mothers",
    "Follow us for more stories and resources"
]
cta = st.selectbox("🔗 Add Call-to-Action", options=cta_options)

# Generate button
if st.button("Generate Post"):
    if not API_KEY or not source_info:
        st.error("❌ API Key or Post Source Info missing!")
    else:
        payload = {
            "preferences": {
                "audience": audience,
                "flowNotes": f"Voice: {persona}. Call-to-action: {cta}.",
                "tone": tone,
                "length": 500
            },
            "strategy": {
                "seo": "maternal health, pregnancy awareness, BumpBridge",
                "referencePost": "Stories that empower maternal care"
            },
            "sources": {
                "text": source_info
            }
        }

        headers = {"X-API-KEY": API_KEY}
        response = requests.post("https://agentsserver.modlee.ai:5000/core_docs_agent_social", json=payload, headers=headers)

        if response.status_code == 200:
            generated_post = response.json().get("response", "No content returned.")
            st.success("✅ Generated Post:")
            st.write(generated_post)

            # Provide a download link
            st.download_button(
                label="📄 Download Post as Text",
                data=generated_post,
                file_name="bumpbridge_post.txt",
                mime="text/plain"
            )
        else:
            st.error(f"❌ Failed to generate: {response.status_code}")
            st.text(response.text)


