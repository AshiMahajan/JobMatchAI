from skill_extractor import extract_skills

sample_text = """
Machine Learning Engineer skilled in Python, TensorFlow,
AWS, Docker, MongoDB and FastAPI.

Worked on NLP and Computer Vision projects using
PyTorch and Hugging Face.
"""

skills = extract_skills(sample_text)

print("Skills Found:")
print(skills)