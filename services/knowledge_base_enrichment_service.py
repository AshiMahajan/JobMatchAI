from domains.skill_enrichment import (
    SkillEnrichmentProposal
)

from repositories.knowledge_base_repository import (
    KnowledgeBaseRepository
)


class KnowledgeBaseEnrichmentService:
    """
    Applies approved skill enrichment proposals
    to the Knowledge Base.

    Only proposals with status='approved' are allowed
    to modify the Knowledge Base.
    """

    def __init__(
        self,
        knowledge_base_repository=None,
    ):

        self.knowledge_base_repository = (
            knowledge_base_repository
            if knowledge_base_repository is not None
            else KnowledgeBaseRepository()
        )

    # ==================================================
    # APPLY PROPOSAL
    # ==================================================

    def apply_proposal(
        self,
        proposal: SkillEnrichmentProposal,
    ) -> dict:
        """
        Apply an approved enrichment proposal to
        the existing Knowledge Base skill.
        """

        self._validate_approved_proposal(
            proposal
        )

        existing_skill = (
            self.knowledge_base_repository.get_skill(
                proposal.skill_id
            )
        )

        if existing_skill is None:

            raise ValueError(
                f"Skill '{proposal.skill_id}' "
                "does not exist in Knowledge Base."
            )

        updated_skill = {

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

        return (
            self.knowledge_base_repository.update_skill(
                skill_id=proposal.skill_id,
                updated_skill=updated_skill,
            )
        )

    # ==================================================
    # VALIDATION
    # ==================================================

    @staticmethod
    def _validate_approved_proposal(
        proposal: SkillEnrichmentProposal,
    ) -> None:

        if proposal.status != "approved":

            raise ValueError(
                "Only proposals with status "
                "'approved' can be applied to "
                "the Knowledge Base."
            )