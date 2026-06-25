# test_semantic.py

from semantic_matcher import semantic_match

resume_skills = [
    "python",
    "nlp",
    "aws",
    "docker"
]

jd_skills = [
    "natural language processing",
    "python",
    "kubernetes",
    "amazon web services"
]

matched, missing = semantic_match(
    resume_skills,
    jd_skills
)

print("\nMATCHED")
print("=" * 50)

for item in matched:
    print(item)

print("\nMISSING")
print("=" * 50)

print(missing)