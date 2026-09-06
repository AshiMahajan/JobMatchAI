from skill_extractor import extract_skills

from ats_engine import calculate_ats_score


def test_match():

    resume_text = """

    Machine Learning Engineer skilled in Python,

    AWS, Docker, TensorFlow and MongoDB.

    """

    jd_text = """

    Looking for candidates with Python,

    AWS, Docker, Kubernetes, FastAPI

    and TensorFlow.

    """

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        jd_text
    )

    result = calculate_ats_score(

        resume_skills,

        jd_skills

    )

    assert result.score >= 0

    assert result.score <= 100

    assert isinstance(
        result.exact_matches,
        list
    )

    assert isinstance(
        result.alias_matches,
        list
    )

    assert isinstance(
        result.semantic_matches,
        list
    )

    assert isinstance(
        result.missing_skills,
        list
    )