from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

import os
import shutil

from schemas import JDRequest

from services.resume_service import (
    extract_resume_skills
)

from services.ats_service import (
    analyze_resume_vs_jd
)

from services.skill_service import (
    SkillService
)

from api.router import router


app = FastAPI(

    title="JobMatch AI",

    version="1.0"

)

app.include_router(router)

skill_service = SkillService()


@app.get("/")
def home():

    return {

        "message": "JobMatch AI API Running"

    }


@app.get("/health")
def health():

    return {

        "status": "healthy"

    }


@app.post("/extract-jd-skills")
def extract_jd_skills(
        request: JDRequest
):

    return {

        "skills":

        skill_service.extract(

            request.job_description

        )

    }


@app.post("/analyze")
async def analyze_resume_jd(

        resume_file: UploadFile = File(...),

        job_description: str = Form(...)
):

    temp_path = (

        f"uploads/{resume_file.filename}"

    )

    with open(

            temp_path,

            "wb"

    ) as buffer:

        shutil.copyfileobj(

            resume_file.file,

            buffer

        )

    resume = extract_resume_skills(

        temp_path

    )

    result = analyze_resume_vs_jd(

        resume.skills,

        job_description

    )

    os.remove(

        temp_path

    )

    return result