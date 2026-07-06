from services.skill_service import SkillService

from ats_engine import calculate_ats_score


skill_service = SkillService()


def analyze_market(
    resume_skills: list[str],
    job_descriptions: list[str]
):

    analyses = []

    for index, jd_text in enumerate(
        job_descriptions,
        start=1
    ):

        jd_skills = skill_service.extract_names(
            jd_text
        )

        ats_result = calculate_ats_score(
            resume_skills,
            jd_skills
        )

        analyses.append({

            "job_id": index,

            "jd_skills": jd_skills,

            "score": ats_result["score"],

            "matched_skills":

                ats_result["exact_matches"]

                +

                ats_result["alias_matches"],

            "semantic_matches":

                ats_result["semantic_matches"],

            "missing_skills":

                ats_result["missing_skills"]

        })

    return analyses