from sentence_transformers import SentenceTransformer

from core.config import SENTENCE_TRANSFORMER_MODEL
from core.logger import logger


try:

    embedding_model = SentenceTransformer(
        SENTENCE_TRANSFORMER_MODEL
    )

    logger.info(
        "Sentence Transformer loaded: %s",
        SENTENCE_TRANSFORMER_MODEL
    )

except Exception as error:

    logger.error(
        "Failed to initialize Sentence Transformer: %s",
        SENTENCE_TRANSFORMER_MODEL
    )

    raise RuntimeError(
        "Embedding model could not be initialized."
    ) from error