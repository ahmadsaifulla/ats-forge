"""FastAPI endpoints."""

from __future__ import annotations

from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_resume_workflow_service
from app.models.schemas import (
    AnalysisResponse,
    AnalyzeRequest,
    ErrorResponse,
    OptimizeResponse,
    ResumeUploadResponse,
)
from app.services.resume_service import ResumeWorkflowService

router = APIRouter()


@router.post(
    "/upload-resume",
    response_model=ResumeUploadResponse,
    responses={400: {"model": ErrorResponse}},
)
async def upload_resume(
    file: UploadFile = File(...),
    service: ResumeWorkflowService = Depends(get_resume_workflow_service),
) -> ResumeUploadResponse:
    """Upload and parse a resume file."""

    return await service.upload_resume(file)


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def analyze_resume(
    payload: AnalyzeRequest,
    service: ResumeWorkflowService = Depends(get_resume_workflow_service),
):
    """Analyze ATS score for a stored resume."""

    return service.analyze(payload)


@router.post(
    "/optimize",
    response_model=OptimizeResponse,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def optimize_resume(
    payload: AnalyzeRequest,
    service: ResumeWorkflowService = Depends(get_resume_workflow_service),
) -> OptimizeResponse:
    """Optimize a resume for ATS alignment."""

    return service.optimize(payload)


@router.get(
    "/download/{document_id}",
    responses={404: {"model": ErrorResponse}},
)
async def download_resume(
    document_id: str,
    service: ResumeWorkflowService = Depends(get_resume_workflow_service),
):
    """Download a generated optimized resume."""

    content = service.storage_service.pop_generated_document(document_id)
    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "reason": "Optimized resume not found."},
        )
    return StreamingResponse(
        BytesIO(content),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="optimized-resume-{document_id}.docx"'
        },
    )
