"""In-memory repository for parsed resume state."""

from __future__ import annotations

from collections.abc import MutableMapping

from app.models.schemas import ParsedResume


class ResumeRepository:
    """Simple in-memory repository for parsed resumes."""

    def __init__(self) -> None:
        self._store: MutableMapping[str, ParsedResume] = {}

    def save(self, resume: ParsedResume) -> ParsedResume:
        """Persist a parsed resume model."""

        self._store[resume.resume_id] = resume
        return resume

    def get(self, resume_id: str) -> ParsedResume | None:
        """Get a parsed resume by ID."""

        return self._store.get(resume_id)
