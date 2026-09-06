from domains.skill_research import (
    SkillResearchResult
)


class SkillResearchService:
    """
    Handles structured research results for skills.

    Responsibilities:
    - Validate research data
    - Create SkillResearchResult objects
    - Convert research results into enrichment proposals

    This service does not directly modify the
    Knowledge Base.
    """

    # ==================================================
    # CREATE RESEARCH RESULT
    # ==================================================

    def create_research_result(
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
    ) -> SkillResearchResult:
        """
        Create a validated research result.
        """

        self._validate_skill_id(
            skill_id
        )

        self._validate_name(
            name
        )

        self._validate_confidence(
            confidence
        )

        self._validate_sources(
            sources
        )

        return SkillResearchResult(

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

    # ==================================================
    # CREATE ENRICHMENT PROPOSAL
    # ==================================================

    def create_enrichment_proposal(
        self,
        research_result: SkillResearchResult,
    ):
        """
        Convert a validated research result into
        an enrichment proposal.

        The SkillEnrichmentService handles
        proposal creation and persistence.
        """

        from services.skill_enrichment_service import (
            SkillEnrichmentService,
        )

        enrichment_service = (
            SkillEnrichmentService()
        )

        return (
            enrichment_service
            .create_proposal_from_research(
                research_result
            )
        )

    # ==================================================
    # VALIDATION
    # ==================================================

    @staticmethod
    def _validate_skill_id(
        skill_id: str,
    ) -> None:

        if not isinstance(
            skill_id,
            str
        ) or not skill_id.strip():

            raise ValueError(
                "Skill ID must be a "
                "non-empty string."
            )

    # --------------------------------------------------

    @staticmethod
    def _validate_name(
        name: str,
    ) -> None:

        if not isinstance(
            name,
            str
        ) or not name.strip():

            raise ValueError(
                "Skill name must be a "
                "non-empty string."
            )

    # --------------------------------------------------

    @staticmethod
    def _validate_confidence(
        confidence: float,
    ) -> None:

        if not isinstance(
            confidence,
            (int, float)
        ):

            raise ValueError(
                "Confidence must be a number."
            )

        if not 0.0 <= confidence <= 1.0:

            raise ValueError(
                "Confidence must be between "
                "0.0 and 1.0."
            )

    # --------------------------------------------------

    @staticmethod
    def _validate_sources(
        sources: list[str],
    ) -> None:

        if not sources:

            raise ValueError(
                "At least one research source "
                "is required."
            )

        if not all(
            isinstance(source, str)
            and source.strip()
            for source in sources
        ):

            raise ValueError(
                "All research sources must be "
                "non-empty strings."
            )