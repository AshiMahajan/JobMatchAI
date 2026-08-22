from pydantic import BaseModel, Field


class LearningPriority(BaseModel):
    """
    Represents the learning priority of a missing skill.

    The model contains both market-demand information
    and dependency information so that learning
    recommendations remain explainable.
    """

    skill: str

    priority: int

    market_percentage: float

    occurrence_count: int

    prerequisites: list[str] = Field(
        default_factory=list
    )

    missing_prerequisites: list[str] = Field(
        default_factory=list
    )

    reason: str