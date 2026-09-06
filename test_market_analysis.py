from services.resume_service import (
    extract_resume_skills
)

from services.market_analysis_service import (
    MarketAnalysisService
)


def test_market_analysis():

    resume = extract_resume_skills(
        "MLE.pdf"
    )

    job_descriptions = [

        """
        Python
        Docker
        AWS
        Terraform
        Kubernetes
        """,

        """
        Python
        SQL
        Docker
        AWS
        Airflow
        """,

        """
        Python
        PySpark
        Databricks
        Snowflake
        AWS
        """

    ]

    service = MarketAnalysisService()

    result = service.analyze_jobs(

        resume.skills,

        job_descriptions

    )

    assert len(result) == 3

    for analysis in result:

        assert analysis.job_id >= 1

        assert isinstance(
            analysis.ats_score,
            float
        )

        assert isinstance(
            analysis.jd_skills,
            list
        )

        assert isinstance(
            analysis.missing_skills,
            list
        )