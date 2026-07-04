from parser import extract_text_from_pdf

from resume_analyzer import analyze_resume

from domains.resume import ResumeProfile

from services.skill_service import SkillService


skill_service = SkillService()


def extract_resume_skills(
        pdf_path: str
) -> ResumeProfile:

    resume_text = extract_text_from_pdf(
        pdf_path
    )

    resume_sections = analyze_resume(
        resume_text
    )

    resume_skills = skill_service.extract_names(
        resume_text
    )

    return ResumeProfile(

        resume_text=resume_text,

        skills=resume_skills,

        sections=resume_sections
    )