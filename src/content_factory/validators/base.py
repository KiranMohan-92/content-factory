"""
Base validator classes and types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any
import re


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"      # Must fix before proceeding
    WARNING = "warning"  # Should fix but can proceed
    INFO = "info"        # Informational note


@dataclass
class ValidationIssue:
    """A single validation issue."""
    code: str
    message: str
    severity: ValidationSeverity
    location: Optional[str] = None  # e.g., "Section: Explanation 3"
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        loc = f" ({self.location})" if self.location else ""
        return f"[{self.severity.value.upper()}] {self.code}{loc}: {self.message}"


@dataclass
class ValidationResult:
    """Result of validating an agent output."""
    valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    raw_content: str = ""

    @property
    def errors(self) -> List[ValidationIssue]:
        """Get only error-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]

    @property
    def warnings(self) -> List[ValidationIssue]:
        """Get only warning-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    def add_error(self, code: str, message: str, location: str = None, suggestion: str = None):
        """Add an error-level issue."""
        self.issues.append(ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.ERROR,
            location=location,
            suggestion=suggestion
        ))
        self.valid = False

    def add_warning(self, code: str, message: str, location: str = None, suggestion: str = None):
        """Add a warning-level issue."""
        self.issues.append(ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.WARNING,
            location=location,
            suggestion=suggestion
        ))

    def add_info(self, code: str, message: str, location: str = None):
        """Add an informational note."""
        self.issues.append(ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.INFO,
            location=location
        ))

    def to_dict(self) -> dict:
        """Export result to dictionary."""
        return {
            "valid": self.valid,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "issues": [
                {
                    "code": i.code,
                    "message": i.message,
                    "severity": i.severity.value,
                    "location": i.location,
                    "suggestion": i.suggestion,
                }
                for i in self.issues
            ],
            "metrics": self.metrics,
        }

    def summary(self) -> str:
        """Get human-readable summary."""
        status = "VALID" if self.valid else "INVALID"
        lines = [
            f"Validation Result: {status}",
            f"  Errors: {self.error_count}",
            f"  Warnings: {self.warning_count}",
        ]
        if self.metrics:
            lines.append("  Metrics:")
            for k, v in self.metrics.items():
                lines.append(f"    {k}: {v}")
        if self.issues:
            lines.append("  Issues:")
            for issue in self.issues:
                lines.append(f"    {issue}")
        return "\n".join(lines)


class ValidationError(Exception):
    """Exception raised when validation fails."""

    def __init__(self, message: str, result: ValidationResult):
        super().__init__(message)
        self.result = result


class Validator(ABC):
    """Base class for all validators."""

    def __init__(self, strict: bool = True):
        """
        Args:
            strict: If True, treat warnings as errors
        """
        self.strict = strict

    @abstractmethod
    def validate(self, content: str) -> ValidationResult:
        """
        Validate content and return result.

        Args:
            content: Raw markdown content to validate

        Returns:
            ValidationResult with issues and metrics
        """
        pass

    def validate_file(self, path: Path) -> ValidationResult:
        """
        Validate content from a file.

        Args:
            path: Path to the markdown file

        Returns:
            ValidationResult
        """
        if not path.exists():
            result = ValidationResult(valid=False)
            result.add_error(
                code="FILE_NOT_FOUND",
                message=f"File not found: {path}",
                suggestion="Ensure the agent has created the output file"
            )
            return result

        content = path.read_text(encoding='utf-8')
        result = self.validate(content)
        result.raw_content = content
        return result

    def validate_or_raise(self, content: str) -> ValidationResult:
        """
        Validate and raise exception if invalid.

        Args:
            content: Content to validate

        Raises:
            ValidationError: If validation fails

        Returns:
            ValidationResult if valid
        """
        result = self.validate(content)
        if not result.valid:
            raise ValidationError(
                f"Validation failed with {result.error_count} errors",
                result
            )
        if self.strict and result.warnings:
            raise ValidationError(
                f"Validation failed with {result.warning_count} warnings (strict mode)",
                result
            )
        return result

    # Common utility methods for subclasses

    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract markdown sections by heading."""
        sections = {}
        current_section = None
        current_content = []

        for line in content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _extract_subsections(self, content: str) -> Dict[str, str]:
        """Extract markdown subsections (### level)."""
        sections = {}
        current_section = None
        current_content = []

        for line in content.split('\n'):
            if line.startswith('### '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[4:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _count_pattern(self, content: str, pattern: str) -> int:
        """Count occurrences of a regex pattern."""
        return len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))

    def _extract_scores(self, content: str) -> Dict[str, float]:
        """Extract numerical scores from content."""
        scores = {}
        # Pattern: "Name: X.X/10" or "Name: X/10"
        pattern = r'(\w[\w\s&]+?):\s*(\d+(?:\.\d+)?)\s*/\s*10'
        for match in re.finditer(pattern, content):
            name = match.group(1).strip().lower().replace(' ', '_')
            scores[name] = float(match.group(2))
        return scores

    def _check_word_count(self, content: str, min_words: int = 0, max_words: int = float('inf')) -> tuple:
        """Check word count against limits."""
        words = len(content.split())
        in_range = min_words <= words <= max_words
        return words, in_range

    def _detect_preachy_language(self, content: str) -> List[tuple]:
        """Detect preachy/lecturing language patterns."""
        preachy_patterns = [
            (r'\byou must\b', "Imperative: 'you must'"),
            (r'\byou need to\b', "Imperative: 'you need to'"),
            (r'\byou should always\b', "Strong imperative: 'you should always'"),
            (r'\bobviously\b', "Dismissive: 'obviously'"),
            (r'\bclearly\b', "Dismissive: 'clearly'"),
            (r'\bthe truth is\b', "Preachy: 'the truth is'"),
            (r'\beveryone knows\b', "Appeal to authority: 'everyone knows'"),
            (r'\bit\'s simple\b', "Dismissive: 'it's simple'"),
            (r'\bjust do\b', "Oversimplifying: 'just do'"),
        ]

        findings = []
        for pattern, description in preachy_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                findings.append((description, len(matches)))

        return findings

    def _check_specific_examples(self, content: str) -> Dict[str, Any]:
        """Check for specific, detailed examples vs vague ones."""
        metrics = {
            "named_examples": 0,
            "numbered_examples": 0,
            "vague_phrases": 0,
        }

        # Named examples (proper nouns suggesting real people/companies)
        named_pattern = r'(?:Sara|Marcus|Chen|David|Elena|James|Sarah|Google|Amazon|Tesla|Apple)\b'
        metrics["named_examples"] = len(re.findall(named_pattern, content))

        # Numbered/quantified examples
        number_patterns = [
            r'\d+\s*%',           # Percentages
            r'\$\d+',             # Dollar amounts
            r'\d+\s*(?:min|hour|day|week|month|year)', # Time periods
            r'\b\d{1,3}(?:,\d{3})*\b', # Large numbers
        ]
        for pattern in number_patterns:
            metrics["numbered_examples"] += len(re.findall(pattern, content))

        # Vague phrases to avoid
        vague_patterns = [
            r'\bthink about\b',
            r'\bconsider\b(?!\s+this)',  # "consider" alone is vague
            r'\breflect on\b',
            r'\bsome people\b',
            r'\bmany experts\b',
            r'\bin general\b',
        ]
        for pattern in vague_patterns:
            metrics["vague_phrases"] += len(re.findall(pattern, content, re.IGNORECASE))

        return metrics
