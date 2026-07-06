import json

from core.config import (
    SKILL_VOCABULARY_PATH,
    KNOWLEDGE_BASE_PATH
)

from core.logger import logger


SKILLS_FILE = SKILL_VOCABULARY_PATH

KNOWLEDGE_BASE_FILE = KNOWLEDGE_BASE_PATH


def load_skills() -> list[str]:

    with open(
            SKILLS_FILE,
            "r",
            encoding="utf-8"
    ) as file:

        return sorted({

            line.strip()

            for line in file

            if line.strip()

            and not line.strip().startswith("#")

        })


def load_knowledge_base() -> list[dict]:

    with open(
            KNOWLEDGE_BASE_FILE,
            "r",
            encoding="utf-8"
    ) as file:

        return json.load(file)


def save_knowledge_base(
        knowledge_base: list[dict]
) -> None:

    knowledge_base.sort(
        key=lambda skill: skill["name"].lower()
    )

    with open(
            KNOWLEDGE_BASE_FILE,
            "w",
            encoding="utf-8"
    ) as file:

        json.dump(
            knowledge_base,
            file,
            indent=4,
            ensure_ascii=False
        )


def create_placeholder(
        skill_name: str
) -> dict:

    return {

        "id": (
            skill_name
            .lower()
            .replace(" ", "_")
        ),

        "name": skill_name,

        "aliases": [
            skill_name.lower()
        ],

        "category": "Pending",

        "parent": None,

        "related": [],

        "status":"pending"

    }


def sync_knowledge_base() -> int:

    skills = load_skills()

    knowledge_base = load_knowledge_base()

    existing_skills = {

        skill["name"].lower()

        for skill in knowledge_base

    }

    added = 0

    for skill in skills:

        if skill.lower() in existing_skills:

            continue

        knowledge_base.append(

            create_placeholder(
                skill
            )

        )

        added += 1

    save_knowledge_base(
        knowledge_base
    )

    logger.info("=" * 50)

    logger.info(
        "Knowledge Base Synchronization Complete"
    )

    logger.info(
        "Skills in vocabulary : %d",
        len(skills)
    )

    logger.info(
        "Knowledge Base size  : %d",
        len(knowledge_base)
    )

    logger.info(
        "New placeholders     : %d",
        added
    )

    logger.info("=" * 50)

    return added


if __name__ == "__main__":

    sync_knowledge_base()