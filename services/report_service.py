from domains.career_analysis import (
    CareerAnalysis,
    JobAnalysis
)

from domains.learning_priority import (
    LearningPriority
)

from domains.skill_gap_analysis import (
    SkillGapAnalysis
)


class ReportService:
    """
    Responsible for constructing the final
    CareerAnalysis domain model.

    This service performs no business logic.
    It simply assembles the results produced
    by other services.
    """

    def build_report(
        self,
        analyses: list[JobAnalysis],
        average_ats_score: float,
        skill_gap_analysis: SkillGapAnalysis,
        learning_priorities: list[LearningPriority]
    ) -> CareerAnalysis:
        """
        Build the final CareerAnalysis report.
        """

        return CareerAnalysis(

            jobs_analyzed=len(
                analyses
            ),

            average_ats_score=(
                average_ats_score
            ),

            resume_coverage=(
                skill_gap_analysis.resume_coverage
            ),

            market_skills=(
                skill_gap_analysis.market_skills
            ),

            top_missing_skills=(
                skill_gap_analysis.top_missing_skills
            ),

            learning_priorities=(
                learning_priorities
            ),

            job_results=(
                analyses
            )
        )