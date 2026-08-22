from pydantic import BaseModel, ConfigDict, Field


class ATSResult(BaseModel):
    """
    Immutable domain model representing the result
    of ATS analysis for a resume against a single
    Job Description.
    """

    model_config = ConfigDict(
        frozen=True
    )

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