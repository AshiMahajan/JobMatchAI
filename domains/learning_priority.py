from pydantic import BaseModel, Field


class LearningPriority(BaseModel):
    """
    Represents the learning priority of a missing skill.

    Priority is determined by the Learning Priority Engine
    using market demand, dependency impact, and readiness.
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

    dependency_impact: int = 0

    readiness: str = "ready"

    reason: str