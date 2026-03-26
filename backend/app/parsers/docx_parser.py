"""DOCX resume parser."""

from __future__ import annotations

from pathlib import Path

from docx import Document

from app.parsers.base import ResumeFileParser
from app.utils.errors import ParsingError
from app.utils.text import normalize_text


class DOCXResumeParser(ResumeFileParser):
    """Extract text from DOCX resumes."""

    def parse(self, file_path: Path) -> str:
        """Parse text from a DOCX file."""

        try:
            document = Document(file_path)
            paragraphs = [paragraph.text for paragraph in document.paragraphs]
        except Exception as exc:  # pragma: no cover - library exceptions vary
            raise ParsingError("Unable to read DOCX resume.") from exc

        text = normalize_text("\n".join(paragraphs))
        if not text:
            raise ParsingError("The uploaded DOCX file is empty.")
        return text
