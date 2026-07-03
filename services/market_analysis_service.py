from skill_extractor import extract_skills
from ats_engine import calculate_ats_score


def analyze_market(
        resume_skills,
        job_descriptions):

    analyses = []

    for index, jd_text in enumerate(job_descriptions, start=1):

        jd_skills = extract_skills(jd_text)

        result = calculate_ats_score(
            resume_skills,
            jd_skills
        )

        analyses.append({

            "job_id": index,

            "jd_skills": jd_skills,

            "score": result["score"],

            "matched_skills":
                result["exact_matches"]
                + result["alias_matches"],

            "semantic_matches":
                result["semantic_matches"],

            "missing_skills":
                result["missing_skills"]
        })

    return analyses