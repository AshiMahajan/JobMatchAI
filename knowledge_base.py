import json

from core.config import KNOWLEDGE_BASE_PATH
from core.logger import logger


class SkillKnowledgeBase:

    def __init__(
        self,
        path=KNOWLEDGE_BASE_PATH
    ):

        self.path = path

        self._load()

        self._build_indexes()

    # ==================================================
    # LOAD KNOWLEDGE BASE
    # ==================================================

    def _load(self) -> None:
        """
        Load the Knowledge Base from disk.
        """

        try:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:

                self.skills = json.load(file)

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

    # ==================================================
    # BUILD INDEXES
    # ==================================================

    def _build_indexes(self) -> None:
        """
        Build fast lookup indexes for canonical
        skill names and aliases.
        """

        self.skill_index = {}

        self.alias_index = {}

        for skill in self.skills:

            canonical = skill["name"]

            self.skill_index[
                canonical.lower()
            ] = skill

            for alias in skill.get(
                "aliases",
                []
            ):

                self.alias_index[
                    alias.lower().strip()
                ] = canonical

    # ==================================================
    # GET SKILL
    # ==================================================

    def get_skill(
        self,
        canonical_name: str
    ) -> dict | None:
        """
        Return a skill by canonical name.
        """

        return self.skill_index.get(
            canonical_name.lower()
        )

    # ==================================================
    # FIND CANONICAL SKILL
    # ==================================================

    def find_canonical_skill(
        self,
        skill_name: str
    ) -> str | None:
        """
        Resolve a skill name or alias to its
        canonical skill name.
        """

        normalized = (
            skill_name
            .lower()
            .strip()
        )

        # Direct canonical-name lookup
        skill = self.skill_index.get(
            normalized
        )

        if skill:

            return skill["name"]

        # Alias lookup
        return self.alias_index.get(
            normalized
        )

    # ==================================================
    # CATEGORY
    # ==================================================

    def get_category(
        self,
        canonical_name: str
    ) -> str | None:

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill.get(
                "category"
            )

        return None

    # ==================================================
    # RELATED SKILLS
    # ==================================================

    def get_related_skills(
        self,
        canonical_name: str
    ) -> list[str]:

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill.get(
                "related",
                []
            )

        return []

    # ==================================================
    # PARENT
    # ==================================================

    def get_parent(
        self,
        canonical_name: str
    ) -> str | None:

        skill = self.get_skill(
            canonical_name
        )

        if skill:

            return skill.get(
                "parent"
            )

        return None

    # ==================================================
    # LIST ALL SKILLS
    # ==================================================

    def list_all_skills(
        self
    ) -> list[str]:

        return sorted(

            skill["name"]

            for skill in self.skills

        )

    # ==================================================
    # PENDING SKILLS
    # ==================================================

    def get_pending_skills(
        self
    ) -> list[dict]:
        """
        Return all skills that still require
        enrichment/review.
        """

        return [

            skill

            for skill in self.skills

            if skill.get("status") == "pending"

        ]

    # ==================================================
    # APPLY ENRICHMENT
    # ==================================================

    def apply_enrichment(
        self,
        proposal
    ) -> dict:
        """
        Apply an approved enrichment proposal
        to the Knowledge Base.

        Only approved proposals can modify
        the Knowledge Base.
        """

        # ----------------------------------------------
        # Validate proposal status
        # ----------------------------------------------

        if proposal.status != "approved":

            raise ValueError(
                "Only approved proposals can be "
                "applied to the Knowledge Base."
            )

        # ----------------------------------------------
        # Find skill
        # ----------------------------------------------

        skill = self.skill_index.get(
            proposal.skill_id.lower()
        )

        if skill is None:

            raise ValueError(
                f"Skill '{proposal.skill_id}' "
                "was not found in the Knowledge Base."
            )

        # ----------------------------------------------
        # Update metadata
        # ----------------------------------------------

        skill["name"] = proposal.name

        skill["aliases"] = list(
            proposal.aliases
        )

        skill["category"] = (
            proposal.category
        )

        skill["parent"] = (
            proposal.parent
        )

        skill["related"] = list(
            proposal.related
        )

        skill["prerequisites"] = list(
            proposal.prerequisites
        )

        skill["unlocks"] = list(
            proposal.unlocks
        )

        skill["status"] = "curated"

        # ----------------------------------------------
        # Persist changes
        # ----------------------------------------------

        self._save()

        # ----------------------------------------------
        # Rebuild indexes
        # ----------------------------------------------

        self._build_indexes()

        logger.info(
            "Skill enrichment applied: %s",
            proposal.name
        )

        return skill

    # ==================================================
    # SAVE KNOWLEDGE BASE
    # ==================================================

    def _save(self) -> None:
        """
        Persist the current Knowledge Base
        to disk.
        """

        try:

            with open(
                self.path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.skills,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except OSError as error:

            logger.error(
                "Failed to save Knowledge Base: %s",
                error
            )

            raise RuntimeError(
                "Knowledge Base could not be saved."
            ) from error