from domains.career_analysis import SkillFrequency
from domains.learning_priority import LearningPriority

from services.skill_dependency_service import (
    SkillDependencyService
)


class LearningPriorityService:
    """
    Generates dependency-aware learning priorities.

    Priority considers:

        1. Dependency impact
        2. Readiness
        3. Market demand

    The service does not use arbitrary numerical weights.

    Skills are grouped into strategic tiers:

        Tier 1:
            Ready skills that unlock other missing skills.

        Tier 2:
            Ready standalone skills.

        Tier 3:
            Skills currently blocked by missing prerequisites.

    Market demand determines ordering within each tier.
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
        Generate dependency-aware learning priorities.
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

        # --------------------------------------------------
        # Resolve complete dependency graph
        # --------------------------------------------------

        ordered_skills: list[str] = []

        visited: set[str] = set()

        visiting: set[str] = set()

        # Resolve all market skills.
        #
        # Market demand is used only to determine
        # which branches of the graph are explored first.
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

        # --------------------------------------------------
        # Dependency impact
        # --------------------------------------------------

        dependency_impacts = (
            self._calculate_dependency_impacts(
                ordered_skills=ordered_skills,
                resume_skill_set=resume_skill_set
            )
        )

        # --------------------------------------------------
        # Build candidate metadata
        # --------------------------------------------------

        candidates = []

        for skill_name in ordered_skills:

            normalized_skill = (
                skill_name.lower()
            )

            market_data = (
                market_skill_lookup.get(
                    normalized_skill
                )
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

            readiness = (
                "ready"
                if not missing_prerequisites
                else "blocked"
            )

            dependency_impact = (
                dependency_impacts.get(
                    normalized_skill,
                    0
                )
            )

            candidates.append({
                "skill": skill_name,
                "market_data": market_data,
                "dependency": dependency,
                "missing_prerequisites": (
                    missing_prerequisites
                ),
                "readiness": readiness,
                "dependency_impact": (
                    dependency_impact
                )
            })

        # --------------------------------------------------
        # Strategic ranking
        # --------------------------------------------------
        #
        # Tier 1:
        #   Ready + unlocks missing skills
        #
        # Tier 2:
        #   Ready standalone
        #
        # Tier 3:
        #   Blocked
        #
        # Market demand is the secondary ordering signal.
        # --------------------------------------------------

        def ranking_key(candidate: dict):

            readiness = candidate[
                "readiness"
            ]

            dependency_impact = candidate[
                "dependency_impact"
            ]

            market_data = candidate[
                "market_data"
            ]

            if (
                readiness == "ready"
                and
                dependency_impact > 0
            ):

                tier = 1

            elif readiness == "ready":

                tier = 2

            else:

                tier = 3

            market_percentage = (
                market_data.market_percentage
                if market_data
                else 0.0
            )

            return (
                tier,
                -dependency_impact,
                -market_percentage,
                candidate["skill"].lower()
            )

        candidates.sort(
            key=ranking_key
        )

        # --------------------------------------------------
        # Build final domain models
        # --------------------------------------------------

        priorities: list[LearningPriority] = []

        for priority_number, candidate in enumerate(
            candidates,
            start=1
        ):

            market_data = candidate[
                "market_data"
            ]

            dependency = candidate[
                "dependency"
            ]

            missing_prerequisites = candidate[
                "missing_prerequisites"
            ]

            readiness = candidate[
                "readiness"
            ]

            dependency_impact = candidate[
                "dependency_impact"
            ]

            priorities.append(
                LearningPriority(

                    skill=candidate["skill"],

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

                    dependency_impact=(
                        dependency_impact
                    ),

                    readiness=(
                        readiness
                    ),

                    reason=self._build_reason(
                        skill_name=candidate["skill"],
                        market_data=market_data,
                        missing_prerequisites=(
                            missing_prerequisites
                        ),
                        dependency_impact=(
                            dependency_impact
                        ),
                        readiness=(
                            readiness
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
        Recursively resolve prerequisites.

        Prerequisites are placed before the skill
        that depends on them.
        """

        normalized_skill = (
            skill_name.lower()
        )

        if normalized_skill in resume_skill_set:

            return

        if normalized_skill in visited:

            return

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

            if (
                normalized_prerequisite
                in resume_skill_set
            ):

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

    def _calculate_dependency_impacts(
        self,
        ordered_skills: list[str],
        resume_skill_set: set[str]
    ) -> dict[str, int]:
        """
        Calculate how many relevant missing skills
        directly depend on each skill.
        """

        ordered_skill_set = {
            skill.lower()
            for skill in ordered_skills
        }

        impacts: dict[str, int] = {
            skill.lower(): 0
            for skill in ordered_skills
        }

        for skill_name in ordered_skills:

            dependency = (
                self.dependency_service.get_dependency(
                    skill_name
                )
            )

            for prerequisite in dependency.prerequisites:

                normalized_prerequisite = (
                    prerequisite.lower()
                )

                if (
                    normalized_prerequisite
                    in ordered_skill_set
                    and
                    normalized_prerequisite
                    not in resume_skill_set
                ):

                    impacts[
                        normalized_prerequisite
                    ] += 1

        return impacts

    @staticmethod
    def _build_reason(
        skill_name: str,
        market_data: SkillFrequency | None,
        missing_prerequisites: list[str],
        dependency_impact: int,
        readiness: str
    ) -> str:
        """
        Build an explainable recommendation reason.
        """

        market_percentage = (
            market_data.market_percentage
            if market_data
            else 0.0
        )

        if (
            readiness == "ready"
            and
            dependency_impact > 0
        ):

            dependent_label = (
                "skill"
                if dependency_impact == 1
                else "skills"
            )

            return (
                f"{skill_name} appears in "
                f"{market_percentage}% of analyzed jobs "
                f"and is ready to learn. "
                f"It unlocks {dependency_impact} "
                f"dependent {dependent_label} "
                f"in the current learning path."
            )

        if missing_prerequisites:

            prerequisites = ", ".join(
                missing_prerequisites
            )

            return (
                f"{skill_name} appears in "
                f"{market_percentage}% of analyzed jobs, "
                f"but requires learning "
                f"{prerequisites} first."
            )

        return (
            f"{skill_name} appears in "
            f"{market_percentage}% of analyzed jobs "
            f"and has no unmet prerequisites."
        )