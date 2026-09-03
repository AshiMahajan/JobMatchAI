from fastapi import APIRouter, HTTPException

from services.skill_enrichment_service import (
    SkillEnrichmentService,
)

from services.knowledge_base_enrichment_service import (
    KnowledgeBaseEnrichmentService,
)


router = APIRouter(
    prefix="/enrichment"
)


enrichment_service = SkillEnrichmentService()

kb_enrichment_service = (
    KnowledgeBaseEnrichmentService()
)


# ==================================================
# GET PENDING PROPOSALS
# ==================================================

@router.get("/pending")
def get_pending_enrichment_proposals():

    proposals = (
        enrichment_service.get_pending_proposals()
    )

    return {
        "count": len(proposals),
        "proposals": proposals,
    }


# ==================================================
# GET PROPOSAL
# ==================================================

@router.get("/{skill_id}")
def get_enrichment_proposal(
    skill_id: str,
):

    proposal = (
        enrichment_service.get_proposal(
            skill_id
        )
    )

    if proposal is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"No enrichment proposal found "
                f"for skill '{skill_id}'."
            ),
        )

    return proposal


# ==================================================
# APPROVE PROPOSAL
# ==================================================

@router.post("/{skill_id}/approve")
def approve_enrichment_proposal(
    skill_id: str,
):

    proposal = (
        enrichment_service.get_proposal(
            skill_id
        )
    )

    if proposal is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"No enrichment proposal found "
                f"for skill '{skill_id}'."
            ),
        )

    try:

        approved = (
            enrichment_service.approve_proposal(
                proposal
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": (
            "Enrichment proposal approved."
        ),
        "proposal": approved,
    }


# ==================================================
# APPLY APPROVED PROPOSAL
# ==================================================

@router.post("/{skill_id}/apply")
def apply_enrichment_proposal(
    skill_id: str,
):

    proposal = (
        enrichment_service.get_proposal(
            skill_id
        )
    )

    if proposal is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"No enrichment proposal found "
                f"for skill '{skill_id}'."
            ),
        )

    try:

        curated_skill = (
            kb_enrichment_service.apply_proposal(
                proposal
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {

        "message": (
            "Approved enrichment proposal "
            "applied to Knowledge Base."
        ),

        "skill": curated_skill,
    }


# ==================================================
# REJECT PROPOSAL
# ==================================================

@router.post("/{skill_id}/reject")
def reject_enrichment_proposal(
    skill_id: str,
):

    proposal = (
        enrichment_service.get_proposal(
            skill_id
        )
    )

    if proposal is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"No enrichment proposal found "
                f"for skill '{skill_id}'."
            ),
        )

    try:

        rejected = (
            enrichment_service.reject_proposal(
                proposal
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": (
            "Enrichment proposal rejected."
        ),
        "proposal": rejected,
    }