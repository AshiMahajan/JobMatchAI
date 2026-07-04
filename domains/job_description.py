from pydantic import BaseModel, Field


class JobDescription(BaseModel):

    raw_text: str

    skills: list[str] = Field(
        default_factory=list
    )