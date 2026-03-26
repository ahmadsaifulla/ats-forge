"""Text normalization and extraction helpers."""

from __future__ import annotations

import re
from collections import Counter


SECTION_PATTERNS = {
    "summary": re.compile(r"^(summary|profile|professional summary)$", re.IGNORECASE),
    "skills": re.compile(r"^(skills|technical skills|core competencies)$", re.IGNORECASE),
    "experience": re.compile(
        r"^(experience|work experience|professional experience|employment history)$",
        re.IGNORECASE,
    ),
    "education": re.compile(r"^(education|academic background)$", re.IGNORECASE),
}

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "have",
    "your",
    "you",
    "into",
    "will",
    "using",
    "about",
    "they",
    "their",
    "role",
    "team",
    "work",
    "years",
    "year",
    "plus",
    "such",
    "able",
    "experience",
}

HIRING_BOILERPLATE = {
    "appreciate",
    "apply",
    "applying",
    "company",
    "considered",
    "depending",
    "fill",
    "growing",
    "hiring",
    "level",
    "list",
    "looking",
    "position",
    "qualifications",
    "rapidly",
    "review",
    "taking",
    "time",
}

ABBREVIATIONS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "js": "javascript",
    "ts": "typescript",
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "etl": "extract transform load",
    "llm": "large language models",
    "api": "application programming interfaces",
    "ats": "applicant tracking systems",
    "oop": "object oriented programming",
    "oops": "object oriented programming",
    "c/c++": "c++",
}

SEMANTIC_SKILL_GROUPS = {
    "machine learning": {"ml", "machine learning", "predictive modeling"},
    "javascript": {"js", "javascript", "ecmascript"},
    "natural language processing": {"nlp", "natural language processing", "text analytics"},
    "applicant tracking systems": {"ats", "applicant tracking", "talent systems"},
    "data analysis": {"analytics", "analysis", "reporting", "dashboards"},
    "object oriented programming": {
        "oop",
        "object oriented programming",
        "object oriented development",
        "object oriented programmer",
    },
    "c++": {"c++", "c/c++"},
}


def normalize_text(text: str) -> str:
    """Normalize whitespace and common resume noise."""

    cleaned = text.replace("\u2022", "-").replace("\uf0b7", "-")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", cleaned)
    cleaned = re.sub(r"([a-z])([A-Z])", r"\1 \2", cleaned)
    return cleaned.strip()


def split_lines(text: str) -> list[str]:
    """Return non-empty normalized lines."""

    return [line.strip() for line in text.splitlines() if line.strip()]


def extract_sections(text: str) -> dict[str, str]:
    """Extract rough sections using common resume headings."""

    lines = split_lines(text)
    sections: dict[str, list[str]] = {"other": []}
    current_section = "other"

    for line in lines:
        matched_section = next(
            (name for name, pattern in SECTION_PATTERNS.items() if pattern.match(line.lower())),
            None,
        )
        if matched_section:
            current_section = matched_section
            sections.setdefault(current_section, [])
            continue
        sections.setdefault(current_section, []).append(line)

    return {name: "\n".join(values).strip() for name, values in sections.items() if values}


def extract_bullets(text: str) -> list[str]:
    """Extract bullet-like lines from resume text."""

    return [
        line.strip(" -")
        for line in split_lines(text)
        if line.lstrip().startswith(("-", "*")) or re.match(r"^\d+\.", line)
    ]


def extract_keywords(text: str, *, max_keywords: int = 30) -> list[str]:
    """Extract candidate keywords from job description text."""

    lowered = expand_abbreviations(text.lower())
    tokens = re.findall(r"\b[a-z][a-z0-9+.#/-]{1,}\b", lowered)
    filtered_tokens = [
        token
        for token in tokens
        if token not in STOPWORDS and token not in HIRING_BOILERPLATE and len(token) > 2
    ]

    unigram_counts = Counter(token.strip() for token in filtered_tokens if token.strip())
    bigram_counts: Counter[str] = Counter()
    for index in range(len(filtered_tokens) - 1):
        first = filtered_tokens[index]
        second = filtered_tokens[index + 1]
        if (
            first in STOPWORDS
            or second in STOPWORDS
            or first in HIRING_BOILERPLATE
            or second in HIRING_BOILERPLATE
        ):
            continue
        bigram = f"{first} {second}".strip()
        if bigram:
            bigram_counts[bigram] += 1

    ranked_unigrams = sorted(
        unigram_counts.items(),
        key=lambda item: (-item[1], -_keyword_priority(item[0]), -len(item[0]), item[0]),
    )
    ranked_bigrams = sorted(
        bigram_counts.items(),
        key=lambda item: (-item[1], -_keyword_priority(item[0]), -len(item[0]), item[0]),
    )

    combined: list[str] = []
    for phrase, _ in ranked_unigrams:
        if phrase not in combined:
            combined.append(phrase)
    for phrase, _ in ranked_bigrams:
        if phrase not in combined and not _is_low_signal_phrase(phrase):
            combined.append(phrase)
    return combined[:max_keywords]


def _keyword_priority(keyword: str) -> int:
    """Return a higher priority for technical, language, and domain-specific keywords."""

    technical_patterns = (
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "fastapi",
        "docker",
        "sql",
        "c++",
        "object oriented",
        "machine learning",
        "artificial intelligence",
        "backend",
        "frontend",
        "api",
    )
    return int(any(pattern in keyword for pattern in technical_patterns))


def _is_low_signal_phrase(phrase: str) -> bool:
    """Return True when a phrase is generic hiring boilerplate."""

    parts = phrase.split()
    return all(part in HIRING_BOILERPLATE or part in STOPWORDS for part in parts)


def expand_abbreviations(text: str) -> str:
    """Expand common abbreviations for improved matching."""

    expanded = text
    for short, long_form in ABBREVIATIONS.items():
        expanded = re.sub(rf"\b{re.escape(short)}\b", long_form, expanded, flags=re.IGNORECASE)
    return expanded


def normalize_keyword(keyword: str) -> str:
    """Normalize a keyword to a canonical form."""

    expanded = expand_abbreviations(keyword.lower())
    expanded = re.sub(r"[^a-z0-9+#.\s/-]", " ", expanded)
    expanded = re.sub(r"\s+", " ", expanded).strip()
    if "object oriented" in expanded:
        return "object oriented programming"
    for canonical, variants in SEMANTIC_SKILL_GROUPS.items():
        if expanded in variants:
            return canonical
    return expanded


def keyword_frequency(text: str, keywords: list[str]) -> dict[str, int]:
    """Count normalized keyword frequency in text."""

    normalized_text = normalize_keyword(text)
    frequencies: dict[str, int] = {}
    for keyword in keywords:
        normalized = normalize_keyword(keyword)
        if not normalized:
            continue
        pattern = rf"\b{re.escape(normalized)}\b"
        frequencies[normalized] = len(re.findall(pattern, normalized_text))
    return dict(sorted(frequencies.items(), key=lambda item: (-item[1], item[0])))


def infer_semantic_skills(text: str) -> list[str]:
    """Infer skills from known semantic groups."""

    normalized_text = normalize_keyword(text)
    inferred = []
    for canonical, variants in SEMANTIC_SKILL_GROUPS.items():
        if any(variant in normalized_text for variant in variants):
            inferred.append(canonical)
    return inferred


def measurable_achievement_count(text: str) -> int:
    """Count bullet points that appear to contain measurable achievements."""

    bullets = extract_bullets(text)
    pattern = re.compile(
        r"(\d+[%+]|[$]\d+|\d+\s*(users|clients|projects|teams|hours|days|months|recruiters|candidates|roles))",
        re.I,
    )
    return sum(1 for bullet in bullets if pattern.search(bullet))
