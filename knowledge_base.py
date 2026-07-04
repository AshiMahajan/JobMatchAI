import json
import os
from datetime import datetime


class SkillKnowledgeBase:

    def __init__(
            self,
            path="data/skills/knowledge_base.json"
    ):

        self.path = path

        with open(
                path,
                "r",
                encoding="utf-8"
        ) as f:

            self.skills = json.load(f)

        # ------------------------
        # Fast Lookup Indexes
        # ------------------------

        self.skill_index = {}

        self.alias_index = {}

        for skill in self.skills:

            canonical = skill["name"]

            self.skill_index[
                canonical.lower()
            ] = skill

            for alias in skill["aliases"]:

                self.alias_index[
                    alias.lower()
                ] = canonical

    # --------------------------

    def get_skill(
            self,
            canonical_name
    ):

        return self.skill_index.get(
            canonical_name.lower()
        )

    # --------------------------

    def find_canonical_skill(
            self,
            skill_name
    ):

        return self.alias_index.get(
            skill_name.lower().strip()
        )

    # --------------------------

    def get_category(
            self,
            canonical_name
    ):

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["category"]

        return None

    # --------------------------

    def get_related_skills(
            self,
            canonical_name
    ):

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["related"]

        return []

    # --------------------------

    def get_parent(
            self,
            canonical_name
    ):

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["parent"]

        return None

    # --------------------------

    def list_all_skills(self):

        return sorted(

            skill["name"]

            for skill in self.skills
        )

    # --------------------------

    def record_unknown_skill(
            self,
            skill_name
    ):

        path = (
            "data/skills/missing_skills.json"
        )

        if not os.path.exists(path):

            with open(
                    path,
                    "w",
                    encoding="utf-8"
            ) as f:

                json.dump({}, f)

        with open(
                path,
                "r",
                encoding="utf-8"
        ) as f:

            data = json.load(f)

        now = datetime.utcnow().isoformat()

        if skill_name not in data:

            data[skill_name] = {

                "count": 1,

                "first_seen": now,

                "last_seen": now
            }

        else:

            data[skill_name]["count"] += 1

            data[skill_name]["last_seen"] = now

        with open(
                path,
                "w",
                encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )