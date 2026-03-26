"""Unit tests for text utilities."""

from app.utils.text import extract_keywords, extract_sections, measurable_achievement_count, normalize_text


def test_normalize_text_removes_noise():
    raw_text = "Skills\u2022Python   FastAPI\n\n\nExperience"
    normalized = normalize_text(raw_text)

    assert "\u2022" not in normalized
    assert "  " not in normalized
    assert normalized.count("\n\n") <= 1


def test_extract_sections_detects_standard_headings(sample_resume_text: str):
    sections = extract_sections(sample_resume_text)

    assert sections["skills"].startswith("Python")
    assert "Improved resume review turnaround" in sections["experience"]


def test_extract_keywords_filters_low_signal_terms(sample_job_description: str):
    keywords = extract_keywords(sample_job_description, max_keywords=10)

    assert "fastapi" in keywords
    assert "python" in keywords


def test_measurable_achievement_count_detects_metrics(sample_resume_text: str):
    assert measurable_achievement_count(sample_resume_text) == 2
