from domains.skill_research import (
    SkillResearchResult
)


class SkillResearchService:
    """
    Handles research results for skills.

    This service does not modify the Knowledge Base.
    It produces structured research results that
    can later be converted into enrichment proposals.
    """

    # --------------------------------------------------
    # Create research result
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Validation
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