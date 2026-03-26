"""ATS scoring engine."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

from app.models.schemas import AnalysisResponse, ScoreBreakdown
from app.nlp.model_manager import get_sentence_transformer, get_spacy_model
from app.utils.text import extract_bullets, extract_keywords, measurable_achievement_count

try:  # pragma: no cover - exercised indirectly when dependency exists
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except Exception:  # pragma: no cover - fallback path is unit tested instead
    TfidfVectorizer = None
    cosine_similarity = None


@dataclass(slots=True)
class ATSWeights:
    """Weight configuration for ATS scoring."""

    keyword: float = 0.5
    semantic: float = 0.3
    structure: float = 0.2


class ATSScoringService:
    """Calculate ATS score for resumes against a job description."""

    def __init__(self, weights: ATSWeights | None = None) -> None:
        self.weights = weights or ATSWeights()

    def analyze(self, resume_id: str, resume_text: str, job_description: str) -> AnalysisResponse:
        """Run complete ATS analysis."""

        keyword_score, matched_keywords, missing_keywords = self._keyword_score(
            resume_text,
            job_description,
        )
        semantic_score = self._semantic_score(resume_text, job_description)
        structure_score, suggestions = self._structure_score(resume_text)
        total_score = (
            keyword_score * self.weights.keyword
            + semantic_score * self.weights.semantic
            + structure_score * self.weights.structure
        )

        return AnalysisResponse(
            resume_id=resume_id,
            total_score=round(total_score, 2),
            breakdown=ScoreBreakdown(
                keyword_score=round(keyword_score, 2),
                semantic_score=round(semantic_score, 2),
                structure_score=round(structure_score, 2),
            ),
            missing_keywords=missing_keywords,
            matched_keywords=matched_keywords,
            suggestions=suggestions,
        )

    def _keyword_score(
        self,
        resume_text: str,
        job_description: str,
    ) -> tuple[float, list[str], list[str]]:
        """Compute TF-IDF cosine similarity and keyword gaps."""

        if TfidfVectorizer is not None and cosine_similarity is not None:
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        else:
            similarity = self._token_overlap_similarity(resume_text, job_description)

        jd_keywords = extract_keywords(job_description)
        resume_lower = resume_text.lower()
        matched = [keyword for keyword in jd_keywords if keyword in resume_lower]
        missing = [keyword for keyword in jd_keywords if keyword not in resume_lower][:15]
        return similarity * 100, matched[:15], missing

    def _semantic_score(self, resume_text: str, job_description: str) -> float:
        """Compute semantic similarity using sentence-transformers with a fallback."""

        model = get_sentence_transformer()
        if model is not None:
            resume_embedding = self._encode_text(model, resume_text)
            job_embedding = self._encode_text(model, job_description)
            similarity = float(resume_embedding @ job_embedding)
            return max(0.0, min(100.0, similarity * 100))

        if TfidfVectorizer is not None and cosine_similarity is not None:
            vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
            matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        else:
            similarity = self._token_overlap_similarity(resume_text, job_description)
        return similarity * 100

    def _structure_score(self, resume_text: str) -> tuple[float, list[str]]:
        """Score ATS-readability signals in the resume structure."""

        lowered = resume_text.lower()
        headings_present = sum(
            1
            for heading in ("skills", "experience", "education")
            if re.search(rf"^\s*{heading}\s*$", lowered, re.MULTILINE)
        )
        bullet_count = len(extract_bullets(resume_text))
        measurable_count = measurable_achievement_count(resume_text)
        noun_chunks = 0
        spacy_model = get_spacy_model()
        if spacy_model is not None:
            doc = spacy_model(resume_text[:10000])
            noun_chunks = len(list(doc.noun_chunks)) if doc.has_annotation("DEP") else 0

        heading_score = min(100.0, headings_present / 3 * 100)
        bullet_score = min(100.0, bullet_count / 8 * 100)
        measurable_score = min(100.0, measurable_count / 4 * 100)
        language_score = 100.0 if noun_chunks > 5 else 65.0
        final_score = (heading_score * 0.35) + (bullet_score * 0.25) + (measurable_score * 0.25) + (language_score * 0.15)

        suggestions: list[str] = []
        if headings_present < 3:
            suggestions.append("Add clear section headings for Skills, Experience, and Education.")
        if bullet_count < 4:
            suggestions.append("Use concise bullet points to make achievements easier for ATS systems to parse.")
        if measurable_count < 2:
            suggestions.append("Add measurable outcomes such as percentages, counts, or revenue impact where accurate.")
        if not suggestions:
            suggestions.append("Resume structure is ATS-friendly; focus next on targeted keyword alignment.")

        return final_score, suggestions


    @staticmethod
    @lru_cache(maxsize=128)
    def _encode_text(model, text: str):
        """Cache embeddings to avoid repeat computation for identical text."""

        return model.encode(text, normalize_embeddings=True)

    @staticmethod
    def _token_overlap_similarity(first_text: str, second_text: str) -> float:
        """Fallback similarity based on normalized token overlap."""

        token_pattern = re.compile(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{1,}\b")
        first_tokens = set(token_pattern.findall(first_text.lower()))
        second_tokens = set(token_pattern.findall(second_text.lower()))
        if not first_tokens or not second_tokens:
            return 0.0
        return len(first_tokens & second_tokens) / len(first_tokens | second_tokens)
