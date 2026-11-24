import re

# Master list of technical skills
SKILLS = [
    "Python", "Java", "C++", "C", "R", "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "HTML", "CSS", "JavaScript", "TypeScript", "React", "Node.js", "Django", "Flask",
    "Streamlit", "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "Data Science", "Data Analysis", "Data Visualization", "Pandas", "NumPy",
    "Scikit-learn", "TensorFlow", "Keras", "PyTorch", "NLP", "Computer Vision",
    "Git", "GitHub", "Docker", "AWS", "Azure", "Excel", "Power BI", "Tableau",
    "Linux", "REST API", "Matplotlib", "Seaborn",
]

# Alternate spellings -> canonical skill name
ALIASES = {
    "natural language processing": "NLP",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "dl": "Deep Learning",
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikitlearn": "Scikit-learn",
    "nodejs": "Node.js",
    "node js": "Node.js",
    "js": "JavaScript",
    "postgres": "PostgreSQL",
    "powerbi": "Power BI",
    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "rest apis": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",
    "cv": "Computer Vision",
}

# Very short names must match with exact case to avoid false hits
CASE_SENSITIVE = {"C", "R", "ML", "AI", "DL", "CV", "JS"}


def _pattern(term, case_sensitive=False):
    """Whole-word regex that also works for C++, Node.js, etc."""
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.compile(r"(?<![A-Za-z0-9+#])" + re.escape(term) + r"(?![A-Za-z0-9+#])", flags)


def normalize_skill(skill):
    """Return the canonical form of a skill name (used for job matching too)."""
    s = skill.strip()
    key = s.lower()
    if key in ALIASES:
        return ALIASES[key]
    for known in SKILLS:
        if known.lower() == key:
            return known
    return s


def extract_skills(resume_text):
    """Extract technical skills from resume text (no duplicates, whole-word match)."""
    found = []

    for skill in SKILLS:
        if _pattern(skill, skill in CASE_SENSITIVE).search(resume_text):
            found.append(skill)

    for alias, canonical in ALIASES.items():
        if canonical in found:
            continue
        cs = alias.upper() in CASE_SENSITIVE
        term = alias.upper() if cs else alias
        if _pattern(term, cs).search(resume_text):
            found.append(canonical)

    return found
