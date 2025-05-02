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
            "authorNotes":    "Focus on work experiences and projects",            # you can put custom notes here
            "flowNotes":      "Start with address, followed by 'Dear Hiring manager,', followed by intro, then skills, then work expeience, Please do not add FAQs, don't add the title, remove the comments, use less than 200 words ",            # or leave empty
            "tone":           "Professional",
            "audienceDescription": "Hiring Manager",
            "length":         "short, less that 200 words, 3 paragraphs"        # short / medium / long
        },
        "strategy": {
            "seo":                "Data analyst resume, SQL, Projects, Coursework, Python",       # e.g. "Data Analyst resume"
            "companyContext":     "Tech startup, fintech company, Top consulting firms",       # e.g. "Tech startup"
            "referenceBlog":      "https://images.ctfassets.net/wp1lcwdav1p1/VrC968tP78Ae91jsbzcAt/8d7dce61a3fdf10c317bff9da0236134/Sample_Data_Analyst_Cover_Letter.png?w=1500&q=60"        # any example blog URL/text
        }
    }

def build_social_payload(resume, jd):
    return {
        "sources": [{
            "name": "Job Description",
            "text": jd
        }],
        "preferences": {
            "audience": "Data analysts, business analysts, Hiring manager",
            "flowNotes": "start with Hello,followed by intro, The text highlights looking for internships",
            "tone": "Professional yet approachable, with clear explanations and industry terminology.",
            "length": 100
        },
        "strategy": {
            "seo":                "",
            "companyContext":     "networking outreach",
            "referencePost":      "https://simplestic.com/email-example-for-networking/"
        }
    }
 
    "sources": {
        "text": "AI in testing has evolved from machine learning to generative AI and now Agentic AI, enhancing automation, decision-making, and compliance."
    

# ─── API caller ─────────────────────────────────────────
def call_modlee(url, payload):
    r = requests.post(url, json=payload, headers=HEADERS)
    if r.status_code == 200:
        return r.json().get("response","").strip()
    else:
        return f"❌ Error {r.status_code}: {r.text}"


# ─── Generate button with LinkedIn debug ─────────────────────────────
if st.button("🚀 Generate Cover Letter & LinkedIn Message"):
    if not resume_text or not job_desc:
        st.warning("⚠️ Please upload a resume and paste the job description.")
    else:
        with st.spinner("🔧 Generating..."):
            # Build payloads
            blog_payload   = build_blog_payload(resume_text, job_desc)
            social_payload = build_social_payload(resume_text, job_desc)

            # Call Cover Letter API
            cover_letter = call_modlee(BLOG_URL, blog_payload)

            # ─── Debug block for LinkedIn ───────────────────────
            with st.expander("🔍 Debug LinkedIn API call"):
                st.write("**Payload sent to social agent:**")
                st.json(social_payload)

                resp = requests.post(SOCIAL_URL, json=social_payload, headers=HEADERS)
                st.write("**Status code:**", resp.status_code)
                try:
                    st.write("**Full response JSON:**")
                    st.json(resp.json())
                except Exception:
                    st.write("**Raw response text:**", resp.text)
            # ──────────────────────────────────────────────────────

            # Use the debugged response (fall back on error message)
            if resp.status_code == 200:
                linkedin_msg = resp.json().get("response", "").strip()
            else:
                linkedin_msg = f"❌ LinkedIn API error {resp.status_code}. See debug above."

        # ─── Show outputs ───────────────────────────────────
        st.subheader("📄 Cover Letter")
        st.markdown(cover_letter)

        st.subheader("💬 LinkedIn Message")
        st.markdown(linkedin_msg)

