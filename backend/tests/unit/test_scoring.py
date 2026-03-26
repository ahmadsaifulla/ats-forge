"""Unit tests for ATS scoring."""

from app.nlp.scoring import ATSScoringService


def test_scoring_returns_breakdown(sample_resume_text: str, sample_job_description: str):
    service = ATSScoringService()

    analysis = service.analyze("resume-1", sample_resume_text, sample_job_description)

    assert analysis.resume_id == "resume-1"
    assert 0 <= analysis.total_score <= 100
    assert analysis.breakdown.keyword_score > 0
    assert analysis.breakdown.structure_score > 0
    assert "keyword optimization" in analysis.missing_keywords


def test_scoring_handles_irrelevant_job_description(sample_resume_text: str):
    service = ATSScoringService()
    irrelevant_jd = "Seeking a marine biologist with scuba certification and coral reef expedition leadership."

    analysis = service.analyze("resume-2", sample_resume_text, irrelevant_jd)

    assert analysis.breakdown.keyword_score < 30
    assert len(analysis.missing_keywords) > 0
