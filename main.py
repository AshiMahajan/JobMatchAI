from fastapi import FastAPI

from fastapi import FastAPI, UploadFile, File, Form
from parser import extract_text_from_pdf
from resume_analyzer import analyze_resume
from skill_extractor import extract_skills
from ats_engine import calculate_ats_score
from skill_engine import SkillEngine
from schemas import JDRequest, SkillRequest

from services.resume_service import (
    extract_resume_skills
)

from services.ats_service import (
    analyze_resume_vs_jd
)

import os
import shutil

app = FastAPI(
    title="JobMatch AI",
    version="1.0"
)

from api.router import router
app.include_router(router)

skill_engine = SkillEngine()

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
        request: JDRequest):

    skills = extract_skills(
        request.job_description
    )

    return {
        "skills": skills
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

    resume_data = (
        extract_resume_skills(
            temp_path
        )
    )

    result = analyze_resume_vs_jd(
        resume_data["resume_skills"],
        job_description
    )

    os.remove(temp_path)

    return result

# @app.post("/skill/intelligence")
# def get_skill_intelligence(request: SkillRequest):

#     canonical = skill_engine.normalize(request.skill)

#     info = skill_engine.describe(request.skill)

#     return {
#         "input": request.skill,
#         "canonical": canonical,
#         "category": info["category"],
#         "parent": info["parent"],
#         "aliases": info.get("aliases", []),
#         "related": info["related"]
#     }