from dataclasses import dataclass


@dataclass
class SkillEnrichmentProposal:
    """
    Represents a proposed enrichment for a skill
    that is currently pending in the Knowledge Base.

    This is a proposal only.
    It must be reviewed before the Knowledge Base
    is modified.
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

    status: str = "pending"