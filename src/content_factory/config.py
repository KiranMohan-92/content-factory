"""
Configuration management for Content Factory.

Provides typed configuration with defaults, validation, and environment variable support.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List
import json
import os


class AgentVersion(Enum):
    """Agent instruction versions."""
    V1 = "v1"
    V2 = "v2"


class ExecutionMode(Enum):
    """Pipeline execution modes."""
    AUTOMATED = "automated"      # Full automation, stops only on rejection
    SUPERVISED = "supervised"    # Checkpoints after each phase
    DRY_RUN = "dry_run"          # Validate without executing


class OutputFormat(Enum):
    """Supported output formats."""
    ARTICLE = "article"
    TWITTER_THREAD = "twitter-thread"
    LINKEDIN_POST = "linkedin-post"
    NEWSLETTER = "newsletter"
    YOUTUBE_SCRIPT = "youtube-script"
    PODCAST_NOTES = "podcast-notes"


@dataclass
class QualityConfig:
    """Quality gate configuration."""

    # Minimum scores (9.0 = world-class minimum)
    min_overall_score: float = 9.3
    min_philosophical_accuracy: float = 9.0
    min_factual_accuracy: float = 9.0
    min_logical_soundness: float = 9.0
    min_clarity: float = 9.0
    min_engagement: float = 9.0
    min_practical_utility: float = 9.0
    min_intellectual_honesty: float = 9.0

    # Score weights (must sum to 1.0)
    weight_philosophical: float = 0.15
    weight_factual: float = 0.10
    weight_logical: float = 0.15
    weight_clarity: float = 0.15
    weight_engagement: float = 0.15
    weight_practical: float = 0.20
    weight_honesty: float = 0.10

    # Quality floor for auto-rejection
    auto_reject_threshold: float = 8.0

    def validate(self) -> bool:
        """Validate configuration consistency."""
        weights = [
            self.weight_philosophical,
            self.weight_factual,
            self.weight_logical,
            self.weight_clarity,
            self.weight_engagement,
            self.weight_practical,
            self.weight_honesty,
        ]
        total = sum(weights)
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Score weights must sum to 1.0, got {total}")
        return True


@dataclass
class GuardrailConfig:
    """Guardrails for resource and quality control."""

    # Token/budget limits
    max_tokens_per_agent: int = 100_000
    max_tokens_per_pipeline: int = 500_000

    # Time limits (seconds)
    max_time_per_agent: int = 600      # 10 minutes
    max_time_per_pipeline: int = 3600  # 1 hour

    # Retry limits
    max_retries_per_agent: int = 2
    max_total_retries: int = 5

    # Quality gates
    quality: QualityConfig = field(default_factory=QualityConfig)

    # Auto-escalation
    escalate_on_repeated_failure: bool = True
    escalation_threshold: int = 2  # Failures before escalating to human


@dataclass
class TelemetryConfig:
    """Telemetry and logging configuration."""

    enabled: bool = True
    log_level: str = "INFO"

    # Structured logging
    log_format: str = "json"  # "json" or "text"
    log_file: Optional[str] = None

    # Metrics collection
    collect_timing: bool = True
    collect_token_usage: bool = True
    collect_quality_scores: bool = True
    collect_error_types: bool = True

    # Persistence
    metrics_file: str = "metrics.jsonl"
    checkpoint_dir: str = "checkpoints"


@dataclass
class ValidationConfig:
    """Output validation configuration."""

    enabled: bool = True
    strict_mode: bool = True  # Fail on any validation error

    # Research validation
    min_explanations: int = 3
    max_explanations: int = 7
    require_evidence_both_sides: bool = True
    require_steelman: bool = True

    # Analysis validation
    require_all_five_tests: bool = True
    require_ranking: bool = True
    require_good_explanation: bool = True

    # Writer validation
    min_counterarguments: int = 2
    require_practical_utility: bool = True
    max_preachy_score: float = 3.0  # 1-10 scale, lower is better

    # Editor validation
    require_all_dimensions_scored: bool = True
    require_decision: bool = True


@dataclass
class PipelineConfig:
    """Full pipeline configuration."""

    # Basic settings
    name: str = "content-factory"
    version: str = "3.0.0"

    # Execution
    mode: ExecutionMode = ExecutionMode.AUTOMATED
    agent_version: AgentVersion = AgentVersion.V2

    # Paths
    base_dir: Path = field(default_factory=lambda: Path.cwd())
    inputs_dir: str = "inputs"
    outputs_dir: str = "outputs"
    agents_dir: str = "agents"
    templates_dir: str = "templates"

    # Output formats
    default_formats: List[OutputFormat] = field(
        default_factory=lambda: [
            OutputFormat.ARTICLE,
            OutputFormat.TWITTER_THREAD,
            OutputFormat.LINKEDIN_POST,
        ]
    )

    # Sub-configurations
    guardrails: GuardrailConfig = field(default_factory=GuardrailConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)

    def get_input_path(self, topic_slug: str) -> Path:
        """Get input brief path for a topic."""
        return self.base_dir / self.inputs_dir / f"{topic_slug}.md"

    def get_output_dir(self, topic_slug: str) -> Path:
        """Get output directory for a topic."""
        return self.base_dir / self.outputs_dir / topic_slug

    def get_agent_path(self, agent_name: str) -> Path:
        """Get agent instruction file path."""
        suffix = "-v2" if self.agent_version == AgentVersion.V2 else ""
        return self.base_dir / self.agents_dir / f"{agent_name}-agent{suffix}.md"


class Config:
    """
    Global configuration manager.

    Supports:
    - Loading from JSON file
    - Environment variable overrides
    - Runtime modification
    - Validation
    """

    _instance: Optional['Config'] = None
    _pipeline: PipelineConfig

    def __init__(self, pipeline_config: Optional[PipelineConfig] = None):
        self._pipeline = pipeline_config or PipelineConfig()

    @classmethod
    def get_instance(cls) -> 'Config':
        """Get or create singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def load(cls, config_path: Path) -> 'Config':
        """Load configuration from JSON file."""
        with open(config_path, 'r') as f:
            data = json.load(f)

        # Build nested configs
        quality_config = QualityConfig(**data.get('quality', {}))
        guardrail_config = GuardrailConfig(
            quality=quality_config,
            **{k: v for k, v in data.get('guardrails', {}).items() if k != 'quality'}
        )
        telemetry_config = TelemetryConfig(**data.get('telemetry', {}))
        validation_config = ValidationConfig(**data.get('validation', {}))

        pipeline_config = PipelineConfig(
            name=data.get('name', 'content-factory'),
            version=data.get('version', '3.0.0'),
            mode=ExecutionMode(data.get('mode', 'automated')),
            agent_version=AgentVersion(data.get('agent_version', 'v2')),
            base_dir=Path(data.get('base_dir', '.')),
            guardrails=guardrail_config,
            telemetry=telemetry_config,
            validation=validation_config,
        )

        cls._instance = cls(pipeline_config)
        return cls._instance

    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables."""
        pipeline = PipelineConfig()

        # Override from environment
        if base_dir := os.environ.get('CONTENT_FACTORY_BASE_DIR'):
            pipeline.base_dir = Path(base_dir)

        if mode := os.environ.get('CONTENT_FACTORY_MODE'):
            pipeline.mode = ExecutionMode(mode)

        if min_score := os.environ.get('CONTENT_FACTORY_MIN_SCORE'):
            pipeline.guardrails.quality.min_overall_score = float(min_score)

        if max_retries := os.environ.get('CONTENT_FACTORY_MAX_RETRIES'):
            pipeline.guardrails.max_retries_per_agent = int(max_retries)

        cls._instance = cls(pipeline)
        return cls._instance

    @property
    def pipeline(self) -> PipelineConfig:
        """Get pipeline configuration."""
        return self._pipeline

    def validate(self) -> bool:
        """Validate entire configuration."""
        self._pipeline.guardrails.quality.validate()
        return True

    def to_dict(self) -> dict:
        """Export configuration to dictionary."""
        return {
            'name': self._pipeline.name,
            'version': self._pipeline.version,
            'mode': self._pipeline.mode.value,
            'agent_version': self._pipeline.agent_version.value,
            'base_dir': str(self._pipeline.base_dir),
            'guardrails': {
                'max_tokens_per_agent': self._pipeline.guardrails.max_tokens_per_agent,
                'max_time_per_agent': self._pipeline.guardrails.max_time_per_agent,
                'max_retries_per_agent': self._pipeline.guardrails.max_retries_per_agent,
            },
            'quality': {
                'min_overall_score': self._pipeline.guardrails.quality.min_overall_score,
                'auto_reject_threshold': self._pipeline.guardrails.quality.auto_reject_threshold,
            },
        }

    def save(self, config_path: Path) -> None:
        """Save configuration to JSON file."""
        with open(config_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
