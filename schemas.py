from pydantic import BaseModel

from pydantic import BaseModel, Field


class MarketJobsRequest(BaseModel):

    job_descriptions: list[str] = Field(
        min_length=1
    )

class JDRequest(BaseModel):
    job_description: str


class SkillRequest(BaseModel):
    skill: str


class CareerAnalysisRequest(BaseModel):
    job_descriptions: list[str]