from domains.career_analysis import CareerAnalysis

from services.learning_priority_service import (
    LearningPriorityService
)

from services.market_analysis_service import (
    MarketAnalysisService
)

from services.report_service import (
    ReportService
)

from services.skill_gap_service import (
    SkillGapService
)


class CareerService:
    """
    Orchestrates the complete Career Intelligence
    analysis pipeline.

    Responsibilities:
        - Analyze multiple Job Descriptions
        - Identify market skill gaps
        - Generate dependency-aware learning priorities
        - Generate the final Career Analysis report
    """

    def __init__(self) -> None:

        self.market_analysis_service = (
            MarketAnalysisService()
        )

        self.skill_gap_service = (
            SkillGapService()
        )

        self.learning_priority_service = (
            LearningPriorityService()
        )

        self.report_service = (
            ReportService()
        )

    def analyze_career(
        self,
        resume_skills: list[str],
        job_descriptions: list[str]
    ) -> CareerAnalysis:
        """
        Execute the complete Career Intelligence
        analysis pipeline.
        """

        # ==================================================
        # Market Analysis
        # ==================================================

        analyses = (
            self.market_analysis_service.analyze_jobs(
                resume_skills,
                job_descriptions
            )
        )

        # ==================================================
        # Average ATS Score
        # ==================================================

        average_ats_score = (
            self.market_analysis_service.calculate_average_ats(
                analyses
            )
        )

        # ==================================================
        # Skill Gap Analysis
        # ==================================================

        skill_gap_analysis = (
            self.skill_gap_service.analyze(
                analyses,
                resume_skills
            )
        )

        # ==================================================
        # Learning Priority Analysis
        # ==================================================

        learning_priorities = (
            self.learning_priority_service.generate_priorities(
                resume_skills=resume_skills,
                missing_skills=(
                    skill_gap_analysis.top_missing_skills
                )
            )
        )

        # ==================================================
        # Final Career Report
        # ==================================================

        return self.report_service.build_report(
            analyses=analyses,
            average_ats_score=average_ats_score,
            skill_gap_analysis=skill_gap_analysis,
            learning_priorities=learning_priorities
        )