def get_match_level(
    score: float
) -> str:

    if score >= 80:
        return "Strong Match"

    if score >= 60:
        return "Good Match"

    if score >= 40:
        return "Moderate Match"

    return "Weak Match"


def generate_recommendations(
    missing_skills: list[str]
) -> list[str]:

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Consider gaining experience with {skill}"
        )

    return recommendations