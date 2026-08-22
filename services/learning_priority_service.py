from domains.learning_priority import LearningPriority
from domains.career_analysis import SkillFrequency

from services.skill_dependency_service import (
    SkillDependencyService
)


class LearningPriorityService:
    """
    Generates dependency-aware learning priorities.

    Learning order is determined using:

        1. Missing market skills
        2. Skill prerequisites
        3. Candidate's existing skills
        4. Market demand

    Prerequisite relationships take precedence over
    raw market demand.

    This prevents advanced skills from being recommended
    before their missing foundations.
    """

    def __init__(self) -> None:

        self.dependency_service = (
            SkillDependencyService()
        )

    def generate_priorities(
        self,
        resume_skills: list[str],
        missing_skills: list[SkillFrequency]
    ) -> list[LearningPriority]:
        """
        Generate an ordered learning priority list.

        Parameters
        ----------
        resume_skills:
            Skills already possessed by the candidate.

        missing_skills:
            Missing market skills produced by the
            Career Intelligence Engine.

        Returns
        -------
        list[LearningPriority]
            Dependency-aware learning priorities.
        """

        if not missing_skills:

            return []

        resume_skill_set = {
            skill.lower()
            for skill in resume_skills
        }

        market_skill_lookup = {
            item.skill.lower(): item
            for item in missing_skills
        }

        ordered_skills: list[str] = []

        visited: set[str] = set()

        visiting: set[str] = set()

        # Highest-demand skills are considered first.
        sorted_missing_skills = sorted(
            missing_skills,
            key=lambda item: (
                -item.market_percentage,
                item.skill.lower()
            )
        )

        for market_skill in sorted_missing_skills:

            self._resolve_learning_order(
                skill_name=market_skill.skill,
                resume_skill_set=resume_skill_set,
                market_skill_lookup=market_skill_lookup,
                ordered_skills=ordered_skills,
                visited=visited,
                visiting=visiting
            )

        priorities: list[LearningPriority] = []

        for priority_number, skill_name in enumerate(
            ordered_skills,
            start=1
        ):

            market_data = market_skill_lookup.get(
                skill_name.lower()
            )

            dependency = (
                self.dependency_service.get_dependency(
                    skill_name
                )
            )

            missing_prerequisites = [

                prerequisite

                for prerequisite
                in dependency.prerequisites

                if prerequisite.lower()
                not in resume_skill_set

            ]

            priorities.append(

                LearningPriority(

                    skill=skill_name,

                    priority=priority_number,

                    market_percentage=(
                        market_data.market_percentage
                        if market_data
                        else 0.0
                    ),

                    occurrence_count=(
                        market_data.occurrence_count
                        if market_data
                        else 0
                    ),

                    prerequisites=(
                        dependency.prerequisites
                    ),

                    missing_prerequisites=(
                        missing_prerequisites
                    ),

                    reason=self._build_reason(
                        skill_name=skill_name,
                        market_data=market_data,
                        missing_prerequisites=(
                            missing_prerequisites
                        )
                    )
                )
            )

        return priorities

    def _resolve_learning_order(
        self,
        skill_name: str,
        resume_skill_set: set[str],
        market_skill_lookup: dict[str, SkillFrequency],
        ordered_skills: list[str],
        visited: set[str],
        visiting: set[str]
    ) -> None:
        """
        Recursively resolve prerequisites before placing
        the requested skill in the learning roadmap.
        """

        normalized_skill = skill_name.lower()

        # Candidate already knows the skill.
        if normalized_skill in resume_skill_set:

            return

        # Already added to roadmap.
        if normalized_skill in visited:

            return

        # Protect against malformed cyclic dependencies.
        if normalized_skill in visiting:

            return

        visiting.add(
            normalized_skill
        )

        dependency = (
            self.dependency_service.get_dependency(
                skill_name
            )
        )

        for prerequisite in dependency.prerequisites:

            normalized_prerequisite = (
                prerequisite.lower()
            )

            if normalized_prerequisite in resume_skill_set:

                continue

            self._resolve_learning_order(
                skill_name=prerequisite,
                resume_skill_set=resume_skill_set,
                market_skill_lookup=market_skill_lookup,
                ordered_skills=ordered_skills,
                visited=visited,
                visiting=visiting
            )

        visiting.remove(
            normalized_skill
        )

        visited.add(
            normalized_skill
        )

        ordered_skills.append(
            skill_name
        )

    @staticmethod
    def _build_reason(
        skill_name: str,
        market_data: SkillFrequency | None,
        missing_prerequisites: list[str]
    ) -> str:
        """
        Build an explainable reason for the learning
        recommendation.
        """

        if market_data and missing_prerequisites:

            prerequisites = ", ".join(
                missing_prerequisites
            )

            return (
                f"{skill_name} appears in "
                f"{market_data.market_percentage}% of analyzed jobs, "
                f"but requires learning {prerequisites} first."
            )

        if market_data:

            return (
                f"{skill_name} appears in "
                f"{market_data.market_percentage}% of analyzed jobs "
                f"and has no unmet prerequisites."
            )

        return (
            f"{skill_name} is recommended because it is a "
            f"prerequisite for another in-demand skill."
        )