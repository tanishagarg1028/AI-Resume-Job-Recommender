# 🤖 AI Resume & Job Recommendation System

A Streamlit web app that reads a PDF resume, detects technical skills, and recommends
jobs ranked by how well your skills match each job's requirements.

## Features
- Upload a resume in PDF format and extract its text (PyMuPDF)
- Automatic technical skill detection (whole-word matching + synonyms like ML, NLP)
- Job matching with a match score (%) for every job
- Shows matched skills and missing skills, with learning suggestions
- Filters: location, experience level, minimum match score

## Project Structure
```
project/
├── app.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── skill_extractor.py
└── data/
    └── jobs.csv
```

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech Stack
Python, Streamlit, Pandas, PyMuPDF

## Future Improvements
- Larger job dataset / live job APIs
- Semantic matching (TF-IDF / embeddings)
- Support for DOCX resumes
