# from collections import Counter

# from sentence_transformers.util import cos_sim
# from sklearn.cluster import AgglomerativeClustering

# from core.embedding import embedding_model

# from domains.role_intelligence import (
#     JobSimilarity,
#     RoleCluster,
#     RoleIntelligenceResult,
#     RoleJob,
# )

# from services.skill_service import SkillService


# class RoleIntelligenceService:
#     """
#     Performs semantic analysis of Job Descriptions.

#     Responsibilities:
#         - Generate JD embeddings.
#         - Calculate semantic similarity between JDs.
#         - Cluster semantically similar JDs.
#         - Determine explicit role titles when available.
#         - Calculate common skills inside each cluster.

#     This service does NOT:
#         - Calculate ATS scores.
#         - Calculate salary.
#         - Generate learning roadmaps.
#         - Generate LLM recommendations.
#     """

#     def __init__(
#         self,
#         similarity_threshold: float = 0.65,
#     ) -> None:

#         self.skill_service = SkillService()

#         self.similarity_threshold = (
#             similarity_threshold
#         )

#     # ==================================================
#     # Public API
#     # ==================================================

#     def analyze(
#         self,
#         job_descriptions: list[str],
#     ) -> RoleIntelligenceResult:
#         """
#         Perform complete role intelligence analysis.
#         """

#         if not job_descriptions:

#             return RoleIntelligenceResult(
#                 jobs_analyzed=0,
#                 clusters=[],
#                 similarities=[],
#             )

#         skills_by_job = []

#         for jd in job_descriptions:

#             skills = self.skill_service.extract_names(
#                 jd
#             )

#             skills_by_job.append(
#                 skills
#             )

#         embeddings = embedding_model.encode(
#             job_descriptions,
#             convert_to_tensor=True
#         )

#         similarities = self._calculate_similarities(
#             embeddings
#         )

#         clusters = self._cluster_jobs(
#             job_descriptions=job_descriptions,
#             skills_by_job=skills_by_job,
#             embeddings=embeddings,
#         )

#         return RoleIntelligenceResult(

#             jobs_analyzed=len(
#                 job_descriptions
#             ),

#             clusters=clusters,

#             similarities=similarities,
#         )

#     # ==================================================
#     # Similarity
#     # ==================================================

#     def _calculate_similarities(
#         self,
#         embeddings,
#     ) -> list[JobSimilarity]:

#         results = []

#         total_jobs = len(
#             embeddings
#         )

#         for i in range(total_jobs):

#             for j in range(
#                 i + 1,
#                 total_jobs
#             ):

#                 similarity = cos_sim(
#                     embeddings[i],
#                     embeddings[j]
#                 ).item()

#                 results.append(

#                     JobSimilarity(

#                         job_id_a=i + 1,

#                         job_id_b=j + 1,

#                         similarity=round(
#                             similarity,
#                             4
#                         ),
#                     )

#                 )

#         return results

#     # ==================================================
#     # Clustering
#     # ==================================================

#     def _cluster_jobs(
#         self,
#         job_descriptions: list[str],
#         skills_by_job: list[list[str]],
#         embeddings,
#     ) -> list[RoleCluster]:

#         total_jobs = len(
#             job_descriptions
#         )

#         # ----------------------------------------------
#         # One JD does not require clustering.
#         # ----------------------------------------------

#         if total_jobs == 1:

#             return [

#                 self._build_cluster(

#                     cluster_id=1,

#                     job_indices=[0],

#                     job_descriptions=job_descriptions,

#                     skills_by_job=skills_by_job,

#                 )

#             ]

#         # ----------------------------------------------
#         # Convert embeddings to numpy.
#         # ----------------------------------------------

#         embedding_matrix = (
#             embeddings.cpu().numpy()
#         )

#         # ----------------------------------------------
#         # Agglomerative clustering using cosine
#         # distance.
#         #
#         # distance = 1 - cosine similarity
#         # ----------------------------------------------

#         clustering = AgglomerativeClustering(

#             n_clusters=None,

#             distance_threshold=(
#                 1.0 -
#                 self.similarity_threshold
#             ),

#             metric="cosine",

#             linkage="average",

#         )

#         labels = clustering.fit_predict(
#             embedding_matrix
#         )

#         # ----------------------------------------------
#         # Build clusters.
#         # ----------------------------------------------

#         grouped = {}

#         for job_index, label in enumerate(labels):

#             grouped.setdefault(
#                 int(label),
#                 []
#             ).append(
#                 job_index
#             )

#         clusters = []

#         for cluster_number, (
#             cluster_label,
#             job_indices
#         ) in enumerate(
#             sorted(
#                 grouped.items()
#             ),
#             start=1
#         ):

#             clusters.append(

#                 self._build_cluster(

#                     cluster_id=cluster_number,

#                     job_indices=job_indices,

#                     job_descriptions=job_descriptions,

#                     skills_by_job=skills_by_job,

#                 )

#             )

#         return clusters

#     # ==================================================
#     # Cluster construction
#     # ==================================================

#     def _build_cluster(
#         self,
#         cluster_id: int,
#         job_indices: list[int],
#         job_descriptions: list[str],
#         skills_by_job: list[list[str]],
#     ) -> RoleCluster:

#         jobs = []

#         all_skills = []

#         roles = []

#         for job_index in job_indices:

#             jd = job_descriptions[
#                 job_index
#             ]

#             skills = skills_by_job[
#                 job_index
#             ]

#             role = self._extract_role(
#                 jd
#             )

#             if role:

#                 roles.append(
#                     role
#                 )

#             all_skills.extend(
#                 skills
#             )

#             jobs.append(

#                 RoleJob(

#                     job_id=job_index + 1,

#                     role=role,

#                     skills=skills,

#                 )

#             )

#         common_skills = self._get_common_skills(
#             all_skills,
#             len(job_indices)
#         )

#         role = self._determine_cluster_role(
#             roles,
#             cluster_id
#         )

#         return RoleCluster(

#             cluster_id=cluster_id,

#             role=role,

#             jobs=jobs,

#             common_skills=common_skills,

#         )

#     # ==================================================
#     # Role extraction
#     # ==================================================

#     @staticmethod
#     def _extract_role(
#         job_description: str,
#     ) -> str | None:
#         """
#         Extract an explicitly provided job title.

#         This intentionally does not use an LLM.
#         """

#         lines = [

#             line.strip()

#             for line in
#             job_description.splitlines()

#             if line.strip()

#         ]

#         if not lines:

#             return None

#         first_line = lines[0]

#         # Ignore obvious section labels.

#         ignored = {
#             "job description",
#             "description",
#             "responsibilities",
#             "requirements",
#             "qualifications",
#             "skills",
#             "about the role",
#         }

#         if first_line.lower() in ignored:

#             if len(lines) > 1:

#                 return lines[1]

#             return None

#         return first_line

#     # ==================================================
#     # Cluster role
#     # ==================================================

#     @staticmethod
#     def _determine_cluster_role(
#         roles: list[str],
#         cluster_id: int,
#     ) -> str:

#         if not roles:

#             return (
#                 f"Role Cluster {cluster_id}"
#             )

#         counter = Counter(
#             role.strip()
#             for role in roles
#             if role.strip()
#         )

#         return counter.most_common(1)[0][0]

#     # ==================================================
#     # Common skills
#     # ==================================================

#     @staticmethod
#     def _get_common_skills(
#         skills: list[str],
#         job_count: int,
#     ) -> list[str]:

#         if not skills or job_count == 0:

#             return []

#         counter = Counter(
#             skill.lower()
#             for skill in skills
#         )

#         # A skill is considered common when
#         # it appears in at least 50% of the jobs.
#         minimum_occurrences = max(
#             1,
#             (job_count + 1) // 2
#         )

#         common = [

#             skill

#             for skill, count
#             in counter.items()

#             if count >= minimum_occurrences

#         ]

#         return sorted(
#             common
#         )

# ---------------------------------------------------------------------------------

from collections import Counter
import re

from sentence_transformers.util import cos_sim
from sklearn.cluster import AgglomerativeClustering

from core.embedding import embedding_model

from domains.role_intelligence import (
    JobSimilarity,
    RoleCluster,
    RoleIntelligenceResult,
    RoleJob,
)

from services.skill_service import SkillService


class RoleIntelligenceService:
    """
    Performs semantic analysis of Job Descriptions.

    Responsibilities:
        - Extract skills from each Job Description.
        - Generate JD embeddings.
        - Calculate semantic similarity between JDs.
        - Cluster semantically similar JDs.
        - Extract explicit role titles when available.
        - Determine representative roles for clusters.
        - Calculate common skills inside each cluster.

    This service does NOT:
        - Calculate ATS scores.
        - Calculate salary.
        - Generate learning roadmaps.
        - Generate LLM recommendations.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.65,
    ) -> None:

        self.skill_service = SkillService()

        self.similarity_threshold = (
            similarity_threshold
        )

    # ==================================================
    # Public API
    # ==================================================

    def analyze(
        self,
        job_descriptions: list[str],
    ) -> RoleIntelligenceResult:
        """
        Perform complete role intelligence analysis.
        """

        if not job_descriptions:

            return RoleIntelligenceResult(
                jobs_analyzed=0,
                clusters=[],
                similarities=[],
            )

        # --------------------------------------------------
        # Extract and normalize skills for every JD.
        # --------------------------------------------------

        skills_by_job = []

        for jd in job_descriptions:

            skills = self.skill_service.extract_names(
                jd
            )

            skills = self._unique_skills(
                skills
            )

            skills_by_job.append(
                skills
            )

        # --------------------------------------------------
        # Generate embeddings.
        # --------------------------------------------------

        embeddings = embedding_model.encode(
            job_descriptions,
            convert_to_tensor=True
        )

        # --------------------------------------------------
        # Calculate pairwise semantic similarity.
        # --------------------------------------------------

        similarities = self._calculate_similarities(
            embeddings
        )

        # --------------------------------------------------
        # Cluster jobs.
        # --------------------------------------------------

        clusters = self._cluster_jobs(
            job_descriptions=job_descriptions,
            skills_by_job=skills_by_job,
            embeddings=embeddings,
        )

        return RoleIntelligenceResult(

            jobs_analyzed=len(
                job_descriptions
            ),

            clusters=clusters,

            similarities=similarities,
        )

    # ==================================================
    # Similarity
    # ==================================================

    def _calculate_similarities(
        self,
        embeddings,
    ) -> list[JobSimilarity]:
        """
        Calculate pairwise cosine similarity between
        every Job Description.
        """

        results = []

        total_jobs = len(
            embeddings
        )

        for i in range(total_jobs):

            for j in range(
                i + 1,
                total_jobs
            ):

                similarity = cos_sim(
                    embeddings[i],
                    embeddings[j]
                ).item()

                results.append(

                    JobSimilarity(

                        job_id_a=i + 1,

                        job_id_b=j + 1,

                        similarity=round(
                            similarity,
                            4
                        ),
                    )

                )

        return results

    # ==================================================
    # Clustering
    # ==================================================

    def _cluster_jobs(
        self,
        job_descriptions: list[str],
        skills_by_job: list[list[str]],
        embeddings,
    ) -> list[RoleCluster]:
        """
        Cluster Job Descriptions according to
        semantic similarity.
        """

        total_jobs = len(
            job_descriptions
        )

        # --------------------------------------------------
        # One JD does not require clustering.
        # --------------------------------------------------

        if total_jobs == 1:

            return [

                self._build_cluster(

                    cluster_id=1,

                    job_indices=[0],

                    job_descriptions=job_descriptions,

                    skills_by_job=skills_by_job,

                )

            ]

        # --------------------------------------------------
        # Convert embeddings to numpy.
        # --------------------------------------------------

        embedding_matrix = (
            embeddings.cpu().numpy()
        )

        # --------------------------------------------------
        # Agglomerative clustering.
        #
        # cosine distance = 1 - cosine similarity
        # --------------------------------------------------

        clustering = AgglomerativeClustering(

            n_clusters=None,

            distance_threshold=(
                1.0 -
                self.similarity_threshold
            ),

            metric="cosine",

            linkage="average",

        )

        labels = clustering.fit_predict(
            embedding_matrix
        )

        # --------------------------------------------------
        # Group job indexes by cluster label.
        # --------------------------------------------------

        grouped = {}

        for job_index, label in enumerate(labels):

            grouped.setdefault(
                int(label),
                []
            ).append(
                job_index
            )

        clusters = []

        for cluster_number, (
            cluster_label,
            job_indices
        ) in enumerate(
            sorted(
                grouped.items()
            ),
            start=1
        ):

            clusters.append(

                self._build_cluster(

                    cluster_id=cluster_number,

                    job_indices=job_indices,

                    job_descriptions=job_descriptions,

                    skills_by_job=skills_by_job,

                )

            )

        return clusters

    # ==================================================
    # Cluster construction
    # ==================================================

    def _build_cluster(
        self,
        cluster_id: int,
        job_indices: list[int],
        job_descriptions: list[str],
        skills_by_job: list[list[str]],
    ) -> RoleCluster:
        """
        Build a RoleCluster from a collection of JDs.
        """

        jobs = []

        all_skills = []

        roles = []

        for job_index in job_indices:

            jd = job_descriptions[
                job_index
            ]

            skills = skills_by_job[
                job_index
            ]

            role = self._extract_role(
                jd
            )

            if role:

                roles.append(
                    role
                )

            all_skills.extend(
                skills
            )

            jobs.append(

                RoleJob(

                    job_id=job_index + 1,

                    role=role,

                    skills=skills,

                )

            )

        common_skills = self._get_common_skills(
            skills_by_job=[
                skills_by_job[index]
                for index in job_indices
            ],
        )

        role = self._determine_cluster_role(
            roles,
            cluster_id
        )

        return RoleCluster(

            cluster_id=cluster_id,

            role=role,

            jobs=jobs,

            common_skills=common_skills,

        )

    # ==================================================
    # Role extraction
    # ==================================================

    @staticmethod
    def _extract_role(
        job_description: str,
    ) -> str | None:
        """
        Attempt to extract a role/title from a Job Description.

        Supported patterns include:

            Machine Learning Engineer

            Job Title: Machine Learning Engineer

            Position: Backend Engineer

            Role: Data Engineer

            We are hiring a Data Engineer...

            We need a Backend Engineer...

            Looking for a Machine Learning Engineer...

        The method intentionally does not use an LLM.
        """

        if not job_description:
            return None

        lines = [

            line.strip()

            for line in
            job_description.splitlines()

            if line.strip()

        ]

        if not lines:
            return None

        # --------------------------------------------------
        # Ignore common section headings.
        # --------------------------------------------------

        ignored_headers = {
            "job description",
            "description",
            "responsibilities",
            "requirements",
            "qualifications",
            "skills",
            "about the role",
            "about the job",
            "job requirements",
            "key responsibilities",
            "what you'll do",
            "what you will do",
        }

        # --------------------------------------------------
        # First look for explicit title labels.
        # --------------------------------------------------

        label_patterns = [

            r"^(?:job\s+title|title|position|role)\s*:\s*(.+)$",

            r"^(?:job\s+title|title|position|role)\s*[-–—]\s*(.+)$",

        ]

        for line in lines:

            for pattern in label_patterns:

                match = re.match(
                    pattern,
                    line,
                    flags=re.IGNORECASE,
                )

                if match:

                    role = (
                        match.group(1)
                        .strip()
                    )

                    return (
                        role
                        if role
                        else None
                    )

        # --------------------------------------------------
        # If the first meaningful line looks like a title,
        # use it.
        #
        # This handles:
        #
        # Machine Learning Engineer
        #
        # Python
        # PyTorch
        # --------------------------------------------------

        first_line = lines[0]

        if (
            first_line.lower()
            not in ignored_headers
            and
            RoleIntelligenceService._looks_like_role_title(
                first_line
            )
        ):

            return first_line

        # --------------------------------------------------
        # Search the beginning of the JD for common
        # natural-language role patterns.
        # --------------------------------------------------

        text = " ".join(lines)

        role_patterns = [

            r"\b(?:we\s+are\s+)?hiring\s+(?:a|an)\s+"
            r"([A-Z][A-Za-z0-9&/+.\-]*(?:\s+[A-Z][A-Za-z0-9&/+.\-]*){0,5})",

            r"\bwe\s+need\s+(?:a|an)\s+"
            r"([A-Z][A-Za-z0-9&/+.\-]*(?:\s+[A-Z][A-Za-z0-9&/+.\-]*){0,5})",

            r"\blooking\s+for\s+(?:a|an)\s+"
            r"([A-Z][A-Za-z0-9&/+.\-]*(?:\s+[A-Z][A-Za-z0-9&/+.\-]*){0,5})",

            r"\bseeking\s+(?:a|an)\s+"
            r"([A-Z][A-Za-z0-9&/+.\-]*(?:\s+[A-Z][A-Za-z0-9&/+.\-]*){0,5})",

        ]

        for pattern in role_patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:

                role = (
                    match.group(1)
                    .strip()
                )

                role = (
                    RoleIntelligenceService
                    ._clean_extracted_role(role)
                )

                if role:

                    return role

        # --------------------------------------------------
        # If no role can be confidently extracted,
        # return None.
        #
        # The cluster will receive a fallback label.
        # --------------------------------------------------

        return None

    # ==================================================
    # Role title heuristic
    # ==================================================

    @staticmethod
    def _looks_like_role_title(
        text: str,
    ) -> bool:
        """
        Determine whether a short line plausibly represents
        a job title.
        """

        cleaned = text.strip()

        if not cleaned:
            return False

        words = cleaned.split()

        # A title should generally be reasonably short.
        if len(words) > 8:
            return False

        # Avoid lines that look like complete sentences.
        sentence_markers = {
            "we",
            "our",
            "the",
            "this",
            "you",
            "your",
            "we're",
            "we",
        }

        if words[0].lower() in sentence_markers:
            return False

        # Avoid obvious sentence punctuation.
        if cleaned.endswith(
            (".", "!", "?", ":")
        ):
            return False

        # A title generally contains at least one
        # role-related keyword.
        role_keywords = {

            "engineer",
            "developer",
            "scientist",
            "analyst",
            "architect",
            "manager",
            "administrator",
            "consultant",
            "designer",
            "specialist",
            "lead",
            "director",
            "intern",
            "researcher",
            "devops",
            "administrator",
            "technician",
        }

        lower_text = cleaned.lower()

        return any(
            keyword in lower_text
            for keyword in role_keywords
        )

    # ==================================================
    # Role cleanup
    # ==================================================

    @staticmethod
    def _clean_extracted_role(
        role: str,
    ) -> str | None:
        """
        Clean a role extracted from natural language.
        """

        if not role:
            return None

        role = role.strip()

        # Remove trailing punctuation.
        role = role.rstrip(
            ".,;:!?-"
        ).strip()

        # Stop at common sentence boundaries.
        role = re.split(
            r"\s+(?:with|who|that|and|experience|experienced)\s+",
            role,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0].strip()

        if not role:
            return None

        # Prevent an excessively long accidental extraction.
        if len(role.split()) > 8:
            return None

        return role

    # ==================================================
    # Cluster role
    # ==================================================

    @staticmethod
    def _determine_cluster_role(
        roles: list[str],
        cluster_id: int,
    ) -> str:
        """
        Determine the representative role for a cluster.

        If explicit roles exist, the most frequent role is used.
        Otherwise a neutral fallback label is returned.
        """

        if not roles:

            return (
                f"Role Cluster {cluster_id}"
            )

        counter = Counter(
            role.strip()
            for role in roles
            if role.strip()
        )

        if not counter:

            return (
                f"Role Cluster {cluster_id}"
            )

        return counter.most_common(1)[0][0]

    # ==================================================
    # Common skills
    # ==================================================

    @staticmethod
    def _get_common_skills(
        skills_by_job: list[list[str]],
    ) -> list[str]:
        """
        Determine skills shared by at least 50% of the
        jobs in a cluster.

        Each job contributes a skill at most once.
        """

        if not skills_by_job:
            return []

        job_count = len(
            skills_by_job
        )

        skill_occurrences = Counter()

        for skills in skills_by_job:

            unique_skills = {
                skill.strip().lower()
                for skill in skills
                if skill.strip()
            }

            skill_occurrences.update(
                unique_skills
            )

        minimum_occurrences = max(
            1,
            (job_count + 1) // 2
        )

        common = [

            skill

            for skill, count
            in skill_occurrences.items()

            if count >= minimum_occurrences

        ]

        return sorted(
            common
        )

    # ==================================================
    # Skill normalization
    # ==================================================

    @staticmethod
    def _unique_skills(
        skills: list[str],
    ) -> list[str]:
        """
        Remove duplicate skills while preserving a
        deterministic representation.
        """

        seen = set()

        unique = []

        for skill in skills:

            if not skill:
                continue

            cleaned = skill.strip()

            if not cleaned:
                continue

            key = cleaned.lower()

            if key in seen:
                continue

            seen.add(key)

            unique.append(
                cleaned
            )

        return sorted(
            unique,
            key=str.lower
        )