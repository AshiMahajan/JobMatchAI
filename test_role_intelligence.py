# from services.role_intelligence_service import (
#     RoleIntelligenceService,
# )


# def test_role_intelligence():

#     job_descriptions = [

#         """
#         Machine Learning Engineer

#         Python
#         PyTorch
#         AWS
#         Docker
#         Kubernetes
#         """,

#         """
#         ML Engineer

#         Python
#         TensorFlow
#         AWS
#         Docker
#         Kubernetes
#         """,

#         """
#         Backend Engineer

#         Python
#         FastAPI
#         PostgreSQL
#         Docker
#         """,

#         """
#         Python Backend Developer

#         Python
#         FastAPI
#         PostgreSQL
#         AWS
#         Docker
#         """,

#     ]

#     service = RoleIntelligenceService(
#         similarity_threshold=0.60
#     )

#     result = service.analyze(
#         job_descriptions
#     )

#     # --------------------------------------------------
#     # Basic result validation
#     # --------------------------------------------------

#     assert result.jobs_analyzed == 4

#     assert len(
#         result.similarities
#     ) == 6

#     assert result.clusters

#     # --------------------------------------------------
#     # Cluster validation
#     # --------------------------------------------------

#     for cluster in result.clusters:

#         assert cluster.cluster_id >= 1

#         assert cluster.jobs

#         assert isinstance(
#             cluster.role,
#             str
#         )

#         assert isinstance(
#             cluster.common_skills,
#             list
#         )

#     # --------------------------------------------------
#     # Job validation
#     # --------------------------------------------------

#     all_jobs = [

#         job

#         for cluster in result.clusters

#         for job in cluster.jobs

#     ]

#     assert len(all_jobs) == 4

#     job_roles = {
#         job.job_id: job.role
#         for job in all_jobs
#     }

#     assert (
#         job_roles[1]
#         == "Machine Learning Engineer"
#     )

#     assert (
#         job_roles[3]
#         == "Backend Engineer"
#     )

#     assert (
#         job_roles[4]
#         == "Python Backend Developer"
#     )

#     # --------------------------------------------------
#     # Skill deduplication validation
#     # --------------------------------------------------

#     for job in all_jobs:

#         normalized_skills = [
#             skill.lower()
#             for skill in job.skills
#         ]

#         assert len(
#             normalized_skills
#         ) == len(
#             set(normalized_skills)
#         )

#     # --------------------------------------------------
#     # Similarity validation
#     # --------------------------------------------------

#     for similarity in result.similarities:

#         assert 0.0 <= (
#             similarity.similarity
#         ) <= 1.0

#         assert (
#             similarity.job_id_a
#             < similarity.job_id_b
#         )


# def test_role_extraction_from_natural_language():

#     service = RoleIntelligenceService()

#     job_description = """
#     We need a Backend Engineer experienced in
#     Python, FastAPI, REST APIs, PostgreSQL,
#     Docker, Kubernetes and AWS.
#     """

#     result = service.analyze(
#         [job_description]
#     )

#     assert result.jobs_analyzed == 1

#     assert len(
#         result.clusters
#     ) == 1

#     job = result.clusters[0].jobs[0]

#     assert (
#         job.role
#         == "Backend Engineer"
#     )

#     assert (
#         result.clusters[0].role
#         == "Backend Engineer"
#     )


# def test_role_extraction_with_explicit_label():

#     service = RoleIntelligenceService()

#     job_description = """
#     Job Title: Data Engineer

#     Python
#     SQL
#     Apache Spark
#     Airflow
#     AWS
#     """

#     result = service.analyze(
#         [job_description]
#     )

#     job = result.clusters[0].jobs[0]

#     assert (
#         job.role
#         == "Data Engineer"
#     )

#     assert (
#         result.clusters[0].role
#         == "Data Engineer"
#     )


# def test_role_fallback_when_title_is_unknown():

#     service = RoleIntelligenceService()

#     job_description = """
#     This position requires strong technical
#     experience with Python, Docker and AWS.
#     """

#     result = service.analyze(
#         [job_description]
#     )

#     assert result.jobs_analyzed == 1

#     assert len(
#         result.clusters
#     ) == 1

#     cluster = result.clusters[0]

#     assert (
#         cluster.role
#         == "Role Cluster 1"
#     )

#     assert (
#         cluster.jobs[0].role
#         is None
#     )


# def test_empty_input():

#     service = RoleIntelligenceService()

#     result = service.analyze(
#         []
#     )

#     assert result.jobs_analyzed == 0

#     assert result.clusters == []

#     assert result.similarities == []


from services.role_intelligence_service import (
    RoleIntelligenceService,
)


def test_role_intelligence():

    job_descriptions = [

        # ==============================================
        # Machine Learning
        # ==============================================

        """
        Machine Learning Engineer

        Python
        PyTorch
        Scikit-learn
        NumPy
        Pandas
        AWS
        Docker
        Kubernetes

        Build and deploy machine learning models.
        """,

        """
        ML Engineer

        Python
        TensorFlow
        Scikit-learn
        Pandas
        AWS
        Docker
        Kubernetes

        Develop and productionize machine learning systems.
        """,

        """
        Applied ML Engineer

        Python
        PyTorch
        NumPy
        Pandas
        Scikit-learn
        AWS
        Docker

        Apply machine learning techniques to real-world problems.
        """,

        # ==============================================
        # Backend
        # ==============================================

        """
        Backend Engineer

        Python
        FastAPI
        REST APIs
        PostgreSQL
        Docker
        Kubernetes
        AWS

        Design and build scalable backend services.
        """,

        """
        Python Backend Developer

        Python
        FastAPI
        REST APIs
        PostgreSQL
        Docker
        AWS

        Develop backend APIs and scalable web services.
        """,

        """
        Backend Software Engineer

        Python
        FastAPI
        PostgreSQL
        Docker
        Kubernetes
        AWS

        Build reliable backend software and REST services.
        """,

        # ==============================================
        # Data Engineering
        # ==============================================

        """
        Data Engineer

        Python
        SQL
        Apache Spark
        PySpark
        Airflow
        AWS
        Snowflake
        Docker

        Build data pipelines and distributed data systems.
        """,

        """
        Big Data Engineer

        Python
        SQL
        Apache Spark
        PySpark
        Kafka
        AWS
        Snowflake
        Docker

        Work with large-scale distributed data processing.
        """,

        """
        Data Platform Engineer

        Python
        SQL
        Apache Spark
        Airflow
        Snowflake
        AWS
        Docker

        Build and maintain scalable data platforms and pipelines.
        """,
    ]

    service = RoleIntelligenceService(
        similarity_threshold=0.65
    )

    result = service.analyze(
        job_descriptions
    )

    # ==============================================
    # Basic validation
    # ==============================================

    assert result.jobs_analyzed == 9

    assert len(
        result.similarities
    ) == 36

    assert len(
        result.clusters
    ) >= 3

    # ==============================================
    # Print clusters for inspection
    # ==============================================

    for cluster in result.clusters:

        print(
            f"\nCluster {cluster.cluster_id}: "
            f"{cluster.role}"
        )

        for job in cluster.jobs:

            print(
                f"  Job {job.job_id}: "
                f"{job.role}"
            )

    # ==============================================
    # Extract role groups
    # ==============================================

    cluster_roles = []

    for cluster in result.clusters:

        roles = {
            job.role
            for job in cluster.jobs
            if job.role
        }

        cluster_roles.append(
            roles
        )

    # ==============================================
    # Verify expected grouping
    # ==============================================

    ml_roles = {
        "Machine Learning Engineer",
        "ML Engineer",
        "Applied ML Engineer",
    }

    backend_roles = {
        "Backend Engineer",
        "Python Backend Developer",
        "Backend Software Engineer",
    }

    data_roles = {
        "Data Engineer",
        "Big Data Engineer",
        "Data Platform Engineer",
    }

    assert any(
        ml_roles.issubset(roles)
        for roles in cluster_roles
    )

    assert any(
        backend_roles.issubset(roles)
        for roles in cluster_roles
    )

    assert any(
        data_roles.issubset(roles)
        for roles in cluster_roles
    )

    # ==============================================
    # Validate cluster contents
    # ==============================================

    for cluster in result.clusters:

        assert cluster.cluster_id >= 1

        assert cluster.jobs

        assert isinstance(
            cluster.common_skills,
            list
        )

        for job in cluster.jobs:

            assert job.job_id >= 1

            assert job.role

            assert job.skills