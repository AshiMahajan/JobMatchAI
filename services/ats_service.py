# services/ats_service.py

from skill_extractor import extract_skills
from ats_engine import calculate_ats_score

from alias_matcher import alias_match
def analyze_resume_vs_jd(
        resume_skills,
        job_description):

    jd_skills = extract_skills(
        job_description
    )

    result = calculate_ats_score(
        resume_skills,
        jd_skills
    )

    return result