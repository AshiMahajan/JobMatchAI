from knowledge_base import SkillKnowledgeBase


class SkillEngine:

    def __init__(self):

        self.kb = SkillKnowledgeBase()

    # -------------------------

    def normalize(
            self,
            skill
    ):

        canonical = self.kb.find_canonical_skill(
            skill
        )

        if canonical:

            return canonical

        return skill.strip()

    # -------------------------

    def describe(
            self,
            skill
    ):

        canonical = self.normalize(
            skill
        )

        info = self.kb.get_skill(
            canonical
        )

        # -------------------------
        # Known Skill
        # -------------------------

        if info:

            info = info.copy()

            info["status"] = "known"

            return info

        # -------------------------
        # Unknown Skill
        # -------------------------

        self.kb.record_unknown_skill(
            canonical
        )

        return {

            "id": canonical.lower(),

            "name": canonical,

            "aliases": [],

            "category": "Unknown",

            "parent": None,

            "related": [],

            "status": "unknown"
        }

    # -------------------------

    def infer_parent_skill(
            self,
            skill
    ):

        canonical = self.normalize(
            skill
        )

        return self.kb.get_parent(
            canonical
        )

    # -------------------------

    def related_skills(
            self,
            skill
    ):

        canonical = self.normalize(
            skill
        )

        return self.kb.get_related_skills(
            canonical
        )