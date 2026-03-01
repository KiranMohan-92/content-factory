from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import (
    CodexCFPipeline,
    load_knowledge_result,
    load_topic_input,
    write_knowledge_artifacts,
    write_publication_artifact,
)


def cmd_knowledge(args: argparse.Namespace) -> int:
    pipeline = CodexCFPipeline()
    topic_input = load_topic_input(Path(args.input))
    result = pipeline.run_knowledge_rail(topic_input)

    out_dir = Path(args.out)
    write_knowledge_artifacts(result, out_dir)

    print(f"Knowledge rail complete. Score={result.best_evaluation.weighted_score} Eligible={result.publication_eligible}")
    print(f"Artifacts: {out_dir / 'knowledge_result.json'} and {out_dir / 'knowledge_report.md'}")
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    pipeline = CodexCFPipeline()
    knowledge = load_knowledge_result(Path(args.knowledge))
    pkg = pipeline.run_publication_rail(knowledge)

    out_dir = Path(args.out)
    write_publication_artifact(pkg, out_dir)

    print(f"Publication rail complete. Eligible={pkg.publication_eligible}")
    print(f"Artifact: {out_dir / 'publication_package.md'}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    pipeline = CodexCFPipeline()
    topic_input = load_topic_input(Path(args.input))

    out_dir = Path(args.out)

    knowledge = pipeline.run_knowledge_rail(topic_input)
    write_knowledge_artifacts(knowledge, out_dir)

    pkg = pipeline.run_publication_rail(knowledge)
    write_publication_artifact(pkg, out_dir)

    print(
        "Run complete. "
        f"Best score={knowledge.best_evaluation.weighted_score}, "
        f"eligible={knowledge.publication_eligible}, synthesized={knowledge.synthesized}"
    )
    print(f"Artifacts in: {out_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="codex-CF epistemic pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p_knowledge = sub.add_parser("knowledge", help="Run knowledge rail")
    p_knowledge.add_argument("--input", required=True, help="Path to topic input JSON")
    p_knowledge.add_argument("--out", required=True, help="Output directory")
    p_knowledge.set_defaults(func=cmd_knowledge)

    p_publish = sub.add_parser("publish", help="Run publication rail")
    p_publish.add_argument("--knowledge", required=True, help="Path to knowledge_result.json")
    p_publish.add_argument("--out", required=True, help="Output directory")
    p_publish.set_defaults(func=cmd_publish)

    p_run = sub.add_parser("run", help="Run both rails")
    p_run.add_argument("--input", required=True, help="Path to topic input JSON")
    p_run.add_argument("--out", required=True, help="Output directory")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
