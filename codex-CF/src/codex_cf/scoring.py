from __future__ import annotations

import re
from dataclasses import dataclass

from .models import ExplanationEvaluation, ExplanationRecord, TestScore


WEIGHTS = {
    "hard_to_vary": 0.22,
    "mechanism": 0.20,
    "reach": 0.14,
    "rejectability": 0.20,
    "integration": 0.14,
    "evidence_hygiene": 0.10,
}

CRITICAL_TESTS = {"hard_to_vary", "mechanism", "rejectability"}
CRITICAL_FLOOR = 6.5
PUBLICATION_THRESHOLD = 8.0

VAGUE_TERMS = {
    "better",
    "effective",
    "optimize",
    "improve",
    "success",
    "innovation",
    "value",
    "impact",
    "powerful",
    "transform",
    "leverage",
    "best",
    "right",
    "always",
    "never",
}

CAUSAL_MARKERS = {
    "because",
    "causes",
    "therefore",
    "leads to",
    "results in",
    "drives",
    "creates",
    "which then",
}

VARIATION_MAP = {
    "better": "different",
    "effective": "acceptable",
    "success": "progress",
    "improve": "adjust",
    "innovation": "change",
    "value": "outcome",
    "impact": "effect",
}


@dataclass
class VariationAttack:
    examples: list[str]
    survived_count: int



def evaluate_explanation(record: ExplanationRecord) -> ExplanationEvaluation:
    attack = run_variation_attack(record)

    tests = [
        score_hard_to_vary(record, attack),
        score_mechanism(record),
        score_reach(record),
        score_rejectability(record),
        score_integration(record),
        score_evidence_hygiene(record),
    ]

    weighted = sum(t.score * WEIGHTS[t.name] for t in tests)
    weighted = _clamp(weighted)

    critical_fail = any(t.critical_fail for t in tests)
    survives_gate = weighted >= PUBLICATION_THRESHOLD and not critical_fail

    return ExplanationEvaluation(
        explanation_id=record.explanation_id,
        title=record.title,
        tests=tests,
        weighted_score=round(weighted, 2),
        survives_gate=survives_gate,
        variation_examples=attack.examples,
    )



def run_variation_attack(record: ExplanationRecord) -> VariationAttack:
    source_text = f"{record.claim} {record.mechanism}".lower()
    examples: list[str] = []

    for term, replacement in VARIATION_MAP.items():
        if term in source_text:
            mutated = source_text.replace(term, replacement, 1)
            examples.append(mutated[:180])

    constraints = _count_constraints(record)
    vague_hits = _count_hits(source_text, VAGUE_TERMS)

    survived = 0
    for _ in examples:
        if constraints < 3:
            survived += 1
        elif vague_hits > 2 and constraints < 5:
            survived += 1

    return VariationAttack(examples=examples[:5], survived_count=survived)



def score_hard_to_vary(record: ExplanationRecord, attack: VariationAttack) -> TestScore:
    text = f"{record.claim} {record.mechanism}".lower()
    constraints = _count_constraints(record)
    vague_hits = _count_hits(text, VAGUE_TERMS)
    causal_hits = _count_causal_markers(text)

    base = 3.0 + constraints * 0.9 + causal_hits * 0.6
    penalty = vague_hits * 0.7 + attack.survived_count * 1.1
    score = _clamp(base - penalty)

    rationale = (
        f"constraints={constraints}, vague_hits={vague_hits}, "
        f"variation_survival={attack.survived_count}, causal_markers={causal_hits}"
    )

    return TestScore(
        name="hard_to_vary",
        score=round(score, 2),
        rationale=rationale,
        critical_fail=score < CRITICAL_FLOOR,
    )



def score_mechanism(record: ExplanationRecord) -> TestScore:
    mechanism = record.mechanism.lower().strip()
    causal_hits = _count_causal_markers(mechanism)
    step_like = len(re.findall(r"\b(then|first|second|finally)\b", mechanism))
    short_penalty = 2.0 if len(mechanism.split()) < 16 else 0.0

    score = _clamp(2.5 + causal_hits * 1.5 + step_like * 0.8 - short_penalty)

    rationale = (
        f"causal_markers={causal_hits}, step_markers={step_like}, "
        f"length_words={len(mechanism.split())}"
    )

    return TestScore(
        name="mechanism",
        score=round(score, 2),
        rationale=rationale,
        critical_fail=score < CRITICAL_FLOOR,
    )



def score_reach(record: ExplanationRecord) -> TestScore:
    scope_words = len(record.scope.split())
    cross_domain_links = len(record.integration_links)
    prediction_count = len(record.predictions)

    score = _clamp(2.0 + min(3.0, scope_words / 12.0) + cross_domain_links * 0.9 + prediction_count * 0.5)

    rationale = (
        f"scope_words={scope_words}, integration_links={cross_domain_links}, "
        f"predictions={prediction_count}"
    )

    return TestScore(name="reach", score=round(score, 2), rationale=rationale, critical_fail=False)



def score_rejectability(record: ExplanationRecord) -> TestScore:
    falsifier_count = len(record.falsifiers)
    prediction_count = len(record.predictions)
    measurable_predictions = 0

    for p in record.predictions:
        if p.metric.strip() and p.threshold.strip() and p.horizon_days > 0:
            measurable_predictions += 1

    score = _clamp(1.5 + falsifier_count * 1.8 + measurable_predictions * 1.3 + prediction_count * 0.4)

    rationale = (
        f"falsifiers={falsifier_count}, measurable_predictions={measurable_predictions}, "
        f"predictions={prediction_count}"
    )

    return TestScore(
        name="rejectability",
        score=round(score, 2),
        rationale=rationale,
        critical_fail=score < CRITICAL_FLOOR,
    )



def score_integration(record: ExplanationRecord) -> TestScore:
    links = len(record.integration_links)
    assumption_count = len(record.assumptions)
    score = _clamp(2.0 + links * 1.4 + min(2.0, assumption_count * 0.35))

    rationale = f"integration_links={links}, assumptions={assumption_count}"
    return TestScore(name="integration", score=round(score, 2), rationale=rationale, critical_fail=False)



def score_evidence_hygiene(record: ExplanationRecord) -> TestScore:
    if not record.evidence:
        return TestScore(
            name="evidence_hygiene",
            score=1.0,
            rationale="no_evidence_items",
            critical_fail=False,
        )

    quality_points = {
        "high": 1.0,
        "medium": 0.7,
        "low": 0.3,
        "unknown": 0.2,
    }

    quality_sum = 0.0
    with_url = 0

    for e in record.evidence:
        quality_sum += quality_points.get(str(e.quality.value if hasattr(e.quality, "value") else e.quality), 0.2)
        if e.url.strip().startswith("http"):
            with_url += 1

    avg_quality = quality_sum / len(record.evidence)
    url_ratio = with_url / len(record.evidence)

    score = _clamp(2.0 + avg_quality * 5.0 + url_ratio * 2.0)
    rationale = f"evidence_count={len(record.evidence)}, avg_quality={avg_quality:.2f}, url_ratio={url_ratio:.2f}"

    return TestScore(name="evidence_hygiene", score=round(score, 2), rationale=rationale, critical_fail=False)



def _count_constraints(record: ExplanationRecord) -> int:
    text = f"{record.claim} {record.mechanism}"
    numbers = len(re.findall(r"\b\d+(?:\.\d+)?\b", text))
    falsifiers = len(record.falsifiers)
    predictions = len(record.predictions)
    named_tokens = len(re.findall(r"\b[A-Z][a-z]{2,}\b", record.claim + " " + record.scope))
    return numbers + falsifiers + predictions + min(3, named_tokens)



def _count_hits(text: str, lexicon: set[str]) -> int:
    return sum(1 for word in lexicon if re.search(rf"\b{re.escape(word)}\b", text))



def _count_causal_markers(text: str) -> int:
    return sum(1 for marker in CAUSAL_MARKERS if marker in text)



def _clamp(value: float, minimum: float = 0.0, maximum: float = 10.0) -> float:
    return max(minimum, min(maximum, value))
