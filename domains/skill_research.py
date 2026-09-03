from dataclasses import dataclass


@dataclass
class SkillResearchResult:
    """
    Represents the researched information
    collected for a skill.

    This object does not modify the
    Knowledge Base.
    """

    skill_id: str

    name: str

    aliases: list[str]

    category: str

    parent: str | None

    related: list[str]

    prerequisites: list[str]

    unlocks: list[str]

    sources: list[str]

    confidence: float