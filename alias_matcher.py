# alias_matcher.py

from aliases import SKILL_ALIASES


def alias_match(resume_skills, jd_skills):

    matches = []

    matched_jd = set()

    for resume_skill in resume_skills:

        normalized_resume = SKILL_ALIASES.get(
            resume_skill.lower(),
            resume_skill.lower()
        )

        for jd_skill in jd_skills:

            normalized_jd = SKILL_ALIASES.get(
                jd_skill.lower(),
                jd_skill.lower()
            )

            if (
                normalized_resume ==
                normalized_jd
                and
                resume_skill.lower() != jd_skill.lower()
            ):

                matches.append({
                    "resume_skill": resume_skill,
                    "jd_skill": jd_skill
                })

                matched_jd.add(
                    jd_skill.lower()
                )

    return matches, matched_jd