from domains.ats_result import ATSResult

from alias_matcher import alias_match
from exact_matcher import exact_match
from semantic_matcher import semantic_match

from services.recommendation_service import (
    generate_recommendations,
    get_match_level,
)


def calculate_ats_score(
    resume_skills: list[str],
    jd_skills: list[str],
) -> ATSResult:
    """
    Calculates the ATS score by comparing resume skills
    against job description skills.

    Matching Strategy:
        1. Exact Match
        2. Alias Match
        3. Semantic Match

    Returns
    -------
    ATSResult
        Structured ATS analysis.
    """

    if not jd_skills:

        return ATSResult(
            score=0.0,
            match_level="No Match",
            exact_matches=[],
            alias_matches=[],
            semantic_matches=[],
            missing_skills=[],
            recommendations=[],
        )

    # ==========================================================
    # Exact Matching
    # ==========================================================

    exact_matches, _ = exact_match(
        resume_skills,
        jd_skills,
    )

    exact_skill_set = {
        skill.lower()
        for skill in exact_matches
    }

    # ==========================================================
    # Alias Matching
    # ==========================================================

    alias_matches, alias_jd_skills = alias_match(
        resume_skills,
        jd_skills,
    )

    # ==========================================================
    # Remaining JD Skills
    # ==========================================================

    unmatched_jd_skills = []

    for skill in jd_skills:

        skill_lower = skill.lower()

        if skill_lower in exact_skill_set:
            continue

        if skill_lower in alias_jd_skills:
            continue

        unmatched_jd_skills.append(skill)

    # ==========================================================
    # Semantic Matching
    # ==========================================================

    semantic_matches, missing_skills = semantic_match(
        resume_skills,
        unmatched_jd_skills,
    )

    # ==========================================================
    # ATS Score
    # ==========================================================

    exact_score = len(exact_matches)

    alias_score = len(alias_matches)

    semantic_score = len(semantic_matches) * 0.75

    final_score = round(
        (
            exact_score
            + alias_score
            + semantic_score
        )
        / len(jd_skills)
        * 100,
        2,
    )

    # ==========================================================
    # Recommendations
    # ==========================================================

    match_level = get_match_level(
        final_score
    )

    recommendations = generate_recommendations(
        missing_skills
    )

    # ==========================================================
    # Response
    # ==========================================================

    return ATSResult(
        score=final_score,
        match_level=match_level,
        exact_matches=exact_matches,
        alias_matches=alias_matches,
        semantic_matches=semantic_matches,
        missing_skills=missing_skills,
        recommendations=recommendations,
    )