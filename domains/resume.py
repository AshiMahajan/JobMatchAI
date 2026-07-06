from pydantic import BaseModel, Field


class ResumeProfile(BaseModel):

    resume_text: str = ""

    skills: list[str] = Field(
        default_factory=list
    )

    sections: dict[str, list[str]] = Field(
        default_factory=dict
    )

    projects: list[str] = Field(
        default_factory=list
    )

    experience: list[str] = Field(
        default_factory=list
    )

    education: list[str] = Field(
        default_factory=list
    )

    certifications: list[str] = Field(
        default_factory=list
    )