from pydantic import BaseModel, ConfigDict, Field

from domains.learning_priority import LearningPriority


class SkillFrequency(BaseModel):
    """
    Represents the frequency of a skill
    across analyzed Job Descriptions.
    """

    model_config = ConfigDict(
        frozen=True
    )

    skill: str

    occurrence_count: int

    market_percentage: float


class JobAnalysis(BaseModel):
    """
    Analysis result of a single Job Description.
    """

    model_config = ConfigDict(
        frozen=True
    )

    job_id: int

    ats_score: float

    jd_skills: list[str] = Field(
        default_factory=list
    )

    matched_skills: list[str] = Field(
        default_factory=list
    )

    semantic_matches: list[str] = Field(
        default_factory=list
    )

    missing_skills: list[str] = Field(
        default_factory=list
    )


class CareerAnalysis(BaseModel):
    """
    Complete Career Intelligence analysis.

    Contains:
        - Overall ATS performance
        - Market skill demand
        - Skill gaps
        - Dependency-aware learning priorities
        - Individual Job Description results
    """

    jobs_analyzed: int

    average_ats_score: float

    resume_coverage: float

    market_skills: list[SkillFrequency] = Field(
        default_factory=list
    )

    top_missing_skills: list[SkillFrequency] = Field(
        default_factory=list
    )

    learning_priorities: list[LearningPriority] = Field(
        default_factory=list
    )

    job_results: list[JobAnalysis] = Field(
        default_factory=list
    )