from section_parser import extract_sections

sample_resume = """
PROFILE
Machine Learning Engineer

SKILLS
Python
AWS
Docker
TensorFlow

EXPERIENCE
Worked with Python and Linux

PROJECTS
Built an NLP system using Hugging Face

EDUCATION
Bachelor of Engineering
"""

sections = extract_sections(sample_resume)

for name, content in sections.items():
    print(f"\n===== {name.upper()} =====")
    print(content)