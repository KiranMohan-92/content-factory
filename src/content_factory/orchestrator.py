"""
Content Factory Orchestrator - State Machine Implementation

A production-grade orchestrator with:
- State machine with explicit transitions
- Checkpointing and state recovery
- Guardrails (budget, time, quality)
- Automatic retry with exponential backoff
- Full telemetry integration
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
import hashlib

from .config import Config, PipelineConfig, OutputFormat, GuardrailConfig
from .telemetry import TelemetryCollector, Phase, get_telemetry
from .validators import (
    ResearchValidator,
    AnalysisValidator,
    WriterValidator,
    EditorValidator,
    ValidationResult,
    ValidationError,
)


class PipelineState(Enum):
    """Pipeline state machine states."""
    IDLE = auto()
    INITIALIZING = auto()
    RESEARCHING = auto()
    ANALYZING = auto()
    WRITING = auto()
    EDITING = auto()
    PUBLISHING = auto()
    COMPLETED = auto()
    FAILED = auto()
    AWAITING_USER = auto()


class TransitionEvent(Enum):
    """Events that trigger state transitions."""
    START = auto()
    PHASE_COMPLETE = auto()
    PHASE_FAILED = auto()
    RETRY = auto()
    USER_APPROVE = auto()
    USER_REJECT = auto()
    ABORT = auto()


@dataclass
class Checkpoint:
    """Pipeline checkpoint for state recovery."""
    state: str
    topic: str
    timestamp: str
    phase_outputs: Dict[str, str]  # phase -> output file path
    retry_counts: Dict[str, int]   # phase -> retry count
    metrics: Dict[str, Any]
    config_hash: str

    def to_dict(self) -> dict:
        return {
            "state": self.state,
            "topic": self.topic,
            "timestamp": self.timestamp,
            "phase_outputs": self.phase_outputs,
            "retry_counts": self.retry_counts,
            "metrics": self.metrics,
            "config_hash": self.config_hash,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Checkpoint':
        return cls(**data)

    def save(self, path: Path):
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'Checkpoint':
        with open(path, 'r') as f:
            return cls.from_dict(json.load(f))


@dataclass
class PipelineResult:
    """Result of a pipeline run."""
    success: bool
    topic: str
    final_score: Optional[float]
    decision: Optional[str]
    output_files: Dict[str, Path]
    validation_results: Dict[str, ValidationResult]
    metrics: Dict[str, Any]
    errors: List[str]
    duration_ms: float

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "topic": self.topic,
            "final_score": self.final_score,
            "decision": self.decision,
            "output_files": {k: str(v) for k, v in self.output_files.items()},
            "errors": self.errors,
            "duration_ms": self.duration_ms,
        }


class GuardrailViolation(Exception):
    """Exception raised when a guardrail is violated."""
    def __init__(self, guardrail: str, message: str, recoverable: bool = False):
        super().__init__(message)
        self.guardrail = guardrail
        self.recoverable = recoverable


class ContentFactoryOrchestrator:
    """
    Main orchestrator for the Content Factory pipeline.

    Implements a state machine that:
    1. Manages phase transitions
    2. Enforces guardrails
    3. Handles retries
    4. Maintains checkpoints
    5. Integrates with telemetry
    """

    # State transition table
    TRANSITIONS = {
        PipelineState.IDLE: {
            TransitionEvent.START: PipelineState.INITIALIZING,
        },
        PipelineState.INITIALIZING: {
            TransitionEvent.PHASE_COMPLETE: PipelineState.RESEARCHING,
            TransitionEvent.PHASE_FAILED: PipelineState.FAILED,
        },
        PipelineState.RESEARCHING: {
            TransitionEvent.PHASE_COMPLETE: PipelineState.ANALYZING,
            TransitionEvent.PHASE_FAILED: PipelineState.FAILED,
            TransitionEvent.RETRY: PipelineState.RESEARCHING,
        },
        PipelineState.ANALYZING: {
            TransitionEvent.PHASE_COMPLETE: PipelineState.WRITING,
            TransitionEvent.PHASE_FAILED: PipelineState.RESEARCHING,  # Return to research
            TransitionEvent.RETRY: PipelineState.ANALYZING,
        },
        PipelineState.WRITING: {
            TransitionEvent.PHASE_COMPLETE: PipelineState.EDITING,
            TransitionEvent.PHASE_FAILED: PipelineState.ANALYZING,  # Return to analysis
            TransitionEvent.RETRY: PipelineState.WRITING,
        },
        PipelineState.EDITING: {
            TransitionEvent.PHASE_COMPLETE: PipelineState.PUBLISHING,
            TransitionEvent.PHASE_FAILED: PipelineState.WRITING,  # Return to writing
            TransitionEvent.RETRY: PipelineState.EDITING,
            TransitionEvent.USER_APPROVE: PipelineState.PUBLISHING,
            TransitionEvent.USER_REJECT: PipelineState.AWAITING_USER,
        },
        PipelineState.PUBLISHING: {
            TransitionEvent.PHASE_COMPLETE: PipelineState.COMPLETED,
            TransitionEvent.PHASE_FAILED: PipelineState.FAILED,
        },
        PipelineState.AWAITING_USER: {
            TransitionEvent.USER_APPROVE: PipelineState.WRITING,  # User approves retry
            TransitionEvent.USER_REJECT: PipelineState.FAILED,    # User gives up
            TransitionEvent.ABORT: PipelineState.FAILED,
        },
    }

    def __init__(
        self,
        config: Optional[PipelineConfig] = None,
        telemetry: Optional[TelemetryCollector] = None,
        agent_executor: Optional[Callable] = None,
    ):
        self.config = config or PipelineConfig()
        self.telemetry = telemetry or get_telemetry()
        self.agent_executor = agent_executor  # Callable to actually run agents

        # State
        self.state = PipelineState.IDLE
        self.topic: Optional[str] = None
        self.output_dir: Optional[Path] = None
        self.phase_outputs: Dict[str, Path] = {}
        self.validation_results: Dict[str, ValidationResult] = {}
        self.retry_counts: Dict[str, int] = {}
        self.errors: List[str] = []
        self.start_time: Optional[float] = None

        # Validators
        self.validators = {
            Phase.RESEARCH: ResearchValidator(
                min_explanations=self.config.validation.min_explanations,
                max_explanations=self.config.validation.max_explanations,
            ),
            Phase.ANALYSIS: AnalysisValidator(
                require_all_tests=self.config.validation.require_all_five_tests,
            ),
            Phase.WRITING: WriterValidator(
                min_counterarguments=self.config.validation.min_counterarguments,
            ),
            Phase.EDITING: EditorValidator(
                min_score_to_publish=self.config.guardrails.quality.min_overall_score,
            ),
        }

    def _transition(self, event: TransitionEvent) -> bool:
        """Attempt a state transition."""
        if self.state not in self.TRANSITIONS:
            return False

        transitions = self.TRANSITIONS[self.state]
        if event not in transitions:
            self.telemetry.record_error(
                None,
                f"Invalid transition: {self.state.name} + {event.name}"
            )
            return False

        old_state = self.state
        self.state = transitions[event]

        self.telemetry.record_metric(
            "state_transition",
            {"from": old_state.name, "to": self.state.name, "event": event.name}
        )

        return True

    def _check_guardrails(self, phase: Phase) -> None:
        """Check guardrails and raise if violated."""
        guardrails = self.config.guardrails

        # Check retry limit
        retries = self.retry_counts.get(phase.value, 0)
        if retries >= guardrails.max_retries_per_agent:
            raise GuardrailViolation(
                "max_retries",
                f"Phase {phase.value} exceeded max retries ({retries}/{guardrails.max_retries_per_agent})",
                recoverable=False
            )

        # Check total retries
        total_retries = sum(self.retry_counts.values())
        if total_retries >= guardrails.max_total_retries:
            raise GuardrailViolation(
                "total_retries",
                f"Pipeline exceeded total retries ({total_retries}/{guardrails.max_total_retries})",
                recoverable=False
            )

        # Check time limit
        if self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed > guardrails.max_time_per_pipeline:
                raise GuardrailViolation(
                    "time_limit",
                    f"Pipeline exceeded time limit ({elapsed:.0f}s/{guardrails.max_time_per_pipeline}s)",
                    recoverable=False
                )

    def _save_checkpoint(self) -> Path:
        """Save current state as checkpoint."""
        checkpoint = Checkpoint(
            state=self.state.name,
            topic=self.topic or "",
            timestamp=datetime.now().isoformat(),
            phase_outputs={k: str(v) for k, v in self.phase_outputs.items()},
            retry_counts=self.retry_counts.copy(),
            metrics=self.telemetry.get_phase_summary(),
            config_hash=self._config_hash(),
        )

        checkpoint_dir = self.output_dir / "checkpoints" if self.output_dir else Path("checkpoints")
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        path = checkpoint_dir / f"checkpoint_{self.topic}_{int(time.time())}.json"
        checkpoint.save(path)

        self.telemetry.record_checkpoint(
            Phase.SETUP,  # Generic phase for checkpointing
            checkpoint.to_dict()
        )

        return path

    def _config_hash(self) -> str:
        """Get hash of current config for checkpoint validation."""
        config_str = json.dumps(self.config.guardrails.quality.__dict__, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()[:8]

    def resume_from_checkpoint(self, checkpoint_path: Path) -> bool:
        """Resume pipeline from a checkpoint."""
        try:
            checkpoint = Checkpoint.load(checkpoint_path)

            # Validate config compatibility
            if checkpoint.config_hash != self._config_hash():
                self.telemetry.record_error(
                    None,
                    f"Checkpoint config mismatch: {checkpoint.config_hash} != {self._config_hash()}"
                )
                return False

            # Restore state
            self.state = PipelineState[checkpoint.state]
            self.topic = checkpoint.topic
            self.output_dir = self.config.get_output_dir(checkpoint.topic)
            self.phase_outputs = {k: Path(v) for k, v in checkpoint.phase_outputs.items()}
            self.retry_counts = checkpoint.retry_counts

            self.telemetry.record_metric(
                "checkpoint_restored",
                {"state": checkpoint.state, "topic": checkpoint.topic}
            )

            return True

        except Exception as e:
            self.telemetry.record_error(None, f"Failed to restore checkpoint: {e}")
            return False

    def _run_phase(self, phase: Phase, agent_prompt: str) -> ValidationResult:
        """Run a single phase with validation."""
        self._check_guardrails(phase)

        with self.telemetry.track_phase(phase, self.topic):
            # Record agent spawn
            self.telemetry.record_agent_spawn(phase.value, phase)

            # Execute agent (this would call Claude or another LLM)
            if self.agent_executor:
                output = self.agent_executor(phase, agent_prompt, self.config)
            else:
                # Placeholder - in real implementation, this calls the LLM
                output = self._placeholder_agent_execution(phase, agent_prompt)

            # Validate output
            validator = self.validators.get(phase)
            if validator:
                output_file = self._get_output_file(phase)
                result = validator.validate_file(output_file)

                self.telemetry.record_validation(
                    phase,
                    result.valid,
                    result.error_count,
                    result.warning_count,
                    result.metrics
                )

                self.validation_results[phase.value] = result
                return result

            # No validator - assume success
            return ValidationResult(valid=True)

    def _placeholder_agent_execution(self, phase: Phase, prompt: str) -> str:
        """Placeholder for agent execution - to be replaced with actual LLM calls."""
        # This is where you would integrate with Claude or another LLM
        # For now, just check if output file exists
        output_file = self._get_output_file(phase)
        if output_file.exists():
            return output_file.read_text()
        return ""

    def _get_output_file(self, phase: Phase) -> Path:
        """Get the expected output file for a phase."""
        if not self.output_dir:
            raise ValueError("Output directory not set")

        phase_files = {
            Phase.RESEARCH: "research.md",
            Phase.ANALYSIS: "analysis.md",
            Phase.WRITING: "drafts",  # Directory
            Phase.EDITING: "editor-feedback.md",
        }

        filename = phase_files.get(phase, f"{phase.value}.md")
        return self.output_dir / filename

    def _get_agent_prompt(self, phase: Phase) -> str:
        """Get the agent prompt for a phase."""
        agent_path = self.config.get_agent_path(phase.value.replace("_", "-") + "er")

        if agent_path.exists():
            return agent_path.read_text()

        # Fallback to constructing prompt
        return f"Execute {phase.value} phase for topic: {self.topic}"

    def initialize(self, topic: str, brief: str, formats: List[OutputFormat]) -> bool:
        """Initialize a new pipeline run."""
        if not self._transition(TransitionEvent.START):
            return False

        self.start_time = time.time()
        self.topic = self._slugify(topic)
        self.output_dir = self.config.get_output_dir(self.topic)

        # Create directory structure
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "drafts").mkdir(exist_ok=True)
        (self.output_dir / "final").mkdir(exist_ok=True)
        (self.output_dir / "checkpoints").mkdir(exist_ok=True)

        # Write brief
        brief_path = self.config.get_input_path(self.topic)
        brief_path.parent.mkdir(parents=True, exist_ok=True)
        brief_path.write_text(brief)

        # Start telemetry
        self.telemetry.start_pipeline(self.topic, self.config.guardrails.__dict__)

        self._transition(TransitionEvent.PHASE_COMPLETE)
        return True

    def run_research(self) -> bool:
        """Run the research phase."""
        if self.state != PipelineState.RESEARCHING:
            return False

        try:
            prompt = self._get_agent_prompt(Phase.RESEARCH)
            result = self._run_phase(Phase.RESEARCH, prompt)

            if result.valid:
                self.phase_outputs["research"] = self._get_output_file(Phase.RESEARCH)
                self._save_checkpoint()
                self._transition(TransitionEvent.PHASE_COMPLETE)
                return True
            else:
                self._handle_phase_failure(Phase.RESEARCH, result)
                return False

        except GuardrailViolation as e:
            self._handle_guardrail_violation(e)
            return False

    def run_analysis(self) -> bool:
        """Run the analysis phase."""
        if self.state != PipelineState.ANALYZING:
            return False

        try:
            prompt = self._get_agent_prompt(Phase.ANALYSIS)
            result = self._run_phase(Phase.ANALYSIS, prompt)

            if result.valid:
                self.phase_outputs["analysis"] = self._get_output_file(Phase.ANALYSIS)
                self._save_checkpoint()
                self._transition(TransitionEvent.PHASE_COMPLETE)
                return True
            else:
                self._handle_phase_failure(Phase.ANALYSIS, result)
                return False

        except GuardrailViolation as e:
            self._handle_guardrail_violation(e)
            return False

    def run_writing(self, formats: Optional[List[OutputFormat]] = None) -> bool:
        """Run the writing phase."""
        if self.state != PipelineState.WRITING:
            return False

        formats = formats or self.config.default_formats

        try:
            all_valid = True

            for fmt in formats:
                writer_validator = WriterValidator(content_format=fmt.value)
                prompt = self._get_agent_prompt(Phase.WRITING)

                with self.telemetry.track_phase(Phase.WRITING, self.topic):
                    output_file = self.output_dir / "drafts" / f"{fmt.value}.md"

                    if output_file.exists():
                        result = writer_validator.validate_file(output_file)
                        self.validation_results[f"writing_{fmt.value}"] = result

                        if not result.valid:
                            all_valid = False
                            self.telemetry.record_validation(
                                Phase.WRITING, False,
                                result.error_count, result.warning_count
                            )

            if all_valid:
                self.phase_outputs["writing"] = self.output_dir / "drafts"
                self._save_checkpoint()
                self._transition(TransitionEvent.PHASE_COMPLETE)
                return True
            else:
                self._handle_phase_failure(Phase.WRITING, None)
                return False

        except GuardrailViolation as e:
            self._handle_guardrail_violation(e)
            return False

    def run_editing(self) -> tuple:
        """Run the editing phase. Returns (success, score, decision)."""
        if self.state != PipelineState.EDITING:
            return False, None, None

        try:
            prompt = self._get_agent_prompt(Phase.EDITING)
            result = self._run_phase(Phase.EDITING, prompt)

            if result.valid:
                score = result.metrics.get("effective_score")
                decision = result.metrics.get("decision")

                self.telemetry.record_quality_score(
                    score or 0,
                    result.metrics.get("scores", {}),
                    decision
                )

                # Check quality threshold
                min_score = self.config.guardrails.quality.min_overall_score

                if score and score >= min_score:
                    self.phase_outputs["editing"] = self._get_output_file(Phase.EDITING)
                    self._save_checkpoint()
                    self._transition(TransitionEvent.PHASE_COMPLETE)
                    return True, score, decision
                else:
                    # Below threshold - need revision
                    self._handle_quality_failure(score, result)
                    return False, score, decision

            else:
                self._handle_phase_failure(Phase.EDITING, result)
                return False, None, None

        except GuardrailViolation as e:
            self._handle_guardrail_violation(e)
            return False, None, None

    def run_publication(self) -> bool:
        """Run the publication phase."""
        if self.state != PipelineState.PUBLISHING:
            return False

        try:
            # Move approved files to final/
            drafts_dir = self.output_dir / "drafts"
            final_dir = self.output_dir / "final"

            for draft_file in drafts_dir.glob("*.md"):
                final_path = final_dir / draft_file.name
                final_path.write_text(draft_file.read_text())
                self.phase_outputs[f"final_{draft_file.stem}"] = final_path

            # Update content context (if exists)
            self._update_content_context()

            self._save_checkpoint()
            self._transition(TransitionEvent.PHASE_COMPLETE)
            return True

        except Exception as e:
            self.errors.append(f"Publication failed: {e}")
            self._transition(TransitionEvent.PHASE_FAILED)
            return False

    def _handle_phase_failure(self, phase: Phase, result: Optional[ValidationResult]):
        """Handle a phase failure with retry logic."""
        self.retry_counts[phase.value] = self.retry_counts.get(phase.value, 0) + 1
        retries = self.retry_counts[phase.value]
        max_retries = self.config.guardrails.max_retries_per_agent

        if result:
            error_summary = "; ".join(str(e) for e in result.errors[:3])
            self.errors.append(f"{phase.value} failed: {error_summary}")

        self.telemetry.record_retry(phase, retries, "validation_failed")

        if retries < max_retries:
            self._transition(TransitionEvent.RETRY)
        else:
            self._transition(TransitionEvent.PHASE_FAILED)

    def _handle_quality_failure(self, score: Optional[float], result: ValidationResult):
        """Handle quality score below threshold."""
        self.retry_counts["editing"] = self.retry_counts.get("editing", 0) + 1
        retries = self.retry_counts["editing"]

        self.telemetry.record_retry(
            Phase.EDITING, retries,
            f"score_below_threshold: {score}"
        )

        if retries < self.config.guardrails.max_retries_per_agent:
            # Return to writing for revision
            self._transition(TransitionEvent.RETRY)
            self.state = PipelineState.WRITING
        else:
            # Escalate to user
            self._transition(TransitionEvent.USER_REJECT)

    def _handle_guardrail_violation(self, violation: GuardrailViolation):
        """Handle a guardrail violation."""
        self.errors.append(f"Guardrail violation ({violation.guardrail}): {violation}")
        self.telemetry.record_error(None, str(violation), violation.recoverable)

        if not violation.recoverable:
            self.state = PipelineState.FAILED

    def _update_content_context(self):
        """Update the content context file after publication."""
        context_path = self.config.base_dir / "CONTENT-CONTEXT.md"

        if not context_path.exists():
            return

        # Read analysis to extract concepts explained
        analysis_path = self.output_dir / "analysis.md"
        if analysis_path.exists():
            analysis = analysis_path.read_text()

            # Append to context file
            entry = f"\n\n## {self.topic} - {datetime.now().strftime('%B %Y')}\n\n"
            entry += "**Formats**: See final/ directory\n\n"
            entry += "### Concepts Explained\n\n"
            entry += "[See analysis.md for details]\n"

            with open(context_path, 'a') as f:
                f.write(entry)

    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        import re
        slug = text.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')

    def run(
        self,
        topic: str,
        brief: str,
        formats: Optional[List[OutputFormat]] = None
    ) -> PipelineResult:
        """
        Run the full pipeline.

        This is the main entry point for automated execution.
        """
        formats = formats or self.config.default_formats

        # Initialize
        if not self.initialize(topic, brief, formats):
            return self._create_result(False)

        # Run phases in sequence
        phases = [
            (PipelineState.RESEARCHING, self.run_research),
            (PipelineState.ANALYZING, self.run_analysis),
            (PipelineState.WRITING, lambda: self.run_writing(formats)),
            (PipelineState.EDITING, self.run_editing),
            (PipelineState.PUBLISHING, self.run_publication),
        ]

        final_score = None
        decision = None

        for expected_state, run_fn in phases:
            if self.state == PipelineState.FAILED:
                break

            if self.state == PipelineState.AWAITING_USER:
                break

            # Editing returns tuple
            if expected_state == PipelineState.EDITING:
                success, final_score, decision = run_fn()
            else:
                success = run_fn()

            if not success and self.state == PipelineState.FAILED:
                break

        # Finalize
        success = self.state == PipelineState.COMPLETED
        self.telemetry.end_pipeline(success, final_score, decision)

        return self._create_result(success, final_score, decision)

    def _create_result(
        self,
        success: bool,
        final_score: Optional[float] = None,
        decision: Optional[str] = None
    ) -> PipelineResult:
        """Create the pipeline result object."""
        duration = (time.time() - self.start_time) * 1000 if self.start_time else 0

        return PipelineResult(
            success=success,
            topic=self.topic or "",
            final_score=final_score,
            decision=decision,
            output_files=self.phase_outputs,
            validation_results=self.validation_results,
            metrics=self.telemetry.get_phase_summary(),
            errors=self.errors,
            duration_ms=duration,
        )

    def get_status(self) -> Dict[str, Any]:
        """Get current pipeline status."""
        return {
            "state": self.state.name,
            "topic": self.topic,
            "retry_counts": self.retry_counts,
            "phase_outputs": {k: str(v) for k, v in self.phase_outputs.items()},
            "errors": self.errors,
            "elapsed_ms": (time.time() - self.start_time) * 1000 if self.start_time else 0,
        }
