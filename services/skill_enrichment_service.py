from domains.skill_enrichment import (
    SkillEnrichmentProposal
)

from repositories.enrichment_proposal_repository import (
    EnrichmentProposalRepository
)


class SkillEnrichmentService:
    """
    Handles the lifecycle of skill enrichment proposals.

    Responsibilities:
    - Create proposals
    - Persist proposals
    - Retrieve proposals awaiting review
    - Approve proposals
    - Reject proposals

    The service contains business logic.
    The repository handles persistence.
    """

    # ==================================================
    # INITIALIZATION
    # ==================================================

    def __init__(
        self,
        repository: EnrichmentProposalRepository | None = None,
    ):

        self.repository = (
            repository
            if repository is not None
            else EnrichmentProposalRepository()
        )

    # ==================================================
    # CREATE PROPOSAL
    # ==================================================

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
        """
        Create and persist a new enrichment proposal.

        Every new proposal enters the
        'pending_review' state.
        """

        self._validate_confidence(
            confidence
        )

        self._validate_sources(
            sources
        )

        self._validate_skill_id(
            skill_id
        )

        self._validate_name(
            name
        )

        proposal = SkillEnrichmentProposal(

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

            status="pending_review",
        )

        # Persist immediately
        self.repository.save(
            proposal
        )

        return proposal

    # ==================================================
    # CREATE FROM RESEARCH
    # ==================================================

    def create_proposal_from_research(
        self,
        research_result,
    ) -> SkillEnrichmentProposal:
        """
        Convert a research result into an enrichment
        proposal and persist it.
        """

        return self.create_proposal(

            skill_id=research_result.skill_id,

            name=research_result.name,

            aliases=research_result.aliases,

            category=research_result.category,

            parent=research_result.parent,

            related=research_result.related,

            prerequisites=(
                research_result.prerequisites
            ),

            unlocks=research_result.unlocks,

            sources=research_result.sources,

            confidence=research_result.confidence,
        )

    # ==================================================
    # GET PENDING PROPOSALS
    # ==================================================

    def get_pending_proposals(
        self,
    ) -> list[SkillEnrichmentProposal]:
        """
        Return all proposals awaiting human review.
        """

        return self.repository.get_pending()

    # ==================================================
    # GET PROPOSAL
    # ==================================================

    def get_proposal(
        self,
        skill_id: str,
    ) -> SkillEnrichmentProposal | None:
        """
        Retrieve a proposal by skill ID.
        """

        return self.repository.get(
            skill_id
        )

    # ==================================================
    # APPROVE PROPOSAL
    # ==================================================

    def approve_proposal(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Approve a pending proposal and persist the
        updated status.
        """

        self._validate_pending_proposal(
            proposal
        )

        proposal.status = "approved"

        self.repository.update(
            proposal
        )

        return proposal

    # ==================================================
    # REJECT PROPOSAL
    # ==================================================

    def reject_proposal(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:
        """
        Reject a pending proposal and persist the
        updated status.
        """

        self._validate_pending_proposal(
            proposal
        )

        proposal.status = "rejected"

        self.repository.update(
            proposal
        )

        return proposal

    # ==================================================
    # VALIDATION
    # ==================================================

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

    # --------------------------------------------------

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
    def _validate_pending_proposal(
        proposal: SkillEnrichmentProposal,
    ) -> None:

        if proposal.status != "pending_review":

            raise ValueError(
                "Only proposals with status "
                "'pending_review' can be approved "
                "or rejected."
            )