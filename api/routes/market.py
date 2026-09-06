from fastapi import APIRouter

from domains.role_intelligence import (
    RoleIntelligenceResult,
)

from schemas import MarketJobsRequest

from services.role_intelligence_service import (
    RoleIntelligenceService,
)


router = APIRouter()

role_intelligence_service = (
    RoleIntelligenceService()
)


@router.post(
    "/market/roles",
    response_model=RoleIntelligenceResult,
)
def analyze_roles(
    request: MarketJobsRequest,
) -> RoleIntelligenceResult:

    return role_intelligence_service.analyze(
        request.job_descriptions
    )