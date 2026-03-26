"""Facade service coordinating resume workflows."""

from __future__ import annotations

from fastapi import UploadFile

from app.models.schemas import AnalyzeRequest, OptimizeResponse, ResumeUploadResponse
from app.nlp.scoring import ATSScoringService
from app.parsers.resume_parser import ResumeParserService
from app.services.optimizer_service import ResumeOptimizerService
from app.services.repository import ResumeRepository
from app.services.storage_service import StorageService
from app.utils.errors import FileStorageError, ParsingError


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

        resume_id, path = await self.storage_service.save_upload(file)
        parsed_resume = self.parser_service.parse(resume_id, path, file.filename or path.name)
        self.repository.save(parsed_resume)
        return ResumeUploadResponse(resume=parsed_resume)

    def analyze(self, payload: AnalyzeRequest):
        """Analyze a stored resume against a job description."""

        resume = self.repository.get(payload.resume_id)
        if resume is None:
            stored_path = self.storage_service.get_upload_path(payload.resume_id)
            if stored_path is None:
                raise FileStorageError("Resume not found. Please upload the resume again.")
            resume = self.parser_service.parse(payload.resume_id, stored_path, stored_path.name)
            self.repository.save(resume)

        return self.scoring_service.analyze(
            resume.resume_id,
            resume.text,
            payload.job_description,
        )

    def optimize(self, payload: AnalyzeRequest) -> OptimizeResponse:
        """Optimize a stored resume for the supplied job description."""

        resume = self.repository.get(payload.resume_id)
        if resume is None:
            raise ParsingError("Resume must be uploaded before optimization.")

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
