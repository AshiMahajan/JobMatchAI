from parser import extract_text_from_pdf

from services.resume_service import (
    extract_resume_skills
)

from services.market_analysis_service import (
    analyze_market
)

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

result = analyze_market(

    resume["resume_skills"],

    job_descriptions

)

from pprint import pprint

pprint(result)