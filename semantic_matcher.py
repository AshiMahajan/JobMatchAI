from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from core.config import (
    SENTENCE_TRANSFORMER_MODEL,
    SEMANTIC_SIMILARITY_THRESHOLD
)

from core.logger import logger


try:

    embedding_model = SentenceTransformer(
        SENTENCE_TRANSFORMER_MODEL
    )

    logger.info(
        "Sentence Transformer loaded: %s",
        SENTENCE_TRANSFORMER_MODEL
    )

except Exception as error:

    logger.error(
        "Failed to initialize Sentence Transformer: %s",
        SENTENCE_TRANSFORMER_MODEL
    )

    raise RuntimeError(
        "Embedding model could not be initialized."
    ) from error


def semantic_match(
        resume_skills: list[str],
        jd_skills: list[str]
) -> tuple[list[dict], list[str]]:

    matched = []

    missing = []

    if not resume_skills or not jd_skills:

        return matched, jd_skills

    resume_embeddings = embedding_model.encode(

        resume_skills,

        convert_to_tensor=True

    )

    jd_embeddings = embedding_model.encode(

        jd_skills,

        convert_to_tensor=True

    )

    for jd_index, jd_skill in enumerate(jd_skills):

        best_score = 0.0

        best_resume_skill = None

        for resume_index, resume_skill in enumerate(resume_skills):

            similarity = cos_sim(

                resume_embeddings[resume_index],

                jd_embeddings[jd_index]

            ).item()

            if similarity > best_score:

                best_score = similarity

                best_resume_skill = resume_skill

        if (

            best_score >= SEMANTIC_SIMILARITY_THRESHOLD

            and

            best_resume_skill.lower() != jd_skill.lower()

        ):

            matched.append({

                "resume_skill": best_resume_skill,

                "jd_skill": jd_skill,

                "similarity": round(
                    best_score,
                    4
                )

            })

        else:

            missing.append(
                jd_skill
            )

    return matched, missing