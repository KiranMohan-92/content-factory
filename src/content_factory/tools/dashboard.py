"""
CLI Dashboard for Content Factory.

Provides real-time monitoring and analysis:
- Pipeline status
- Quality metrics
- Validation results
- Historical trends
- Error summaries
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import sys
import os

from ..config import PipelineConfig
from ..telemetry import TelemetryCollector, PipelineMetrics
from .analysis import QualityAnalyzer


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"

    @classmethod
    def disable(cls):
        """Disable colors (for non-TTY output)."""
        cls.RESET = ""
        cls.BOLD = ""
        cls.RED = ""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.BLUE = ""
        cls.CYAN = ""
        cls.GRAY = ""


# Disable colors if not in terminal
if not sys.stdout.isatty():
    Colors.disable()


def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    return f"{color}{text}{Colors.RESET}"


def bold(text: str) -> str:
    """Make text bold."""
    return f"{Colors.BOLD}{text}{Colors.RESET}"


class Dashboard:
    """
    CLI Dashboard for Content Factory monitoring.

    Usage:
        dashboard = Dashboard(outputs_dir)
        dashboard.show_status()  # Current pipeline status
        dashboard.show_quality() # Quality metrics
        dashboard.show_history() # Historical analysis
    """

    def __init__(
        self,
        outputs_dir: Optional[Path] = None,
        telemetry: Optional[TelemetryCollector] = None,
    ):
        self.outputs_dir = outputs_dir or Path("outputs")
        self.telemetry = telemetry
        self.analyzer = QualityAnalyzer(self.outputs_dir)

    def _box(self, title: str, content: List[str], width: int = 70) -> str:
        """Create a box around content."""
        lines = [
            "┌" + "─" * (width - 2) + "┐",
            "│" + bold(f" {title}".ljust(width - 2)) + "│",
            "├" + "─" * (width - 2) + "┤",
        ]

        for line in content:
            # Truncate and pad
            display_line = line[:width - 4].ljust(width - 4)
            lines.append("│ " + display_line + " │")

        lines.append("└" + "─" * (width - 2) + "┘")
        return "\n".join(lines)

    def _progress_bar(self, value: float, max_value: float = 10, width: int = 20) -> str:
        """Create a progress bar."""
        filled = int((value / max_value) * width)
        empty = width - filled

        if value >= 9.3:
            color = Colors.GREEN
        elif value >= 8.5:
            color = Colors.YELLOW
        else:
            color = Colors.RED

        bar = color + "█" * filled + Colors.GRAY + "░" * empty + Colors.RESET
        return f"[{bar}] {value:.1f}/{max_value}"

    def _score_color(self, score: float) -> str:
        """Get color for a score."""
        if score >= 9.3:
            return Colors.GREEN
        elif score >= 8.5:
            return Colors.YELLOW
        else:
            return Colors.RED

    def show_status(self, pipeline_metrics: Optional[PipelineMetrics] = None):
        """Show current pipeline status."""
        print("\n" + bold("═" * 70))
        print(bold("  CONTENT FACTORY STATUS DASHBOARD"))
        print(bold("═" * 70) + "\n")

        if pipeline_metrics:
            self._show_active_pipeline(pipeline_metrics)
        else:
            print(colorize("  No active pipeline", Colors.GRAY))

        print()

        # Show recent completions
        self._show_recent_completions()

    def _show_active_pipeline(self, metrics: PipelineMetrics):
        """Show active pipeline status."""
        status = "✓ SUCCESS" if metrics.success else "⚡ IN PROGRESS" if not metrics.end_time else "✗ FAILED"
        status_color = Colors.GREEN if metrics.success else Colors.YELLOW if not metrics.end_time else Colors.RED

        content = [
            f"Topic: {bold(metrics.topic)}",
            f"Status: {colorize(status, status_color)}",
            f"Duration: {metrics.total_duration_ms/1000:.1f}s",
            "",
            "Phases:",
        ]

        for phase, phase_metrics in metrics.phases.items():
            phase_status = "✓" if phase_metrics.success else "✗" if phase_metrics.error_message else "⋯"
            phase_color = Colors.GREEN if phase_metrics.success else Colors.RED if phase_metrics.error_message else Colors.GRAY

            line = f"  {colorize(phase_status, phase_color)} {phase.ljust(12)} "
            line += f"{phase_metrics.duration_ms/1000:.1f}s"

            if phase_metrics.quality_score:
                score_color = self._score_color(phase_metrics.quality_score)
                line += f"  Score: {colorize(f'{phase_metrics.quality_score:.1f}', score_color)}"

            if phase_metrics.retry_count > 0:
                line += f"  {colorize(f'(retry {phase_metrics.retry_count})', Colors.YELLOW)}"

            content.append(line)

        if metrics.final_score:
            content.extend([
                "",
                f"Final Score: {self._progress_bar(metrics.final_score)}",
                f"Decision: {colorize(metrics.decision or 'PENDING', Colors.CYAN)}",
            ])

        print(self._box("Active Pipeline", content))

    def _show_recent_completions(self, n: int = 5):
        """Show recent completed pipelines."""
        self.analyzer.load_from_outputs()

        if not self.analyzer.data_points:
            print(colorize("  No completed pipelines found", Colors.GRAY))
            return

        # Sort by timestamp
        sorted_points = sorted(
            self.analyzer.data_points,
            key=lambda x: x.timestamp,
            reverse=True
        )[:n]

        content = []
        for dp in sorted_points:
            score_color = self._score_color(dp.overall_score)
            decision_color = Colors.GREEN if dp.decision == "PUBLISH" else Colors.YELLOW

            line = f"{dp.topic[:30].ljust(30)} "
            line += colorize(f"{dp.overall_score:.1f}", score_color) + " "
            line += colorize(dp.decision[:8].ljust(8), decision_color)

            content.append(line)

        print(self._box("Recent Completions", content))

    def show_quality(self):
        """Show quality metrics dashboard."""
        self.analyzer.load_from_outputs()

        if not self.analyzer.data_points:
            print(colorize("\n  No quality data available\n", Colors.GRAY))
            return

        print("\n" + bold("═" * 70))
        print(bold("  QUALITY METRICS"))
        print(bold("═" * 70) + "\n")

        # Overall stats
        stats = self.analyzer.get_overall_stats()
        self._show_overall_stats(stats)

        print()

        # Dimension breakdown
        self._show_dimension_breakdown()

        print()

        # Trend
        self._show_trend()

    def _show_overall_stats(self, stats: Dict[str, Any]):
        """Show overall statistics."""
        mean_score = stats.get("mean_score", 0)
        score_color = self._score_color(mean_score)
        publish_rate = stats.get("publish_rate", 0) * 100
        above_threshold = stats.get("above_threshold", 0) * 100

        content = [
            f"Total Topics: {bold(str(stats.get('total_topics', 0)))}",
            "",
            f"Mean Score:   {self._progress_bar(mean_score)}",
            f"Std Dev:      {stats.get('std_dev', 0):.3f}",
            f"Range:        {stats.get('min_score', 0):.1f} - {stats.get('max_score', 0):.1f}",
            "",
            f"Publish Rate: {colorize(f'{publish_rate:.0f}%', Colors.CYAN)}",
            f"Above 9.3:    {colorize(f'{above_threshold:.0f}%', score_color)}",
        ]

        print(self._box("Overall Quality", content))

    def _show_dimension_breakdown(self):
        """Show dimension-by-dimension breakdown."""
        analysis = self.analyzer.get_dimension_analysis()

        if not analysis:
            return

        content = []
        for dim, stats in sorted(analysis.items(), key=lambda x: x[1]["mean"]):
            score = stats["mean"]
            weight = stats["weight"]
            score_color = self._score_color(score)

            bar_width = int(score * 2)
            bar = colorize("█" * bar_width, score_color) + Colors.GRAY + "░" * (20 - bar_width) + Colors.RESET

            dim_display = dim.replace("_", " ").title()[:20].ljust(20)
            content.append(f"{dim_display} [{bar}] {score:.1f} ({weight:.0%})")

        print(self._box("Dimension Breakdown", content))

    def _show_trend(self):
        """Show quality trend."""
        trend = self.analyzer.get_trend()

        if trend.get("trend") == "insufficient_data":
            return

        trend_icon = {
            "improving": colorize("↑", Colors.GREEN),
            "declining": colorize("↓", Colors.RED),
            "stable": colorize("→", Colors.YELLOW),
        }.get(trend["trend"], "?")

        content = [
            f"Trend: {trend_icon} {bold(trend['trend'].upper())}",
            "",
            f"Recent {trend['window']} topics: {trend['recent_avg']:.2f}",
            f"Previous topics:       {trend['older_avg']:.2f}",
            f"Change:                {trend['change']:+.3f}",
        ]

        print(self._box("Quality Trend", content))

    def show_history(self, n: int = 10):
        """Show historical analysis."""
        self.analyzer.load_from_outputs()

        if not self.analyzer.data_points:
            print(colorize("\n  No history available\n", Colors.GRAY))
            return

        print("\n" + bold("═" * 70))
        print(bold("  HISTORICAL ANALYSIS"))
        print(bold("═" * 70) + "\n")

        # Best topics
        best = self.analyzer.get_best_topics(5)
        self._show_topic_list("Top Performers", best, Colors.GREEN)

        print()

        # Worst topics
        worst = self.analyzer.get_worst_topics(5)
        self._show_topic_list("Needs Improvement", worst, Colors.RED)

        print()

        # Weak dimensions
        self._show_weak_dimensions()

    def _show_topic_list(self, title: str, topics: List, color: str):
        """Show a list of topics with scores."""
        content = []
        for i, (topic, score) in enumerate(topics, 1):
            score_display = colorize(f"{score:.2f}", color)
            content.append(f"{i}. {topic[:40].ljust(40)} {score_display}")

        print(self._box(title, content))

    def _show_weak_dimensions(self):
        """Show consistently weak dimensions."""
        weak = self.analyzer.identify_weak_dimensions()

        if not weak:
            return

        content = [
            colorize("Dimensions consistently below 9.0:", Colors.YELLOW),
            "",
        ]

        for dim, score, note in weak:
            dim_display = dim.replace("_", " ").title()
            content.append(f"• {dim_display}: {colorize(f'{score:.2f}', Colors.RED)}")
            content.append(f"  {colorize(note, Colors.GRAY)}")

        print(self._box("Weak Areas", content))

    def show_validation(self, topic: str):
        """Show validation details for a topic."""
        topic_dir = self.outputs_dir / topic

        if not topic_dir.exists():
            print(colorize(f"\n  Topic '{topic}' not found\n", Colors.RED))
            return

        print("\n" + bold("═" * 70))
        print(bold(f"  VALIDATION DETAILS: {topic}"))
        print(bold("═" * 70) + "\n")

        # Import validators
        from ..validators import (
            ResearchValidator,
            AnalysisValidator,
            WriterValidator,
            EditorValidator,
        )

        validations = [
            ("Research", ResearchValidator(), topic_dir / "research.md"),
            ("Analysis", AnalysisValidator(), topic_dir / "analysis.md"),
            ("Editor Feedback", EditorValidator(), topic_dir / "editor-feedback.md"),
        ]

        for name, validator, path in validations:
            if path.exists():
                result = validator.validate_file(path)
                self._show_validation_result(name, result)
            else:
                print(colorize(f"  {name}: File not found", Colors.GRAY))

            print()

    def _show_validation_result(self, name: str, result):
        """Show a single validation result."""
        status = colorize("✓ VALID", Colors.GREEN) if result.valid else colorize("✗ INVALID", Colors.RED)

        content = [
            f"Status: {status}",
            f"Errors: {colorize(str(result.error_count), Colors.RED if result.error_count else Colors.GREEN)}",
            f"Warnings: {colorize(str(result.warning_count), Colors.YELLOW if result.warning_count else Colors.GREEN)}",
        ]

        if result.errors:
            content.append("")
            content.append(colorize("Errors:", Colors.RED))
            for error in result.errors[:5]:
                content.append(f"  • {error.message[:50]}")

        if result.warnings:
            content.append("")
            content.append(colorize("Warnings:", Colors.YELLOW))
            for warning in result.warnings[:3]:
                content.append(f"  • {warning.message[:50]}")

        # Show key metrics
        if result.metrics:
            content.append("")
            content.append("Metrics:")
            for key, value in list(result.metrics.items())[:5]:
                if isinstance(value, float):
                    content.append(f"  {key}: {value:.2f}")
                elif isinstance(value, (int, str)):
                    content.append(f"  {key}: {value}")

        print(self._box(name, content))

    def show_full(self):
        """Show full dashboard."""
        self.show_status()
        self.show_quality()
        self.show_history()

    def generate_report(self) -> str:
        """Generate text report for export."""
        self.analyzer.load_from_outputs()
        report = self.analyzer.generate_report()
        return report.to_markdown()


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Content Factory Dashboard")
    parser.add_argument("--outputs", "-o", default="outputs", help="Outputs directory")
    parser.add_argument("--command", "-c", choices=["status", "quality", "history", "full", "validate", "report"],
                        default="full", help="Dashboard view")
    parser.add_argument("--topic", "-t", help="Topic for validation view")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")

    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    dashboard = Dashboard(outputs_dir=Path(args.outputs))

    if args.command == "status":
        dashboard.show_status()
    elif args.command == "quality":
        dashboard.show_quality()
    elif args.command == "history":
        dashboard.show_history()
    elif args.command == "validate":
        if not args.topic:
            print("Error: --topic required for validate command")
            sys.exit(1)
        dashboard.show_validation(args.topic)
    elif args.command == "report":
        print(dashboard.generate_report())
    else:
        dashboard.show_full()


if __name__ == "__main__":
    main()
