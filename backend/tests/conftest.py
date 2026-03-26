"""Shared pytest fixtures."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest
from docx import Document
from fastapi.testclient import TestClient

from app.api.dependencies import get_resume_repository
from app.core.config import get_settings
from app.main import create_app


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path: Path):
    """Force storage into a temp directory for each test."""

    settings = get_settings()
    settings.upload_dir = tmp_path / "uploads"
    settings.generated_dir = tmp_path / "generated"
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.generated_dir.mkdir(parents=True, exist_ok=True)
    from app.api.dependencies import get_resume_workflow_service

    get_resume_repository()._store.clear()
    get_resume_workflow_service().storage_service.clear_generated_documents()
    yield
    get_resume_repository()._store.clear()
    get_resume_workflow_service().storage_service.clear_generated_documents()


@pytest.fixture
def client() -> TestClient:
    """Return a FastAPI test client."""

    app = create_app()
    return TestClient(app)


@pytest.fixture
def sample_resume_text() -> str:
    """Return a representative resume sample."""

    return """Jane Doe
Summary
Product-minded software engineer building internal tools and candidate workflows.

Skills
Python, FastAPI, React, SQL, Docker

Experience
- Built hiring workflow automation for a recruiting operations team.
- Improved resume review turnaround by 35% through workflow redesign.
- Designed APIs for analytics dashboards used by 12 recruiters.

Education
BS Computer Science
"""


@pytest.fixture
def sample_job_description() -> str:
    """Return a representative job description."""

    return (
        "We are hiring a software engineer with FastAPI, React, SQL, Docker, "
        "keyword optimization, ATS workflow, analytics, communication, and Python experience."
    )


@pytest.fixture
def sample_docx_bytes(sample_resume_text: str) -> bytes:
    """Return a DOCX file in memory for upload tests."""

    document = Document()
    for line in sample_resume_text.splitlines():
        document.add_paragraph(line)
    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()


@pytest.fixture
def resume_catalog() -> list[str]:
    """Return diverse synthetic resume formats for deterministic testing."""

    return [
        """Alex Chen
SUMMARY
Backend engineer focused on Python services and internal tooling.
SKILLS
Python, FastAPI, PostgreSQL, Docker
EXPERIENCE
- Built APIs for recruiting dashboards used by 25 hiring managers.
EDUCATION
BS Computer Science
""",
        """Jordan Patel
Profile
Frontend developer building analytics-heavy hiring products.
Technical Skills
React, TypeScript, CSS, JavaScript
Professional Experience
- Improved recruiter workflow completion by 22%.
Education
BA Information Systems
""",
        """Taylor Morgan
Core Competencies
SQL, Tableau, Reporting, Stakeholder Communication
Employment History
- Developed scorecards for talent operations and weekly KPI reporting.
Academic Background
MBA
""",
        """Riley Brooks
Summary
Recruiting operations specialist supporting ATS process improvement.
Experience
- Coordinated 120 interview loops across quarterly hiring cycles.
- Reduced scheduling turnaround by 31%.
Education
BS Management
""",
        """Casey Nguyen
Skills
Machine Learning, NLP, Python, Scikit-learn
Experience
- Built document classification pipelines for resume ingestion.
- Increased extraction accuracy to 91%.
Education
MS Data Science
""",
        """Morgan Lee
Summary
Product manager aligning candidate workflow requirements with engineering delivery.
Experience
- Led roadmap planning for application review automation.
Education
BA Business Administration
""",
        """Sam Rivera
Summary
Cloud engineer with AWS and CI/CD experience.
Skills
AWS, Terraform, Kubernetes, CI/CD
Experience
- Automated deployment pipelines for HR applications.
Education
BS Information Technology
""",
        """Jamie Kim
Summary
Full-stack engineer with JS, TS, React, Node, and API design experience.
Experience
- Built multi-tenant dashboards for recruiting analytics.
Education
BS Software Engineering
""",
        """Avery Scott
Profile
Data analyst focused on dashboards, SQL optimization, and reporting.
Experience
- Built weekly performance reports for talent acquisition leaders.
- Supported 14 recruiters with funnel analysis.
Education
BS Statistics
""",
        """Drew Hall
Summary
Operations generalist.
Experience
- Worked on hiring.
Education
College Diploma
""",
    ]


@pytest.fixture
def job_description_catalog() -> list[str]:
    """Return varied job descriptions for ATS scoring tests."""

    return [
        "Hiring a backend engineer with Python, FastAPI, PostgreSQL, Docker, APIs, and analytics experience.",
        "Seeking a frontend engineer with React, JavaScript, TypeScript, CSS, dashboards, and collaboration skills.",
        "Looking for a recruiting operations specialist with ATS, scheduling, communication, reporting, and workflow improvement experience.",
        "Need a machine learning engineer with NLP, Python, model evaluation, document parsing, and data pipeline experience.",
        "Searching for a data analyst with SQL, dashboards, stakeholder communication, reporting, and KPI tracking expertise.",
    ]
