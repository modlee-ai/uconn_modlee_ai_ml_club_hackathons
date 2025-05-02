# Smart Job Application Assistant

A simple Streamlit web application that automates the creation of professional cover letters using the Modlee Agent API. Users can upload their resume (PDF or DOCX) and paste a job description. The app then generates a tailored cover letter.

## 🔧 Features

- **Resume Upload**: Accepts PDF or Word documents and extracts text automatically.
- **Job Description Input**: Allows pasting any job description.
- **Cover Letter Generation**: Uses Modlee’s `core_docs_agent_blog` endpoint to generate a cover letter.
- **Markdown Cleanup**: Strips out any headings or markdown syntax so the user sees only the final letter.

## 🧠 Modlee Agents Used

- **core_docs_agent_blog**: Generates the cover letter based on provided job description and payload parameters.

### Payload Details
```json
{
  "sources": [{ "name": "Job Description", "text": "<job_description_text>" }],
       "preferences": {
            "authorNotes":        "Focus on projects and skills,Return only the plain‑text letter body. Do not include any headings, markdown syntax, or comments.",            # e.g. "Focus on projects and skills"
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
```

## 🚀 Setup & Run Instructions

1. **Clone this repository**
   ```bash
   git clone https://github.com/<your-username>/Team-ONE.git
   cd Team-ONE
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your Modlee API key**
   - Open `app.py` and replace `PASTE_YOUR_MODLEE_API_KEY_HERE` with your actual API key.
4. **Run the app locally**
   ```bash
   streamlit run app.py
   ```
5. **Or deploy** on Streamlit Cloud by connecting this repo and specifying `app.py` as the main file.

## 🔗 Demo

The live app is available at: https://team-one-nnvf5ywosxrthjkb9ikxbz.streamlit.app/

## 📸 Screenshots
Screenshot of the interface
![Screenshot 2025-05-02 150252](https://github.com/user-attachments/assets/a292b5cd-681d-46bc-8227-7cfb5fe51e97)

Screenshot of the Output
![Screenshot 2025-05-02 151415](https://github.com/user-attachments/assets/a73b7dc9-e5ca-4e41-8f68-23880196aada)



---

*Developed for the UConn Modlee AI/ML Club Hackathon.*

