"""
Telemetry and structured logging for Content Factory.

Provides:
- Structured JSON logging
- Metrics collection (timing, tokens, quality scores)
- Event tracking
- Performance analysis
"""

import json
import time
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from contextlib import contextmanager
import threading


class EventType(Enum):
    """Types of telemetry events."""
    PIPELINE_START = "pipeline_start"
    PIPELINE_END = "pipeline_end"
    PHASE_START = "phase_start"
    PHASE_END = "phase_end"
    AGENT_SPAWN = "agent_spawn"
    AGENT_COMPLETE = "agent_complete"
    AGENT_ERROR = "agent_error"
    VALIDATION_START = "validation_start"
    VALIDATION_END = "validation_end"
    VALIDATION_ERROR = "validation_error"
    QUALITY_SCORE = "quality_score"
    RETRY = "retry"
    CHECKPOINT = "checkpoint"
    ERROR = "error"
    WARNING = "warning"
    METRIC = "metric"


class Phase(Enum):
    """Pipeline phases."""
    SETUP = "setup"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    WRITING = "writing"
    EDITING = "editing"
    PUBLICATION = "publication"


@dataclass
class TelemetryEvent:
    """A single telemetry event."""
    timestamp: str
    event_type: str
    phase: Optional[str]
    topic: Optional[str]
    data: Dict[str, Any]
    duration_ms: Optional[float] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "phase": self.phase,
            "topic": self.topic,
            "data": self.data,
            "duration_ms": self.duration_ms,
            "error": self.error,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class PhaseMetrics:
    """Metrics for a single phase."""
    phase: str
    start_time: float = 0
    end_time: float = 0
    duration_ms: float = 0
    token_count: int = 0
    retry_count: int = 0
    validation_errors: int = 0
    validation_warnings: int = 0
    quality_score: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None

    @property
    def duration_seconds(self) -> float:
        return self.duration_ms / 1000


@dataclass
class PipelineMetrics:
    """Aggregate metrics for a full pipeline run."""
    topic: str
    start_time: str
    end_time: Optional[str] = None
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_retries: int = 0
    phases: Dict[str, PhaseMetrics] = field(default_factory=dict)
    final_score: Optional[float] = None
    decision: Optional[str] = None
    success: bool = False
    error_count: int = 0

    def add_phase(self, phase: PhaseMetrics):
        self.phases[phase.phase] = phase
        self.total_duration_ms += phase.duration_ms
        self.total_tokens += phase.token_count
        self.total_retries += phase.retry_count
        if phase.error_message:
            self.error_count += 1

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_retries": self.total_retries,
            "phases": {k: asdict(v) for k, v in self.phases.items()},
            "final_score": self.final_score,
            "decision": self.decision,
            "success": self.success,
            "error_count": self.error_count,
        }


class TelemetryCollector:
    """
    Collects and manages telemetry data.

    Thread-safe collection of events and metrics with
    file persistence and analysis capabilities.
    """

    def __init__(
        self,
        output_dir: Optional[Path] = None,
        enabled: bool = True,
        log_level: str = "INFO"
    ):
        self.enabled = enabled
        self.output_dir = output_dir or Path(".")
        self.events: List[TelemetryEvent] = []
        self.current_pipeline: Optional[PipelineMetrics] = None
        self.current_phase: Optional[PhaseMetrics] = None
        self._lock = threading.Lock()

        # Setup logging
        self.logger = logging.getLogger("content_factory")
        self.logger.setLevel(getattr(logging, log_level.upper()))

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s'
            ))
            self.logger.addHandler(handler)

    def _now(self) -> str:
        """Get current ISO timestamp."""
        return datetime.now().isoformat()

    def _emit(self, event: TelemetryEvent):
        """Emit an event (thread-safe)."""
        if not self.enabled:
            return

        with self._lock:
            self.events.append(event)

        # Log to console
        level = logging.ERROR if event.error else logging.INFO
        msg = f"[{event.event_type}] {event.phase or 'system'}"
        if event.data:
            msg += f" | {json.dumps(event.data)}"
        if event.error:
            msg += f" | ERROR: {event.error}"

        self.logger.log(level, msg)

    def start_pipeline(self, topic: str, config: Optional[dict] = None):
        """Start tracking a new pipeline run."""
        self.current_pipeline = PipelineMetrics(
            topic=topic,
            start_time=self._now()
        )

        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.PIPELINE_START.value,
            phase=None,
            topic=topic,
            data={"config": config or {}}
        ))

    def end_pipeline(self, success: bool, final_score: Optional[float] = None, decision: Optional[str] = None):
        """End pipeline tracking."""
        if self.current_pipeline:
            self.current_pipeline.end_time = self._now()
            self.current_pipeline.success = success
            self.current_pipeline.final_score = final_score
            self.current_pipeline.decision = decision

        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.PIPELINE_END.value,
            phase=None,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={
                "success": success,
                "final_score": final_score,
                "decision": decision,
                "total_duration_ms": self.current_pipeline.total_duration_ms if self.current_pipeline else 0,
            }
        ))

    @contextmanager
    def track_phase(self, phase: Phase, topic: Optional[str] = None):
        """Context manager for tracking a phase."""
        phase_metrics = PhaseMetrics(phase=phase.value, start_time=time.time())
        self.current_phase = phase_metrics

        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.PHASE_START.value,
            phase=phase.value,
            topic=topic or (self.current_pipeline.topic if self.current_pipeline else None),
            data={}
        ))

        try:
            yield phase_metrics
            phase_metrics.success = True
        except Exception as e:
            phase_metrics.success = False
            phase_metrics.error_message = str(e)
            raise
        finally:
            phase_metrics.end_time = time.time()
            phase_metrics.duration_ms = (phase_metrics.end_time - phase_metrics.start_time) * 1000

            self._emit(TelemetryEvent(
                timestamp=self._now(),
                event_type=EventType.PHASE_END.value,
                phase=phase.value,
                topic=topic or (self.current_pipeline.topic if self.current_pipeline else None),
                data={
                    "success": phase_metrics.success,
                    "duration_ms": phase_metrics.duration_ms,
                    "tokens": phase_metrics.token_count,
                    "retries": phase_metrics.retry_count,
                },
                duration_ms=phase_metrics.duration_ms,
                error=phase_metrics.error_message
            ))

            if self.current_pipeline:
                self.current_pipeline.add_phase(phase_metrics)

            self.current_phase = None

    def record_agent_spawn(self, agent_type: str, phase: Phase):
        """Record an agent being spawned."""
        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.AGENT_SPAWN.value,
            phase=phase.value,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={"agent_type": agent_type}
        ))

    def record_agent_complete(self, agent_type: str, phase: Phase, tokens: int = 0):
        """Record an agent completing."""
        if self.current_phase:
            self.current_phase.token_count += tokens

        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.AGENT_COMPLETE.value,
            phase=phase.value,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={"agent_type": agent_type, "tokens": tokens}
        ))

    def record_validation(
        self,
        phase: Phase,
        valid: bool,
        errors: int = 0,
        warnings: int = 0,
        metrics: Optional[dict] = None
    ):
        """Record validation results."""
        if self.current_phase:
            self.current_phase.validation_errors += errors
            self.current_phase.validation_warnings += warnings

        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.VALIDATION_END.value,
            phase=phase.value,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={
                "valid": valid,
                "errors": errors,
                "warnings": warnings,
                "metrics": metrics or {}
            }
        ))

    def record_quality_score(
        self,
        score: float,
        dimension_scores: Optional[Dict[str, float]] = None,
        decision: Optional[str] = None
    ):
        """Record quality score from editor."""
        if self.current_phase:
            self.current_phase.quality_score = score

        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.QUALITY_SCORE.value,
            phase=Phase.EDITING.value,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={
                "overall_score": score,
                "dimension_scores": dimension_scores or {},
                "decision": decision,
                "meets_threshold": score >= 9.3,
            }
        ))

    def record_retry(self, phase: Phase, attempt: int, reason: str):
        """Record a retry attempt."""
        if self.current_phase:
            self.current_phase.retry_count += 1

        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.RETRY.value,
            phase=phase.value,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={"attempt": attempt, "reason": reason}
        ))

    def record_error(self, phase: Optional[Phase], error: str, recoverable: bool = True):
        """Record an error."""
        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.ERROR.value,
            phase=phase.value if phase else None,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={"recoverable": recoverable},
            error=error
        ))

    def record_checkpoint(self, phase: Phase, state: dict):
        """Record a checkpoint for state recovery."""
        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.CHECKPOINT.value,
            phase=phase.value,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={"state": state}
        ))

    def record_metric(self, name: str, value: Any, phase: Optional[Phase] = None):
        """Record a custom metric."""
        self._emit(TelemetryEvent(
            timestamp=self._now(),
            event_type=EventType.METRIC.value,
            phase=phase.value if phase else None,
            topic=self.current_pipeline.topic if self.current_pipeline else None,
            data={"metric_name": name, "value": value}
        ))

    # Persistence methods

    def save_events(self, filepath: Optional[Path] = None):
        """Save events to JSONL file."""
        path = filepath or (self.output_dir / "events.jsonl")
        with open(path, 'a') as f:
            for event in self.events:
                f.write(event.to_json() + '\n')

    def save_pipeline_metrics(self, filepath: Optional[Path] = None):
        """Save current pipeline metrics to JSON."""
        if not self.current_pipeline:
            return

        path = filepath or (self.output_dir / f"pipeline_{self.current_pipeline.topic}.json")
        with open(path, 'w') as f:
            json.dump(self.current_pipeline.to_dict(), f, indent=2)

    def load_events(self, filepath: Path) -> List[TelemetryEvent]:
        """Load events from JSONL file."""
        events = []
        with open(filepath, 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                events.append(TelemetryEvent(**data))
        return events

    # Analysis methods

    def get_phase_summary(self) -> Dict[str, Dict]:
        """Get summary statistics by phase."""
        if not self.current_pipeline:
            return {}

        return {
            phase: {
                "duration_ms": metrics.duration_ms,
                "tokens": metrics.token_count,
                "retries": metrics.retry_count,
                "success": metrics.success,
                "quality_score": metrics.quality_score,
            }
            for phase, metrics in self.current_pipeline.phases.items()
        }

    def get_error_summary(self) -> List[Dict]:
        """Get summary of all errors."""
        errors = [
            e.to_dict() for e in self.events
            if e.event_type == EventType.ERROR.value
        ]
        return errors

    def get_performance_report(self) -> str:
        """Generate a text performance report."""
        if not self.current_pipeline:
            return "No pipeline data available"

        p = self.current_pipeline
        lines = [
            "=" * 60,
            "CONTENT FACTORY PERFORMANCE REPORT",
            "=" * 60,
            f"Topic: {p.topic}",
            f"Status: {'SUCCESS' if p.success else 'FAILED'}",
            f"Final Score: {p.final_score or 'N/A'}",
            f"Decision: {p.decision or 'N/A'}",
            "",
            "TIMING",
            "-" * 40,
            f"Total Duration: {p.total_duration_ms/1000:.1f}s",
        ]

        for phase, metrics in p.phases.items():
            status = "OK" if metrics.success else "FAIL"
            lines.append(f"  {phase}: {metrics.duration_ms/1000:.1f}s [{status}]")

        lines.extend([
            "",
            "RESOURCES",
            "-" * 40,
            f"Total Tokens: {p.total_tokens:,}",
            f"Total Retries: {p.total_retries}",
            f"Errors: {p.error_count}",
        ])

        if p.phases:
            lines.extend([
                "",
                "PHASE DETAILS",
                "-" * 40,
            ])
            for phase, m in p.phases.items():
                lines.append(f"{phase.upper()}:")
                lines.append(f"  Duration: {m.duration_ms/1000:.1f}s")
                lines.append(f"  Tokens: {m.token_count:,}")
                lines.append(f"  Retries: {m.retry_count}")
                if m.quality_score:
                    lines.append(f"  Quality Score: {m.quality_score}")
                if m.error_message:
                    lines.append(f"  Error: {m.error_message}")

        lines.append("=" * 60)
        return "\n".join(lines)


# Global telemetry instance
_telemetry: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get or create global telemetry instance."""
    global _telemetry
    if _telemetry is None:
        _telemetry = TelemetryCollector()
    return _telemetry


def set_telemetry(collector: TelemetryCollector):
    """Set global telemetry instance."""
    global _telemetry
    _telemetry = collector
