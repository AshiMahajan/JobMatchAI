from skill_extractor import extract_skills

from skill_engine import SkillEngine


class SkillService:

    def __init__(self):

        self.engine = SkillEngine()

    # ----------------------------------

    def extract(
            self,
            text: str
    ) -> list[dict]:

        raw_skills = extract_skills(
            text
        )

        enriched_skills = []

        for skill in raw_skills:

            enriched_skills.append(

                self.engine.describe(
                    skill
                )

            )

        return enriched_skills

    # ----------------------------------

    def extract_names(
            self,
            text: str
    ) -> list[str]:

        skills = self.extract(
            text
        )

        return sorted(

            skill["name"]

            for skill in skills

        )

    # ----------------------------------

    def extract_known(
            self,
            text: str
    ) -> list[dict]:

        skills = self.extract(
            text
        )

        return [

            skill

            for skill in skills

            if skill["status"] == "known"

        ]

    # ----------------------------------

    def extract_unknown(
            self,
            text: str
    ) -> list[dict]:

        skills = self.extract(
            text
        )

        return [

            skill

            for skill in skills

            if skill["status"] == "unknown"

        ]