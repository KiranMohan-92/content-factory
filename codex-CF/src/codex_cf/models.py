from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class SourceQuality(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


@dataclass
class EvidenceItem:
    source: str
    claim: str
    quality: SourceQuality = SourceQuality.UNKNOWN
    url: str = ""
    notes: str = ""


@dataclass
class Prediction:
    statement: str
    metric: str
    threshold: str
    horizon_days: int


@dataclass
class Falsifier:
    condition: str
    test_method: str


@dataclass
class ExplanationRecord:
    explanation_id: str
    title: str
    claim: str
    mechanism: str
    scope: str
    assumptions: list[str] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    integration_links: list[str] = field(default_factory=list)
    predictions: list[Prediction] = field(default_factory=list)
    falsifiers: list[Falsifier] = field(default_factory=list)
    notes: str = ""


@dataclass
class TestScore:
    name: str
    score: float
    rationale: str
    critical_fail: bool = False


@dataclass
class ExplanationEvaluation:
    explanation_id: str
    title: str
    tests: list[TestScore]
    weighted_score: float
    survives_gate: bool
    variation_examples: list[str] = field(default_factory=list)


@dataclass
class KnowledgeResult:
    topic: str
    timestamp: str
    evaluations: list[ExplanationEvaluation]
    best_explanation: ExplanationRecord
    best_evaluation: ExplanationEvaluation
    synthesized: bool
    publication_eligible: bool


@dataclass
class PublicationPackage:
    topic: str
    explanation_id: str
    title: str
    claim: str
    mechanism: str
    assumptions: list[str]
    key_falsifiers: list[str]
    what_would_change_my_mind: list[str]
    epistemic_score: float
    publication_eligible: bool
    generated_at: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def to_dict(obj: Any) -> dict[str, Any]:
    """Convert dataclasses and enums into JSON-safe dictionaries."""
    if hasattr(obj, "__dataclass_fields__"):
        data = asdict(obj)
    elif isinstance(obj, dict):
        data = obj
    else:
        raise TypeError(f"Unsupported type for to_dict: {type(obj)}")

    return _normalize(data)


def _normalize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    return value
