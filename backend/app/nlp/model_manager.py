"""Lazy-loaded NLP model access."""

from __future__ import annotations

import logging
from functools import lru_cache

from app.core.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_spacy_model():
    """Load the spaCy language model lazily."""

    settings = get_settings()
    try:
        import spacy

        return spacy.load(settings.spacy_model)
    except Exception:  # pragma: no cover - depends on runtime install state
        logger.warning("spaCy model %s not available; using lightweight fallback.", settings.spacy_model)
        return None


@lru_cache(maxsize=1)
def get_sentence_transformer():
    """Load the sentence-transformer model lazily."""

    settings = get_settings()
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(settings.sentence_transformer_model)
    except Exception:  # pragma: no cover - depends on runtime install state
        logger.warning("SentenceTransformer model %s failed to load.", settings.sentence_transformer_model)
        return None
