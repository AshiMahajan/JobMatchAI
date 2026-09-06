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

    def get_all(
        self,
    ) -> list[dict]:
        """
        Return all skills from the Knowledge Base.
        """

        return self._load()

    # ==================================================
    # GET SKILL BY ID
    # ==================================================

    def get_skill(
        self,
        skill_id: str,
    ) -> dict | None:
        """
        Find a skill by its ID.
        """

        if not isinstance(
            skill_id,
            str,
        ) or not skill_id.strip():

            return None

        normalized_id = (
            skill_id.strip().lower()
        )

        skills = self._load()

        for skill in skills:

            existing_id = skill.get(
                "id",
                "",
            )

            if (
                isinstance(existing_id, str)
                and existing_id.strip().lower()
                == normalized_id
            ):

                return skill

        return None

    # ==================================================
    # GET SKILL BY NAME OR ALIAS
    # ==================================================

    def get_skill_by_name(
        self,
        skill_name: str,
    ) -> dict | None:
        """
        Find a skill by its name or one of its aliases.

        Matching is case-insensitive and ignores
        leading/trailing whitespace.

        Example:

            "LightGBM"
            "lightgbm"
            "LGBM"

        can all resolve to the same Knowledge Base
        record if the name or alias exists.
        """

        if not isinstance(
            skill_name,
            str,
        ) or not skill_name.strip():

            return None

        normalized_name = (
            skill_name.strip().lower()
        )

        skills = self._load()

        for skill in skills:

            # ------------------------------------------
            # CHECK OFFICIAL NAME
            # ------------------------------------------

            existing_name = skill.get(
                "name",
                "",
            )

            if (
                isinstance(existing_name, str)
                and existing_name.strip().lower()
                == normalized_name
            ):

                return skill

            # ------------------------------------------
            # CHECK ALIASES
            # ------------------------------------------

            aliases = skill.get(
                "aliases",
                [],
            )

            if not isinstance(
                aliases,
                list,
            ):

                continue

            for alias in aliases:

                if (
                    isinstance(alias, str)
                    and alias.strip().lower()
                    == normalized_name
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

        normalized_id = (
            skill_id.strip().lower()
        )

        for index, skill in enumerate(skills):

            existing_id = skill.get(
                "id",
                "",
            )

            if (
                isinstance(existing_id, str)
                and existing_id.strip().lower()
                == normalized_id
            ):

                skills[index] = updated_skill

                self._write(
                    skills
                )

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

        Raises an error if the skill ID already exists.
        """

        skills = self._load()

        skill_id = skill.get(
            "id"
        )

        if not isinstance(
            skill_id,
            str,
        ) or not skill_id.strip():

            raise ValueError(
                "Skill must contain an ID."
            )

        normalized_id = (
            skill_id.strip().lower()
        )

        for existing in skills:

            existing_id = existing.get(
                "id",
                "",
            )

            if (
                isinstance(existing_id, str)
                and existing_id.strip().lower()
                == normalized_id
            ):

                raise ValueError(
                    f"Skill '{skill_id}' already "
                    "exists in Knowledge Base."
                )

        skills.append(
            skill
        )

        self._write(
            skills
        )

        return skill

    # ==================================================
    # LOAD
    # ==================================================

    def _load(
        self,
    ) -> list[dict]:
        """
        Load the Knowledge Base JSON.
        """

        try:

            with open(
                self.path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(
                    file
                )

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