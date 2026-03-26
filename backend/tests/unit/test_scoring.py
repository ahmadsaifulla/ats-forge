"""Unit tests for ATS scoring."""

import pytest

from app.nlp.scoring import ATSScoringService


def test_scoring_returns_breakdown(sample_resume_text: str, sample_job_description: str):
    service = ATSScoringService()

    analysis = service.analyze("resume-1", sample_resume_text, sample_job_description)

    assert analysis.resume_id == "resume-1"
    assert 0 <= analysis.total_score <= 100
    assert analysis.breakdown.keyword_score > 0
    assert analysis.breakdown.structure_score > 0
    assert "keyword optimization" in analysis.missing_keywords
    assert analysis.keyword_insights.skill_frequencies
    assert analysis.keyword_insights.stuffing_penalty >= 0


def test_scoring_handles_irrelevant_job_description(sample_resume_text: str):
    service = ATSScoringService()
    irrelevant_jd = "Seeking a marine biologist with scuba certification and coral reef expedition leadership."

    analysis = service.analyze("resume-2", sample_resume_text, irrelevant_jd)

    assert analysis.breakdown.keyword_score < 30
    assert len(analysis.missing_keywords) > 0


@pytest.mark.parametrize("resume_index", list(range(10)))
@pytest.mark.parametrize("job_index", list(range(5)))
def test_scoring_is_deterministic_across_resume_and_job_catalogs(
    resume_catalog: list[str],
    job_description_catalog: list[str],
    resume_index: int,
    job_index: int,
):
    service = ATSScoringService()
    resume_text = resume_catalog[resume_index]
    job_description = job_description_catalog[job_index]

    first = service.analyze("resume-x", resume_text, job_description)
    second = service.analyze("resume-x", resume_text, job_description)

    assert first.total_score == second.total_score
    assert first.breakdown == second.breakdown
    assert first.keyword_insights == second.keyword_insights
