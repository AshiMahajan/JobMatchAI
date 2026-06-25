# services/resume_service.py

from parser import extract_text_from_pdf
from resume_analyzer import analyze_resume


def extract_resume_skills(pdf_path):

    resume_text = extract_text_from_pdf(
        pdf_path
    )

    resume_sections = analyze_resume(
        resume_text
    )

    resume_skills = []

    for section_skills in resume_sections.values():

        resume_skills.extend(
            section_skills
        )

    resume_skills = list(
        set(resume_skills)
    )

    return {
        "resume_text": resume_text,
        "resume_skills": resume_skills,
        "sections": resume_sections
    }