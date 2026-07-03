from fastapi import APIRouter

from schemas import SkillRequest

from skill_engine import SkillEngine

router = APIRouter()

engine = SkillEngine()


@router.post("/skill/intelligence")
def get_skill_intelligence(request: SkillRequest):

    canonical = engine.normalize(
        request.skill
    )

    info = engine.describe(
        request.skill
    )

    return {

        "input": request.skill,

        "canonical": canonical,

        "category": info["category"],

        "parent": info["parent"],

        "aliases": info["aliases"],

        "related": info["related"]
    }