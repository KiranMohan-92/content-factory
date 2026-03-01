"""
Validator for Analyzer Agent output (analysis.md).

Ensures:
- All 5 Deutsch tests applied to ALL explanations
- Each test has evidence (not just PASS/FAIL)
- Explanations are ranked with justification
- Good explanation identified or conjectured
- Implications documented (theoretical + practical)
"""

import re
from typing import Dict, List, Optional, Tuple
from .base import Validator, ValidationResult


class AnalysisValidator(Validator):
    """Validates analysis.md output from Analyzer Agent."""

    # The five Deutsch tests
    REQUIRED_TESTS = [
        "hard-to-vary",
        "mechanism",
        "reach",
        "rejectability",
        "integration",
    ]

    def __init__(
        self,
        require_all_tests: bool = True,
        require_ranking: bool = True,
        require_good_explanation: bool = True,
        require_evidence: bool = True,
        strict: bool = True
    ):
        super().__init__(strict=strict)
        self.require_all_tests = require_all_tests
        self.require_ranking = require_ranking
        self.require_good_explanation = require_good_explanation
        self.require_evidence = require_evidence

    def validate(self, content: str) -> ValidationResult:
        """Validate analysis.md content."""
        result = ValidationResult(valid=True, raw_content=content)

        # Extract sections
        sections = self._extract_sections(content)

        # 1. Find and validate explanations with their tests
        explanations = self._extract_evaluated_explanations(content)
        self._validate_test_coverage(explanations, result)
        self._validate_test_evidence(explanations, result)

        # 2. Validate ranking section
        self._validate_ranking(content, sections, explanations, result)

        # 3. Validate good explanation section
        self._validate_good_explanation(content, sections, result)

        # 4. Validate implications
        self._validate_implications(sections, result)

        # 5. Validate intellectual honesty
        self._validate_intellectual_honesty(content, sections, result)

        # 6. Compute metrics
        result.metrics = self._compute_metrics(content, explanations)

        return result

    def _extract_evaluated_explanations(self, content: str) -> List[Dict]:
        """Extract explanations with their test results."""
        explanations = []

        # Find explanation blocks (### Explanation N: "Name")
        pattern = r'###\s+(?:Explanation\s+\d+:?\s*)?["\']?([^"\'#\n]+)["\']?\s*\n(.*?)(?=###\s+(?:Explanation|Ranking|The Good)|## |$)'
        matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)

        for match in matches:
            name = match.group(1).strip().strip('"\'')
            body = match.group(2).strip()

            # Skip meta-sections
            skip_names = ['ranking', 'good explanation', 'implications', 'handoff']
            if any(skip in name.lower() for skip in skip_names):
                continue

            # Extract test results
            tests = self._extract_test_results(body)

            # Extract score if present (e.g., "Score: 4/5")
            score_match = re.search(r'Score:\s*(\d+)\s*/\s*5', body)
            score = int(score_match.group(1)) if score_match else None

            explanations.append({
                "name": name,
                "body": body,
                "tests": tests,
                "score": score,
            })

        return explanations

    def _extract_test_results(self, body: str) -> Dict[str, Dict]:
        """Extract individual test results from an explanation body."""
        tests = {}

        for test_name in self.REQUIRED_TESTS:
            # Look for test header
            pattern = rf'\*\*(?:\d+\.\s*)?{test_name}[^*]*\*\*[:\s]*\[?(PASS|FAIL)[^*\n]*\]?'
            match = re.search(pattern, body, re.IGNORECASE)

            if match:
                passed = match.group(1).upper() == "PASS"

                # Find evidence section
                evidence_pattern = rf'{test_name}.*?Evidence[:\s]*(.*?)(?=\*\*\d+\.|Verdict|$)'
                evidence_match = re.search(evidence_pattern, body, re.IGNORECASE | re.DOTALL)
                evidence = evidence_match.group(1).strip() if evidence_match else ""

                # Find reasoning section
                reasoning_pattern = rf'{test_name}.*?Reasoning[:\s]*(.*?)(?=\*\*\d+\.|$)'
                reasoning_match = re.search(reasoning_pattern, body, re.IGNORECASE | re.DOTALL)
                reasoning = reasoning_match.group(1).strip() if reasoning_match else ""

                tests[test_name] = {
                    "found": True,
                    "passed": passed,
                    "has_evidence": len(evidence) > 20,
                    "has_reasoning": len(reasoning) > 20,
                    "evidence_length": len(evidence),
                }
            else:
                tests[test_name] = {
                    "found": False,
                    "passed": None,
                    "has_evidence": False,
                    "has_reasoning": False,
                    "evidence_length": 0,
                }

        return tests

    def _validate_test_coverage(
        self,
        explanations: List[Dict],
        result: ValidationResult
    ):
        """Validate that all 5 tests are applied to all explanations."""
        if not explanations:
            result.add_error(
                code="NO_EXPLANATIONS_EVALUATED",
                message="No evaluated explanations found",
                suggestion="Add '### Explanation N:' sections with 5 test results each"
            )
            return

        result.metrics["explanation_count"] = len(explanations)

        for exp in explanations:
            location = f"Explanation: {exp['name'][:30]}..."

            missing_tests = []
            for test_name in self.REQUIRED_TESTS:
                if test_name not in exp["tests"] or not exp["tests"][test_name]["found"]:
                    missing_tests.append(test_name)

            if missing_tests and self.require_all_tests:
                result.add_error(
                    code="MISSING_TESTS",
                    message=f"Missing tests: {', '.join(missing_tests)}",
                    location=location,
                    suggestion=f"Apply all 5 tests: {', '.join(self.REQUIRED_TESTS)}"
                )

            # Count tests applied
            tests_applied = sum(1 for t in exp["tests"].values() if t["found"])
            if tests_applied < 5:
                result.add_warning(
                    code="INCOMPLETE_TESTING",
                    message=f"Only {tests_applied}/5 tests applied",
                    location=location
                )

    def _validate_test_evidence(
        self,
        explanations: List[Dict],
        result: ValidationResult
    ):
        """Validate that each test has evidence, not just PASS/FAIL."""
        if not self.require_evidence:
            return

        for exp in explanations:
            location = f"Explanation: {exp['name'][:30]}..."

            for test_name, test_data in exp["tests"].items():
                if not test_data["found"]:
                    continue

                if not test_data["has_evidence"] and not test_data["has_reasoning"]:
                    result.add_warning(
                        code="TEST_NO_EVIDENCE",
                        message=f"Test '{test_name}' has no supporting evidence/reasoning",
                        location=location,
                        suggestion=f"Add 'Evidence:' and 'Reasoning:' after {test_name} verdict"
                    )

    def _validate_ranking(
        self,
        content: str,
        sections: Dict[str, str],
        explanations: List[Dict],
        result: ValidationResult
    ):
        """Validate ranking section exists and is justified."""
        ranking_section = sections.get("Ranking") or sections.get("Ranking of Explanations")

        if not ranking_section and self.require_ranking:
            result.add_error(
                code="MISSING_RANKING",
                message="No 'Ranking' section found",
                suggestion="Add '## Ranking' with numbered list of explanations by test results"
            )
            return

        if ranking_section:
            # Check that ranking mentions scores
            has_scores = bool(re.search(r'\d+/5', ranking_section))
            if not has_scores:
                result.add_warning(
                    code="RANKING_NO_SCORES",
                    message="Ranking doesn't show test scores (e.g., '4/5')",
                    location="Ranking",
                    suggestion="Add scores like 'Score: 4/5 tests passed'"
                )

            # Check that ranking mentions explanations
            exp_names = [e["name"].lower()[:20] for e in explanations]
            mentioned = sum(1 for name in exp_names if name in ranking_section.lower())

            if mentioned < len(explanations):
                result.add_warning(
                    code="INCOMPLETE_RANKING",
                    message=f"Only {mentioned}/{len(explanations)} explanations mentioned in ranking",
                    location="Ranking"
                )

    def _validate_good_explanation(
        self,
        content: str,
        sections: Dict[str, str],
        result: ValidationResult
    ):
        """Validate good explanation section."""
        good_section = (
            sections.get("The Good Explanation") or
            sections.get("Good Explanation") or
            sections.get("Identified Good Explanation")
        )

        if not good_section and self.require_good_explanation:
            result.add_error(
                code="MISSING_GOOD_EXPLANATION",
                message="No 'Good Explanation' section found",
                suggestion="Add '## The Good Explanation' identifying or conjecturing the best explanation"
            )
            return

        if good_section:
            # Check for key components
            required_components = [
                ("hard-to-vary", "Why It's Hard-to-Vary"),
                ("mechanism", "The Mechanism"),
                ("reach", "The Reach"),
                ("test", "Testability"),
                ("integrat", "Integration"),
            ]

            missing = []
            for keyword, display_name in required_components:
                if keyword not in good_section.lower():
                    missing.append(display_name)

            if missing:
                result.add_warning(
                    code="INCOMPLETE_GOOD_EXPLANATION",
                    message=f"Good Explanation missing: {', '.join(missing)}",
                    location="The Good Explanation",
                    suggestion="Include all 5 test results for the good explanation"
                )

    def _validate_implications(
        self,
        sections: Dict[str, str],
        result: ValidationResult
    ):
        """Validate implications section."""
        implications = sections.get("Implications")

        if not implications:
            result.add_warning(
                code="MISSING_IMPLICATIONS",
                message="No 'Implications' section found",
                suggestion="Add '## Implications' with theoretical and practical sections"
            )
            return

        # Check for theoretical vs practical
        has_theoretical = bool(re.search(r'theoretic', implications, re.IGNORECASE))
        has_practical = bool(re.search(r'practic', implications, re.IGNORECASE))

        if not has_theoretical:
            result.add_info(
                code="MISSING_THEORETICAL",
                message="Consider adding 'Theoretical Understanding' subsection",
                location="Implications"
            )

        if not has_practical:
            result.add_warning(
                code="MISSING_PRACTICAL",
                message="Missing 'Practical Application' subsection",
                location="Implications",
                suggestion="Add practical implications - what should people do differently?"
            )

    def _validate_intellectual_honesty(
        self,
        content: str,
        sections: Dict[str, str],
        result: ValidationResult
    ):
        """Validate intellectual honesty indicators."""
        # Check for uncertainty acknowledgment
        uncertainty_patterns = [
            r'\buncertain',
            r'\blimitation',
            r'\bdon\'t know',
            r'\bnot sure',
            r'\bsurvives criticism',
            r'\bso far',
        ]

        uncertainty_count = sum(
            1 for p in uncertainty_patterns
            if re.search(p, content, re.IGNORECASE)
        )

        result.metrics["uncertainty_acknowledgments"] = uncertainty_count

        if uncertainty_count == 0:
            result.add_warning(
                code="NO_UNCERTAINTY",
                message="No uncertainty acknowledgment found",
                suggestion="Add caveats like 'survives criticism so far' or acknowledge limitations"
            )

        # Check for what would change mind
        if 'what would change' not in content.lower() and 'change my mind' not in content.lower():
            result.add_info(
                code="NO_FALSIFICATION_PERSONAL",
                message="Consider adding 'What Would Change My Mind' section"
            )

    def _compute_metrics(self, content: str, explanations: List[Dict]) -> Dict:
        """Compute validation metrics."""
        words = len(content.split())

        # Count test applications
        total_tests = 0
        passed_tests = 0
        tests_with_evidence = 0

        for exp in explanations:
            for test in exp["tests"].values():
                if test["found"]:
                    total_tests += 1
                    if test["passed"]:
                        passed_tests += 1
                    if test["has_evidence"]:
                        tests_with_evidence += 1

        return {
            "total_words": words,
            "explanation_count": len(explanations),
            "total_test_applications": total_tests,
            "expected_test_applications": len(explanations) * 5,
            "passed_tests": passed_tests,
            "tests_with_evidence": tests_with_evidence,
            "test_coverage": total_tests / (len(explanations) * 5) if explanations else 0,
            "evidence_coverage": tests_with_evidence / total_tests if total_tests else 0,
        }
