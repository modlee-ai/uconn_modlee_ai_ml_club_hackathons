import streamlit as st
import requests
import fitz   # PyMuPDF
import docx   # python‑docx

# ─── Page setup ─────────────────────────────────────────
st.set_page_config(page_title="Smart Job Assistant")
st.title("💼 Smart Job Application Assistant")

# ─── Resume upload ──────────────────────────────────────
st.subheader("📄 Upload your Resume (.pdf or .docx)")
uploaded_resume = st.file_uploader("Choose your resume file", type=["pdf","docx"])

def extract_text(file):
    if file.name.endswith(".pdf"):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return "\n".join(p.get_text() for p in doc)
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

resume_text = ""
if uploaded_resume:
    resume_text = extract_text(uploaded_resume)
    st.success("✅ Resume uploaded and processed successfully!")

# ─── Job description ────────────────────────────────────
job_desc = st.text_area("📌 Paste the Job Description", height=200)

# ─── Modlee API setup ───────────────────────────────────
API_KEY       = "5e303d0da6b499b9d59614709caa64f1"
BLOG_URL      = "https://agentsserver.modlee.ai:5000/core_docs_agent_blog"
SOCIAL_URL    = "https://agentsserver.modlee.ai:5000/core_docs_agent_social"
HEADERS       = {"X-API-KEY": API_KEY}

# ─── Payload builders ───────────────────────────────────
def build_blog_payload(resume, jd):
    return {
        "sources": [{
            "name": "Job Description",
            "text": jd
        }],
        "preferences": {
            "authorNotes":    "",            # you can put custom notes here
            "flowNotes":      "",            # or leave empty
            "tone":           "Professional",
            "audienceDescription": "Hiring Manager",
            "length":         "short"        # short / medium / long
        },
        "strategy": {
            "seo":                "",       # e.g. "Data Analyst resume"
            "companyContext":     "",       # e.g. "Tech startup"
            "referenceBlog":      ""        # any example blog URL/text
        }
    }

def build_social_payload(resume, jd):
    return {
        "sources": [{
            "name": "Job Description",
            "text": jd
        }],
        "preferences": {
            "authorNotes":        "",
            "flowNotes":          "",
            "tone":               "Friendly",
            "audienceDescription": "Recruiter",
            "length":             "short"
        },
        "strategy": {
            "seo":                "",
            "companyContext":     "",
            "referenceBlog":      ""
        }
    }

# ─── API caller ─────────────────────────────────────────
def call_modlee(url, payload):
    r = requests.post(url, json=payload, headers=HEADERS)
    if r.status_code == 200:
        return r.json().get("response","").strip()
    else:
        return f"❌ Error {r.status_code}: {r.text}"

# ─── Generate button ───────────────────────────────────
if st.button("🚀 Generate Cover Letter & LinkedIn Message"):
    if not resume_text or not job_desc:
        st.warning("⚠️ Please upload a resume and paste the job description.")
    else:
        with st.spinner("🔧 Generating..."):
            blog_payload   = build_blog_payload(resume_text, job_desc)
            social_payload = build_social_payload(resume_text, job_desc)

            cover_letter = call_modlee(BLOG_URL, blog_payload)
            linkedin_msg = call_modlee(SOCIAL_URL, social_payload)

        st.subheader("📄 Cover Letter")
        st.markdown(cover_letter)

        st.subheader("💬 LinkedIn Message")
        st.markdown(linkedin_msg)
