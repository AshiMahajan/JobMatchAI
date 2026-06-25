# test_resume_pipeline.py

from parser import extract_text_from_pdf
from resume_analyzer import analyze_resume

text = extract_text_from_pdf("MLE.pdf")

result = analyze_resume(text)

for section, skills in result.items():

    print("\n" + "=" * 50)
    print(section.upper())
    print("=" * 50)

    print(skills)