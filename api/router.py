from fastapi import APIRouter

from api.routes.resume import (
    router as resume_router
)

from api.routes.analysis import (
    router as ats_router
)

from api.routes.skills import (
    router as skill_router
)

from api.routes.market import (
    router as market_router
)

from api.routes.career import (
    router as career_router
)

from api.routes.enrichment import (
    router as enrichment_router
)


router = APIRouter()


router.include_router(
    resume_router,
    tags=["Resume"]
)


router.include_router(
    ats_router,
    tags=["ATS"]
)


router.include_router(
    skill_router,
    tags=["Skills"]
)


router.include_router(
    market_router,
    tags=["Market"]
)


router.include_router(
    career_router,
    tags=["Career"]
)


router.include_router(
    enrichment_router,
    tags=["Enrichment"]
)