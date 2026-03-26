"""Base parser contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class ResumeFileParser(ABC):
    """Abstract parser for resume file formats."""

    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """Extract text from the provided file."""
