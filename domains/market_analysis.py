from pydantic import BaseModel, Field


class JobMarketResult(BaseModel):

    job_id: int

    jd_skills: list[str]

    score: float

    matched_skills: list[str] = Field(
        default_factory=list
    )

    semantic_matches: list[str] = Field(
        default_factory=list
    )

    missing_skills: list[str] = Field(
        default_factory=list
    )


class MarketAnalysisResult(BaseModel):

    jobs: list[JobMarketResult] = Field(
        default_factory=list
    )