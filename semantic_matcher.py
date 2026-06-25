# semantic_matcher.py

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

SIMILARITY_THRESHOLD = 0.70


def semantic_match(resume_skills, jd_skills):

    matched = []
    missing = []

    if not resume_skills or not jd_skills:
        return matched, jd_skills

    resume_embeddings = model.encode(
        resume_skills,
        convert_to_tensor=True
    )

    jd_embeddings = model.encode(
        jd_skills,
        convert_to_tensor=True
    )

    for jd_idx, jd_skill in enumerate(jd_skills):

        best_score = 0
        best_resume_skill = None

        for resume_idx, resume_skill in enumerate(resume_skills):

            similarity = cos_sim(
                resume_embeddings[resume_idx],
                jd_embeddings[jd_idx]
            ).item()

            if similarity > best_score:

                best_score = similarity
                best_resume_skill = resume_skill

        if (
            best_score >= SIMILARITY_THRESHOLD
            and best_resume_skill.lower() != jd_skill.lower()
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