from resume_analyzer import analyze_resume

sample_resume = """
SKILLS
Python
AWS
Docker

EXPERIENCE
Worked with Kubernetes and Linux

PROJECTS
Built a RAG chatbot using LangChain and FAISS
"""

result = analyze_resume(sample_resume)

for section, skills in result.items():

    print(f"\n{section.upper()}")

    print(skills)