from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)

import json
import shutil

from schemas import CareerAnalysisRequest

from core.config import UPLOADS_DIR
from core.logger import logger

from services.resume_service import extract_resume_skills
from services.career_service import CareerService

router = APIRouter()

career_service = CareerService()


@router.post("/career-analysis")
async def analyze_career(

    resume_file: UploadFile = File(...),

    job_descriptions: str = Form(...)

):

    if not resume_file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )

    try:

        request = CareerAnalysisRequest(
            job_descriptions=json.loads(job_descriptions)
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail="Invalid job_descriptions format."
        ) from error

    UPLOADS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = UPLOADS_DIR / resume_file.filename

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

        result = career_service.analyze_career(

            resume.skills,

            request.job_descriptions

        )

        logger.info(
            "Career analysis completed successfully."
        )

        return result

    except Exception as error:

        logger.exception(
            "Career analysis failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to perform career analysis."
        ) from error

    finally:

        if temp_path.exists():

            temp_path.unlink()