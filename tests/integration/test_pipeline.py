"""
Integration tests for Content Factory pipeline.

Tests the full orchestrator flow with:
- State machine transitions
- Validation at each phase
- Checkpoint/recovery
- Guardrail enforcement
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from content_factory.orchestrator import (
    ContentFactoryOrchestrator,
    PipelineState,
    TransitionEvent,
    GuardrailViolation,
)
from content_factory.config import PipelineConfig, OutputFormat, GuardrailConfig, QualityConfig
from content_factory.telemetry import TelemetryCollector


class TestPipelineStateMachine:
    """Tests for pipeline state machine transitions."""

    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator with test config."""
        config = PipelineConfig(
            base_dir=Path(tempfile.mkdtemp()),
        )
        telemetry = TelemetryCollector(enabled=False)
        return ContentFactoryOrchestrator(config=config, telemetry=telemetry)

    def test_initial_state_is_idle(self, orchestrator):
        """Pipeline should start in IDLE state."""
        assert orchestrator.state == PipelineState.IDLE

    def test_start_transitions_to_initializing(self, orchestrator):
        """START event should transition from IDLE to INITIALIZING."""
        result = orchestrator._transition(TransitionEvent.START)
        assert result == True
        assert orchestrator.state == PipelineState.INITIALIZING

    def test_invalid_transition_fails(self, orchestrator):
        """Invalid transition should return False."""
        # Can't go from IDLE to ANALYZING
        orchestrator.state = PipelineState.IDLE
        result = orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert result == False

    def test_full_happy_path_transitions(self, orchestrator):
        """Test complete successful path through state machine."""
        # IDLE -> INITIALIZING
        orchestrator._transition(TransitionEvent.START)
        assert orchestrator.state == PipelineState.INITIALIZING

        # INITIALIZING -> RESEARCHING
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert orchestrator.state == PipelineState.RESEARCHING

        # RESEARCHING -> ANALYZING
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert orchestrator.state == PipelineState.ANALYZING

        # ANALYZING -> WRITING
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert orchestrator.state == PipelineState.WRITING

        # WRITING -> EDITING
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert orchestrator.state == PipelineState.EDITING

        # EDITING -> PUBLISHING
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert orchestrator.state == PipelineState.PUBLISHING

        # PUBLISHING -> COMPLETED
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert orchestrator.state == PipelineState.COMPLETED

    def test_retry_stays_in_same_state(self, orchestrator):
        """RETRY should keep pipeline in same state."""
        orchestrator._transition(TransitionEvent.START)
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert orchestrator.state == PipelineState.RESEARCHING

        orchestrator._transition(TransitionEvent.RETRY)
        assert orchestrator.state == PipelineState.RESEARCHING

    def test_failure_fallback_transitions(self, orchestrator):
        """PHASE_FAILED should transition to appropriate fallback state."""
        # Get to ANALYZING
        orchestrator._transition(TransitionEvent.START)
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        assert orchestrator.state == PipelineState.ANALYZING

        # Failure in ANALYZING should go back to RESEARCHING
        orchestrator._transition(TransitionEvent.PHASE_FAILED)
        assert orchestrator.state == PipelineState.RESEARCHING


class TestPipelineInitialization:
    """Tests for pipeline initialization."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        path = Path(tempfile.mkdtemp())
        yield path
        shutil.rmtree(path, ignore_errors=True)

    @pytest.fixture
    def orchestrator(self, temp_dir):
        """Create orchestrator with temp directory."""
        config = PipelineConfig(base_dir=temp_dir)
        telemetry = TelemetryCollector(enabled=False)
        return ContentFactoryOrchestrator(config=config, telemetry=telemetry)

    def test_initialize_creates_directories(self, orchestrator, temp_dir):
        """Initialize should create required directories."""
        brief = "# Test Topic\n\nThis is a test brief."
        result = orchestrator.initialize("Test Topic", brief, [OutputFormat.ARTICLE])

        assert result == True
        assert (temp_dir / "inputs" / "test-topic.md").exists()
        assert (temp_dir / "outputs" / "test-topic").is_dir()
        assert (temp_dir / "outputs" / "test-topic" / "drafts").is_dir()
        assert (temp_dir / "outputs" / "test-topic" / "final").is_dir()

    def test_initialize_writes_brief(self, orchestrator, temp_dir):
        """Initialize should write brief to inputs directory."""
        brief = "# Test Topic\n\nThis is a test brief with content."
        orchestrator.initialize("Test Topic", brief, [OutputFormat.ARTICLE])

        brief_path = temp_dir / "inputs" / "test-topic.md"
        assert brief_path.read_text() == brief

    def test_slugify_works_correctly(self, orchestrator):
        """Topic names should be properly slugified."""
        test_cases = [
            ("Simple Test", "simple-test"),
            ("Test With   Spaces", "test-with-spaces"),
            ("Test-With-Dashes", "test-with-dashes"),
            ("Test_With_Underscores", "test-with-underscores"),
            ("Test!@#Special$%^Characters", "testspecialcharacters"),
        ]

        for input_text, expected in test_cases:
            assert orchestrator._slugify(input_text) == expected


class TestGuardrails:
    """Tests for guardrail enforcement."""

    @pytest.fixture
    def strict_config(self):
        """Create config with strict guardrails."""
        return PipelineConfig(
            base_dir=Path(tempfile.mkdtemp()),
            guardrails=GuardrailConfig(
                max_retries_per_agent=2,
                max_total_retries=3,
                max_time_per_pipeline=60,  # 1 minute
            )
        )

    @pytest.fixture
    def orchestrator(self, strict_config):
        """Create orchestrator with strict guardrails."""
        telemetry = TelemetryCollector(enabled=False)
        return ContentFactoryOrchestrator(config=strict_config, telemetry=telemetry)

    def test_retry_limit_enforced(self, orchestrator):
        """Should raise when retry limit exceeded."""
        from content_factory.telemetry import Phase

        orchestrator.retry_counts["research"] = 2  # At limit
        orchestrator.start_time = 0  # Fake start time

        with pytest.raises(GuardrailViolation) as exc_info:
            orchestrator._check_guardrails(Phase.RESEARCH)

        assert "max retries" in str(exc_info.value).lower()

    def test_total_retry_limit_enforced(self, orchestrator):
        """Should raise when total retries exceeded."""
        from content_factory.telemetry import Phase

        orchestrator.retry_counts = {
            "research": 1,
            "analysis": 1,
            "writing": 1,
        }  # Total = 3, at limit
        orchestrator.start_time = 0

        with pytest.raises(GuardrailViolation) as exc_info:
            orchestrator._check_guardrails(Phase.RESEARCH)

        assert "total retries" in str(exc_info.value).lower()

    def test_within_limits_passes(self, orchestrator):
        """Should not raise when within limits."""
        from content_factory.telemetry import Phase
        import time

        orchestrator.retry_counts = {"research": 0}
        orchestrator.start_time = time.time()  # Just started

        # Should not raise
        orchestrator._check_guardrails(Phase.RESEARCH)


class TestCheckpointing:
    """Tests for checkpoint save/restore."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        path = Path(tempfile.mkdtemp())
        yield path
        shutil.rmtree(path, ignore_errors=True)

    @pytest.fixture
    def orchestrator(self, temp_dir):
        """Create orchestrator."""
        config = PipelineConfig(base_dir=temp_dir)
        telemetry = TelemetryCollector(enabled=False)
        return ContentFactoryOrchestrator(config=config, telemetry=telemetry)

    def test_checkpoint_saves_state(self, orchestrator, temp_dir):
        """Checkpoint should save current state."""
        orchestrator.initialize("Test Topic", "Brief", [OutputFormat.ARTICLE])
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)  # To RESEARCHING

        checkpoint_path = orchestrator._save_checkpoint()

        assert checkpoint_path.exists()

        # Load and verify
        import json
        with open(checkpoint_path) as f:
            data = json.load(f)

        assert data["state"] == "RESEARCHING"
        assert data["topic"] == "test-topic"

    def test_checkpoint_restore_works(self, orchestrator, temp_dir):
        """Should be able to restore from checkpoint."""
        # Initialize and progress
        orchestrator.initialize("Test Topic", "Brief", [OutputFormat.ARTICLE])
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)
        orchestrator._transition(TransitionEvent.PHASE_COMPLETE)  # To ANALYZING
        orchestrator.phase_outputs["research"] = temp_dir / "outputs/test-topic/research.md"

        checkpoint_path = orchestrator._save_checkpoint()

        # Create new orchestrator
        new_config = PipelineConfig(base_dir=temp_dir)
        new_orchestrator = ContentFactoryOrchestrator(
            config=new_config,
            telemetry=TelemetryCollector(enabled=False)
        )

        # Restore
        success = new_orchestrator.resume_from_checkpoint(checkpoint_path)

        assert success == True
        assert new_orchestrator.state == PipelineState.ANALYZING
        assert new_orchestrator.topic == "test-topic"


class TestValidationIntegration:
    """Tests for validation integration with pipeline."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory with fixtures."""
        path = Path(tempfile.mkdtemp())

        # Copy fixtures
        fixtures_dir = Path(__file__).parent.parent / "fixtures"
        if fixtures_dir.exists():
            # Create output structure
            output_dir = path / "outputs" / "test-topic"
            output_dir.mkdir(parents=True)

            # Copy sample research
            sample_research = fixtures_dir / "sample_research.md"
            if sample_research.exists():
                (output_dir / "research.md").write_text(sample_research.read_text())

            # Copy sample editor feedback
            sample_feedback = fixtures_dir / "sample_editor_feedback.md"
            if sample_feedback.exists():
                (output_dir / "editor-feedback.md").write_text(sample_feedback.read_text())

        yield path
        shutil.rmtree(path, ignore_errors=True)

    def test_research_validation_integration(self, temp_dir):
        """Research validator should work with real files."""
        from content_factory.validators import ResearchValidator

        research_path = temp_dir / "outputs" / "test-topic" / "research.md"
        if not research_path.exists():
            pytest.skip("Fixture not available")

        validator = ResearchValidator()
        result = validator.validate_file(research_path)

        assert result.valid or result.warning_count > 0  # Valid or just warnings
        assert "explanation_count" in result.metrics

    def test_editor_validation_integration(self, temp_dir):
        """Editor validator should work with real files."""
        from content_factory.validators import EditorValidator

        feedback_path = temp_dir / "outputs" / "test-topic" / "editor-feedback.md"
        if not feedback_path.exists():
            pytest.skip("Fixture not available")

        validator = EditorValidator()
        result = validator.validate_file(feedback_path)

        assert "effective_score" in result.metrics
        assert result.metrics["effective_score"] > 0


class TestPipelineResult:
    """Tests for PipelineResult generation."""

    @pytest.fixture
    def temp_dir(self):
        path = Path(tempfile.mkdtemp())
        yield path
        shutil.rmtree(path, ignore_errors=True)

    def test_result_captures_success(self, temp_dir):
        """Successful pipeline should return success result."""
        config = PipelineConfig(base_dir=temp_dir)
        orchestrator = ContentFactoryOrchestrator(
            config=config,
            telemetry=TelemetryCollector(enabled=False)
        )

        # Manually set success state
        orchestrator.state = PipelineState.COMPLETED
        orchestrator.topic = "test-topic"
        orchestrator.start_time = 0

        result = orchestrator._create_result(True, 9.5, "PUBLISH")

        assert result.success == True
        assert result.final_score == 9.5
        assert result.decision == "PUBLISH"

    def test_result_captures_errors(self, temp_dir):
        """Failed pipeline should capture errors."""
        config = PipelineConfig(base_dir=temp_dir)
        orchestrator = ContentFactoryOrchestrator(
            config=config,
            telemetry=TelemetryCollector(enabled=False)
        )

        orchestrator.topic = "test-topic"
        orchestrator.start_time = 0
        orchestrator.errors = ["Error 1", "Error 2"]

        result = orchestrator._create_result(False)

        assert result.success == False
        assert len(result.errors) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
