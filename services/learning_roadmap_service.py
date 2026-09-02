from domains.learning_priority import LearningPriority

from domains.learning_roadmap import (
    LearningRoadmap,
    RoadmapPhase,
    RoadmapStep,
)

from skill_engine import SkillEngine


class LearningRoadmapService:
    """
    Builds a personalized learning roadmap from
    dependency-aware learning priorities.
    """

    def __init__(self) -> None:

        self.skill_engine = SkillEngine()

    # ======================================================
    # ROADMAP BUILDING
    # ======================================================

    def build_roadmap(
        self,
        learning_priorities: list[LearningPriority],
    ) -> LearningRoadmap:
        """
        Build a dependency-aware learning roadmap.
        """

        if not learning_priorities:

            return LearningRoadmap(
                total_phases=0,
                total_steps=0,
                phases=[],
            )

        skill_lookup = {
            priority.skill.lower(): priority
            for priority in learning_priorities
        }

        phases: dict[str, int] = {}

        # --------------------------------------------------
        # Calculate phase for every skill
        # --------------------------------------------------

        for priority in learning_priorities:

            self._calculate_phase(
                skill_name=priority.skill,
                skill_lookup=skill_lookup,
                phases=phases,
                visiting=set(),
            )

        # --------------------------------------------------
        # Build roadmap steps
        # --------------------------------------------------

        steps: list[RoadmapStep] = []

        for priority in learning_priorities:

            objectives = (
                self.skill_engine.get_learning_objectives(
                    priority.skill
                )
            )

            steps.append(
                RoadmapStep(

                    skill=priority.skill,

                    priority=priority.priority,

                    market_percentage=(
                        priority.market_percentage
                    ),

                    occurrence_count=(
                        priority.occurrence_count
                    ),

                    status=priority.readiness,

                    prerequisites=(
                        priority.prerequisites
                    ),

                    missing_prerequisites=(
                        priority.missing_prerequisites
                    ),

                    unlocks=self._find_unlocked_skills(
                        skill_name=priority.skill,
                        learning_priorities=(
                            learning_priorities
                        ),
                    ),

                    dependency_impact=(
                        priority.dependency_impact
                    ),

                    objectives=objectives,

                    reason=priority.reason,
                )
            )

        # --------------------------------------------------
        # Group steps by phase
        # --------------------------------------------------

        phase_map: dict[
            int,
            list[RoadmapStep]
        ] = {}

        for step in steps:

            phase_number = phases[
                step.skill.lower()
            ]

            phase_map.setdefault(
                phase_number,
                []
            ).append(step)

        # --------------------------------------------------
        # Build RoadmapPhase objects
        # --------------------------------------------------

        roadmap_phases: list[RoadmapPhase] = []

        for phase_number in sorted(
            phase_map
        ):

            phase_steps = phase_map[
                phase_number
            ]

            phase_steps.sort(
                key=lambda step: (
                    step.priority,
                    step.skill.lower(),
                )
            )

            roadmap_phases.append(
                RoadmapPhase(

                    phase=phase_number,

                    skills=phase_steps,
                )
            )

        return LearningRoadmap(

            total_phases=len(
                roadmap_phases
            ),

            total_steps=len(
                steps
            ),

            phases=roadmap_phases,
        )

    # ======================================================
    # PHASE CALCULATION
    # ======================================================

    def _calculate_phase(
        self,
        skill_name: str,
        skill_lookup: dict[str, LearningPriority],
        phases: dict[str, int],
        visiting: set[str],
    ) -> int:
        """
        Calculate dependency depth.

        Known prerequisites do not contribute
        to the phase.

        Missing prerequisites that exist in
        the roadmap determine the dependency depth.
        """

        normalized_skill = (
            skill_name.lower()
        )

        if normalized_skill in phases:

            return phases[
                normalized_skill
            ]

        if normalized_skill in visiting:

            raise ValueError(
                "Circular dependency detected "
                f"while calculating roadmap phase "
                f"for '{skill_name}'."
            )

        visiting.add(
            normalized_skill
        )

        priority = skill_lookup.get(
            normalized_skill
        )

        if priority is None:

            visiting.remove(
                normalized_skill
            )

            return 1

        missing_prerequisites = (
            priority.missing_prerequisites
        )

        if not missing_prerequisites:

            phase = 1

        else:

            prerequisite_phases = []

            for prerequisite in (
                missing_prerequisites
            ):

                normalized_prerequisite = (
                    prerequisite.lower()
                )

                if (
                    normalized_prerequisite
                    not in skill_lookup
                ):
                    continue

                prerequisite_phase = (
                    self._calculate_phase(
                        skill_name=prerequisite,
                        skill_lookup=skill_lookup,
                        phases=phases,
                        visiting=visiting,
                    )
                )

                prerequisite_phases.append(
                    prerequisite_phase
                )

            if prerequisite_phases:

                phase = (
                    max(
                        prerequisite_phases
                    )
                    + 1
                )

            else:

                phase = 1

        visiting.remove(
            normalized_skill
        )

        phases[
            normalized_skill
        ] = phase

        return phase

    # ======================================================
    # UNLOCK CALCULATION
    # ======================================================

    def _find_unlocked_skills(
        self,
        skill_name: str,
        learning_priorities: list[LearningPriority],
    ) -> list[str]:
        """
        Find skills in the current roadmap that
        directly depend on the supplied skill.
        """

        normalized_skill = (
            skill_name.lower()
        )

        unlocks: list[str] = []

        for priority in learning_priorities:

            if (
                priority.skill.lower()
                == normalized_skill
            ):
                continue

            prerequisites = {
                prerequisite.lower()
                for prerequisite
                in priority.prerequisites
            }

            if normalized_skill in prerequisites:

                unlocks.append(
                    priority.skill
                )

        return sorted(
            unlocks,
            key=str.lower,
        )