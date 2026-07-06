from services.skill_service import SkillService

from ats_engine import calculate_ats_score


skill_service = SkillService()


def analyze_resume_vs_jd(
    resume_skills: list[str],
    job_description: str
):

    jd_skills = skill_service.extract_names(
        job_description
    )

    ats_result = calculate_ats_score(
        resume_skills,
        jd_skills
    )

    return ats_result