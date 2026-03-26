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
}


def normalize_text(text: str) -> str:
    """Normalize whitespace and common resume noise."""

    cleaned = text.replace("\u2022", "-").replace("\uf0b7", "-")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", cleaned)
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

    lowered = text.lower()
    phrases = re.findall(r"\b[a-z][a-z0-9+.#/-]{1,}\b(?:\s+[a-z][a-z0-9+.#/-]{1,}\b)?", lowered)
    filtered = [
        phrase.strip()
        for phrase in phrases
        if len(phrase) > 2 and not all(part in STOPWORDS for part in phrase.split())
    ]
    counts = Counter(filtered)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], -len(item[0]), item[0]))
    return [phrase for phrase, _ in ranked[:max_keywords]]


def measurable_achievement_count(text: str) -> int:
    """Count bullet points that appear to contain measurable achievements."""

    bullets = extract_bullets(text)
    pattern = re.compile(r"(\d+[%+]|[$]\d+|\d+\s*(users|clients|projects|teams|hours|days|months))", re.I)
    return sum(1 for bullet in bullets if pattern.search(bullet))
