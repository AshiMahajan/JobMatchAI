# services/recommendation_service.py

def get_match_level(score):

    if score >= 80:
        return "Strong Match"

    elif score >= 60:
        return "Good Match"

    elif score >= 40:
        return "Moderate Match"

    else:
        return "Weak Match"


def generate_recommendations(
        missing_skills):

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Consider gaining experience with {skill}"
        )

    return recommendations