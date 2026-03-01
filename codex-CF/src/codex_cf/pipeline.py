from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .models import (
    EvidenceItem,
    ExplanationRecord,
    Falsifier,
    KnowledgeResult,
    Prediction,
    PublicationPackage,
    SourceQuality,
    now_iso,
    to_dict,
)
from .scoring import CRITICAL_FLOOR, PUBLICATION_THRESHOLD, evaluate_explanation


@dataclass
class GateConfig:
    threshold: float = PUBLICATION_THRESHOLD
    critical_floor: float = CRITICAL_FLOOR


class CodexCFPipeline:
    def __init__(self, gate: GateConfig | None = None):
        self.gate = gate or GateConfig()

    def run_knowledge_rail(self, topic_input: dict[str, Any]) -> KnowledgeResult:
        topic = topic_input["topic"]
        candidates = [self._to_explanation(c) for c in topic_input.get("candidate_explanations", [])]

        if not candidates:
            raise ValueError("No candidate_explanations provided")

        evaluations = [evaluate_explanation(c) for c in candidates]
        evaluations.sort(key=lambda e: e.weighted_score, reverse=True)

        best_eval = evaluations[0]
        best_record = _find_by_id(candidates, best_eval.explanation_id)

        synthesized = False

        if not best_eval.survives_gate:
            synthesized_record = self._synthesize(candidates, evaluations, topic)
            synthesized_eval = evaluate_explanation(synthesized_record)
            evaluations.append(synthesized_eval)

            if synthesized_eval.weighted_score > best_eval.weighted_score:
                best_eval = synthesized_eval
                best_record = synthesized_record
                synthesized = True

        publication_eligible = self._passes_gate(best_eval)

        return KnowledgeResult(
            topic=topic,
            timestamp=now_iso(),
            evaluations=evaluations,
            best_explanation=best_record,
            best_evaluation=best_eval,
            synthesized=synthesized,
            publication_eligible=publication_eligible,
        )

    def run_publication_rail(self, knowledge: KnowledgeResult) -> PublicationPackage:
        best = knowledge.best_explanation
        eval_ = knowledge.best_evaluation

        falsifier_lines = [f"{f.condition} | Test: {f.test_method}" for f in best.falsifiers]
        if not falsifier_lines:
            falsifier_lines = ["No explicit falsifier provided."]

        change_my_mind = []
        for f in best.falsifiers:
            change_my_mind.append(f"If observed: {f.condition}")

        for p in best.predictions:
            change_my_mind.append(
                f"If metric '{p.metric}' misses threshold '{p.threshold}' within {p.horizon_days} days"
            )

        if not change_my_mind:
            change_my_mind = ["Add measurable predictions and falsifiers before publication."]

        return PublicationPackage(
            topic=knowledge.topic,
            explanation_id=best.explanation_id,
            title=best.title,
            claim=best.claim,
            mechanism=best.mechanism,
            assumptions=best.assumptions,
            key_falsifiers=falsifier_lines,
            what_would_change_my_mind=change_my_mind,
            epistemic_score=eval_.weighted_score,
            publication_eligible=knowledge.publication_eligible,
            generated_at=now_iso(),
        )

    def _passes_gate(self, evaluation) -> bool:
        if evaluation.weighted_score < self.gate.threshold:
            return False

        for test in evaluation.tests:
            if test.critical_fail:
                return False
            if test.name in {"hard_to_vary", "mechanism", "rejectability"} and test.score < self.gate.critical_floor:
                return False

        return True

    def _synthesize(
        self,
        records: list[ExplanationRecord],
        evaluations,
        topic: str,
    ) -> ExplanationRecord:
        top = evaluations[:2]
        first = _find_by_id(records, top[0].explanation_id)
        second = _find_by_id(records, top[1].explanation_id) if len(top) > 1 else first

        merged_assumptions = _unique(first.assumptions + second.assumptions)
        merged_links = _unique(first.integration_links + second.integration_links)
        merged_evidence = first.evidence[:2] + second.evidence[:2]
        merged_predictions = first.predictions[:2] + second.predictions[:2]
        merged_falsifiers = first.falsifiers[:2] + second.falsifiers[:2]

        if not merged_predictions:
            merged_predictions.append(
                Prediction(
                    statement=f"Synthesis for {topic} should improve discriminative power against baseline explanations.",
                    metric="discriminative_test_pass_rate",
                    threshold="> baseline",
                    horizon_days=90,
                )
            )

        if not merged_falsifiers:
            merged_falsifiers.append(
                Falsifier(
                    condition="Synthesis fails to outperform strongest baseline on pre-registered tests",
                    test_method="run pre-registered discriminative experiments",
                )
            )

        return ExplanationRecord(
            explanation_id="synth-001",
            title=f"Synthesized Conjecture for {topic}",
            claim=(
                f"{first.claim} AND {second.claim}. "
                "The combined conjecture is preferred only if it survives stricter falsification tests."
            ),
            mechanism=(
                f"{first.mechanism} Then, {second.mechanism} "
                "This sequence is accepted only when both stages produce measurable improvements."
            ),
            scope=f"Union scope: {first.scope} + {second.scope}",
            assumptions=merged_assumptions,
            evidence=merged_evidence,
            integration_links=merged_links,
            predictions=merged_predictions,
            falsifiers=merged_falsifiers,
            notes="Auto-synthesized because no candidate passed epistemic gate.",
        )

    def _to_explanation(self, raw: dict[str, Any]) -> ExplanationRecord:
        evidence = [
            EvidenceItem(
                source=e.get("source", ""),
                claim=e.get("claim", ""),
                quality=SourceQuality(e.get("quality", "unknown")),
                url=e.get("url", ""),
                notes=e.get("notes", ""),
            )
            for e in raw.get("evidence", [])
        ]

        predictions = [
            Prediction(
                statement=p.get("statement", ""),
                metric=p.get("metric", ""),
                threshold=p.get("threshold", ""),
                horizon_days=int(p.get("horizon_days", 0)),
            )
            for p in raw.get("predictions", [])
        ]

        falsifiers = [
            Falsifier(
                condition=f.get("condition", ""),
                test_method=f.get("test_method", ""),
            )
            for f in raw.get("falsifiers", [])
        ]

        return ExplanationRecord(
            explanation_id=raw["explanation_id"],
            title=raw["title"],
            claim=raw["claim"],
            mechanism=raw["mechanism"],
            scope=raw.get("scope", ""),
            assumptions=raw.get("assumptions", []),
            evidence=evidence,
            integration_links=raw.get("integration_links", []),
            predictions=predictions,
            falsifiers=falsifiers,
            notes=raw.get("notes", ""),
        )


def write_knowledge_artifacts(result: KnowledgeResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "knowledge_result.json"
    md_path = out_dir / "knowledge_report.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(to_dict(result), f, indent=2)

    lines = [
        f"# Knowledge Report: {result.topic}",
        "",
        f"Generated: {result.timestamp}",
        f"Publication Eligible: {result.publication_eligible}",
        f"Synthesized: {result.synthesized}",
        "",
        "## Best Explanation",
        f"- ID: {result.best_explanation.explanation_id}",
        f"- Title: {result.best_explanation.title}",
        f"- Epistemic Score: {result.best_evaluation.weighted_score}",
        "",
        "## Test Scores",
    ]

    for test in result.best_evaluation.tests:
        lines.append(f"- {test.name}: {test.score} ({test.rationale})")

    lines.extend(["", "## Candidate Ranking"])
    ranking = sorted(result.evaluations, key=lambda e: e.weighted_score, reverse=True)
    for idx, ev in enumerate(ranking, start=1):
        lines.append(f"{idx}. {ev.explanation_id} | {ev.title} | {ev.weighted_score}")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def write_publication_artifact(pkg: PublicationPackage, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "publication_package.md"

    lines = [
        f"# Publication Package: {pkg.topic}",
        "",
        f"Generated: {pkg.generated_at}",
        f"Publication Eligible: {pkg.publication_eligible}",
        f"Epistemic Score: {pkg.epistemic_score}",
        "",
        "## Core Claim",
        pkg.claim,
        "",
        "## Mechanism",
        pkg.mechanism,
        "",
        "## Assumptions",
    ]

    for assumption in pkg.assumptions or ["No assumptions provided."]:
        lines.append(f"- {assumption}")

    lines.extend(["", "## Key Falsifiers"])
    for item in pkg.key_falsifiers:
        lines.append(f"- {item}")

    lines.extend(["", "## What Would Change My Mind"])
    for item in pkg.what_would_change_my_mind:
        lines.append(f"- {item}")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def load_topic_input(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_knowledge_result(path: Path) -> KnowledgeResult:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    pipe = CodexCFPipeline()

    # Rebuild best explanation through parser to keep schema normalized.
    best_record = pipe._to_explanation(raw["best_explanation"])

    from .models import ExplanationEvaluation, TestScore

    evaluations = []
    for ev in raw.get("evaluations", []):
        tests = [
            TestScore(
                name=t["name"],
                score=float(t["score"]),
                rationale=t["rationale"],
                critical_fail=bool(t.get("critical_fail", False)),
            )
            for t in ev.get("tests", [])
        ]

        evaluations.append(
            ExplanationEvaluation(
                explanation_id=ev["explanation_id"],
                title=ev["title"],
                tests=tests,
                weighted_score=float(ev["weighted_score"]),
                survives_gate=bool(ev["survives_gate"]),
                variation_examples=ev.get("variation_examples", []),
            )
        )

    best_eval = next(e for e in evaluations if e.explanation_id == raw["best_evaluation"]["explanation_id"])

    return KnowledgeResult(
        topic=raw["topic"],
        timestamp=raw["timestamp"],
        evaluations=evaluations,
        best_explanation=best_record,
        best_evaluation=best_eval,
        synthesized=bool(raw.get("synthesized", False)),
        publication_eligible=bool(raw.get("publication_eligible", False)),
    )


def _find_by_id(records: list[ExplanationRecord], explanation_id: str) -> ExplanationRecord:
    for r in records:
        if r.explanation_id == explanation_id:
            return r
    raise KeyError(f"Explanation ID not found: {explanation_id}")


def _unique(values: list[str]) -> list[str]:
    seen = set()
    out = []
    for v in values:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out
