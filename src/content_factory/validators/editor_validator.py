"""
Validator for Editor Agent output (editor-feedback.md).

Ensures:
- All 7 dimensions scored
- Scores are within valid range
- Weighted average calculated correctly
- Decision matches score (PUBLISH/REVISION/REJECT)
- Actionable feedback provided for scores <9.3
"""

import re
from typing import Dict, List, Optional, Tuple
from .base import Validator, ValidationResult


class EditorValidator(Validator):
    """Validates editor-feedback.md output from Editor Agent."""

    # Required scoring dimensions with weights
    DIMENSIONS = {
        "philosophical_accuracy": {"weight": 0.15, "aliases": ["philosophical", "philosophy"]},
        "factual_accuracy": {"weight": 0.10, "aliases": ["factual", "facts"]},
        "logical_soundness": {"weight": 0.15, "aliases": ["logical", "logic"]},
        "clarity": {"weight": 0.15, "aliases": ["clarity", "accessibility", "clarity_accessibility"]},
        "engagement": {"weight": 0.15, "aliases": ["engagement", "writing", "engagement_writing"]},
        "practical_utility": {"weight": 0.20, "aliases": ["practical", "utility"]},
        "intellectual_honesty": {"weight": 0.10, "aliases": ["honesty", "intellectual"]},
    }

    # Decision thresholds
    THRESHOLDS = {
        "publish_world_class": 9.5,
        "publish_minimum": 9.3,
        "major_revision": 9.0,
        "return_to_writer": 8.0,
        "reject": 7.0,
    }

    def __init__(
        self,
        min_score_to_publish: float = 9.3,
        min_dimension_score: float = 9.0,
        require_all_dimensions: bool = True,
        require_decision: bool = True,
        strict: bool = True
    ):
        super().__init__(strict=strict)
        self.min_score_to_publish = min_score_to_publish
        self.min_dimension_score = min_dimension_score
        self.require_all_dimensions = require_all_dimensions
        self.require_decision = require_decision

    def validate(self, content: str) -> ValidationResult:
        """Validate editor-feedback.md content."""
        result = ValidationResult(valid=True, raw_content=content)

        # 1. Extract and validate dimension scores
        scores = self._extract_dimension_scores(content)
        self._validate_dimension_scores(scores, result)

        # 2. Calculate and validate overall score
        calculated_score = self._calculate_weighted_score(scores)
        stated_score = self._extract_overall_score(content)
        self._validate_overall_score(calculated_score, stated_score, result)

        # 3. Extract and validate decision
        decision = self._extract_decision(content)
        self._validate_decision(decision, calculated_score or stated_score, result)

        # 4. Check for actionable feedback
        self._validate_actionable_feedback(content, calculated_score or stated_score, result)

        # 5. Compute metrics
        result.metrics = self._compute_metrics(content, scores, calculated_score, stated_score, decision)

        return result

    def _extract_dimension_scores(self, content: str) -> Dict[str, float]:
        """Extract scores for each dimension."""
        scores = {}

        for dimension, info in self.DIMENSIONS.items():
            aliases = [dimension] + info["aliases"]

            for alias in aliases:
                # Pattern: "Dimension: X.X/10" or "Dimension | X.X |"
                patterns = [
                    rf'{alias}[^:\d]*[:\|]\s*(\d+(?:\.\d+)?)\s*/?\s*10',
                    rf'{alias}[^:\d]*[:\|]\s*\*?\*?(\d+(?:\.\d+)?)/10\*?\*?',
                    rf'\|\s*{alias}[^|]*\|\s*(\d+(?:\.\d+)?)\s*/?\s*10',
                ]

                for pattern in patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        scores[dimension] = float(match.group(1))
                        break

                if dimension in scores:
                    break

        return scores

    def _extract_overall_score(self, content: str) -> Optional[float]:
        """Extract the stated overall score."""
        patterns = [
            r'(?:total|overall|final)[^:\d]*score[^:\d]*[:\s]+(\d+(?:\.\d+)?)\s*/\s*10',
            r'score[:\s]+\*?\*?(\d+(?:\.\d+)?)/10\*?\*?',
            r'\|\s*(?:total|overall)\s*\|\s*\*?\*?(\d+(?:\.\d+)?)/10\*?\*?',
            r'(\d+(?:\.\d+)?)/10\s*[✓✅]',  # Score with checkmark
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return float(match.group(1))

        return None

    def _calculate_weighted_score(self, scores: Dict[str, float]) -> Optional[float]:
        """Calculate weighted average from dimension scores."""
        if not scores:
            return None

        total_weight = 0
        weighted_sum = 0

        for dimension, info in self.DIMENSIONS.items():
            if dimension in scores:
                weighted_sum += scores[dimension] * info["weight"]
                total_weight += info["weight"]

        if total_weight < 0.5:  # Less than half of weights found
            return None

        return round(weighted_sum / total_weight * (1 / total_weight), 2)

    def _extract_decision(self, content: str) -> Optional[str]:
        """Extract the editorial decision."""
        decision_patterns = [
            (r'decision[:\s]+\*?\*?(publish|approved?|accept)', "PUBLISH"),
            (r'decision[:\s]+\*?\*?(major revision|revision needed)', "MAJOR_REVISION"),
            (r'decision[:\s]+\*?\*?(return to writer|rewrite)', "RETURN_TO_WRITER"),
            (r'decision[:\s]+\*?\*?(reject|rejected)', "REJECT"),
            (r'✅\s*(?:publish|approved)', "PUBLISH"),
            (r'⚠️\s*(?:revision|major)', "MAJOR_REVISION"),
            (r'❌\s*(?:reject)', "REJECT"),
        ]

        for pattern, decision in decision_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return decision

        return None

    def _validate_dimension_scores(self, scores: Dict[str, float], result: ValidationResult):
        """Validate that all dimensions are scored appropriately."""
        result.metrics["dimensions_scored"] = len(scores)
        result.metrics["dimensions_expected"] = len(self.DIMENSIONS)

        # Check for missing dimensions
        missing = [d for d in self.DIMENSIONS if d not in scores]
        if missing and self.require_all_dimensions:
            result.add_error(
                code="MISSING_DIMENSIONS",
                message=f"Missing scores for: {', '.join(missing)}",
                suggestion="Score all 7 dimensions: philosophical, factual, logical, clarity, engagement, practical, honesty"
            )

        # Check individual dimension scores
        below_minimum = []
        for dimension, score in scores.items():
            if score < 0 or score > 10:
                result.add_error(
                    code="INVALID_SCORE",
                    message=f"Invalid score {score} for {dimension} (must be 0-10)",
                    location=dimension
                )
            elif score < self.min_dimension_score:
                below_minimum.append((dimension, score))

        result.metrics["scores"] = scores
        result.metrics["dimensions_below_minimum"] = len(below_minimum)

        if below_minimum:
            dims_list = ", ".join(f"{d}: {s}" for d, s in below_minimum)
            result.add_warning(
                code="LOW_DIMENSION_SCORES",
                message=f"Dimensions below {self.min_dimension_score}: {dims_list}",
                suggestion=f"All dimensions should be {self.min_dimension_score}+ for world-class content"
            )

    def _validate_overall_score(
        self,
        calculated: Optional[float],
        stated: Optional[float],
        result: ValidationResult
    ):
        """Validate overall score consistency."""
        result.metrics["calculated_score"] = calculated
        result.metrics["stated_score"] = stated

        if stated is None:
            result.add_error(
                code="MISSING_OVERALL_SCORE",
                message="No overall score found",
                suggestion="Add 'Final Score: X.X/10' or table with total"
            )
            return

        # Check if calculated matches stated (within tolerance)
        if calculated is not None:
            difference = abs(calculated - stated)
            if difference > 0.2:
                result.add_warning(
                    code="SCORE_MISMATCH",
                    message=f"Calculated score ({calculated:.2f}) differs from stated ({stated:.2f})",
                    suggestion="Verify weighted average calculation"
                )

        # Check if score meets threshold
        effective_score = stated or calculated
        if effective_score and effective_score < self.min_score_to_publish:
            result.add_info(
                code="BELOW_PUBLISH_THRESHOLD",
                message=f"Score {effective_score:.2f} is below publish threshold ({self.min_score_to_publish})"
            )

    def _validate_decision(
        self,
        decision: Optional[str],
        score: Optional[float],
        result: ValidationResult
    ):
        """Validate decision matches score."""
        result.metrics["decision"] = decision

        if decision is None and self.require_decision:
            result.add_error(
                code="MISSING_DECISION",
                message="No editorial decision found",
                suggestion="Add 'Decision: PUBLISH/MAJOR REVISION/REJECT'"
            )
            return

        if score is None:
            return

        # Check decision consistency
        expected_decision = self._get_expected_decision(score)

        if decision and expected_decision:
            if decision != expected_decision:
                result.add_warning(
                    code="DECISION_SCORE_MISMATCH",
                    message=f"Decision '{decision}' may not match score {score:.2f} (expected '{expected_decision}')",
                    suggestion=f"Score {score:.2f} typically warrants {expected_decision}"
                )

    def _get_expected_decision(self, score: float) -> str:
        """Get expected decision based on score."""
        if score >= self.THRESHOLDS["publish_minimum"]:
            return "PUBLISH"
        elif score >= self.THRESHOLDS["major_revision"]:
            return "MAJOR_REVISION"
        elif score >= self.THRESHOLDS["return_to_writer"]:
            return "RETURN_TO_WRITER"
        else:
            return "REJECT"

    def _validate_actionable_feedback(
        self,
        content: str,
        score: Optional[float],
        result: ValidationResult
    ):
        """Validate actionable feedback is provided when needed."""
        if score is None:
            return

        if score < self.min_score_to_publish:
            # Should have actionable feedback
            action_patterns = [
                r'(?:fix|address|improve|add|remove|change|revise)',
                r'(?:should|need to|must|require)',
                r'(?:issue|problem|weakness|gap)',
                r'(?:path to|how to reach|to improve)',
            ]

            action_count = sum(
                len(re.findall(p, content, re.IGNORECASE))
                for p in action_patterns
            )

            result.metrics["actionable_feedback_indicators"] = action_count

            if action_count < 3:
                result.add_error(
                    code="NO_ACTIONABLE_FEEDBACK",
                    message="Score below threshold but no actionable feedback found",
                    suggestion="Provide specific fixes: what to change, how to improve"
                )

            # Check for "path to 9.3" section
            has_path = bool(re.search(r'path to \d+\.\d+|how to reach|to improve', content, re.IGNORECASE))
            if not has_path:
                result.add_warning(
                    code="NO_IMPROVEMENT_PATH",
                    message="No 'Path to 9.3+' section found",
                    suggestion="Add section explaining how to reach publishable score"
                )

    def _compute_metrics(
        self,
        content: str,
        scores: Dict[str, float],
        calculated: Optional[float],
        stated: Optional[float],
        decision: Optional[str]
    ) -> Dict:
        """Compute validation metrics."""
        effective_score = stated or calculated or 0

        return {
            "word_count": len(content.split()),
            "dimensions_scored": len(scores),
            "dimensions_expected": len(self.DIMENSIONS),
            "scores": scores,
            "calculated_score": calculated,
            "stated_score": stated,
            "effective_score": effective_score,
            "decision": decision,
            "meets_threshold": effective_score >= self.min_score_to_publish,
            "expected_decision": self._get_expected_decision(effective_score) if effective_score else None,
        }


class ScoreCalculator:
    """Helper class for score calculations and analysis."""

    WEIGHTS = {
        "philosophical_accuracy": 0.15,
        "factual_accuracy": 0.10,
        "logical_soundness": 0.15,
        "clarity": 0.15,
        "engagement": 0.15,
        "practical_utility": 0.20,
        "intellectual_honesty": 0.10,
    }

    @classmethod
    def calculate_weighted_score(cls, scores: Dict[str, float]) -> float:
        """Calculate weighted average score."""
        total = sum(
            scores.get(dim, 0) * weight
            for dim, weight in cls.WEIGHTS.items()
        )
        return round(total, 2)

    @classmethod
    def get_score_breakdown(cls, scores: Dict[str, float]) -> str:
        """Get formatted score breakdown."""
        lines = ["Score Breakdown:"]
        total = 0

        for dim, weight in cls.WEIGHTS.items():
            score = scores.get(dim, 0)
            contribution = score * weight
            total += contribution
            lines.append(f"  {dim}: {score}/10 × {weight:.0%} = {contribution:.3f}")

        lines.append(f"  Total: {total:.2f}/10")
        return "\n".join(lines)

    @classmethod
    def identify_weak_dimensions(
        cls,
        scores: Dict[str, float],
        threshold: float = 9.0
    ) -> List[Tuple[str, float, float]]:
        """Identify dimensions below threshold with impact."""
        weak = []
        for dim, weight in cls.WEIGHTS.items():
            score = scores.get(dim, 0)
            if score < threshold:
                impact = (threshold - score) * weight
                weak.append((dim, score, impact))

        return sorted(weak, key=lambda x: x[2], reverse=True)

    @classmethod
    def score_to_reach(cls, current_scores: Dict[str, float], target: float = 9.3) -> Dict[str, float]:
        """Calculate improvements needed to reach target score."""
        current = cls.calculate_weighted_score(current_scores)
        gap = target - current

        if gap <= 0:
            return {}  # Already at target

        improvements = {}
        remaining_gap = gap

        # Prioritize by weight (biggest impact)
        sorted_dims = sorted(cls.WEIGHTS.items(), key=lambda x: x[1], reverse=True)

        for dim, weight in sorted_dims:
            current_score = current_scores.get(dim, 0)
            max_improvement = 10.0 - current_score

            if max_improvement > 0:
                needed_for_gap = remaining_gap / weight
                actual_improvement = min(needed_for_gap, max_improvement)

                if actual_improvement > 0.1:  # Only suggest meaningful improvements
                    improvements[dim] = round(current_score + actual_improvement, 1)
                    remaining_gap -= actual_improvement * weight

            if remaining_gap <= 0.01:
                break

        return improvements
