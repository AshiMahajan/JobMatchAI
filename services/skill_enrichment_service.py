from domains.skill_enrichment import (
    SkillEnrichmentProposal
)

from repositories.enrichment_proposal_repository import (
    EnrichmentProposalRepository
)

from services.knowledge_base_enrichment_service import (
    KnowledgeBaseEnrichmentService
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
    - Apply approved proposals to the Knowledge Base
    """

    # ==================================================
    # INITIALIZATION
    # ==================================================

    def __init__(
        self,
        repository: EnrichmentProposalRepository | None = None,
        kb_enrichment_service: (
            KnowledgeBaseEnrichmentService | None
        ) = None,
    ):

        self.repository = (
            repository
            if repository is not None
            else EnrichmentProposalRepository()
        )

        self.kb_enrichment_service = (
            kb_enrichment_service
            if kb_enrichment_service is not None
            else KnowledgeBaseEnrichmentService()
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
    # GET PENDING
    # ==================================================

    def get_pending_proposals(
        self,
    ) -> list[SkillEnrichmentProposal]:

        return self.repository.get_pending()

    # ==================================================
    # GET PROPOSAL
    # ==================================================

    def get_proposal(
        self,
        skill_id: str,
    ) -> SkillEnrichmentProposal | None:

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

        self._validate_pending_proposal(
            proposal
        )

        proposal.status = "approved"

        self.repository.update(
            proposal
        )

        return proposal

    # ==================================================
    # APPROVE + APPLY TO KNOWLEDGE BASE
    # ==================================================

    def approve_and_apply(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> dict:
        """
        Approve a proposal and immediately apply
        the approved data to the Knowledge Base.

        Returns the curated Knowledge Base record.
        """

        approved = self.approve_proposal(
            proposal
        )

        return self.kb_enrichment_service.apply_proposal(
            approved
        )

    # ==================================================
    # REJECT PROPOSAL
    # ==================================================

    def reject_proposal(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> SkillEnrichmentProposal:

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