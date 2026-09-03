import json

from pathlib import Path

from core.config import KNOWLEDGE_BASE_PATH


class KnowledgeBaseRepository:
    """
    Handles persistence of the Skill Knowledge Base.

    This repository is responsible for reading and updating
    skill records in knowledge_base.json.

    Business decisions such as whether a proposal should be
    approved are handled by services, not this repository.
    """

    def __init__(
        self,
        path=KNOWLEDGE_BASE_PATH,
    ):
        self.path = Path(path)

    # ==================================================
    # GET ALL SKILLS
    # ==================================================

    def get_all(self) -> list[dict]:
        """
        Return all skills from the Knowledge Base.
        """

        return self._load()

    # ==================================================
    # GET SKILL
    # ==================================================

    def get_skill(
        self,
        skill_id: str,
    ) -> dict | None:
        """
        Find a skill by its ID.
        """

        skills = self._load()

        for skill in skills:

            if (
                skill.get("id", "").lower()
                == skill_id.lower()
            ):

                return skill

        return None

    # ==================================================
    # UPDATE SKILL
    # ==================================================

    def update_skill(
        self,
        skill_id: str,
        updated_skill: dict,
    ) -> dict:
        """
        Replace an existing skill with updated data.
        """

        skills = self._load()

        for index, skill in enumerate(skills):

            if (
                skill.get("id", "").lower()
                == skill_id.lower()
            ):

                skills[index] = updated_skill

                self._write(skills)

                return updated_skill

        raise ValueError(
            f"Skill '{skill_id}' not found "
            "in Knowledge Base."
        )

    # ==================================================
    # ADD SKILL
    # ==================================================

    def add_skill(
        self,
        skill: dict,
    ) -> dict:
        """
        Add a new skill to the Knowledge Base.

        Raises an error if the skill already exists.
        """

        skills = self._load()

        skill_id = skill.get("id")

        if not skill_id:

            raise ValueError(
                "Skill must contain an ID."
            )

        for existing in skills:

            if (
                existing.get("id", "").lower()
                == skill_id.lower()
            ):

                raise ValueError(
                    f"Skill '{skill_id}' already "
                    "exists in Knowledge Base."
                )

        skills.append(skill)

        self._write(skills)

        return skill

    # ==================================================
    # LOAD
    # ==================================================

    def _load(self) -> list[dict]:
        """
        Load the Knowledge Base JSON.
        """

        try:

            with open(
                self.path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

        except FileNotFoundError as error:

            raise RuntimeError(
                "Knowledge Base file not found."
            ) from error

        except json.JSONDecodeError as error:

            raise RuntimeError(
                "Knowledge Base contains invalid JSON."
            ) from error

        if not isinstance(
            data,
            list,
        ):

            raise RuntimeError(
                "Knowledge Base must contain "
                "a JSON list."
            )

        return data

    # ==================================================
    # WRITE
    # ==================================================

    def _write(
        self,
        skills: list[dict],
    ) -> None:
        """
        Persist the Knowledge Base to disk.
        """

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                skills,
                file,
                indent=4,
                ensure_ascii=False,
            )