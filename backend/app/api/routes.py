"""FastAPI endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.api.dependencies import get_resume_workflow_service
from app.models.schemas import (
    AnalysisResponse,
    AnalyzeRequest,
    ErrorResponse,
    OptimizeResponse,
    ResumeUploadResponse,
)
from app.services.resume_service import ResumeWorkflowService
from app.utils.errors import ATSForgeError

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

    try:
        return await service.upload_resume(file)
    except ATSForgeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


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

    try:
        return service.analyze(payload)
    except ATSForgeError as exc:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


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

    try:
        return service.optimize(payload)
    except ATSForgeError as exc:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@router.get(
    "/download/{document_id}",
    responses={404: {"model": ErrorResponse}},
)
async def download_resume(
    document_id: str,
    service: ResumeWorkflowService = Depends(get_resume_workflow_service),
):
    """Download a generated optimized resume."""

    path = service.storage_service.get_generated_document(document_id)
    if path is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Optimized resume not found.")
    return FileResponse(
        path=path,
        filename=f"optimized-resume-{document_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
