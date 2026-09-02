from domains.skill_enrichment import (
    SkillEnrichmentProposal
)


class SkillEnrichmentService:
    """
    Handles enrichment proposals for skills that
    are pending in the Knowledge Base.

    This service does not directly modify the
    Knowledge Base.
    """

    # --------------------------------------------------

    def create_proposal(
        self,
        skill_id: str,
        name: str,
        aliases: list[str],
        category: str,
        parent: str | None,
        related: list[str],
        prerequisites: list[str],
        unlocks: list[str],
        sources: list[str],
        confidence: float,
    ) -> SkillEnrichmentProposal:

        self._validate_confidence(
            confidence
        )

        return SkillEnrichmentProposal(

            skill_id=skill_id,

            name=name,

            aliases=aliases,

            category=category,

            parent=parent,

            related=related,

            prerequisites=prerequisites,

            unlocks=unlocks,

            sources=sources,

            confidence=confidence,

        )

    # --------------------------------------------------

    def approve_proposal(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Mark an enrichment proposal as approved.

        The Knowledge Base is not updated here yet.
        """

        proposal.status = "approved"

        return proposal

    # --------------------------------------------------

    def reject_proposal(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Mark an enrichment proposal as rejected.

        The Knowledge Base is not modified.
        """

        proposal.status = "rejected"

        return proposal

    # --------------------------------------------------

    @staticmethod
    def _validate_confidence(
        confidence: float,
    ) -> None:

        if not 0.0 <= confidence <= 1.0:

            raise ValueError(
                "Confidence must be between "
                "0.0 and 1.0."
            )