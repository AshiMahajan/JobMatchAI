from pydantic import BaseModel, Field


class ATSResult(BaseModel):

    score: float

    match_level: str

    exact_matches: list[str] = Field(
        default_factory=list
    )

    alias_matches: list[str] = Field(
        default_factory=list
    )

    semantic_matches: list[str] = Field(
        default_factory=list
    )

    missing_skills: list[str] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
        default_factory=list
    )