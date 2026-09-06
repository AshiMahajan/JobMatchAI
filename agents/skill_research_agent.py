from crewai import Agent, Crew, LLM, Task

from agents.tools.web_research_tool import (
    WebResearchTool,
)

from core.config import (
    OPENROUTER_API_KEY,
)


class SkillResearchAgent:
    """
    CrewAI-based agent responsible for researching
    unknown skills using web sources.

    This agent does not modify the Knowledge Base.
    """

    def __init__(self):

        if not OPENROUTER_API_KEY:

            raise RuntimeError(
                "OPENROUTER_API_KEY is not configured."
            )

        self.web_research_tool = WebResearchTool()

        self.llm = LLM(
            model="openrouter/openrouter/free",
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

        self.agent = Agent(

            role="Skill Research Specialist",

            goal=(
                "Research unknown technical skills using "
                "reliable web sources and produce accurate "
                "structured information."
            ),

            backstory=(
                "You are a technical research specialist "
                "working for JobMatch AI. Your job is to "
                "investigate skills that are not yet present "
                "in the Knowledge Base. You prioritize "
                "official documentation and reliable "
                "technical sources."
            ),

            tools=[
                self.web_research_tool,
            ],

            llm=self.llm,

            verbose=True,
        )

    def create_research_task(
            self,
            skill_name: str,
    ) -> Task:
        """
        Create a CrewAI task for researching a skill.
        """

        return Task(

            description=(
                f"Research the technical skill '{skill_name}'.\n\n"

                "Use the web research tool to gather "
                "reliable information.\n\n"

                "Determine:\n"
                "- Official name\n"
                "- Common aliases\n"
                "- Category\n"
                "- Parent technology or concept\n"
                "- Related technologies\n"
                "- Prerequisites\n"
                "- Skills or technologies it can unlock\n"
                "- Reliable source URLs\n\n"

                "Prioritize official documentation and "
                "other authoritative technical sources. "
                "Do not invent information."
            ),

            expected_output=(
                "A clear research report containing the "
                "skill's name, aliases, category, parent, "
                "related technologies, prerequisites, "
                "unlocks, sources, and a confidence assessment."
            ),

            agent=self.agent,
        )

    def run_research(
        self,
        skill_name: str,
    ) -> str:
        """
        Execute the research workflow for a skill.
        """

        task = self.create_research_task(
            skill_name
        )

        crew = Crew(
            agents=[
                self.agent,
            ],
            tasks=[
                task,
            ],
            verbose=True,
        )

        result = crew.kickoff()

        return str(result)