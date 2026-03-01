"""
Validator for Researcher Agent output (research.md).

Ensures:
- 3-7 competing explanations documented
- Each explanation has evidence for AND against
- Steelman test passed (fair representation)
- No evaluation/judgment (that's Analyzer's job)
- Problem statement is clear
- Patterns and gaps identified
"""

import re
from typing import Dict, List
from .base import Validator, ValidationResult


class ResearchValidator(Validator):
    """Validates research.md output from Researcher Agent."""

    def __init__(
        self,
        min_explanations: int = 3,
        max_explanations: int = 7,
        require_evidence_both_sides: bool = True,
        require_steelman: bool = True,
        strict: bool = True
    ):
        super().__init__(strict=strict)
        self.min_explanations = min_explanations
        self.max_explanations = max_explanations
        self.require_evidence_both_sides = require_evidence_both_sides
        self.require_steelman = require_steelman

    def validate(self, content: str) -> ValidationResult:
        """Validate research.md content."""
        result = ValidationResult(valid=True, raw_content=content)

        # Extract sections
        sections = self._extract_sections(content)

        # 1. Check for problem statement
        self._validate_problem_statement(content, sections, result)

        # 2. Extract and validate explanations
        explanations = self._extract_explanations(content)
        self._validate_explanation_count(explanations, result)
        self._validate_explanation_structure(explanations, result)

        # 3. Check for patterns and gaps section
        self._validate_patterns_section(sections, result)

        # 4. Check for bias indicators (should be neutral)
        self._validate_neutrality(content, result)

        # 5. Compute metrics
        result.metrics = self._compute_metrics(content, explanations)

        return result

    def _validate_problem_statement(
        self,
        content: str,
        sections: Dict[str, str],
        result: ValidationResult
    ):
        """Validate presence and quality of problem statement."""
        problem_section = sections.get("The Problem") or sections.get("Problem")

        if not problem_section:
            result.add_error(
                code="MISSING_PROBLEM_STATEMENT",
                message="No 'The Problem' section found",
                suggestion="Add a clear '## The Problem' section explaining what's confusing/controversial"
            )
            return

        # Check problem statement length (should be substantive)
        words = len(problem_section.split())
        if words < 30:
            result.add_warning(
                code="SHORT_PROBLEM_STATEMENT",
                message=f"Problem statement is only {words} words - may be too brief",
                location="The Problem",
                suggestion="Expand to explain why this problem is difficult/important"
            )

        result.metrics["problem_statement_words"] = words

    def _extract_explanations(self, content: str) -> List[Dict[str, str]]:
        """Extract individual explanations from the content."""
        explanations = []

        # Look for patterns like "### Explanation 1:" or "### [Name]"
        pattern = r'###\s+(?:Explanation\s+\d+:?\s*)?["\']?([^"\'#\n]+)["\']?\s*\n(.*?)(?=###|\Z)'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            name = match.group(1).strip().strip('"\'')
            body = match.group(2).strip()

            # Skip meta-sections that aren't explanations
            skip_names = [
                'where explanations conflict', 'what\'s being assumed',
                'what evidence is disputed', 'what\'s missing',
                'questions for analysis', 'patterns and gaps',
                'cautions about biases', 'sources'
            ]
            if any(skip in name.lower() for skip in skip_names):
                continue

            explanations.append({
                "name": name,
                "body": body,
                "has_core_claim": bool(re.search(r'\*\*Core Claim\*\*', body, re.IGNORECASE)),
                "has_supporting_evidence": bool(re.search(r'\*\*Supporting Evidence\*\*', body, re.IGNORECASE)),
                "has_counter_evidence": bool(re.search(r'\*\*Counter.?Evidence\*\*', body, re.IGNORECASE)),
                "has_prevalence": bool(re.search(r'\*\*Prevalence\*\*', body, re.IGNORECASE)),
                "has_steelman": bool(re.search(r'\*\*(?:Strongest Form|Steelman)', body, re.IGNORECASE)),
            })

        return explanations

    def _validate_explanation_count(
        self,
        explanations: List[Dict],
        result: ValidationResult
    ):
        """Validate the number of explanations."""
        count = len(explanations)
        result.metrics["explanation_count"] = count

        if count < self.min_explanations:
            result.add_error(
                code="TOO_FEW_EXPLANATIONS",
                message=f"Found {count} explanations, minimum is {self.min_explanations}",
                suggestion=f"Add {self.min_explanations - count} more competing explanations"
            )
        elif count > self.max_explanations:
            result.add_warning(
                code="TOO_MANY_EXPLANATIONS",
                message=f"Found {count} explanations, maximum recommended is {self.max_explanations}",
                suggestion="Consider consolidating similar explanations"
            )

    def _validate_explanation_structure(
        self,
        explanations: List[Dict],
        result: ValidationResult
    ):
        """Validate each explanation has required components."""
        for i, exp in enumerate(explanations, 1):
            location = f"Explanation {i}: {exp['name'][:30]}..."

            # Core claim required
            if not exp["has_core_claim"]:
                result.add_error(
                    code="MISSING_CORE_CLAIM",
                    message="Missing 'Core Claim' section",
                    location=location,
                    suggestion="Add '**Core Claim**: ...' describing what this view says"
                )

            # Evidence both sides required
            if self.require_evidence_both_sides:
                if not exp["has_supporting_evidence"]:
                    result.add_error(
                        code="MISSING_SUPPORTING_EVIDENCE",
                        message="Missing 'Supporting Evidence' section",
                        location=location,
                        suggestion="Add '**Supporting Evidence**: ...' with reasons people believe this"
                    )

                if not exp["has_counter_evidence"]:
                    result.add_error(
                        code="MISSING_COUNTER_EVIDENCE",
                        message="Missing 'Counter-Evidence' section",
                        location=location,
                        suggestion="Add '**Counter-Evidence**: ...' with challenges to this view"
                    )

            # Steelman required
            if self.require_steelman and not exp["has_steelman"]:
                result.add_warning(
                    code="MISSING_STEELMAN",
                    message="Missing 'Strongest Form' (steelman) section",
                    location=location,
                    suggestion="Add '**Strongest Form (Steelmanned)**: ...' presenting the best version"
                )

            # Prevalence is informative
            if not exp["has_prevalence"]:
                result.add_info(
                    code="MISSING_PREVALENCE",
                    message="Missing 'Prevalence' indicator",
                    location=location
                )

    def _validate_patterns_section(
        self,
        sections: Dict[str, str],
        result: ValidationResult
    ):
        """Validate patterns and gaps section exists."""
        patterns_section = sections.get("Patterns and Gaps") or sections.get("Landscape Patterns")

        if not patterns_section:
            result.add_warning(
                code="MISSING_PATTERNS_SECTION",
                message="No 'Patterns and Gaps' section found",
                suggestion="Add section identifying conflicts, assumptions, disputed evidence, and gaps"
            )
            return

        # Check for required subsections
        required_patterns = [
            ("conflict", "Where Explanations Conflict"),
            ("assum", "What's Being Assumed"),
            ("missing", "What's Missing From All Views"),
        ]

        for keyword, expected in required_patterns:
            if keyword not in patterns_section.lower():
                result.add_info(
                    code="INCOMPLETE_PATTERNS",
                    message=f"Consider adding: {expected}",
                    location="Patterns and Gaps"
                )

    def _validate_neutrality(self, content: str, result: ValidationResult):
        """Check for signs of bias/evaluation (which should be in Analysis, not Research)."""
        # Evaluation language that belongs in Analysis
        evaluation_patterns = [
            (r'\bthis is (?:the )?(?:best|correct|right|true)\b', "Evaluative: 'this is best/correct'"),
            (r'\bthis explanation (?:fails|wins|loses)\b', "Evaluative judgment"),
            (r'\bclearly (?:wrong|right|better|worse)\b', "Evaluative: 'clearly wrong/right'"),
            (r'\b(?:good|bad) explanation\b', "Evaluation of explanation quality"),
            (r'\bthis (?:passes|fails) the .* test\b', "Applying Deutsch tests (belongs in Analysis)"),
        ]

        bias_count = 0
        for pattern, description in evaluation_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                bias_count += len(matches)
                result.add_warning(
                    code="EVALUATION_IN_RESEARCH",
                    message=f"Found {len(matches)} instance(s) of: {description}",
                    suggestion="Research should document, not evaluate. Move evaluation to Analysis."
                )

        result.metrics["bias_indicators"] = bias_count

    def _compute_metrics(self, content: str, explanations: List[Dict]) -> Dict:
        """Compute validation metrics."""
        words = len(content.split())

        # Count evidence points
        supporting_points = self._count_pattern(content, r'(?:Supporting Evidence|Why people|Who Believes)')
        counter_points = self._count_pattern(content, r'(?:Counter.?Evidence|Where .* struggles|fails)')

        # Count sources
        sources = self._count_pattern(content, r'(?:\[.+?\]\(.+?\)|https?://|Source:|Reference:)')

        return {
            "total_words": words,
            "explanation_count": len(explanations),
            "supporting_evidence_sections": supporting_points,
            "counter_evidence_sections": counter_points,
            "source_references": sources,
            "completeness_score": self._compute_completeness(explanations),
        }

    def _compute_completeness(self, explanations: List[Dict]) -> float:
        """Compute completeness score (0-1) based on explanation structure."""
        if not explanations:
            return 0.0

        total_checks = 0
        passed_checks = 0

        for exp in explanations:
            checks = [
                exp["has_core_claim"],
                exp["has_supporting_evidence"],
                exp["has_counter_evidence"],
                exp["has_prevalence"],
                exp["has_steelman"],
            ]
            total_checks += len(checks)
            passed_checks += sum(checks)

        return passed_checks / total_checks if total_checks > 0 else 0.0
