from pydantic import BaseModel


class JDRequest(BaseModel):
    job_description: str


class SkillRequest(BaseModel):
    skill: str


class CareerAnalysisRequest(BaseModel):
    job_descriptions: list[str]