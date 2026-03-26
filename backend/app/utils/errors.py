"""Custom application exceptions."""


class ATSForgeError(Exception):
    """Base application exception."""


class ParsingError(ATSForgeError):
    """Raised when a resume cannot be parsed."""


class ScannedPDFError(ParsingError):
    """Raised when a PDF appears to be scanned and contains no extractable text."""


class OptimizationError(ATSForgeError):
    """Raised when resume optimization fails."""


class FileStorageError(ATSForgeError):
    """Raised when file storage operations fail."""
