# Content Factory v3.0 - World-Class Agentic Content System

A production-grade implementation of David Deutsch's epistemological framework for creating explanatory content through systematic error elimination.

## What's New in v3.0

### Phase 1: Instrumentation ✅
- **Output validators** for each agent with comprehensive checks
- **Structured JSON logging** with full telemetry
- **Test framework** with unit and integration tests
- **Metrics collection** (timing, tokens, quality scores, error types)

### Phase 2: Empirical Validation ✅
- **Ablation study framework** for testing architectural decisions
- **Quality analyzer** for historical trend detection
- **Cross-topic comparison** tools
- **Dimension breakdown analysis**

### Phase 3: Production Engineering ✅
- **State machine orchestrator** with explicit transitions
- **Checkpointing and recovery** for fault tolerance
- **Guardrails** (budget, time, quality thresholds)
- **CLI dashboard** for monitoring

## Installation

```bash
cd content-factory
pip install -e ".[dev]"
```

## Quick Start

### Run the Pipeline
```bash
# Full pipeline for a topic
content-factory run "Why goal-setting fails" \
    --formats article,twitter-thread,linkedin-post \
    --brief "Analyze why most goal-setting frameworks fail to produce results"

# Validate outputs
content-factory validate "why-goal-setting-fails"

# Show dashboard
content-factory dashboard --view full
```

### Python API
```python
from content_factory import ContentFactoryOrchestrator, Config
from content_factory.config import PipelineConfig, OutputFormat

# Create orchestrator
config = PipelineConfig(base_dir=Path("."))
orchestrator = ContentFactoryOrchestrator(config=config)

# Run pipeline
result = orchestrator.run(
    topic="Why goal-setting fails",
    brief="# Goal Setting Analysis\n\nAnalyze why frameworks fail.",
    formats=[OutputFormat.ARTICLE, OutputFormat.TWITTER_THREAD]
)

print(f"Success: {result.success}")
print(f"Score: {result.final_score}")
print(f"Decision: {result.decision}")
```

### Validate Outputs
```python
from content_factory.validators import ResearchValidator, EditorValidator

# Validate research output
validator = ResearchValidator(min_explanations=3, max_explanations=7)
result = validator.validate_file(Path("outputs/topic/research.md"))

print(f"Valid: {result.valid}")
print(f"Errors: {result.error_count}")
print(f"Metrics: {result.metrics}")
```

### Run Ablation Study
```python
from content_factory.tools import AblationStudy, AblationConfig
from content_factory.config import PipelineConfig

config = AblationConfig(
    name="architecture_test",
    description="Testing 4-agent sequential architecture",
    base_config=PipelineConfig(),
    topics=["topic-1", "topic-2", "topic-3"],
    runs_per_variant=3,
)

study = AblationStudy(config)
study.add_all_standard_ablations()

results = study.run()
analysis = study.analyze()
print(analysis.get_full_report())
```

## Architecture

### State Machine
```
IDLE → INITIALIZING → RESEARCHING → ANALYZING → WRITING → EDITING → PUBLISHING → COMPLETED
                           ↑            ↑           ↑          ↑
                           └── RETRY ───┴── RETRY ──┴── RETRY ─┘
                                                        ↓
                                               AWAITING_USER → FAILED
```

### Validators
Each agent output is validated before proceeding:

| Phase | Validator | Key Checks |
|-------|-----------|------------|
| Research | `ResearchValidator` | 3-7 explanations, steelman test, evidence both sides |
| Analysis | `AnalysisValidator` | All 5 Deutsch tests applied, ranking, good explanation |
| Writing | `WriterValidator` | Counterarguments, practical utility, tone check |
| Editing | `EditorValidator` | All 7 dimensions scored, decision matches score |

### Quality Scoring (7 Dimensions)
| Dimension | Weight | Minimum |
|-----------|--------|---------|
| Philosophical Accuracy | 15% | 9.0 |
| Factual Accuracy | 10% | 9.0 |
| Logical Soundness | 15% | 9.0 |
| Clarity & Accessibility | 15% | 9.0 |
| Engagement & Writing | 15% | 9.0 |
| **Practical Utility** | **20%** | 9.0 |
| Intellectual Honesty | 10% | 9.0 |

**Minimum to Publish: 9.3/10**

### Guardrails
- **Token budget**: 100K per agent, 500K per pipeline
- **Time limits**: 10 min per agent, 1 hour per pipeline
- **Retry limits**: 2 per agent, 5 total
- **Quality floor**: Auto-reject below 8.0

## CLI Commands

```bash
# Run pipeline
content-factory run <topic> [--formats <formats>] [--brief <file>]

# Validate outputs
content-factory validate <topic> [--phase <phase>]

# Show dashboard
content-factory dashboard [--view status|quality|history|full]

# Analyze quality
content-factory analyze [--report]

# Run ablation study
content-factory ablation [--standard] [--topics <file>]

# Show status
content-factory status
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=content_factory

# Run specific test file
pytest tests/unit/test_validators.py -v
```

## Directory Structure

```
content-factory/
├── src/content_factory/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── config.py           # Configuration
│   ├── orchestrator.py     # State machine orchestrator
│   ├── telemetry.py        # Logging and metrics
│   ├── validators/         # Output validators
│   │   ├── base.py
│   │   ├── research_validator.py
│   │   ├── analysis_validator.py
│   │   ├── writer_validator.py
│   │   └── editor_validator.py
│   └── tools/              # Analysis tools
│       ├── ablation.py     # Ablation studies
│       ├── analysis.py     # Quality analysis
│       └── dashboard.py    # CLI dashboard
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── agents/                 # Agent instructions (v1 & v2)
├── templates/              # Output format templates
├── inputs/                 # Topic briefs
├── outputs/                # Generated content
└── pyproject.toml
```

## Key Improvements Over v2.0

| Aspect | v2.0 | v3.0 |
|--------|------|------|
| Validation | Manual inspection | Automated validators |
| Orchestration | Markdown instructions | Python state machine |
| Error handling | Manual retry | Automatic with backoff |
| Telemetry | None | Full structured logging |
| Testing | None | Unit + integration tests |
| Guardrails | Manual enforcement | Automatic limits |
| Recovery | Start over | Checkpoint resume |
| Analysis | Manual review | Quality analyzer + trends |

## Philosophy

This system embodies David Deutsch's epistemological principles:

1. **Good explanations are hard-to-vary** - The architecture is constrained by dependencies
2. **Knowledge grows through conjecture & criticism** - Sequential agents criticize each other's work
3. **Problems are inevitable AND soluble** - Error handling with automatic retry
4. **Quality comes from error elimination** - Multiple validation layers

## License

MIT
