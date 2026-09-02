from knowledge_base import SkillKnowledgeBase

class SkillEngine:

    def __init__(self):

        self.kb = SkillKnowledgeBase()

    # ----------------------------------

    def normalize(
            self,
            skill: str
    ) -> str:

        canonical = self.kb.find_canonical_skill(
            skill
        )

        if canonical:

            return canonical

        return skill.strip()

    # ----------------------------------

    def describe(
            self,
            skill: str
    ) -> dict:

        canonical = self.normalize(
            skill
        )

        info = self.kb.get_skill(
            canonical
        )

        # Skill exists in the Knowledge Base
        if info:

            return info.copy()

        # Placeholder for a detected skill that
        # has not yet been enriched.
        return {

            "id": canonical.lower(),

            "name": canonical,

            "aliases": [
                canonical.lower()
            ],

            "category": "Unknown",

            "parent": None,

            "related": [],

            "status": "unknown",

            "learning": {

                "objectives": []

            }

        }

    # ----------------------------------

    def infer_parent_skill(
            self,
            skill: str
    ) -> str | None:

        canonical = self.normalize(
            skill
        )

        return self.kb.get_parent(
            canonical
        )

    # ----------------------------------

    def related_skills(
            self,
            skill: str
    ) -> list[str]:

        canonical = self.normalize(
            skill
        )

        return self.kb.get_related_skills(
            canonical
        )

    # ----------------------------------

    def get_learning_objectives(
            self,
            skill: str
    ) -> list[str]:

        canonical = self.normalize(
            skill
        )

        info = self.kb.get_skill(
            canonical
        )

        if not info:

            return []

        learning = info.get(
            "learning",
            {}
        )

        return learning.get(
            "objectives",
            []
        )