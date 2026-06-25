# ats_engine.py

from exact_matcher import exact_match
from alias_matcher import alias_match
from semantic_matcher import semantic_match

from services.recommendation_service import (
    get_match_level,
    generate_recommendations
)


def calculate_ats_score(
        resume_skills,
        jd_skills):

    if not jd_skills:

        return {
            "score": 0,
            "match_level": "No Match",
            "exact_matches": [],
            "alias_matches": [],
            "semantic_matches": [],
            "missing_skills": [],
            "recommendations": []
        }

    # ======================
    # Exact Matches
    # ======================

    exact_matches, _ = exact_match(
        resume_skills,
        jd_skills
    )

    exact_set = {
        skill.lower()
        for skill in exact_matches
    }

    # ======================
    # Alias Matches
    # ======================

    alias_matches, alias_jd_skills = alias_match(
        resume_skills,
        jd_skills
    )

    # ======================
    # Remaining JD Skills
    # ======================

    remaining_jd_skills = []

    for skill in jd_skills:

        skill_lower = skill.lower()

        if skill_lower in exact_set:
            continue

        if skill_lower in alias_jd_skills:
            continue

        remaining_jd_skills.append(
            skill
        )

    # ======================
    # Semantic Matches
    # ======================

    semantic_matches, semantic_missing = semantic_match(
        resume_skills,
        remaining_jd_skills
    )

    # ======================
    # Scoring
    # ======================

    exact_score = len(
        exact_matches
    )

    alias_score = len(
        alias_matches
    )

    semantic_score = (
        len(semantic_matches) * 0.75
    )

    final_score = round(
        (
            exact_score +
            alias_score +
            semantic_score
        )
        / len(jd_skills)
        * 100,
        2
    )

    # ======================
    # Recommendations
    # ======================

    match_level = get_match_level(
        final_score
    )

    recommendations = (
        generate_recommendations(
            semantic_missing
        )
    )

    # ======================
    # Response
    # ======================

    return {

        "score": final_score,

        "match_level": match_level,

        "exact_matches": exact_matches,

        "alias_matches": alias_matches,

        "semantic_matches": semantic_matches,

        "missing_skills": semantic_missing,

        "recommendations": recommendations
    }