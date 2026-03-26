"""High-level resume parsing service."""

from __future__ import annotations

import logging
from pathlib import Path

from app.models.schemas import ParsedResume
from app.parsers.docx_parser import DOCXResumeParser
from app.parsers.pdf_parser import PDFResumeParser
from app.utils.errors import ParsingError
from app.utils.text import expand_abbreviations, extract_sections, normalize_text

logger = logging.getLogger(__name__)


class ResumeParserService:
    """Parse resumes and map them into a structured representation."""

    def __init__(self) -> None:
        self._parsers = {
            ".pdf": (PDFResumeParser(), "pdf"),
            ".docx": (DOCXResumeParser(), "docx"),
        }

    def parse(self, resume_id: str, file_path: Path, original_filename: str) -> ParsedResume:
        """Parse the uploaded file into a structured resume model."""

        suffix = file_path.suffix.lower()
        parser_entry = self._parsers.get(suffix)
        if parser_entry is None:
            raise ParsingError("Unsupported file type. Please upload a PDF or DOCX resume.")

        parser, detected_type = parser_entry
        text = normalize_text(expand_abbreviations(parser.parse(file_path)))
        sections = extract_sections(text)
        warnings: list[str] = []
        if "skills" not in sections:
            warnings.append("Skills section was not explicitly detected.")
        if "experience" not in sections:
            warnings.append("Experience section was not explicitly detected.")
        if "education" not in sections:
            warnings.append("Education section was not explicitly detected.")
        logger.info(
            "resume_parsed",
            extra={
                "resume_id": resume_id,
                "source_filename": original_filename,
                "detected_type": detected_type,
                "warnings": warnings,
            },
        )

        return ParsedResume(
            resume_id=resume_id,
            filename=original_filename,
            text=text,
            sections=sections,
            detected_file_type=detected_type,
            warnings=warnings,
        )
