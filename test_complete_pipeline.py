# test_complete_pipeline.py

from parser import extract_text_from_pdf
from resume_analyzer import analyze_resume
from skill_extractor import extract_skills
from ats_engine import calculate_ats_score


# ==========================================================
# Resume PDF
# ==========================================================

resume_text = extract_text_from_pdf(
    "MLE.pdf"
)


# ==========================================================
# Extract skills by section
# ==========================================================

resume_sections = analyze_resume(
    resume_text
)


# ==========================================================
# Merge all resume skills into one list
# ==========================================================

resume_skills = []

for section_skills in resume_sections.values():

    resume_skills.extend(
        section_skills
    )


resume_skills = list(
    set(resume_skills)
)


# ==========================================================
# Sample JD
# ==========================================================

jd_text = """
Machine Learning Engineer

Required Skills:

Python
AWS
Docker
TensorFlow
Kubernetes
MongoDB
FastAPI
Natural Language Processing
"""


# ==========================================================
# Extract JD skills
# ==========================================================

jd_skills = extract_skills(
    jd_text
)


# ==========================================================
# Calculate ATS score
# ==========================================================

result = calculate_ats_score(
    resume_skills,
    jd_skills
)


# ==========================================================
# Output
# ==========================================================

print("\n" + "=" * 60)

print("ATS SCORE")

print("=" * 60)


print(
    f"\nScore: {result.score}%"
)


print(
    f"Match Level: {result.match_level}"
)


# ==========================================================
# Exact Matches
# ==========================================================

print("\nEXACT MATCHES")

print("-" * 60)


for skill in result.exact_matches:

    print(skill)


# ==========================================================
# Alias Matches
# ==========================================================

print("\nALIAS MATCHES")

print("-" * 60)


for match in result.alias_matches:

    print(
        f"{match.resume_skill} "
        f"↔ "
        f"{match.jd_skill}"
    )


# ==========================================================
# Semantic Matches
# ==========================================================

print("\nSEMANTIC MATCHES")

print("-" * 60)


for match in result.semantic_matches:

    print(
        f"{match.resume_skill} "
        f"↔ "
        f"{match.jd_skill} "
        f"({match.similarity})"
    )


# ==========================================================
# Missing Skills
# ==========================================================

print("\nMISSING SKILLS")

print("-" * 60)


for skill in result.missing_skills:

    print(skill)


# ==========================================================
# Recommendations
# ==========================================================

print("\nRECOMMENDATIONS")

print("-" * 60)


for recommendation in result.recommendations:

    print(recommendation)