"""Dependency providers for FastAPI routes."""

from __future__ import annotations

from functools import lru_cache

from app.nlp.scoring import ATSScoringService
from app.parsers.resume_parser import ResumeParserService
from app.services.optimizer_service import ResumeOptimizerService
from app.services.repository import ResumeRepository
from app.services.resume_service import ResumeWorkflowService
from app.services.storage_service import StorageService


@lru_cache(maxsize=1)
def get_resume_repository() -> ResumeRepository:
    """Return the in-memory repository singleton."""

    return ResumeRepository()


@lru_cache(maxsize=1)
def get_resume_workflow_service() -> ResumeWorkflowService:
    """Return the primary workflow service singleton."""

    return ResumeWorkflowService(
        storage_service=StorageService(),
        repository=get_resume_repository(),
        parser_service=ResumeParserService(),
        scoring_service=ATSScoringService(),
        optimizer_service=ResumeOptimizerService(),
    )
