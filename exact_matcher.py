# exact_matcher.py

def exact_match(resume_skills, jd_skills):

    resume_set = set(
        skill.lower()
        for skill in resume_skills
    )

    jd_set = set(
        skill.lower()
        for skill in jd_skills
    )

    matched = resume_set.intersection(
        jd_set
    )

    missing = jd_set - resume_set

    return (
        list(matched),
        list(missing)
    )