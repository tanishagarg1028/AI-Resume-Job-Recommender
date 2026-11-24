import fitz  # PyMuPDF
import pandas as pd
import streamlit as st

from src.skill_extractor import extract_skills, normalize_skill

# ---------------- Page configuration ----------------
st.set_page_config(
    page_title="AI Resume & Job Recommendation System",
    page_icon="📄",
    layout="wide",
)

st.title("🤖 AI Resume & Job Recommendation System")
st.write(
    "Upload your resume and get AI-powered job recommendations "
    "based on your skills and experience."
)
st.divider()

# ---------------- Resume upload ----------------
st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])

skills = []  # always defined, even before a resume is uploaded

if uploaded_file is not None:
    try:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        resume_text = "".join(page.get_text() for page in pdf_document)
    except Exception as e:
        resume_text = ""
        st.error(f"Could not read this PDF: {e}")

    if resume_text.strip():
        st.success("Resume uploaded successfully! ✅")

        st.subheader("📄 Extracted Resume Text")
        st.text_area("Resume Content", resume_text, height=300)

        skills = extract_skills(resume_text)

        st.subheader("🔎 Skills Detected")
        if skills:
            st.success(f"Found {len(skills)} technical skills!")
            st.write("  ".join(f"`{s}`" for s in skills))
        else:
            st.warning("No technical skills were detected in the resume.")
    elif uploaded_file is not None:
        st.warning(
            "No text could be extracted from this PDF. "
            "Please upload a text-based PDF (not a scanned image)."
        )

# ---------------- Job recommendations ----------------
st.divider()
st.header("💼 Recommended Jobs")

if uploaded_file is None:
    st.info("Upload your resume above to see job recommendations.")
elif not skills:
    st.warning("No skills detected. Cannot recommend jobs.")
else:
    try:
        jobs = pd.read_csv("data/jobs.csv")
    except Exception as e:
        st.error(f"Error loading job data: {e}")
        st.stop()

    # ----- Filters -----
    st.subheader("🔍 Filter Jobs")
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_location = st.selectbox(
            "📍 Location", ["All Locations"] + sorted(jobs["Location"].unique().tolist())
        )
    with col2:
        selected_experience = st.selectbox(
            "💼 Experience Level",
            ["All Experience Levels"] + sorted(jobs["Experience"].unique().tolist()),
        )
    with col3:
        min_score = st.slider("📊 Minimum Match Score (%)", 0, 100, 0, step=5)

    filtered_jobs = jobs.copy()
    if selected_location != "All Locations":
        filtered_jobs = filtered_jobs[filtered_jobs["Location"] == selected_location]
    if selected_experience != "All Experience Levels":
        filtered_jobs = filtered_jobs[filtered_jobs["Experience"] == selected_experience]

    # ----- Matching -----
    user_skills = {normalize_skill(s).lower() for s in skills}
    recommendations = []

    for _, job in filtered_jobs.iterrows():
        required = []
        for s in str(job["Required Skills"]).split(","):
            if s.strip():
                required.append(normalize_skill(s))

        matched = [s for s in required if s.lower() in user_skills]
        missing = [s for s in required if s.lower() not in user_skills]
        score = (len(matched) / len(required) * 100) if required else 0

        if score >= min_score:
            recommendations.append({
                "Job Title": job["Job Title"],
                "Company": job["Company"],
                "Location": job["Location"],
                "Experience": job["Experience"],
                "Job Description": job["Job Description"],
                "Match Score": round(score, 2),
                "Matched Skills": matched,
                "Missing Skills": missing,
            })

    recommendations.sort(key=lambda x: x["Match Score"], reverse=True)

    # ----- Display -----
    if not recommendations:
        st.info("No jobs match your filters. Try lowering the minimum match score.")
    else:
        st.write(f"Showing **{len(recommendations)}** job(s), best match first.")

    for job in recommendations:
        st.subheader(f"🔹 {job['Job Title']}")
        st.write(f"**Company:** {job['Company']}")
        st.write(f"📍 **Location:** {job['Location']}")
        st.write(f"💼 **Experience:** {job['Experience']}")
        st.write(f"📝 **Job Description:** {job['Job Description']}")

        st.write(f"**📊 Match Score:** {job['Match Score']}%")
        st.progress(int(job["Match Score"]))

        if job["Matched Skills"]:
            st.success("✅ Matched Skills: " + ", ".join(job["Matched Skills"]))
        else:
            st.info("✅ Matched Skills: None")

        if job["Missing Skills"]:
            st.warning("❌ Missing Skills: " + ", ".join(job["Missing Skills"]))
            st.write(
                "💡 **Recommendation:** Learn the missing skills above "
                "to improve your chances for this job."
            )
        else:
            st.success("🎉 You have all the required skills for this job!")

        st.divider()
