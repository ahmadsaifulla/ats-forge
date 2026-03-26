"""Local storage for uploaded and generated resume artifacts."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings
from app.utils.errors import FileStorageError


class StorageService:
    """Persist uploaded files and generated output."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def save_upload(self, file: UploadFile) -> tuple[str, Path]:
        """Save an uploaded resume file to local storage."""

        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in {".pdf", ".docx"}:
            raise FileStorageError("Only PDF and DOCX resumes are supported.")
        if file.content_type not in {
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/octet-stream",
        }:
            raise FileStorageError("Unsupported content type for uploaded resume.")

        resume_id = uuid4().hex
        target_path = self.settings.upload_dir / f"{resume_id}{suffix}"
        content = await file.read()
        max_bytes = self.settings.max_upload_size_mb * 1024 * 1024
        if len(content) == 0:
            raise FileStorageError("Uploaded file is empty.")
        if len(content) > max_bytes:
            raise FileStorageError(
                f"Uploaded file exceeds the {self.settings.max_upload_size_mb}MB limit."
            )

        try:
            target_path.write_bytes(content)
        except OSError as exc:
            raise FileStorageError("Unable to save the uploaded file.") from exc

        return resume_id, target_path

    def get_upload_path(self, resume_id: str) -> Path | None:
        """Return the stored upload path if present."""

        for suffix in (".pdf", ".docx"):
            candidate = self.settings.upload_dir / f"{resume_id}{suffix}"
            if candidate.exists():
                return candidate
        return None

    def save_generated_document(self, document_id: str, content: bytes) -> Path:
        """Persist a generated resume document."""

        target_path = self.settings.generated_dir / f"{document_id}.docx"
        try:
            target_path.write_bytes(content)
        except OSError as exc:
            raise FileStorageError("Unable to save the optimized resume.") from exc
        return target_path

    def get_generated_document(self, document_id: str) -> Path | None:
        """Return a generated document path if available."""

        candidate = self.settings.generated_dir / f"{document_id}.docx"
        return candidate if candidate.exists() else None
