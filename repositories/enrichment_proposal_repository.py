import json

from pathlib import Path

from domains.skill_enrichment import (
    SkillEnrichmentProposal
)


class EnrichmentProposalRepository:
    """
    Handles persistence of skill enrichment proposals.

    This repository is responsible only for storage.
    It does not contain business logic and does not
    modify the Knowledge Base.
    """

    def __init__(
        self,
        path: str = "data/enrichment_proposals.json",
    ):
        self.path = Path(path)

        self._ensure_storage_exists()

    # ==================================================
    # SAVE
    # ==================================================

    def save(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Save a new enrichment proposal.

        Raises an error if a proposal for the same
        skill already exists.
        """

        proposals = self._load()

        for existing in proposals:

            if (
                existing["skill_id"].lower()
                == proposal.skill_id.lower()
            ):

                raise ValueError(
                    "An enrichment proposal already "
                    f"exists for skill '{proposal.skill_id}'."
                )

        proposals.append(
            self._to_dict(proposal)
        )

        self._write(
            proposals
        )

        return proposal

    # ==================================================
    # GET
    # ==================================================

    def get(
        self,
        skill_id: str,
    ) -> SkillEnrichmentProposal | None:
        """
        Retrieve a proposal by skill ID.
        """

        proposals = self._load()

        for proposal_data in proposals:

            if (
                proposal_data["skill_id"].lower()
                == skill_id.lower()
            ):

                return self._from_dict(
                    proposal_data
                )

        return None

    # ==================================================
    # GET PENDING
    # ==================================================

    def get_pending(
        self,
    ) -> list[SkillEnrichmentProposal]:
        """
        Return all proposals currently waiting
        for human review.
        """

        proposals = self._load()

        return [
            self._from_dict(proposal)
            for proposal in proposals
            if proposal.get("status")
            == "pending_review"
        ]

    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Update an existing proposal.
        """

        proposals = self._load()

        for index, existing in enumerate(
            proposals
        ):

            if (
                existing["skill_id"].lower()
                == proposal.skill_id.lower()
            ):

                proposals[index] = (
                    self._to_dict(proposal)
                )

                self._write(
                    proposals
                )

                return proposal

        raise ValueError(
            "Enrichment proposal not found for "
            f"skill '{proposal.skill_id}'."
        )

    # ==================================================
    # DELETE
    # ==================================================

    def delete(
        self,
        skill_id: str,
    ) -> None:
        """
        Delete a proposal by skill ID.
        """

        proposals = self._load()

        updated_proposals = [
            proposal
            for proposal in proposals
            if proposal["skill_id"].lower()
            != skill_id.lower()
        ]

        if len(updated_proposals) == len(
            proposals
        ):

            raise ValueError(
                "Enrichment proposal not found for "
                f"skill '{skill_id}'."
            )

        self._write(
            updated_proposals
        )

    # ==================================================
    # STORAGE
    # ==================================================

    def _load(self) -> list[dict]:
        """
        Load proposals from JSON storage.
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

        except json.JSONDecodeError as error:

            raise RuntimeError(
                "Enrichment proposal storage "
                "contains invalid JSON."
            ) from error

        if not isinstance(
            data,
            list,
        ):

            raise RuntimeError(
                "Enrichment proposal storage "
                "must contain a JSON list."
            )

        return data

    # --------------------------------------------------

    def _write(
        self,
        proposals: list[dict],
    ) -> None:
        """
        Persist proposals to JSON storage.
        """

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                proposals,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------

    def _ensure_storage_exists(
        self,
    ) -> None:
        """
        Create the storage directory and JSON file
        if they do not already exist.
        """

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.path.exists():

            self._write([])

    # ==================================================
    # SERIALIZATION
    # ==================================================

    @staticmethod
    def _to_dict(
        proposal: SkillEnrichmentProposal,
    ) -> dict:
        """
        Convert a proposal domain object into
        JSON-compatible data.
        """

        return {

            "skill_id": proposal.skill_id,

            "name": proposal.name,

            "aliases": proposal.aliases,

            "category": proposal.category,

            "parent": proposal.parent,

            "related": proposal.related,

            "prerequisites": (
                proposal.prerequisites
            ),

            "unlocks": proposal.unlocks,

            "sources": proposal.sources,

            "confidence": proposal.confidence,

            "status": proposal.status,
        }

    # --------------------------------------------------

    @staticmethod
    def _from_dict(
        data: dict,
    ) -> SkillEnrichmentProposal:
        """
        Convert stored JSON data back into
        a SkillEnrichmentProposal.
        """

        return SkillEnrichmentProposal(

            skill_id=data["skill_id"],

            name=data["name"],

            aliases=data["aliases"],

            category=data["category"],

            parent=data["parent"],

            related=data["related"],

            prerequisites=data[
                "prerequisites"
            ],

            unlocks=data["unlocks"],

            sources=data["sources"],

            confidence=data["confidence"],

            status=data["status"],
        )