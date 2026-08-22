from domains.skill_dependency import SkillDependency

from skill_engine import SkillEngine


class SkillDependencyService:
    """
    Provides dependency intelligence for skills.

    This service retrieves prerequisite, unlock,
    and related-skill relationships from the
    Skill Knowledge Base.

    It does not calculate learning priority.
    """

    def __init__(self) -> None:

        self.skill_engine = SkillEngine()

    def get_dependency(
        self,
        skill_name: str
    ) -> SkillDependency:

        skill = self.skill_engine.describe(
            skill_name
        )

        if skill["status"] == "unknown":

            return SkillDependency(
                skill=skill_name
            )

        return SkillDependency(

            skill=skill["name"],

            prerequisites=skill.get(
                "prerequisites",
                []
            ),

            unlocks=skill.get(
                "unlocks",
                []
            ),

            related=skill.get(
                "related",
                []
            )
        )