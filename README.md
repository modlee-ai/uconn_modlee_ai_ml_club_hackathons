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
```
## 🚀 Live Demo

You can try the live version of our Streamlit app here:  
👉 [**Launch BumpBridge App**](https://app-checkoutteamstardustuconn-fdcxutekgdbgj5zdntumsy.streamlit.app/)

This interactive demo allows you to generate community-driven maternal health messages using Modlee AI agents. No installation needed — just click and explore!

## 🔐 Environment Setup
Make sure to create a `.env` file in the project directory with your Modlee API key:
```
MODLEE_AGENTS_API_KEY=6406c861d5a67f68fffeadcf6f0cd597
```

## ▶️ How to Run

Follow the steps below to run the project locally:

1. **Setup the environment**  
   Make sure you have Python 3 installed. It's recommended to use a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows use: venv\Scripts\activate
      python agents.py
      python -m streamlit run main.py



## 📸 Demo Screenshots
![image](https://github.com/user-attachments/assets/0d4ad05a-eabd-4b7d-879a-3a1f9bf06fe3)


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
