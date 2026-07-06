from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
)

import os
import shutil

from core.config import UPLOADS_DIR
from schemas import JDRequest

from services.resume_service import (
    extract_resume_skills,
)

from services.ats_service import (
    analyze_resume_vs_jd,
)

from services.skill_service import (
    SkillService,
)

from api.router import router

from fastapi import HTTPException

from core.config import (
    UPLOADS_DIR
)

from core.logger import logger

from core.config import (
    UPLOADS_DIR
)

app = FastAPI(
    title="JobMatch AI",
    version="1.0",
)

app.include_router(router)

skill_service = SkillService()


@app.get("/")
def home() -> dict:

    return {
        "message": "JobMatch AI API Running"
    }


@app.get("/health")
def health() -> dict:

    return {
        "status": "healthy"
    }


@app.post("/extract-jd-skills")
def extract_jd_skills(
        request: JDRequest
) -> dict:

    return {

        "skills": skill_service.extract(

            request.job_description

        )

    }


@app.post("/analyze")
async def analyze_resume_jd(

        resume_file: UploadFile = File(...),

        job_description: str = Form(...)

):

    if not resume_file.filename.lower().endswith(".pdf"):

        logger.error(
            "Unsupported file type uploaded: %s",
            resume_file.filename
        )

        raise HTTPException(
        status_code=400,
        detail="Only PDF resumes are currently supported."
        )

    UPLOADS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = (
        UPLOADS_DIR / resume_file.filename
    )

    try:

        with open(
                temp_path,
                "wb"
        ) as buffer:

            shutil.copyfileobj(
                resume_file.file,
                buffer
            )

        resume = extract_resume_skills(
            str(temp_path)
        )

        result = analyze_resume_vs_jd(

            resume.skills,

            job_description

        )

        logger.info(
            "Resume analyzed successfully: %s",
            resume_file.filename
        )

        return result

    except Exception as error:

        logger.error(
            "Resume analysis failed: %s",
            resume_file.filename
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to analyze the uploaded resume."
        ) from error

    finally:

        if temp_path.exists():

            temp_path.unlink()