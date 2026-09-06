# from pydantic import BaseModel, Field


# class RoleJob(BaseModel):
#     """
#     Represents a Job Description inside a role cluster.
#     """

#     job_id: int

#     role: str | None = None

#     skills: list[str] = Field(
#         default_factory=list
#     )


# class RoleCluster(BaseModel):
#     """
#     Represents a group of semantically similar
#     Job Descriptions.
#     """

#     cluster_id: int

#     role: str

#     jobs: list[RoleJob] = Field(
#         default_factory=list
#     )

#     common_skills: list[str] = Field(
#         default_factory=list
#     )


# class JobSimilarity(BaseModel):
#     """
#     Represents semantic similarity between
#     two Job Descriptions.
#     """

#     job_id_a: int

#     job_id_b: int

#     similarity: float


# class RoleIntelligenceResult(BaseModel):
#     """
#     Complete role intelligence analysis.
#     """

#     jobs_analyzed: int

#     clusters: list[RoleCluster] = Field(
#         default_factory=list
#     )

#     similarities: list[JobSimilarity] = Field(
#         default_factory=list
#     )

# ----------------------------------------------------------------

from pydantic import BaseModel, Field


class RoleJob(BaseModel):
    """
    Represents one Job Description inside a role cluster.

    role:
        Explicitly detected job title when one can be
        identified from the Job Description.
        Otherwise None.
    """

    job_id: int

    role: str | None = None

    skills: list[str] = Field(
        default_factory=list
    )


class RoleCluster(BaseModel):
    """
    Represents a group of semantically similar
    Job Descriptions.

    The cluster itself receives a representative role.
    Individual jobs retain their own detected role.
    """

    cluster_id: int

    role: str

    jobs: list[RoleJob] = Field(
        default_factory=list
    )

    common_skills: list[str] = Field(
        default_factory=list
    )


class JobSimilarity(BaseModel):
    """
    Represents semantic similarity between two
    Job Descriptions.

    similarity:
        Cosine similarity produced by the sentence
        transformer embedding model.
    """

    job_id_a: int

    job_id_b: int

    similarity: float


class RoleIntelligenceResult(BaseModel):
    """
    Complete Role Intelligence analysis.

    Contains:
        - number of analyzed jobs
        - semantic role clusters
        - pairwise JD similarities
    """

    jobs_analyzed: int

    clusters: list[RoleCluster] = Field(
        default_factory=list
    )

    similarities: list[JobSimilarity] = Field(
        default_factory=list
    )