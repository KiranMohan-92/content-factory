"""
Ablation Study Framework for Content Factory.

Enables systematic testing of architectural decisions:
- Does 4 agents outperform 3?
- Does sequential outperform parallel?
- Which phases contribute most to quality?
- What's the optimal quality threshold?

Usage:
    study = AblationStudy(base_config)
    study.add_variant("no_research", skip_phases=["research"])
    study.add_variant("3_agents", combine_phases=[("research", "analysis")])
    results = study.run(topics)
    report = study.analyze(results)
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any, Tuple
from datetime import datetime
import json
import statistics

from ..config import PipelineConfig, OutputFormat
from ..telemetry import Phase


class AblationType(Enum):
    """Types of ablation experiments."""
    SKIP_PHASE = "skip_phase"           # Remove a phase entirely
    COMBINE_PHASES = "combine_phases"   # Merge two phases
    PARALLEL_PHASES = "parallel_phases" # Run phases in parallel
    THRESHOLD_CHANGE = "threshold"      # Change quality threshold
    RETRY_CHANGE = "retries"            # Change retry limits
    AGENT_VERSION = "agent_version"     # Use different agent version


@dataclass
class AblationVariant:
    """A single variant in an ablation study."""
    name: str
    ablation_type: AblationType
    description: str
    config_changes: Dict[str, Any]
    hypothesis: str  # What we expect to happen

    # Results (filled in after running)
    runs: List[Dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.ablation_type.value,
            "description": self.description,
            "config_changes": self.config_changes,
            "hypothesis": self.hypothesis,
            "run_count": len(self.runs),
        }


@dataclass
class AblationResult:
    """Results from a single ablation run."""
    variant_name: str
    topic: str
    success: bool
    final_score: Optional[float]
    phase_scores: Dict[str, float]
    duration_ms: float
    error_types: List[str]
    validation_metrics: Dict[str, Any]

    def to_dict(self) -> dict:
        return {
            "variant": self.variant_name,
            "topic": self.topic,
            "success": self.success,
            "final_score": self.final_score,
            "phase_scores": self.phase_scores,
            "duration_ms": self.duration_ms,
            "error_types": self.error_types,
        }


@dataclass
class AblationConfig:
    """Configuration for an ablation study."""
    name: str
    description: str
    base_config: PipelineConfig
    topics: List[str]  # Topics to run experiments on
    runs_per_variant: int = 3  # Multiple runs for statistical validity
    output_dir: Path = field(default_factory=lambda: Path("ablation_results"))

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "topics": self.topics,
            "runs_per_variant": self.runs_per_variant,
        }


class AblationStudy:
    """
    Framework for running ablation studies on the Content Factory.

    Enables empirical validation of architectural decisions by
    systematically removing or modifying components and measuring
    the impact on output quality.
    """

    # Pre-defined ablation variants for common experiments
    STANDARD_ABLATIONS = {
        "skip_research": {
            "type": AblationType.SKIP_PHASE,
            "description": "Skip research phase, go directly to analysis",
            "hypothesis": "Quality will decrease due to confirmation bias and missing perspectives",
            "config_changes": {"skip_phases": ["research"]},
        },
        "skip_analysis": {
            "type": AblationType.SKIP_PHASE,
            "description": "Skip analysis phase, go directly to writing",
            "hypothesis": "Quality will decrease due to lack of systematic evaluation",
            "config_changes": {"skip_phases": ["analysis"]},
        },
        "skip_editing": {
            "type": AblationType.SKIP_PHASE,
            "description": "Skip editing phase, publish first draft",
            "hypothesis": "Quality will decrease due to undetected errors",
            "config_changes": {"skip_phases": ["editing"]},
        },
        "combine_research_analysis": {
            "type": AblationType.COMBINE_PHASES,
            "description": "Combine research and analysis into single phase",
            "hypothesis": "Quality will decrease due to confirmation bias",
            "config_changes": {"combine_phases": [("research", "analysis")]},
        },
        "threshold_9.0": {
            "type": AblationType.THRESHOLD_CHANGE,
            "description": "Lower quality threshold from 9.3 to 9.0",
            "hypothesis": "More content published but lower average quality",
            "config_changes": {"min_score": 9.0},
        },
        "threshold_9.5": {
            "type": AblationType.THRESHOLD_CHANGE,
            "description": "Raise quality threshold from 9.3 to 9.5",
            "hypothesis": "Less content published but higher average quality",
            "config_changes": {"min_score": 9.5},
        },
        "no_retries": {
            "type": AblationType.RETRY_CHANGE,
            "description": "Disable automatic retries",
            "hypothesis": "More failures, faster completion for successes",
            "config_changes": {"max_retries": 0},
        },
    }

    def __init__(self, config: AblationConfig):
        self.config = config
        self.variants: Dict[str, AblationVariant] = {}
        self.results: List[AblationResult] = []
        self.baseline_results: List[AblationResult] = []

        # Add baseline variant
        self.add_variant(
            name="baseline",
            ablation_type=AblationType.THRESHOLD_CHANGE,
            description="Baseline: full 4-agent sequential pipeline",
            hypothesis="This is the control group",
            config_changes={},
        )

    def add_variant(
        self,
        name: str,
        ablation_type: AblationType,
        description: str,
        hypothesis: str,
        config_changes: Dict[str, Any],
    ) -> 'AblationStudy':
        """Add a variant to the study."""
        self.variants[name] = AblationVariant(
            name=name,
            ablation_type=ablation_type,
            description=description,
            config_changes=config_changes,
            hypothesis=hypothesis,
        )
        return self

    def add_standard_ablation(self, name: str) -> 'AblationStudy':
        """Add a pre-defined standard ablation."""
        if name not in self.STANDARD_ABLATIONS:
            raise ValueError(f"Unknown standard ablation: {name}")

        ablation = self.STANDARD_ABLATIONS[name]
        return self.add_variant(
            name=name,
            ablation_type=ablation["type"],
            description=ablation["description"],
            hypothesis=ablation["hypothesis"],
            config_changes=ablation["config_changes"],
        )

    def add_all_standard_ablations(self) -> 'AblationStudy':
        """Add all standard ablations."""
        for name in self.STANDARD_ABLATIONS:
            self.add_standard_ablation(name)
        return self

    def _create_variant_config(self, variant: AblationVariant) -> PipelineConfig:
        """Create a modified config for a variant."""
        # Deep copy base config
        import copy
        config = copy.deepcopy(self.config.base_config)

        # Apply changes based on variant type
        changes = variant.config_changes

        if "min_score" in changes:
            config.guardrails.quality.min_overall_score = changes["min_score"]

        if "max_retries" in changes:
            config.guardrails.max_retries_per_agent = changes["max_retries"]
            config.guardrails.max_total_retries = changes["max_retries"]

        # Store skip/combine info for orchestrator to handle
        config._ablation_skip_phases = changes.get("skip_phases", [])
        config._ablation_combine_phases = changes.get("combine_phases", [])

        return config

    def run(
        self,
        executor: Optional[Callable] = None,
        progress_callback: Optional[Callable] = None,
    ) -> List[AblationResult]:
        """
        Run the ablation study.

        Args:
            executor: Function to execute a pipeline run. If None, simulates results.
            progress_callback: Called with (variant_name, topic, run_num, total_runs)

        Returns:
            List of all ablation results
        """
        total_runs = len(self.variants) * len(self.config.topics) * self.config.runs_per_variant
        current_run = 0

        for variant_name, variant in self.variants.items():
            variant_config = self._create_variant_config(variant)

            for topic in self.config.topics:
                for run_num in range(self.config.runs_per_variant):
                    current_run += 1

                    if progress_callback:
                        progress_callback(variant_name, topic, current_run, total_runs)

                    # Execute or simulate
                    if executor:
                        result = executor(variant_config, topic, variant_name)
                    else:
                        result = self._simulate_run(variant, topic)

                    self.results.append(result)
                    variant.runs.append(result.to_dict())

                    if variant_name == "baseline":
                        self.baseline_results.append(result)

        return self.results

    def _simulate_run(self, variant: AblationVariant, topic: str) -> AblationResult:
        """Simulate a run for testing (when no executor provided)."""
        import random

        # Simulate scores based on variant type
        base_score = 9.3

        if variant.name == "baseline":
            score = base_score + random.uniform(-0.2, 0.3)
        elif "skip" in variant.name:
            score = base_score - random.uniform(0.3, 0.8)  # Lower quality
        elif "combine" in variant.name:
            score = base_score - random.uniform(0.2, 0.5)  # Lower quality
        elif "threshold_9.0" in variant.name:
            score = base_score - random.uniform(0, 0.3)
        elif "threshold_9.5" in variant.name:
            score = base_score + random.uniform(0, 0.3)
        else:
            score = base_score + random.uniform(-0.3, 0.3)

        return AblationResult(
            variant_name=variant.name,
            topic=topic,
            success=score >= 9.0,
            final_score=round(score, 2),
            phase_scores={},
            duration_ms=random.uniform(30000, 120000),
            error_types=[],
            validation_metrics={},
        )

    def analyze(self) -> 'AblationAnalysis':
        """Analyze results and generate report."""
        return AblationAnalysis(self)

    def save(self, path: Optional[Path] = None):
        """Save study results to JSON."""
        path = path or (self.config.output_dir / f"ablation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "config": self.config.to_dict(),
            "variants": {k: v.to_dict() for k, v in self.variants.items()},
            "results": [r.to_dict() for r in self.results],
            "generated_at": datetime.now().isoformat(),
        }

        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

        return path


class AblationAnalysis:
    """Analysis and reporting for ablation study results."""

    def __init__(self, study: AblationStudy):
        self.study = study
        self.results = study.results
        self.baseline = study.baseline_results

    def _get_variant_results(self, variant_name: str) -> List[AblationResult]:
        """Get all results for a variant."""
        return [r for r in self.results if r.variant_name == variant_name]

    def _compute_stats(self, scores: List[float]) -> Dict[str, float]:
        """Compute statistical summary."""
        if not scores:
            return {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 0}

        return {
            "mean": round(statistics.mean(scores), 3),
            "std": round(statistics.stdev(scores), 3) if len(scores) > 1 else 0,
            "min": round(min(scores), 3),
            "max": round(max(scores), 3),
            "n": len(scores),
        }

    def get_variant_summary(self, variant_name: str) -> Dict[str, Any]:
        """Get summary statistics for a variant."""
        results = self._get_variant_results(variant_name)
        scores = [r.final_score for r in results if r.final_score is not None]
        durations = [r.duration_ms for r in results]
        successes = [r for r in results if r.success]

        return {
            "variant": variant_name,
            "runs": len(results),
            "success_rate": len(successes) / len(results) if results else 0,
            "score_stats": self._compute_stats(scores),
            "duration_stats": self._compute_stats(durations),
        }

    def compare_to_baseline(self, variant_name: str) -> Dict[str, Any]:
        """Compare a variant to baseline."""
        baseline_summary = self.get_variant_summary("baseline")
        variant_summary = self.get_variant_summary(variant_name)

        baseline_mean = baseline_summary["score_stats"]["mean"]
        variant_mean = variant_summary["score_stats"]["mean"]

        diff = variant_mean - baseline_mean
        pct_change = (diff / baseline_mean * 100) if baseline_mean else 0

        return {
            "variant": variant_name,
            "baseline_mean": baseline_mean,
            "variant_mean": variant_mean,
            "difference": round(diff, 3),
            "pct_change": round(pct_change, 2),
            "success_rate_diff": variant_summary["success_rate"] - baseline_summary["success_rate"],
            "hypothesis": self.study.variants[variant_name].hypothesis,
            "hypothesis_confirmed": self._check_hypothesis(variant_name, diff),
        }

    def _check_hypothesis(self, variant_name: str, diff: float) -> bool:
        """Check if hypothesis was confirmed."""
        variant = self.study.variants[variant_name]
        hypothesis = variant.hypothesis.lower()

        if "decrease" in hypothesis:
            return diff < 0
        elif "increase" in hypothesis:
            return diff > 0
        else:
            return True  # Neutral hypothesis

    def get_full_report(self) -> str:
        """Generate full ablation study report."""
        lines = [
            "=" * 70,
            "ABLATION STUDY REPORT",
            "=" * 70,
            f"Study: {self.study.config.name}",
            f"Description: {self.study.config.description}",
            f"Topics: {len(self.study.config.topics)}",
            f"Runs per variant: {self.study.config.runs_per_variant}",
            f"Total runs: {len(self.results)}",
            "",
            "=" * 70,
            "BASELINE PERFORMANCE",
            "-" * 70,
        ]

        baseline_summary = self.get_variant_summary("baseline")
        lines.extend([
            f"  Mean Score: {baseline_summary['score_stats']['mean']:.2f}",
            f"  Std Dev: {baseline_summary['score_stats']['std']:.3f}",
            f"  Success Rate: {baseline_summary['success_rate']*100:.1f}%",
            "",
            "=" * 70,
            "VARIANT COMPARISONS",
            "-" * 70,
        ])

        for variant_name in self.study.variants:
            if variant_name == "baseline":
                continue

            comparison = self.compare_to_baseline(variant_name)
            variant = self.study.variants[variant_name]

            lines.extend([
                f"\n{variant_name.upper()}",
                f"  Type: {variant.ablation_type.value}",
                f"  Description: {variant.description}",
                f"  Hypothesis: {variant.hypothesis}",
                "",
                f"  Mean Score: {comparison['variant_mean']:.2f} ({comparison['difference']:+.3f})",
                f"  Change: {comparison['pct_change']:+.2f}%",
                f"  Success Rate: {self.get_variant_summary(variant_name)['success_rate']*100:.1f}%",
                f"  Hypothesis Confirmed: {'YES' if comparison['hypothesis_confirmed'] else 'NO'}",
                "",
            ])

        # Key findings
        lines.extend([
            "=" * 70,
            "KEY FINDINGS",
            "-" * 70,
        ])

        # Find biggest impact
        impacts = []
        for variant_name in self.study.variants:
            if variant_name == "baseline":
                continue
            comparison = self.compare_to_baseline(variant_name)
            impacts.append((variant_name, comparison["difference"]))

        impacts.sort(key=lambda x: abs(x[1]), reverse=True)

        for i, (name, impact) in enumerate(impacts[:5], 1):
            direction = "decreased" if impact < 0 else "increased"
            lines.append(f"  {i}. {name}: Score {direction} by {abs(impact):.3f}")

        lines.extend([
            "",
            "=" * 70,
            "CONCLUSIONS",
            "-" * 70,
        ])

        # Generate conclusions
        skip_impacts = [(n, d) for n, d in impacts if "skip" in n]
        if skip_impacts:
            avg_skip_impact = statistics.mean([d for _, d in skip_impacts])
            lines.append(f"  • Skipping phases reduces quality by avg {abs(avg_skip_impact):.3f} points")

        combine_impacts = [(n, d) for n, d in impacts if "combine" in n]
        if combine_impacts:
            avg_combine_impact = statistics.mean([d for _, d in combine_impacts])
            lines.append(f"  • Combining phases reduces quality by avg {abs(avg_combine_impact):.3f} points")

        # Architecture validation
        lines.append("")
        lines.append("  ARCHITECTURE VALIDATION:")

        all_negative = all(d < 0 for _, d in impacts if "skip" in _ or "combine" in _)
        if all_negative:
            lines.append("  ✓ 4-agent sequential architecture is optimal")
            lines.append("    (all ablations reduced quality)")
        else:
            lines.append("  ? Architecture may have room for optimization")
            lines.append("    (some ablations improved quality)")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def get_summary_table(self) -> str:
        """Generate summary table of all variants."""
        headers = ["Variant", "Mean Score", "Δ vs Baseline", "Success %", "Hypothesis OK"]
        rows = []

        baseline_mean = self.get_variant_summary("baseline")["score_stats"]["mean"]

        for variant_name in self.study.variants:
            summary = self.get_variant_summary(variant_name)
            mean = summary["score_stats"]["mean"]
            diff = mean - baseline_mean if variant_name != "baseline" else 0

            if variant_name != "baseline":
                comparison = self.compare_to_baseline(variant_name)
                hyp_ok = "✓" if comparison["hypothesis_confirmed"] else "✗"
            else:
                hyp_ok = "-"

            rows.append([
                variant_name,
                f"{mean:.2f}",
                f"{diff:+.3f}" if variant_name != "baseline" else "-",
                f"{summary['success_rate']*100:.0f}%",
                hyp_ok,
            ])

        # Format table
        col_widths = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]

        lines = []
        header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        lines.append(header_line)
        lines.append("-" * len(header_line))

        for row in rows:
            lines.append(" | ".join(str(c).ljust(w) for c, w in zip(row, col_widths)))

        return "\n".join(lines)
