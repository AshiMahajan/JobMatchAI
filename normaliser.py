# normalizer.py

from aliases import SKILL_ALIASES


def normalize_skills(skills):

    normalized = []

    for skill in skills:

        skill = skill.lower().strip()

        normalized.append(
            SKILL_ALIASES.get(
                skill,
                skill
            )
        )

    return normalized