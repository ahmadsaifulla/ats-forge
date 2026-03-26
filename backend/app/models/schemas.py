"""Pydantic schemas used by the API and services."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ParsedResume(BaseModel):
    """Structured parsed resume payload."""

    resume_id: str
    filename: str
    text: str
    sections: dict[str, str]
    detected_file_type: Literal["pdf", "docx"]
    warnings: list[str] = Field(default_factory=list)


class ResumeUploadResponse(BaseModel):
    """Response returned after resume upload."""

    resume: ParsedResume


class AnalyzeRequest(BaseModel):
    """Request body for ATS analysis."""

    resume_id: str = Field(min_length=1)
    job_description: str = Field(min_length=20, max_length=20000)

    @field_validator("job_description")
    @classmethod
    def sanitize_job_description(cls, value: str) -> str:
        """Prevent low-signal submissions."""

        stripped = value.strip()
        if len(stripped.split()) < 5:
            raise ValueError("Job description must contain at least five words.")
        return stripped


class ScoreBreakdown(BaseModel):
    """ATS score components."""

    keyword_score: float
    semantic_score: float
    structure_score: float


class AnalysisResponse(BaseModel):
    """ATS analysis response."""

    resume_id: str
    total_score: float
    breakdown: ScoreBreakdown
    missing_keywords: list[str]
    matched_keywords: list[str]
    suggestions: list[str]


class OptimizedResumeSection(BaseModel):
    """A resume section in the generated output."""

    title: str
    content: list[str]


class OptimizedResume(BaseModel):
    """Structured optimized resume payload."""

    resume_id: str
    document_id: str
    plain_text: str
    sections: list[OptimizedResumeSection]
    disclaimer: str
    generated_at: datetime


class OptimizeResponse(BaseModel):
    """Resume optimization response."""

    original_analysis: AnalysisResponse
    optimized_analysis: AnalysisResponse
    optimized_resume: OptimizedResume


class ErrorResponse(BaseModel):
    """Error envelope."""

    detail: str
