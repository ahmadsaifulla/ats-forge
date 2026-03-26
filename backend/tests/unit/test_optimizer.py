"""Unit tests for optimizer behavior."""

from app.services.optimizer_service import ResumeOptimizerService


def test_optimizer_preserves_truthful_structure(sample_resume_text: str):
    service = ResumeOptimizerService()

    optimized_resume, _ = service.optimize(
        "resume-1",
        sample_resume_text,
        "Software engineer with analytics, stakeholder communication, FastAPI, React, and process improvement experience.",
        ["analytics", "stakeholder communication"],
    )

    assert optimized_resume.sections[0].title == "SUMMARY"
    assert "stakeholder communication" in optimized_resume.plain_text.lower()
    assert "inventing new experience" not in optimized_resume.plain_text.lower()
    assert "target role keywords to incorporate where accurate" not in optimized_resume.plain_text.lower()
    assert any(section.title == "SKILLS" for section in optimized_resume.sections)
    assert any(item.label == "Rewritten content" for item in optimized_resume.sections[0].items)


def test_optimizer_rewrites_weak_bullets_into_action_oriented_lines():
    service = ResumeOptimizerService()
    resume_text = """Summary
Hands-on operations specialist.

Experience
- responsible for resume screening and intake coordination
- worked on interview scheduling for recruiters
"""

    optimized_resume, _ = service.optimize(
        "resume-2",
        resume_text,
        "Recruiting coordinator with scheduling, communication, intake, and applicant tracking experience.",
        ["applicant tracking", "communication"],
    )

    experience_section = next(section for section in optimized_resume.sections if section.title == "EXPERIENCE")
    assert experience_section.content[0].startswith(("Delivered", "Drove", "Led", "Managed", "Coordinated"))
    assert "responsible for" not in " ".join(experience_section.content).lower()
    suggestions_section = next(section for section in optimized_resume.sections if section.title == "SUGGESTED ADDITIONS")
    assert all(label == "Suggested additions" for label in suggestions_section.labels)
