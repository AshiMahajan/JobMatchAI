# scorer.py

def calculate_score(resume_skills, jd_skills):

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = resume_set.intersection(jd_set)

    missing = jd_set - resume_set

    if len(jd_set) == 0:
        score = 0
    else:
        score = round((len(matched) / len(jd_set)) * 100, 2)
    
    critical_bonus = 0

    if "python" in matched:
        critical_bonus += 5

    if "aws" in matched:
        critical_bonus += 5

    score = min(score + critical_bonus, 100)

    return {
        "score": score,
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing))
    }