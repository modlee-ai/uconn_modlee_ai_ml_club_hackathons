import streamlit as st
import requests
import fitz   # PyMuPDF for PDF reading
import docx   # python‑docx for Word reading

# ─── Helper: Strip out markdown headings/comments ───────────────────────────
def strip_markdown(text: str) -> str:
    lines = text.splitlines()
    return "\n".join(
        line for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    )

# ─── Page setup ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Cover Letter Generator")
st.title("✉️ Smart Cover Letter Generator")

# ─── Resume upload ─────────────────────────────────────────────────────────
st.subheader("📄 Upload your Resume (.pdf or .docx)")
uploaded_resume = st.file_uploader("Choose your resume file", type=["pdf","docx"])

def extract_text(file) -> str:
    if file.name.endswith(".pdf"):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)
    elif file.name.endswith(".docx"):
        document = docx.Document(file)
        return "\n".join(p.text for p in document.paragraphs)
    return ""

resume_text = ""
if uploaded_resume:
    resume_text = extract_text(uploaded_resume)
    st.success("✅ Resume uploaded and processed successfully!")

# ─── Job description ───────────────────────────────────────────────────────
st.subheader("📝 Paste the Job Description")
job_desc = st.text_area("Enter the job description here", height=200)

# ─── Modlee API setup ──────────────────────────────────────────────────────
API_KEY  = "5e303d0da6b499b9d59614709caa64f1"
BLOG_URL = "https://agentsserver.modlee.ai:5000/core_docs_agent_blog"
HEADERS  = {"X-API-KEY": API_KEY}

# ─── Build payload for cover letter ────────────────────────────────────────
def build_cover_payload(jd: str) -> dict:
    return {
        "sources": [{
            "name": "Job Description",
            "text": jd
        }],
         "preferences": {
            "authorNotes":        "Remove all FAQs, Focus on projects and skills,Return only the plain‑text letter body. Do not include any headings, markdown syntax, or comments.",            # e.g. "Focus on projects and skills"
            "flowNotes":          "start with address, date, 'Dear hiring manager', intro, skills, work experience, projects",            # e.g. "Start with greeting, then match resume"
            "tone":               "Professional",
            "audienceDescription":"Hiring Manager",
            "length":             "short"        # short (~100w), medium (~200w), long
        },
        "strategy": {
            "seo":               "Data Analyst, SQL, Python",            # optional keywords
            "companyContext":    "",            # optional context
            "referenceBlog":     "https://i.pinimg.com/474x/6d/92/0f/6d920f941d41b817c4dc51979f08209e.jpg"             # optional example URL/text
        }
    }

# ─── Call Modlee API ────────────────────────────────────────────────────────
def call_modlee(url: str, payload: dict) -> str:
    try:
        r = requests.post(url, json=payload, headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("response","").strip()
        else:
            return f"❌ Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"❌ Exception: {e}"

# ─── Generate Cover Letter ─────────────────────────────────────────────────
if st.button("🚀 Generate Cover Letter"):
    if not resume_text or not job_desc:
        st.warning("⚠️ Please upload your resume AND paste the job description.")
    else:
        with st.spinner("✍️ Generating your cover letter..."):
            payload   = build_cover_payload(job_desc)
            cover_raw = call_modlee(BLOG_URL, payload)
            cover     = strip_markdown(cover_raw)

        st.subheader("📄 Your Generated Cover Letter")
        st.markdown(cover)
