from pydantic import BaseModel, Field


class RoadmapStep(BaseModel):
    """
    Represents one skill within a learning roadmap phase.
    """

    skill: str

    priority: int

    market_percentage: float

    occurrence_count: int

    status: str

    prerequisites: list[str] = Field(
        default_factory=list
    )

    missing_prerequisites: list[str] = Field(
        default_factory=list
    )

    unlocks: list[str] = Field(
        default_factory=list
    )

    dependency_impact: int = 0

    reason: str


class RoadmapPhase(BaseModel):
    """
    Represents a stage in the personalized
    learning roadmap.
    """

    phase: int

    skills: list[RoadmapStep] = Field(
        default_factory=list
    )


class LearningRoadmap(BaseModel):
    """
    Represents the complete personalized
    learning roadmap.
    """

    total_phases: int

    total_steps: int

    phases: list[RoadmapPhase] = Field(
        default_factory=list
    )