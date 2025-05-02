# 🤱 BumpBridge – Awareness Post Generator

## 🧠 Overview
**BumpBridge** is a maternal health awareness tool built using **Modlee's Agentic AI API**. It empowers users to generate targeted awareness posts using a voice/persona of their choice. These posts are tailored to different tones, audiences, and call-to-actions, ensuring impactful messaging for healthcare and community support around pregnancy and motherhood.

## 🚀 Features
- **Persona-driven voice selection** (e.g. Nurse, Young Mother, NGO Worker)
- **User-customized tone and target audience**
- **Call-to-action dropdown suggestions**
- **Post source input** for story or factual inspiration
- **One-click generation of awareness posts** via Modlee’s `core_docs_agent_social` endpoint
- **Downloadable output** for easy sharing

## 🧩 Modlee Agent Used
We used the following Modlee Agent:

**`/core_docs_agent_social`** – This Modlee agent allows generation of short social posts based on structured user intent such as tone, topic, audience, and style preferences.

## 🛠️ Project Structure
```
bumpbridge-AI/
│
├── main.py             # Streamlit frontend (user input and API integration)
├── agents.py           # Agent request handler with dotenv config
├── .env                # Secure storage of API key (not committed)
└── bumpbridge_post.txt # Sample generated post output (optional)
```

## 🔐 Environment Setup
Make sure to create a `.env` file in the project directory with your Modlee API key:
```
MODLEE_AGENTS_API_KEY=6406c861d5a67f68fffeadcf6f0cd597
```

## ▶️ How to Run
1. Clone the project repo:
```bash
git clone https://github.com/YOUR_USERNAME/uconn_modlee_ai_ml_club_hackathon.git
```

2. Navigate to your project folder and install requirements:
```bash
cd bumpbridge-AI
pip install -r requirements.txt  # (Create one with streamlit, dotenv, requests)
```

3. Run the app:
```bash
streamlit run main.py
```

## 📸 Demo Screenshots
- App layout with header and emoji branding
- Persona dropdown selection and tone selector
- Generated awareness post and download option

## 📋 Sample Use Case
> "A health worker wants to write an inspirational post on how fathers can support expecting mothers. They select the persona 'Nurse', tone 'Supportive', and CTA 'Volunteer to support expecting mothers'. With one click, the post is generated using the Modlee agent."

## ✅ Submission Details
This project is submitted as part of the **UConn Modlee AI/ML Club Hackathon**.

### Team Name
**Team_Stardust**

### Contributors
- Jasvitha Vatsavaya (💡 Idea, UI Design, Modlee Integration, Testing)

### Git Branch for Submission
```bash
github-checkout_Team_Stardust
```

## 🙌 Acknowledgments
Thanks to Modlee and UConn AI/ML Club for organizing this hackathon and providing powerful APIs to bring our ideas to life.

---
Feel free to contact us for demo videos or additional explanation.
