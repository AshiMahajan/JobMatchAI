from pydantic import BaseModel, Field


class SkillDependency(BaseModel):
    """
    Represents the dependency relationships of a skill.
    """

    skill: str

    prerequisites: list[str] = Field(
        default_factory=list
    )

    unlocks: list[str] = Field(
        default_factory=list
    )

    related: list[str] = Field(
        default_factory=list
    )