# exact_matcher.py

def exact_match(
    resume_skills: list[str],
    jd_skills: list[str]
):
    """
    Performs case-insensitive exact skill matching while
    preserving the original job description skill names
    and their ordering.

    Returns
    -------
    tuple
        (
            matched_skills,
            missing_skills
        )
    """

    # Normalize resume skills for comparison
    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    # Preserve JD ordering
    matched = [
        skill
        for skill in jd_skills
        if skill.lower() in resume_set
    ]

    missing = [
        skill
        for skill in jd_skills
        if skill.lower() not in resume_set
    ]

    return matched, missing