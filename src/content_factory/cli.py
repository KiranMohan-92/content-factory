#!/usr/bin/env python3
"""
Content Factory CLI - World-Class Agentic Content System.

Usage:
    content-factory run <topic> [--formats=<formats>] [--brief=<file>]
    content-factory validate <topic> [--phase=<phase>]
    content-factory dashboard [--view=<view>]
    content-factory analyze [--report]
    content-factory ablation [--standard] [--topics=<file>]
    content-factory status

Commands:
    run         Run the full pipeline for a topic
    validate    Validate outputs for a topic
    dashboard   Show interactive dashboard
    analyze     Analyze quality metrics
    ablation    Run ablation study
    status      Show current pipeline status

Options:
    -h --help               Show this help message
    --formats=<formats>     Output formats (article,twitter,linkedin) [default: article,twitter-thread,linkedin-post]
    --brief=<file>          Path to brief file (or inline topic description)
    --phase=<phase>         Specific phase to validate (research,analysis,writing,editing)
    --view=<view>           Dashboard view (status,quality,history,full) [default: full]
    --report                Generate markdown report
    --standard              Run standard ablation variants
    --topics=<file>         Topics file for ablation study
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .config import PipelineConfig, OutputFormat
from .orchestrator import ContentFactoryOrchestrator, PipelineResult
from .telemetry import TelemetryCollector, set_telemetry
from .tools.dashboard import Dashboard
from .tools.analysis import QualityAnalyzer
from .tools.ablation import AblationStudy, AblationConfig
from .validators import (
    ResearchValidator,
    AnalysisValidator,
    WriterValidator,
    EditorValidator,
)


def parse_formats(formats_str: str) -> List[OutputFormat]:
    """Parse format string into OutputFormat list."""
    format_map = {
        "article": OutputFormat.ARTICLE,
        "twitter": OutputFormat.TWITTER_THREAD,
        "twitter-thread": OutputFormat.TWITTER_THREAD,
        "linkedin": OutputFormat.LINKEDIN_POST,
        "linkedin-post": OutputFormat.LINKEDIN_POST,
        "newsletter": OutputFormat.NEWSLETTER,
        "youtube": OutputFormat.YOUTUBE_SCRIPT,
    }

    formats = []
    for f in formats_str.split(","):
        f = f.strip().lower()
        if f in format_map:
            formats.append(format_map[f])
        else:
            print(f"Warning: Unknown format '{f}', skipping")

    return formats or [OutputFormat.ARTICLE]


def cmd_run(args):
    """Run the content factory pipeline."""
    # Setup
    base_dir = Path(args.base_dir)
    config = PipelineConfig(base_dir=base_dir)

    telemetry = TelemetryCollector(
        output_dir=base_dir / "telemetry",
        enabled=True
    )
    set_telemetry(telemetry)

    # Parse formats
    formats = parse_formats(args.formats)

    # Get brief
    if args.brief:
        brief_path = Path(args.brief)
        if brief_path.exists():
            brief = brief_path.read_text()
        else:
            brief = args.brief  # Treat as inline brief
    else:
        brief = f"# {args.topic}\n\nPlease analyze this topic."

    # Create orchestrator
    orchestrator = ContentFactoryOrchestrator(
        config=config,
        telemetry=telemetry,
    )

    print(f"\n{'='*60}")
    print(f"  CONTENT FACTORY")
    print(f"{'='*60}")
    print(f"  Topic: {args.topic}")
    print(f"  Formats: {', '.join(f.value for f in formats)}")
    print(f"  Mode: {'Dry Run' if args.dry_run else 'Full Execution'}")
    print(f"{'='*60}\n")

    if args.dry_run:
        print("Dry run - validating configuration only")
        config.guardrails.quality.validate()
        print("Configuration valid!")
        return 0

    # Run pipeline
    result = orchestrator.run(args.topic, brief, formats)

    # Show results
    print(f"\n{'='*60}")
    if result.success:
        print(f"  ✅ SUCCESS")
    else:
        print(f"  ❌ FAILED")

    print(f"{'='*60}")
    print(f"  Final Score: {result.final_score or 'N/A'}")
    print(f"  Decision: {result.decision or 'N/A'}")
    print(f"  Duration: {result.duration_ms/1000:.1f}s")

    if result.output_files:
        print(f"\n  Output Files:")
        for name, path in result.output_files.items():
            print(f"    {name}: {path}")

    if result.errors:
        print(f"\n  Errors:")
        for error in result.errors:
            print(f"    - {error}")

    print(f"{'='*60}\n")

    # Show telemetry report
    if args.verbose:
        print(telemetry.get_performance_report())

    return 0 if result.success else 1


def cmd_validate(args):
    """Validate outputs for a topic."""
    base_dir = Path(args.base_dir)
    outputs_dir = base_dir / "outputs" / args.topic

    if not outputs_dir.exists():
        print(f"Error: Topic '{args.topic}' not found in outputs/")
        return 1

    validators = {
        "research": (ResearchValidator(), "research.md"),
        "analysis": (AnalysisValidator(), "analysis.md"),
        "editing": (EditorValidator(), "editor-feedback.md"),
    }

    phases = [args.phase] if args.phase else validators.keys()

    print(f"\n{'='*60}")
    print(f"  VALIDATION: {args.topic}")
    print(f"{'='*60}\n")

    all_valid = True

    for phase in phases:
        if phase not in validators:
            print(f"Unknown phase: {phase}")
            continue

        validator, filename = validators[phase]
        filepath = outputs_dir / filename

        if not filepath.exists():
            print(f"  {phase.upper()}: File not found ({filename})")
            continue

        result = validator.validate_file(filepath)

        status = "✅ VALID" if result.valid else "❌ INVALID"
        print(f"  {phase.upper()}: {status}")
        print(f"    Errors: {result.error_count}")
        print(f"    Warnings: {result.warning_count}")

        if result.errors:
            for error in result.errors[:3]:
                print(f"      - {error.message}")

        if not result.valid:
            all_valid = False

        print()

    return 0 if all_valid else 1


def cmd_dashboard(args):
    """Show dashboard."""
    base_dir = Path(args.base_dir)
    dashboard = Dashboard(outputs_dir=base_dir / "outputs")

    view = args.view.lower()

    if view == "status":
        dashboard.show_status()
    elif view == "quality":
        dashboard.show_quality()
    elif view == "history":
        dashboard.show_history()
    else:
        dashboard.show_full()

    return 0


def cmd_analyze(args):
    """Analyze quality metrics."""
    base_dir = Path(args.base_dir)
    analyzer = QualityAnalyzer(outputs_dir=base_dir / "outputs")

    count = analyzer.load_from_outputs()
    print(f"Loaded {count} topics\n")

    if count == 0:
        print("No data to analyze")
        return 1

    if args.report:
        report = analyzer.generate_report()
        print(report.to_markdown())
    else:
        # Show summary
        stats = analyzer.get_overall_stats()
        print("Overall Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        print("\nWeak Dimensions:")
        for dim, score, note in analyzer.identify_weak_dimensions():
            print(f"  {dim}: {score:.2f} ({note})")

    return 0


def cmd_ablation(args):
    """Run ablation study."""
    base_dir = Path(args.base_dir)

    # Load topics
    if args.topics:
        topics_path = Path(args.topics)
        topics = topics_path.read_text().strip().split("\n")
    else:
        # Use existing topics
        outputs_dir = base_dir / "outputs"
        topics = [d.name for d in outputs_dir.iterdir() if d.is_dir()][:3]

    if not topics:
        print("No topics available for ablation study")
        return 1

    print(f"\n{'='*60}")
    print(f"  ABLATION STUDY")
    print(f"{'='*60}")
    print(f"  Topics: {len(topics)}")
    print(f"  Standard ablations: {args.standard}")
    print(f"{'='*60}\n")

    # Create study
    config = AblationConfig(
        name="content_factory_ablation",
        description="Testing Content Factory architecture",
        base_config=PipelineConfig(base_dir=base_dir),
        topics=topics,
        runs_per_variant=1,  # Use 3 for real studies
        output_dir=base_dir / "ablation_results",
    )

    study = AblationStudy(config)

    if args.standard:
        study.add_all_standard_ablations()

    # Run study (simulated for now)
    def progress(variant, topic, current, total):
        print(f"  [{current}/{total}] {variant}: {topic}")

    results = study.run(progress_callback=progress)

    # Analyze
    analysis = study.analyze()
    print(analysis.get_full_report())

    # Save
    output_path = study.save()
    print(f"\nResults saved to: {output_path}")

    return 0


def cmd_status(args):
    """Show current status."""
    base_dir = Path(args.base_dir)
    outputs_dir = base_dir / "outputs"

    print(f"\n{'='*60}")
    print(f"  CONTENT FACTORY STATUS")
    print(f"{'='*60}\n")

    # Count topics
    if outputs_dir.exists():
        topics = [d for d in outputs_dir.iterdir() if d.is_dir()]
        print(f"  Total Topics: {len(topics)}")

        # Count by status
        completed = 0
        in_progress = 0

        for topic_dir in topics:
            if (topic_dir / "final").exists() and any((topic_dir / "final").iterdir()):
                completed += 1
            else:
                in_progress += 1

        print(f"  Completed: {completed}")
        print(f"  In Progress: {in_progress}")
    else:
        print("  No outputs directory found")

    print(f"\n{'='*60}\n")

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Content Factory - World-Class Agentic Content System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--base-dir", "-d",
        default=".",
        help="Base directory for content factory"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run pipeline for a topic")
    run_parser.add_argument("topic", help="Topic name")
    run_parser.add_argument("--formats", "-f", default="article,twitter-thread,linkedin-post",
                           help="Output formats")
    run_parser.add_argument("--brief", "-b", help="Brief file or inline description")
    run_parser.add_argument("--dry-run", action="store_true", help="Validate only")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate topic outputs")
    validate_parser.add_argument("topic", help="Topic name")
    validate_parser.add_argument("--phase", "-p", help="Specific phase to validate")

    # Dashboard command
    dashboard_parser = subparsers.add_parser("dashboard", help="Show dashboard")
    dashboard_parser.add_argument("--view", default="full",
                                 choices=["status", "quality", "history", "full"])

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze quality metrics")
    analyze_parser.add_argument("--report", action="store_true", help="Generate report")

    # Ablation command
    ablation_parser = subparsers.add_parser("ablation", help="Run ablation study")
    ablation_parser.add_argument("--standard", action="store_true",
                                help="Run standard ablations")
    ablation_parser.add_argument("--topics", help="Topics file")

    # Status command
    subparsers.add_parser("status", help="Show status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Dispatch to command
    commands = {
        "run": cmd_run,
        "validate": cmd_validate,
        "dashboard": cmd_dashboard,
        "analyze": cmd_analyze,
        "ablation": cmd_ablation,
        "status": cmd_status,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
