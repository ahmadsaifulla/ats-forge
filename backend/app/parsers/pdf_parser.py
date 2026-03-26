"""PDF resume parser."""

from __future__ import annotations

from pathlib import Path

import pdfplumber

from app.parsers.base import ResumeFileParser
from app.utils.errors import ParsingError, ScannedPDFError
from app.utils.text import normalize_text


class PDFResumeParser(ResumeFileParser):
    """Extract text from PDF resumes."""

    def parse(self, file_path: Path) -> str:
        """Parse text from a PDF file."""

        try:
            with pdfplumber.open(file_path) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
        except Exception as exc:  # pragma: no cover - library exceptions vary
            raise ParsingError("Unable to read PDF resume.") from exc

        text = normalize_text("\n".join(pages))
        if not text or len(text.split()) < 15:
            raise ScannedPDFError(
                "The uploaded PDF appears to be scanned or image-based. Please upload a text-based PDF or DOCX file."
            )
        return text
