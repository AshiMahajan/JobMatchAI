from domains.skill_enrichment import (
    SkillEnrichmentProposal,
)

from repositories.knowledge_base_repository import (
    KnowledgeBaseRepository,
)


class KnowledgeBaseEnrichmentService:
    """
    Applies approved skill-enrichment proposals
    to the Skill Knowledge Base.

    Business rule:
    Only proposals with status='approved'
    may modify the Knowledge Base.
    """

    def __init__(
        self,
        repository: KnowledgeBaseRepository | None = None,
    ):

        self.repository = (
            repository
            if repository is not None
            else KnowledgeBaseRepository()
        )

    def apply_proposal(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> dict:

        self._validate_approved_proposal(
            proposal
        )

        existing_skill = (
            self.repository.get_skill(
                proposal.skill_id
            )
        )

        curated_skill = (
            self._build_curated_skill(
                proposal
            )
        )

        if existing_skill is not None:

            return self.repository.update_skill(
                proposal.skill_id,
                curated_skill,
            )

        return self.repository.add_skill(
            curated_skill
        )

    @staticmethod
    def _build_curated_skill(
        proposal: SkillEnrichmentProposal,
    ) -> dict:

        return {

            "id": proposal.skill_id,

            "name": proposal.name,

            "aliases": proposal.aliases,

            "category": proposal.category,

            "parent": proposal.parent,

            "related": proposal.related,

            "status": "curated",

            "prerequisites": (
                proposal.prerequisites
            ),

            "unlocks": proposal.unlocks,
        }

    @staticmethod
    def _validate_approved_proposal(
        proposal: SkillEnrichmentProposal,
    ) -> None:

        if proposal.status != "approved":

            raise ValueError(
                "Only approved enrichment "
                "proposals can update the "
                "Knowledge Base."
            )