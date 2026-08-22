from domains.ats_result import ATSResult

from ats_engine import calculate_ats_score
from services.skill_service import SkillService


class ATSService:
    """
    Service responsible for ATS analysis
    between a resume and a single Job Description.
    """

    def __init__(self) -> None:
        self.skill_service = SkillService()

    def analyze_resume_vs_jd(
        self,
        resume_skills: list[str],
        job_description: str,
    ) -> ATSResult:
        """
        Analyze a resume against a single
        Job Description.
        """

        jd_skills = self.skill_service.extract_names(
            job_description
        )

        return calculate_ats_score(
            resume_skills,
            jd_skills,
        )