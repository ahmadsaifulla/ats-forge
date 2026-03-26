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
    get_resume_repository()._store.clear()
    yield
    get_resume_repository()._store.clear()


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
