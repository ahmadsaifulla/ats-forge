"""Temporary storage for uploaded parsing inputs and generated documents."""

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings
from app.utils.errors import FileStorageError


class StorageService:
    """Manage temporary upload files and ephemeral generated output."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._generated_documents: dict[str, bytes] = {}

    async def create_temp_upload(self, file: UploadFile) -> tuple[str, Path]:
        """Create a temporary upload file for parsing."""

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
        content = await file.read()
        max_bytes = self.settings.max_upload_size_mb * 1024 * 1024
        if len(content) == 0:
            raise FileStorageError("Uploaded file is empty.")
        if len(content) > max_bytes:
            raise FileStorageError(
                f"Uploaded file exceeds the {self.settings.max_upload_size_mb}MB limit."
            )

        try:
            with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(content)
                return resume_id, Path(temp_file.name)
        except OSError as exc:
            raise FileStorageError("Unable to stage the uploaded file for parsing.") from exc

    def delete_temp_upload(self, path: Path) -> None:
        """Delete a temporary upload file."""

        try:
            if path.exists():
                path.unlink()
        except OSError:
            pass

    def save_generated_document(self, document_id: str, content: bytes) -> Path:
        """Persist a generated resume document in memory."""

        self._generated_documents[document_id] = content
        return Path(f"{document_id}.docx")

    def get_generated_document(self, document_id: str) -> bytes | None:
        """Return generated document bytes if available."""

        return self._generated_documents.get(document_id)

    def pop_generated_document(self, document_id: str) -> bytes | None:
        """Return and remove generated document bytes."""

        return self._generated_documents.pop(document_id, None)

    def clear_generated_documents(self) -> None:
        """Clear stored generated documents."""

        self._generated_documents.clear()
