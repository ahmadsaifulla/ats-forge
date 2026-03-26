"""Custom application exceptions."""

from __future__ import annotations


class ATSForgeError(Exception):
    """Base application exception with structured error metadata."""

    def __init__(self, error: str, reason: str, *, status_code: int = 400) -> None:
        super().__init__(reason)
        self.error = error
        self.reason = reason
        self.status_code = status_code


class ParsingError(ATSForgeError):
    """Raised when a resume cannot be parsed."""

    def __init__(self, reason: str) -> None:
        super().__init__("parsing_error", reason, status_code=400)


class ScannedPDFError(ParsingError):
    """Raised when a PDF appears to be scanned and contains no extractable text."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.error = "scanned_pdf"


class OptimizationError(ATSForgeError):
    """Raised when resume optimization fails."""

    def __init__(self, reason: str) -> None:
        super().__init__("optimization_error", reason, status_code=400)


class FileStorageError(ATSForgeError):
    """Raised when file storage operations fail."""

    def __init__(self, reason: str) -> None:
        super().__init__("file_error", reason, status_code=400)


class NotFoundError(ATSForgeError):
    """Raised when a requested item is not available."""

    def __init__(self, reason: str) -> None:
        super().__init__("not_found", reason, status_code=404)
