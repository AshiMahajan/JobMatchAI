from crewai import Agent, Task, Crew, Process, LLM

from core.config import OPENROUTER_API_KEY

from agents.tools.web_research_tool import (
    WebResearchTool,
)

from domains.skill_research import (
    SkillResearchResult,
)


class SkillResearchCrew:
    """
    Research pipeline for unknown technical skills.

    Workflow:

        Skill
          ↓
        Targeted web research
          ↓
        Research synthesis
          ↓
        SkillResearchResult

    The web research is performed by the application.
    The CrewAI agent is used only for synthesis.

    The Knowledge Base is never modified here.
    """

    def __init__(
        self,
        max_searches: int = 3,
    ):

        self.max_searches = max_searches

        self.llm = LLM(
            model="openrouter/openai/gpt-4o-mini",
            api_key=OPENROUTER_API_KEY,
            temperature=0.1,
        )

        self.web_research = WebResearchTool(
            n_results=5,
        )

    # ==================================================
    # CREATE AGENT
    # ==================================================

    def _create_agent(
        self,
    ) -> Agent:

        return Agent(

            role="Technical Skill Researcher",

            goal=(
                "Produce a high-quality, useful, and "
                "technically accurate structured profile "
                "for a software or technology skill using "
                "the supplied web research."
            ),

            backstory=(
                "You are a technical research specialist "
                "for JobMatch AI. The application performs "
                "web research before giving the evidence "
                "to you. Your job is to synthesize that "
                "evidence into a useful technical skill "
                "profile.\n\n"

                "You should reason carefully from the "
                "supplied evidence. You may make reasonable "
                "technical inferences when they are strongly "
                "supported by the research and normal "
                "technical relationships, but you must not "
                "invent arbitrary technologies or claims.\n\n"

                "Prefer useful enrichment over empty fields. "
                "However, never fabricate specific facts, "
                "URLs, aliases, or relationships."
            ),

            tools=[],

            llm=self.llm,

            max_iter=1,

            verbose=True,
        )

    # ==================================================
    # CREATE TASK
    # ==================================================

    def _create_task(
        self,
        agent: Agent,
        skill_name: str,
        skill_id: str,
        research: str,
    ) -> Task:

        return Task(

            description=(

                f"Create a high-quality structured "
                f"technical profile for '{skill_name}'.\n\n"

                f"The application assigned the exact "
                f"skill ID '{skill_id}'.\n\n"

                "==================================================\n"
                "RESEARCH RULES\n"
                "==================================================\n\n"

                "The application has already performed "
                "the web searches.\n\n"

                "Do NOT perform web searches.\n"
                "Do NOT call tools.\n"
                "Use the supplied research as your evidence.\n\n"

                "You should synthesize the research rather "
                "than merely copy individual snippets.\n\n"

                "The objective is useful enrichment. Do not "
                "leave fields empty merely because one search "
                "snippet did not explicitly state the answer.\n\n"

                "Reason across the supplied sources when "
                "determining technical relationships.\n\n"

                "For example, if the research clearly establishes "
                "that a technology is a Python numerical/scientific "
                "computing library, reasonable relationships "
                "between Python, numerical computing, arrays, "
                "scientific computing, and commonly associated "
                "ecosystem technologies may be included when "
                "supported by the research.\n\n"

                "Do not invent arbitrary relationships simply "
                "to fill every field.\n\n"

                "==================================================\n"
                "FIELD INSTRUCTIONS\n"
                "==================================================\n\n"

                "1. skill_id\n"
                "Must be exactly the supplied skill ID.\n\n"

                "2. name\n"
                "Use the official or most commonly recognized "
                "technical name.\n\n"

                "3. aliases\n"
                "Include genuine commonly used alternative names, "
                "abbreviations, or expansions when supported "
                "by the research.\n"
                "Do not include unrelated terms.\n\n"

                "4. category\n"
                "Choose a useful technical category such as "
                "Programming Language, Framework, Library, "
                "Cloud Computing, Database, DevOps, Machine "
                "Learning, Data Science, Operating System, "
                "API, Tool, Platform, etc.\n\n"

                "Use the most specific reasonable category "
                "supported by the research.\n\n"

                "5. parent\n"
                "Identify the broader technology, ecosystem, "
                "language, platform, or concept that this "
                "skill belongs to when reasonably supported.\n\n"

                "Examples:\n"
                "NumPy → Python\n"
                "React → JavaScript\n"
                "PyTorch → Python / Machine Learning\n"
                "Azure Functions → Microsoft Azure\n\n"

                "If there is genuinely no useful parent, "
                "use null.\n\n"

                "6. related\n"
                "Identify technologies that are commonly used "
                "with, adjacent to, or technically related to "
                "the skill.\n\n"

                "Prefer concrete technologies rather than "
                "generic concepts.\n\n"

                "Examples for a numerical Python library could "
                "include related scientific Python technologies "
                "if the research supports the relationship.\n\n"

                "7. prerequisites\n"
                "Identify knowledge or technologies a learner "
                "would reasonably need before using the skill "
                "effectively.\n\n"

                "These can include:\n"
                "- programming languages\n"
                "- fundamental concepts\n"
                "- platforms\n"
                "- related technologies\n\n"

                "Do not confuse prerequisites with features.\n\n"

                "8. unlocks\n"
                "Identify skills, technologies, or capabilities "
                "that learning this skill reasonably enables.\n\n"

                "Examples include downstream technologies, "
                "development areas, or technical capabilities "
                "that depend strongly on the skill.\n\n"

                "Do not claim that merely knowing a library "
                "automatically qualifies someone for an "
                "unrelated technology.\n\n"

                "9. sources\n"
                "Only include URLs that actually appear in the "
                "supplied research.\n\n"

                "Prefer official documentation over secondary "
                "sources.\n\n"

                "Do not create, modify, or guess URLs.\n\n"

                "10. confidence\n"
                "Give a realistic confidence score between "
                "0.0 and 1.0 based on the strength and "
                "consistency of the supplied evidence.\n\n"

                "Do NOT automatically use 1.0 merely because "
                "the skill name is obvious.\n\n"

                "==================================================\n"
                "QUALITY RULES\n"
                "==================================================\n\n"

                "The final result should be useful for a "
                "Knowledge Base used by a job-matching system.\n\n"

                "Prefer:\n"
                "- meaningful categories\n"
                "- useful parent technologies\n"
                "- genuine aliases\n"
                "- relevant ecosystem technologies\n"
                "- realistic prerequisites\n"
                "- realistic downstream capabilities\n"
                "- authoritative sources\n\n"

                "Avoid:\n"
                "- hallucinated technologies\n"
                "- arbitrary relationships\n"
                "- fake aliases\n"
                "- fake URLs\n"
                "- generic filler\n"
                "- excessive confidence\n\n"

                "If a field truly cannot be determined, leave "
                "it empty rather than fabricating an answer.\n\n"

                "==================================================\n"
                "WEB RESEARCH\n"
                "==================================================\n\n"

                f"{research}\n\n"

                "==================================================\n"
                "FINAL REQUIREMENT\n"
                "==================================================\n\n"

                f"The skill_id MUST be exactly '{skill_id}'."
            ),

            expected_output=(
                "A complete and useful "
                "SkillResearchResult containing "
                "well-supported technical enrichment."
            ),

            output_pydantic=SkillResearchResult,

            agent=agent,
        )

    # ==================================================
    # BUILD SEARCH QUERIES
    # ==================================================

    @staticmethod
    def _build_queries(
        skill_name: str,
    ) -> list[str]:
        """
        Build targeted searches covering different
        dimensions of the skill.

        Three searches provide considerably better
        evidence than one overloaded search query.
        """

        return [

            # ------------------------------------------
            # SEARCH 1 — OFFICIAL IDENTITY / OVERVIEW
            # ------------------------------------------

            (
                f'"{skill_name}" '
                "official documentation "
                "overview what is "
                "programming language framework library "
                "platform"
            ),

            # ------------------------------------------
            # SEARCH 2 — ECOSYSTEM / RELATIONSHIPS
            # ------------------------------------------

            (
                f'"{skill_name}" '
                "ecosystem related technologies "
                "commonly used with "
                "integrations dependencies"
            ),

            # ------------------------------------------
            # SEARCH 3 — PREREQUISITES / LEARNING
            # ------------------------------------------

            (
                f'"{skill_name}" '
                "prerequisites "
                "requirements "
                "getting started "
                "learning path "
                "used for"
            ),
        ]

    # ==================================================
    # RUN RESEARCH
    # ==================================================

    def research(
        self,
        skill_name: str,
        skill_id: str,
    ) -> SkillResearchResult:

        if not isinstance(
            skill_name,
            str,
        ) or not skill_name.strip():

            raise ValueError(
                "Skill name must be a "
                "non-empty string."
            )

        if not isinstance(
            skill_id,
            str,
        ) or not skill_id.strip():

            raise ValueError(
                "Skill ID must be a "
                "non-empty string."
            )

        skill_name = skill_name.strip()
        skill_id = skill_id.strip()

        # --------------------------------------------------
        # TARGETED WEB RESEARCH
        # --------------------------------------------------

        queries = self._build_queries(
            skill_name
        )

        queries = queries[
            : self.max_searches
        ]

        web_research = (
            self.web_research.search_multiple(
                queries
            )
        )

        # --------------------------------------------------
        # ONE LLM SYNTHESIS PASS
        # --------------------------------------------------

        agent = self._create_agent()

        task = self._create_task(
            agent=agent,
            skill_name=skill_name,
            skill_id=skill_id,
            research=web_research,
        )

        crew = Crew(

            agents=[
                agent
            ],

            tasks=[
                task
            ],

            process=Process.sequential,

            verbose=True,
        )

        result = crew.kickoff()

        if result.pydantic is None:

            raise RuntimeError(
                "Skill research did not return "
                "a valid SkillResearchResult."
            )

        research_result = (
            result.pydantic
        )

        # --------------------------------------------------
        # ENFORCE APPLICATION-OWNED ID
        # --------------------------------------------------

        research_result.skill_id = (
            skill_id
        )

        return research_result