from collections import Counter

from domains.career_analysis import JobAnalysis, SkillFrequency
from domains.skill_gap_analysis import SkillGapAnalysis


class SkillGapService:
    """
    Performs market skill-gap analysis using the
    results of multiple Job Description analyses.

    Responsibilities:
        - Calculate market skill frequency
        - Calculate missing skill frequency
        - Calculate resume market coverage
    """

    def analyze(
        self,
        analyses: list[JobAnalysis],
        resume_skills: list[str]
    ) -> SkillGapAnalysis:
        """
        Generate a complete Skill Gap Analysis.
        """

        market_skills = self._get_market_skills(
            analyses
        )

        top_missing_skills = self._get_top_missing_skills(
            analyses
        )

        resume_coverage = self._calculate_resume_coverage(
            resume_skills,
            market_skills
        )

        return SkillGapAnalysis(
            market_skills=market_skills,
            top_missing_skills=top_missing_skills,
            resume_coverage=resume_coverage
        )

    def _get_market_skills(
        self,
        analyses: list[JobAnalysis]
    ) -> list[SkillFrequency]:

        counter = self._build_frequency(
            analysis.jd_skills
            for analysis in analyses
        )

        total_jobs = len(analyses)

        return self._to_skill_frequency(
            counter,
            total_jobs
        )

    def _get_top_missing_skills(
        self,
        analyses: list[JobAnalysis]
    ) -> list[SkillFrequency]:

        counter = self._build_frequency(
            analysis.missing_skills
            for analysis in analyses
        )

        total_jobs = len(analyses)

        return self._to_skill_frequency(
            counter,
            total_jobs
        )

    def _calculate_resume_coverage(
        self,
        resume_skills: list[str],
        market_skills: list[SkillFrequency]
    ) -> float:
        """
        Calculates percentage of market skills
        covered by the resume.
        """

        if not market_skills:
            return 0.0

        resume_set = {
            skill.lower()
            for skill in resume_skills
        }

        market_set = {
            skill.skill.lower()
            for skill in market_skills
        }

        covered = len(
            resume_set.intersection(
                market_set
            )
        )

        return round(
            covered / len(market_set) * 100,
            2
        )

    @staticmethod
    def _build_frequency(
        skill_lists
    ) -> Counter:

        counter = Counter()

        for skills in skill_lists:
            counter.update(skills)

        return counter

    @staticmethod
    def _to_skill_frequency(
        counter: Counter,
        total_jobs: int
    ) -> list[SkillFrequency]:
        """
        Convert Counter into sorted
        SkillFrequency objects.
        """

        if total_jobs == 0:
            return []

        frequencies = []

        sorted_items = sorted(
            counter.items(),
            key=lambda item: (-item[1], item[0].lower())
        )

        for skill, count in sorted_items:

            frequencies.append(
                SkillFrequency(
                    skill=skill,
                    occurrence_count=count,
                    market_percentage=round(
                        count / total_jobs * 100,
                        2
                    )
                )
            )

        return frequencies