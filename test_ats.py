from ats_engine import calculate_ats_score


def test_ats_alias_matching():

    resume_skills = [

        "python",

        "aws",

        "docker"

    ]

    jd_skills = [

        "python",

        "amazon web services",

        "docker"

    ]

    result = calculate_ats_score(

        resume_skills,

        jd_skills

    )

    assert result.score > 0

    assert "python" in result.exact_matches

    assert "docker" in result.exact_matches

    assert len(result.alias_matches) == 1

    assert result.alias_matches[0].resume_skill == "aws"

    assert (
        result.alias_matches[0].jd_skill
        == "amazon web services"
    )