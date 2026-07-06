from fastapi import APIRouter

from schemas import SkillRequest

from skill_engine import SkillEngine


router = APIRouter()

engine = SkillEngine()


@router.post("/skill/intelligence")
def skill_intelligence(
        request: SkillRequest
):

    info = engine.describe(
        request.skill
    )

    return {

        "query": request.skill,

        "canonical": info["name"],

        "category": info["category"],

        "parent": info["parent"],

        "aliases": info["aliases"],

        "related": info["related"],

        "status": info["status"]

    }