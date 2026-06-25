from ats_engine import calculate_ats_score

resume_skills = [
    "python",
    "aws",
    "docker"
]

jd_skills = [
    "python",
    "amazon web services",
    "docker"
]

result = calculate_ats_score(
    resume_skills,
    jd_skills
)

print(result)