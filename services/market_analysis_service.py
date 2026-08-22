from collections import Counter

from ats_engine import calculate_ats_score
from domains.career_analysis import JobAnalysis
from services.skill_service import SkillService


class MarketAnalysisService:
    """
    Performs analysis of multiple job descriptions against a
    candidate's resume.

    Responsibilities:
        - Extract skills from each Job Description.
        - Compute ATS score for every JD.
        - Return structured JobAnalysis objects.

    This service intentionally does NOT compute:
        - Skill frequency
        - Skill gap ranking
        - Learning roadmap
        - Career recommendations

    Those belong to their respective services.
    """

    def __init__(self) -> None:
        self.skill_service = SkillService()

    def analyze_jobs(
        self,
        resume_skills: list[str],
        job_descriptions: list[str]
    ) -> list[JobAnalysis]:
        """
        Analyze a collection of Job Descriptions.

        Parameters
        ----------
        resume_skills : list[str]
            Skills extracted from the resume.

        job_descriptions : list[str]
            Raw Job Description texts.

        Returns
        -------
        list[JobAnalysis]
            Analysis result for every Job Description.
        """

        analyses: list[JobAnalysis] = []

        for job_id, jd_text in enumerate(job_descriptions, start=1):

            analysis = self._analyze_single_job(
                job_id=job_id,
                resume_skills=resume_skills,
                job_description=jd_text
            )

            analyses.append(analysis)

        return analyses

    def calculate_skill_frequency(
        self,
        analyses: list[JobAnalysis]
    ) -> Counter:
        """
        Calculate how frequently each skill appears
        across all analyzed Job Descriptions.
        """

        counter: Counter = Counter()

        for analysis in analyses:
            counter.update(analysis.jd_skills)

        return counter

    def calculate_average_ats(
        self,
        analyses: list[JobAnalysis]
    ) -> float:
        """
        Calculate the average ATS score across
        all analyzed Job Descriptions.
        """

        if not analyses:
            return 0.0

        total_score = sum(
            analysis.ats_score
            for analysis in analyses
        )

        return round(
            total_score / len(analyses),
            2
        )

    def _analyze_single_job(
        self,
        job_id: int,
        resume_skills: list[str],
        job_description: str,
        ) -> JobAnalysis:
        """
        Analyze one Job Description.
        """

        jd_skills = self.skill_service.extract_names(
            job_description
        )

        ats_result = calculate_ats_score(
            resume_skills,
            jd_skills,
        )

        return JobAnalysis(

        job_id=job_id,

        ats_score=ats_result.score,

        jd_skills=jd_skills,

        matched_skills=(
            ats_result.exact_matches
            +
            ats_result.alias_matches
        ),

        semantic_matches=ats_result.semantic_matches,

        missing_skills=ats_result.missing_skills,
    )