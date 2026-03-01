# codex-CF

A from-scratch redesign of Content Factory optimized for **knowledge creation**, not just content production.

## Core Idea

`codex-CF` treats explanations as first-class objects and runs them through hostile criticism before anything is publishable.

Pipeline:

1. `Knowledge Rail`
- Ingest competing internet explanations.
- Apply Deutsch-style tests: Hard-to-Vary, Mechanism, Reach, Rejectability, Integration.
- Run variation attacks and evidence hygiene checks.
- If all candidates fail, synthesize a stronger conjecture.

2. `Publication Rail`
- Only package explanations that pass epistemic thresholds.
- Emit publish-ready reasoning artifacts with falsifiers and "what would change my mind" triggers.

## Project Structure

- `src/codex_cf/models.py`: explanation and evaluation datamodels
- `src/codex_cf/scoring.py`: epistemic scoring engine
- `src/codex_cf/pipeline.py`: knowledge rail + publication rail orchestrator
- `src/codex_cf/cli.py`: CLI
- `examples/input_topic.json`: sample run input
- `tests/`: unit tests for scoring and synthesis behavior

## Quick Start

```bash
cd codex-CF
python -m pip install -e .

# Run knowledge + publication rails
codex-cf run --input examples/input_topic.json --out runs/demo

# Or run stages separately
codex-cf knowledge --input examples/input_topic.json --out runs/demo
codex-cf publish --knowledge runs/demo/knowledge_result.json --out runs/demo
```

## Output Artifacts

- `knowledge_result.json`
- `knowledge_report.md`
- `publication_package.md`

## Quality Gate

Default publication gate is epistemic score `>= 8.0` plus no critical test below `6.5`.

## Design Notes

See `docs/ARCHITECTURE.md` for formal design and scoring details.
