from domains.skill_enrichment import (
    SkillEnrichmentProposal,
)

from repositories.enrichment_proposal_repository import (
    EnrichmentProposalRepository,
)

from services.knowledge_base_enrichment_service import (
    KnowledgeBaseEnrichmentService,
)

from agents.crews.skill_research_crew import (
    SkillResearchCrew,
)


class SkillEnrichmentService:
    """
    Handles the lifecycle of skill enrichment proposals.

    Responsibilities:

    - Check whether a skill exists in the Knowledge Base
    - Determine whether the existing skill is curated
    - Generate IDs for newly discovered skills
    - Research unknown or pending technical skills
    - Create enrichment proposals
    - Persist proposals
    - Retrieve proposals awaiting review
    - Approve proposals
    - Reject proposals
    - Apply approved proposals to the Knowledge Base

    Research never directly modifies the Knowledge Base.
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

        self.research_crew = (
            SkillResearchCrew()
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

        Every new proposal starts with:
        pending_review
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
    # CREATE PROPOSAL FROM RESEARCH
    # ==================================================

    def create_proposal_from_research(
        self,
        research_result,
    ) -> SkillEnrichmentProposal:
        """
        Convert a SkillResearchResult into an enrichment
        proposal and persist it.

        The Knowledge Base is not modified here.
        """

        return self.create_proposal(

            skill_id=research_result.skill_id,

            name=research_result.name,

            aliases=research_result.aliases,

            category=research_result.category,

            parent=research_result.parent,

            related=research_result.related,

            prerequisites=research_result.prerequisites,

            unlocks=research_result.unlocks,

            sources=research_result.sources,

            confidence=research_result.confidence,
        )

    # ==================================================
    # RESEARCH SKILL
    # ==================================================

    def research_skill(
        self,
        skill_name: str,
    ):
        """
        Research a technical skill.

        Flow:

            skill name
                ↓
            check Knowledge Base
                ↓
            curated skill exists
                → return existing skill
                ↓
            unknown / pending skill
                ↓
            perform fresh web research
                ↓
            synthesize enrichment
                ↓
            create pending_review proposal
                ↓
            return proposal

        Research never directly modifies the Knowledge Base.
        """

        self._validate_name(
            skill_name
        )

        skill_name = skill_name.strip()

        # --------------------------------------------------
        # CHECK KNOWLEDGE BASE
        # --------------------------------------------------

        existing_skill = (
            self.kb_enrichment_service
            .repository
            .get_skill_by_name(
                skill_name
            )
        )

        # --------------------------------------------------
        # EXISTING CURATED SKILL
        # --------------------------------------------------

        if existing_skill is not None:

            status = existing_skill.get(
                "status"
            )

            if status == "curated":

                return existing_skill

        # --------------------------------------------------
        # GENERATE SKILL ID
        # --------------------------------------------------

        skill_id = (
            self._generate_skill_id(
                skill_name
            )
        )

        # --------------------------------------------------
        # ALWAYS PERFORM FRESH RESEARCH
        # --------------------------------------------------
        #
        # IMPORTANT:
        #
        # We intentionally do NOT return an existing
        # pending proposal here.
        #
        # This endpoint is a research endpoint.
        # Calling it again should perform fresh research
        # so poor/old proposals can be regenerated.
        #
        # The repository's save/update behavior determines
        # how duplicate proposals are handled.
        #
        # --------------------------------------------------

        research_result = (
            self.research_crew.research(
                skill_name=skill_name,
                skill_id=skill_id,
            )
        )

        # --------------------------------------------------
        # CREATE ENRICHMENT PROPOSAL
        # --------------------------------------------------

        proposal = (
            self.create_proposal_from_research(
                research_result
            )
        )

        return proposal

    # ==================================================
    # GENERATE SKILL ID
    # ==================================================

    @staticmethod
    def _generate_skill_id(
        skill_name: str,
    ) -> str:
        """
        Generate a deterministic normalized skill ID.

        Examples:

            LightGBM
            -> lightgbm

            Real Time Inference
            -> real_time_inference

            Machine Learning
            -> machine_learning

            React.js
            -> react_js
        """

        normalized = (
            skill_name
            .strip()
            .lower()
        )

        normalized = "".join(

            character
            if character.isalnum()
            else " "

            for character in normalized
        )

        skill_id = "_".join(
            normalized.split()
        )

        if not skill_id:

            raise ValueError(
                "Unable to generate a valid skill ID."
            )

        return skill_id

    # ==================================================
    # GET PENDING PROPOSALS
    # ==================================================

    def get_pending_proposals(
        self,
    ) -> list[SkillEnrichmentProposal]:

        return (
            self.repository.get_pending()
        )

    # ==================================================
    # GET PROPOSAL
    # ==================================================

    def get_proposal(
        self,
        skill_id: str,
    ) -> SkillEnrichmentProposal | None:

        self._validate_skill_id(
            skill_id
        )

        return self.repository.get(
            skill_id
        )

    # ==================================================
    # APPROVE PROPOSAL
    # ==================================================

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
    
        # Apply to Knowledge Base first.
        self.kb_enrichment_service.apply_proposal(
            proposal
        )
    
        # Only archive after successful KB application.
        self.repository.archive_approved(
            proposal
        )
    
        return proposal


    # ==================================================
    # APPROVE + APPLY
    # ==================================================

    # def approve_and_apply(
    #     self,
    #     proposal: SkillEnrichmentProposal,
    # ) -> dict:

    #     approved = self.approve_proposal(
    #         proposal
    #     )

    #     return self.kb_enrichment_service.repository.get_skill(
    #         approved.skill_id
    #     )

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

        return self.repository.reject(
            proposal
        )
    
    # ==================================================
    # VALIDATION
    # ==================================================

    @staticmethod
    def _validate_confidence(
        confidence: float,
    ) -> None:

        if not isinstance(
            confidence,
            (int, float),
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

            isinstance(
                source,
                str,
            )
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
            str,
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
            str,
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
    
    # ==================================================
    # RESTORE REJECTED PROPOSAL
    # ==================================================

    def restore_rejected(
        self,
        skill_id: str,
    ) -> SkillEnrichmentProposal:

        return (
            self.repository.restore_rejected(
                skill_id
            )
        )