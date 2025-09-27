"""
Docstring parser for extracting structured PROMPT, METADATA, and NOTES sections.

This module provides functionality to parse Python function docstrings that contain
structured sections for LLM orchestration, including:

- PROMPT: Natural language instructions for LLM execution
- METADATA: Structured configuration in YAML format
- NOTES: Additional documentation and context

The parser handles various docstring formats and provides robust error handling
for malformed or missing sections.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

from .exceptions import ValidationError


class DocstringParseResult:
    """Result of parsing a docstring with structured sections."""

    def __init__(
        self,
        prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        notes: Optional[str] = None,
        raw_docstring: str = "",
    ) -> None:
        self.prompt = prompt
        self.metadata = metadata or {}
        self.notes = notes
        self.raw_docstring = raw_docstring

    def __repr__(self) -> str:
        return (
            f"DocstringParseResult(prompt={self.prompt!r}, "
            f"metadata={self.metadata!r}, notes={self.notes!r})"
        )


class DocstringParser:
    """Parser for structured docstrings with PROMPT, METADATA, and NOTES sections."""

    # Regex pattern to match section headers (only known section names)
    SECTION_PATTERN = re.compile(
        r"^(PROMPT|METADATA|NOTES):\s*$",
        re.MULTILINE
    )

    # Pattern to identify YAML content in METADATA section
    METADATA_START_PATTERN = re.compile(
        r"^METADATA:\s*$",
        re.MULTILINE
    )

    def __init__(self) -> None:
        if yaml is None:
            raise ImportError(
                "PyYAML is required for docstring parsing. "
                "Install with: pip install PyYAML"
            )

    def parse(self, docstring: str) -> DocstringParseResult:
        """
        Parse a docstring and extract structured sections.

        Args:
            docstring: The raw docstring to parse

        Returns:
            DocstringParseResult containing extracted sections

        Raises:
            ValidationError: If the docstring format is invalid
        """
        if not docstring or not docstring.strip():
            return DocstringParseResult(raw_docstring=docstring)

        # Clean up the docstring (remove leading/trailing whitespace, dedent)
        cleaned_docstring = self._clean_docstring(docstring)

        # Find section boundaries
        sections = self._find_sections(cleaned_docstring)

        # Extract content for each section
        prompt_content = self._extract_section_content(
            cleaned_docstring, sections, "PROMPT"
        )
        metadata_content = self._extract_section_content(
            cleaned_docstring, sections, "METADATA"
        )
        notes_content = self._extract_section_content(
            cleaned_docstring, sections, "NOTES"
        )

        # Parse metadata as YAML if present
        parsed_metadata = {}
        if metadata_content:
            try:
                parsed_metadata = yaml.safe_load(metadata_content) or {}
                if not isinstance(parsed_metadata, dict):
                    raise ValidationError(
                        "METADATA section must contain a YAML object (dictionary)",
                        details={"content": metadata_content}
                    )
            except yaml.YAMLError as e:
                raise ValidationError(
                    f"Invalid YAML in METADATA section: {e}",
                    details={"content": metadata_content}
                )

        return DocstringParseResult(
            prompt=prompt_content,
            metadata=parsed_metadata,
            notes=notes_content,
            raw_docstring=docstring,
        )

    def _clean_docstring(self, docstring: str) -> str:
        """Clean and normalize docstring format."""
        # Remove leading/trailing whitespace
        cleaned = docstring.strip()

        # Handle triple-quoted docstrings by removing common leading whitespace
        lines = cleaned.split('\n')

        # Find minimum indentation (excluding empty lines)
        non_empty_lines = [line for line in lines if line.strip()]
        if not non_empty_lines:
            return cleaned

        # Calculate common leading whitespace
        min_indent = float('inf')
        for line in non_empty_lines:
            if line.strip():  # Skip empty lines for indentation calculation
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)

        # Remove common leading whitespace
        if min_indent > 0 and min_indent != float('inf'):
            cleaned_lines = []
            for line in lines:
                if line.strip():  # Keep empty lines as-is
                    cleaned_lines.append(line[min_indent:])
                else:
                    cleaned_lines.append(line)
            cleaned = '\n'.join(cleaned_lines)

        return cleaned

    def _find_sections(self, docstring: str) -> Dict[str, Tuple[int, int]]:
        """
        Find section boundaries in the docstring.

        Returns:
            Dictionary mapping section names to (start_line, end_line) tuples
        """
        sections = {}
        lines = docstring.split('\n')

        current_section = None
        current_start = 0

        for i, line in enumerate(lines):
            match = self.SECTION_PATTERN.match(line.strip())
            if match:
                section_name = match.group(1).upper()

                # Save previous section if it exists
                if current_section:
                    sections[current_section] = (current_start, i)

                # Start new section
                current_section = section_name
                current_start = i + 1  # Content starts on next line

        # Handle the last section
        if current_section:
            sections[current_section] = (current_start, len(lines))

        return sections

    def _extract_section_content(
        self,
        docstring: str,
        sections: Dict[str, Tuple[int, int]],
        section_name: str
    ) -> Optional[str]:
        """Extract content for a specific section."""
        if section_name not in sections:
            return None

        start_line, end_line = sections[section_name]
        lines = docstring.split('\n')

        # Extract lines for this section
        section_lines = lines[start_line:end_line]

        # Join and clean up
        content = '\n'.join(section_lines).strip()

        return content if content else None


def parse_docstring(docstring: str) -> DocstringParseResult:
    """
    Convenience function to parse a docstring.

    Args:
        docstring: The raw docstring to parse

    Returns:
        DocstringParseResult containing extracted sections
    """
    parser = DocstringParser()
    return parser.parse(docstring)