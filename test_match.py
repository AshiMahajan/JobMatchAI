from skill_extractor import extract_skills
from scorer import calculate_score

resume_text = """
Machine Learning Engineer skilled in Python,
AWS, Docker, TensorFlow and MongoDB.
"""

jd_text = """
Looking for candidates with Python,
AWS, Docker, Kubernetes, FastAPI
and TensorFlow.
"""

resume_skills = extract_skills(resume_text)
jd_skills = extract_skills(jd_text)

result = calculate_score(
    resume_skills,
    jd_skills
)

print("\nATS Score:")
print(result["score"])

print("\nMatched Skills:")
print(result["matched_skills"])

print("\nMissing Skills:")
print(result["missing_skills"])