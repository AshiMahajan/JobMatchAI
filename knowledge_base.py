import json


class SkillKnowledgeBase:

    def __init__(self,
                 path="data/skills/knowledge_base.json"):

        with open(path,
                  "r",
                  encoding="utf-8") as f:

            self.skills = json.load(f)

    # --------------------------

    def get_skill(self,
                  canonical_name):

        for skill in self.skills:

            if skill["name"].lower() == canonical_name.lower():

                return skill

        return None

    # --------------------------

    def find_canonical_skill(self,
                             input_skill):

        input_skill = input_skill.lower().strip()

        for skill in self.skills:

            aliases = [
                alias.lower()
                for alias in skill["aliases"]
            ]

            if input_skill in aliases:

                return skill["name"]

        return None

    # --------------------------

    def get_category(self,
                     canonical_name):

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["category"]

        return None

    # --------------------------

    def get_related_skills(self,
                           canonical_name):

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["related"]

        return []

    # --------------------------

    def get_parent(self,
                   canonical_name):

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["parent"]

        return None

    # --------------------------

    def list_all_skills(self):

        return [
            skill["name"]
            for skill in self.skills
        ]