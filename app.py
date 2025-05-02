import streamlit as st
import requests

st.set_page_config(page_title="Smart Job Assistant")
st.title("💼 Smart Job Application Assistant")

import fitz  # PyMuPDF
import docx

st.subheader("📄 Upload your Resume (.pdf or .docx)")
uploaded_resume = st.file_uploader("Choose your resume file", type=["pdf", "docx"])

def extract_text(file):
    if file.name.endswith(".pdf"):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return "\n".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

resume_text = ""
if uploaded_resume:
    resume_text = extract_text(uploaded_resume)
    st.success("✅ Resume uploaded and processed successfully!")


job_desc = st.text_area("Paste the Job Description", height=200)

API_KEY = "5e303d0da6b499b9d59614709caa64f1"
BLOG_URL = "https://agentsserver.modlee.ai:5000/core_docs_agent_blog"
SOCIAL_URL = "https://agentsserver.modlee.ai:5000/core_docs_agent_social"
HEADERS = {"X-API-KEY": API_KEY}

def build_payload(jd, type):
    return {
        "sources": [{"name": "Job Description", "text": jd}],
        "preferences": {
            "authorNotes": f"Generate a {type} message. Keep it short and professional.",
            "tone": "Professional" if type == "cover letter" else "Friendly",
            "audienceDescription": "Recruiter"
        },
        "strategy": {
            "companyContext": "Resume provided separately"
        }
    }

def call_modlee(url, payload):
    try:
        r = requests.post(url, json=payload, headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("response", "").strip()
        else:
            return f"Error {r.status_code}: {r.text}"
    except Exception as e:
        return str(e)

if st.button("Generate"):
    if not resume or not job_desc:
        st.warning("Please paste both Resume and Job Description.")
    else:
        with st.spinner("Generating..."):
            cover = call_modlee(BLOG_URL, build_payload(job_desc, "cover letter"))
            msg = call_modlee(SOCIAL_URL, build_payload(job_desc, "linkedin message"))

        st.subheader("📄 Cover Letter")
        st.markdown(cover)

        st.subheader("💬 LinkedIn Message")
        st.markdown(msg)
