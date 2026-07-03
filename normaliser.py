from skill_engine import SkillEngine

engine = SkillEngine()


def normalize_skills(skills):

    normalized = []

    for skill in skills:

        normalized.append(
            engine.normalize(skill)
        )

    return list(set(normalized))