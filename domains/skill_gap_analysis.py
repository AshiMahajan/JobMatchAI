from pydantic import BaseModel, ConfigDict, Field

from domains.career_analysis import SkillFrequency


class SkillGapAnalysis(BaseModel):
    """
    Immutable domain model representing
    market skill gap analysis.

    Produced after analyzing multiple
    Job Descriptions.
    """

    model_config = ConfigDict(
        frozen=True
    )

    market_skills: list[SkillFrequency] = Field(
        default_factory=list
    )

    top_missing_skills: list[SkillFrequency] = Field(
        default_factory=list
    )

    resume_coverage: float