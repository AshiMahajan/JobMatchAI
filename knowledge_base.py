import json

from core.config import (
    KNOWLEDGE_BASE_PATH
)

from core.logger import logger

class SkillKnowledgeBase:

    def __init__(
            self,
            path=KNOWLEDGE_BASE_PATH
    ):

        self.path = path

        try:

            with open(
                    self.path,
                    "r",
                    encoding="utf-8"
            ) as file:

                self.skills = json.load(
                file
)

                logger.info(
                    "Knowledge Base loaded (%d skills).",
                    len(self.skills)
)

        except FileNotFoundError as error:

            logger.error(
                "Knowledge Base file not found: %s",
                self.path
            )

            raise RuntimeError(
                "Knowledge Base could not be loaded."
            ) from error

        except json.JSONDecodeError as error:

            logger.error(
                "Knowledge Base contains invalid JSON."
            )

            raise RuntimeError(
                "Knowledge Base is corrupted."
            ) from error

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

    # ----------------------------------

    def get_skill(
            self,
            canonical_name: str
    ) -> dict | None:

        return self.skill_index.get(
            canonical_name.lower()
        )

    # ----------------------------------

    def find_canonical_skill(
            self,
            skill_name: str
    ) -> str | None:

        return self.alias_index.get(
            skill_name.lower().strip()
        )

    # ----------------------------------

    def get_category(
            self,
            canonical_name: str
    ) -> str | None:

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["category"]

        return None

    # ----------------------------------

    def get_related_skills(
            self,
            canonical_name: str
    ) -> list[str]:

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["related"]

        return []

    # ----------------------------------

    def get_parent(
            self,
            canonical_name: str
    ) -> str | None:

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill["parent"]

        return None

    # ----------------------------------

    def list_all_skills(
            self
    ) -> list[str]:

        return sorted(

            skill["name"]

            for skill in self.skills

        )