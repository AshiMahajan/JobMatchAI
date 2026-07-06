import spacy

from spacy.matcher import PhraseMatcher

from core.config import (
    SKILL_VOCABULARY_PATH,
    SPACY_MODEL
)

from core.logger import logger


# ---------------------------------------
# Load spaCy model
# ---------------------------------------

try:

    nlp = spacy.load(
        SPACY_MODEL
    )

    logger.info(
        "spaCy model loaded: %s",
        SPACY_MODEL
    )

except OSError as error:

    logger.error(
        "spaCy model '%s' could not be loaded.",
        SPACY_MODEL
    )

    raise RuntimeError(
        "Required spaCy model is not installed."
    ) from error


matcher = PhraseMatcher(
    nlp.vocab,
    attr="LOWER"
)


# ---------------------------------------
# Load Skill Vocabulary
# ---------------------------------------

try:

    with open(
            SKILL_VOCABULARY_PATH,
            "r",
            encoding="utf-8"
    ) as file:

        skills = [

            line.strip()

            for line in file

            if line.strip()

            and not line.strip().startswith("#")

        ]

    logger.info(
        "Skill vocabulary loaded (%d skills).",
        len(skills)
    )

except FileNotFoundError as error:

    logger.error(
        "Skill vocabulary file not found: %s",
        SKILL_VOCABULARY_PATH
    )

    raise RuntimeError(
        "Skill vocabulary could not be loaded."
    ) from error


patterns = [

    nlp.make_doc(skill)

    for skill in skills

]

matcher.add(
    "SKILLS",
    patterns
)


# ---------------------------------------
# Skill Extraction
# ---------------------------------------

def extract_skills(
        text: str
) -> list[str]:

    doc = nlp(text)

    matches = matcher(doc)

    found = set()

    for _, start, end in matches:

        found.add(

            doc[start:end].text

        )

    return sorted(found)