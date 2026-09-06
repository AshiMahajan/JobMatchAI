from pydantic import BaseModel, Field


class SkillResearchResult(BaseModel):

    skill_id: str

    name: str

    aliases: list[str] = Field(
        default_factory=list
    )

    category: str

    parent: str | None = None

    related: list[str] = Field(
        default_factory=list
    )

    prerequisites: list[str] = Field(
        default_factory=list
    )

    unlocks: list[str] = Field(
        default_factory=list
    )

    sources: list[str] = Field(
        default_factory=list
    )

    confidence: float