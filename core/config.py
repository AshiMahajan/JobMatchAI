import os

from pathlib import Path

from dotenv import load_dotenv


# ==================================================
# ENVIRONMENT
# ==================================================

load_dotenv()


# ==================================================
# PROJECT DIRECTORIES
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

SKILLS_DIR = DATA_DIR / "skills"

UPLOADS_DIR = BASE_DIR / "uploads"


# ==================================================
# SKILL FILES
# ==================================================

SKILL_VOCABULARY_PATH = (
    DATA_DIR / "skills.txt"
)

KNOWLEDGE_BASE_PATH = (
    SKILLS_DIR / "knowledge_base.json"
)


# ==================================================
# NLP MODELS
# ==================================================

SPACY_MODEL = "en_core_web_sm"

SENTENCE_TRANSFORMER_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ==================================================
# MATCHING
# ==================================================

SEMANTIC_SIMILARITY_THRESHOLD = 0.70


# ==================================================
# LLM CONFIGURATION
# ==================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)