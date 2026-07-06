from pathlib import Path


# ------------------------------
# Project Directories
# ------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

SKILLS_DIR = DATA_DIR / "skills"

UPLOADS_DIR = BASE_DIR / "uploads"


# ------------------------------
# Skill Files
# ------------------------------

SKILL_VOCABULARY_PATH = (
    DATA_DIR / "skills.txt"
)

KNOWLEDGE_BASE_PATH = (
    SKILLS_DIR / "knowledge_base.json"
)


# ------------------------------
# NLP Models
# ------------------------------

SPACY_MODEL = "en_core_web_sm"

SENTENCE_TRANSFORMER_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ------------------------------
# Matching
# ------------------------------

SEMANTIC_SIMILARITY_THRESHOLD = 0.70