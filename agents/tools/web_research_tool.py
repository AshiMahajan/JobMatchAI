from crewai_tools import SerperDevTool


class WebResearchTool:
    """
    Performs targeted web research for technical skills.

    The application controls exactly which searches are performed.
    The resulting research is passed to the LLM for synthesis.

    This class does NOT use an autonomous CrewAI agent.
    """

    def __init__(
        self,
        n_results: int = 5,
    ):
        self.search_tool = SerperDevTool(
            n_results=n_results,
        )

    # ==================================================
    # PUBLIC SEARCH
    # ==================================================

    def search(
        self,
        query: str,
    ) -> str:
        """
        Execute one web search and return cleaned results.
        """

        if not isinstance(
            query,
            str,
        ) or not query.strip():

            raise ValueError(
                "Research query must be "
                "a non-empty string."
            )

        raw_result = self.search_tool.run(
            search_query=query,
        )

        return self._trim_result(
            raw_result
        )

    # ==================================================
    # MULTI SEARCH
    # ==================================================

    def search_multiple(
        self,
        queries: list[str],
    ) -> str:
        """
        Execute multiple targeted searches.

        Each search is kept separately so the synthesis
        model can understand which evidence came from which
        research dimension.
        """

        if not isinstance(
            queries,
            list,
        ) or not queries:

            raise ValueError(
                "At least one research query is required."
            )

        sections = []

        for index, query in enumerate(
            queries,
            start=1,
        ):

            if not isinstance(
                query,
                str,
            ) or not query.strip():

                continue

            result = self.search(
                query
            )

            sections.append(
                f"""
==============================
RESEARCH SEARCH {index}
==============================

QUERY:
{query}

RESULTS:
{result}
""".strip()
            )

        if not sections:

            raise ValueError(
                "No valid research queries were supplied."
            )

        return "\n\n".join(
            sections
        )

    # ==================================================
    # TRIM RESULT
    # ==================================================

    @staticmethod
    def _trim_result(
        raw_result,
    ) -> str:
        """
        Convert Serper output into compact research text.

        We retain:
        - title
        - snippet
        - URL

        This keeps token usage under control while still
        giving the synthesis model useful evidence.
        """

        if (
            isinstance(
                raw_result,
                dict,
            )
            and "organic" in raw_result
        ):

            trimmed = []

            for item in raw_result.get(
                "organic",
                [],
            )[:5]:

                title = item.get(
                    "title",
                    "",
                )

                snippet = item.get(
                    "snippet",
                    "",
                )

                link = item.get(
                    "link",
                    "",
                )

                trimmed.append(
                    {
                        "title": title,
                        "snippet": snippet,
                        "link": link,
                    }
                )

            return str(
                trimmed
            )[:6000]

        return str(
            raw_result
        )[:6000]