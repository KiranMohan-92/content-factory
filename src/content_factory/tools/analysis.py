"""
Quality Analysis Tools for Content Factory.

Provides:
- Historical quality score analysis
- Trend detection
- Cross-topic comparison
- Dimension breakdown analysis
- Error pattern identification
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json
import statistics
import re


@dataclass
class QualityDataPoint:
    """A single quality measurement."""
    topic: str
    timestamp: str
    overall_score: float
    dimension_scores: Dict[str, float]
    decision: str
    format_type: str = "article"
    retry_count: int = 0
    duration_ms: float = 0


@dataclass
class ComparisonReport:
    """Report comparing quality across topics or time periods."""
    title: str
    generated_at: str
    data_points: List[QualityDataPoint]
    summary: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "generated_at": self.generated_at,
            "data_point_count": len(self.data_points),
            "summary": self.summary,
            "insights": self.insights,
            "recommendations": self.recommendations,
        }

    def to_markdown(self) -> str:
        """Generate markdown report."""
        lines = [
            f"# {self.title}",
            f"Generated: {self.generated_at}",
            "",
            "## Summary",
            "",
        ]

        for key, value in self.summary.items():
            lines.append(f"- **{key}**: {value}")

        lines.extend([
            "",
            "## Key Insights",
            "",
        ])

        for insight in self.insights:
            lines.append(f"- {insight}")

        lines.extend([
            "",
            "## Recommendations",
            "",
        ])

        for rec in self.recommendations:
            lines.append(f"- {rec}")

        return "\n".join(lines)


class QualityAnalyzer:
    """
    Analyzes quality data from Content Factory runs.

    Can analyze:
    - Historical trends
    - Cross-topic patterns
    - Dimension weaknesses
    - Error patterns
    """

    DIMENSION_WEIGHTS = {
        "philosophical_accuracy": 0.15,
        "factual_accuracy": 0.10,
        "logical_soundness": 0.15,
        "clarity": 0.15,
        "engagement": 0.15,
        "practical_utility": 0.20,
        "intellectual_honesty": 0.10,
    }

    def __init__(self, outputs_dir: Optional[Path] = None):
        self.outputs_dir = outputs_dir or Path("outputs")
        self.data_points: List[QualityDataPoint] = []

    def load_from_outputs(self) -> int:
        """Load quality data from output directories."""
        count = 0

        for topic_dir in self.outputs_dir.iterdir():
            if not topic_dir.is_dir():
                continue

            feedback_path = topic_dir / "editor-feedback.md"
            if not feedback_path.exists():
                continue

            data_point = self._parse_editor_feedback(feedback_path, topic_dir.name)
            if data_point:
                self.data_points.append(data_point)
                count += 1

        return count

    def _parse_editor_feedback(self, path: Path, topic: str) -> Optional[QualityDataPoint]:
        """Parse editor feedback file for quality data."""
        try:
            content = path.read_text()

            # Extract overall score
            score_match = re.search(r'(?:Final|Overall|Total)\s*Score[:\s]+(\d+\.?\d*)\s*/\s*10', content, re.IGNORECASE)
            overall_score = float(score_match.group(1)) if score_match else None

            if overall_score is None:
                return None

            # Extract dimension scores
            dimension_scores = {}
            for dim in self.DIMENSION_WEIGHTS:
                pattern = rf'{dim.replace("_", "[ _]")}[^:\d]*[:\|]\s*(\d+\.?\d*)\s*/\s*10'
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    dimension_scores[dim] = float(match.group(1))

            # Extract decision
            decision = "UNKNOWN"
            if re.search(r'decision[:\s]+.*?publish', content, re.IGNORECASE):
                decision = "PUBLISH"
            elif re.search(r'decision[:\s]+.*?revision', content, re.IGNORECASE):
                decision = "REVISION"
            elif re.search(r'decision[:\s]+.*?reject', content, re.IGNORECASE):
                decision = "REJECT"

            # Get timestamp from file
            timestamp = datetime.fromtimestamp(path.stat().st_mtime).isoformat()

            return QualityDataPoint(
                topic=topic,
                timestamp=timestamp,
                overall_score=overall_score,
                dimension_scores=dimension_scores,
                decision=decision,
            )

        except Exception:
            return None

    def add_data_point(self, data_point: QualityDataPoint):
        """Add a data point manually."""
        self.data_points.append(data_point)

    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall quality statistics."""
        if not self.data_points:
            return {}

        scores = [dp.overall_score for dp in self.data_points]

        return {
            "total_topics": len(self.data_points),
            "mean_score": round(statistics.mean(scores), 2),
            "std_dev": round(statistics.stdev(scores), 3) if len(scores) > 1 else 0,
            "min_score": min(scores),
            "max_score": max(scores),
            "publish_rate": sum(1 for dp in self.data_points if dp.decision == "PUBLISH") / len(self.data_points),
            "above_threshold": sum(1 for s in scores if s >= 9.3) / len(scores),
        }

    def get_dimension_analysis(self) -> Dict[str, Dict[str, float]]:
        """Analyze scores by dimension."""
        dimension_scores: Dict[str, List[float]] = {dim: [] for dim in self.DIMENSION_WEIGHTS}

        for dp in self.data_points:
            for dim, score in dp.dimension_scores.items():
                if dim in dimension_scores:
                    dimension_scores[dim].append(score)

        analysis = {}
        for dim, scores in dimension_scores.items():
            if scores:
                analysis[dim] = {
                    "mean": round(statistics.mean(scores), 2),
                    "std": round(statistics.stdev(scores), 3) if len(scores) > 1 else 0,
                    "min": min(scores),
                    "count": len(scores),
                    "weight": self.DIMENSION_WEIGHTS[dim],
                    "weighted_impact": round(statistics.mean(scores) * self.DIMENSION_WEIGHTS[dim], 3),
                }

        return analysis

    def identify_weak_dimensions(self, threshold: float = 9.0) -> List[Tuple[str, float, str]]:
        """Identify dimensions consistently below threshold."""
        analysis = self.get_dimension_analysis()
        weak = []

        for dim, stats in analysis.items():
            if stats["mean"] < threshold:
                improvement_needed = threshold - stats["mean"]
                weak.append((
                    dim,
                    stats["mean"],
                    f"Needs +{improvement_needed:.2f} to reach {threshold}"
                ))

        return sorted(weak, key=lambda x: x[1])

    def get_trend(self, window: int = 5) -> Dict[str, Any]:
        """Analyze quality trend over time."""
        if len(self.data_points) < window:
            return {"trend": "insufficient_data"}

        # Sort by timestamp
        sorted_points = sorted(self.data_points, key=lambda x: x.timestamp)

        # Calculate moving average
        recent_scores = [dp.overall_score for dp in sorted_points[-window:]]
        older_scores = [dp.overall_score for dp in sorted_points[:-window]]

        recent_avg = statistics.mean(recent_scores) if recent_scores else 0
        older_avg = statistics.mean(older_scores) if older_scores else 0

        diff = recent_avg - older_avg

        if diff > 0.1:
            trend = "improving"
        elif diff < -0.1:
            trend = "declining"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "recent_avg": round(recent_avg, 2),
            "older_avg": round(older_avg, 2),
            "change": round(diff, 3),
            "window": window,
        }

    def identify_error_patterns(self) -> Dict[str, int]:
        """Identify common error patterns from validation results."""
        # This would integrate with validation results
        # For now, return dimension-based patterns
        weak_dims = self.identify_weak_dimensions()

        patterns = {}
        for dim, score, _ in weak_dims:
            if dim == "practical_utility":
                patterns["vague_advice"] = patterns.get("vague_advice", 0) + 1
            elif dim == "logical_soundness":
                patterns["weak_counterarguments"] = patterns.get("weak_counterarguments", 0) + 1
            elif dim == "engagement":
                patterns["preachy_tone"] = patterns.get("preachy_tone", 0) + 1

        return patterns

    def generate_report(self, title: str = "Quality Analysis Report") -> ComparisonReport:
        """Generate comprehensive quality report."""
        stats = self.get_overall_stats()
        dimension_analysis = self.get_dimension_analysis()
        weak_dims = self.identify_weak_dimensions()
        trend = self.get_trend()

        insights = []
        recommendations = []

        # Generate insights
        if stats.get("mean_score", 0) >= 9.3:
            insights.append(f"Average quality ({stats['mean_score']:.2f}) meets world-class threshold")
        else:
            insights.append(f"Average quality ({stats['mean_score']:.2f}) is below 9.3 threshold")

        if trend.get("trend") == "improving":
            insights.append(f"Quality is improving: +{trend['change']:.3f} over recent {trend['window']} topics")
        elif trend.get("trend") == "declining":
            insights.append(f"Quality is declining: {trend['change']:.3f} over recent {trend['window']} topics")

        for dim, score, note in weak_dims[:3]:
            insights.append(f"Weakness in {dim.replace('_', ' ')}: {score:.2f}/10")

        # Generate recommendations
        for dim, score, note in weak_dims[:3]:
            if dim == "practical_utility":
                recommendations.append("Add more specific examples with names, numbers, and actionable steps")
            elif dim == "logical_soundness":
                recommendations.append("Strengthen counterargument handling - steelman objections")
            elif dim == "engagement":
                recommendations.append("Reduce preachy tone - use exploratory language")
            elif dim == "clarity":
                recommendations.append("Simplify complex passages - shorter sentences, clearer structure")
            else:
                recommendations.append(f"Focus on improving {dim.replace('_', ' ')}")

        if stats.get("publish_rate", 0) < 0.8:
            recommendations.append("High rejection rate - consider more thorough analysis phase")

        return ComparisonReport(
            title=title,
            generated_at=datetime.now().isoformat(),
            data_points=self.data_points,
            summary={
                "topics_analyzed": stats.get("total_topics", 0),
                "mean_score": stats.get("mean_score", 0),
                "publish_rate": f"{stats.get('publish_rate', 0)*100:.1f}%",
                "quality_trend": trend.get("trend", "unknown"),
                "weakest_dimension": weak_dims[0][0] if weak_dims else "none",
            },
            insights=insights,
            recommendations=recommendations,
        )

    def compare_topics(self, topic_a: str, topic_b: str) -> Dict[str, Any]:
        """Compare quality between two topics."""
        dp_a = next((dp for dp in self.data_points if dp.topic == topic_a), None)
        dp_b = next((dp for dp in self.data_points if dp.topic == topic_b), None)

        if not dp_a or not dp_b:
            return {"error": "One or both topics not found"}

        comparison = {
            "topic_a": topic_a,
            "topic_b": topic_b,
            "score_a": dp_a.overall_score,
            "score_b": dp_b.overall_score,
            "difference": round(dp_a.overall_score - dp_b.overall_score, 2),
            "dimension_diffs": {},
        }

        for dim in self.DIMENSION_WEIGHTS:
            score_a = dp_a.dimension_scores.get(dim, 0)
            score_b = dp_b.dimension_scores.get(dim, 0)
            comparison["dimension_diffs"][dim] = round(score_a - score_b, 2)

        return comparison

    def get_best_topics(self, n: int = 5) -> List[Tuple[str, float]]:
        """Get top N topics by score."""
        sorted_points = sorted(self.data_points, key=lambda x: x.overall_score, reverse=True)
        return [(dp.topic, dp.overall_score) for dp in sorted_points[:n]]

    def get_worst_topics(self, n: int = 5) -> List[Tuple[str, float]]:
        """Get bottom N topics by score."""
        sorted_points = sorted(self.data_points, key=lambda x: x.overall_score)
        return [(dp.topic, dp.overall_score) for dp in sorted_points[:n]]
