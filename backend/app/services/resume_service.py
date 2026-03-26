"""Facade service coordinating resume workflows."""

from __future__ import annotations

import logging

from fastapi import UploadFile

from app.models.schemas import AnalyzeRequest, OptimizeResponse, ResumeUploadResponse
from app.nlp.scoring import ATSScoringService
from app.parsers.resume_parser import ResumeParserService
from app.services.optimizer_service import ResumeOptimizerService
from app.services.repository import ResumeRepository
from app.services.storage_service import StorageService
from app.utils.errors import NotFoundError

logger = logging.getLogger(__name__)


class ResumeWorkflowService:
    """Coordinate parsing, analysis, and optimization flows."""

    def __init__(
        self,
        storage_service: StorageService,
        repository: ResumeRepository,
        parser_service: ResumeParserService,
        scoring_service: ATSScoringService,
        optimizer_service: ResumeOptimizerService,
    ) -> None:
        self.storage_service = storage_service
        self.repository = repository
        self.parser_service = parser_service
        self.scoring_service = scoring_service
        self.optimizer_service = optimizer_service

    async def upload_resume(self, file: UploadFile) -> ResumeUploadResponse:
        """Save and parse an uploaded resume."""

        resume_id, path = await self.storage_service.create_temp_upload(file)
        try:
            parsed_resume = self.parser_service.parse(resume_id, path, file.filename or path.name)
            self.repository.save(parsed_resume)
            logger.info(
                "resume_upload_success",
                extra={"resume_id": resume_id, "upload_name": file.filename or path.name},
            )
            return ResumeUploadResponse(resume=parsed_resume)
        finally:
            self.storage_service.delete_temp_upload(path)

    def analyze(self, payload: AnalyzeRequest):
        """Analyze a stored resume against a job description."""

        resume = self.repository.get(payload.resume_id)
        if resume is None:
            raise NotFoundError("Resume not found. Please upload the resume again.")

        analysis = self.scoring_service.analyze(
            resume.resume_id,
            resume.text,
            payload.job_description,
        )
        logger.info(
            "resume_analysis_complete",
            extra={
                "resume_id": resume.resume_id,
                "total_score": analysis.total_score,
                "breakdown": analysis.breakdown.model_dump(),
            },
        )
        return analysis

    def optimize(self, payload: AnalyzeRequest) -> OptimizeResponse:
        """Optimize a stored resume for the supplied job description."""

        resume = self.repository.get(payload.resume_id)
        if resume is None:
            raise NotFoundError("Resume must be uploaded before optimization.")

        original_analysis = self.scoring_service.analyze(
            resume.resume_id,
            resume.text,
            payload.job_description,
        )
        optimized_resume, docx_bytes = self.optimizer_service.optimize(
            resume.resume_id,
            resume.text,
            payload.job_description,
            original_analysis.missing_keywords,
        )
        self.storage_service.save_generated_document(optimized_resume.document_id, docx_bytes)
        optimized_analysis = self.scoring_service.analyze(
            resume.resume_id,
            optimized_resume.plain_text,
            payload.job_description,
        )
        return OptimizeResponse(
            original_analysis=original_analysis,
            optimized_analysis=optimized_analysis,
            optimized_resume=optimized_resume,
        )
