# Content Factory v2

A production-grade agentic content system built on David Deutsch's epistemological framework — creating explanatory content through systematic error elimination.

## How It Works

Instead of single-shot AI generation, Content Factory runs a **sequential multi-agent pipeline** where each agent specialises in catching a specific class of errors the previous agent can't see:

1. **Researcher Agent** — Gathers competing explanations, evidence, and source material
2. **Analyzer Agent** — Criticises explanations using Deutsch's hard-to-vary framework
3. **Writer Agent** — Translates analysis into accessible, well-structured prose
4. **Editor Agent** — Catches residual errors, enforces quality standards, and formats for each platform

The result is content that has survived multiple rounds of systematic criticism — not just one AI pass.

## Repo Structure

```
content-factory/
├── agents/                  # Agent prompt definitions (v1 + v2)
│   ├── analyzer-agent-v2.md
│   ├── researcher-agent-v2.md
│   ├── writer-agent-v2.md
│   ├── editor-agent-v2.md
│   ├── twitter-thread-agent-v2.md
│   └── ...
├── templates/               # Output templates per format
│   ├── article-template.md
│   ├── twitter-thread-template-v2.md
│   ├── linkedin-post-template.md
│   └── ...
├── src/content_factory/     # Core Python package
│   ├── orchestrator.py      # State-machine pipeline runner
│   ├── config.py            # Pipeline configuration
│   ├── cli.py               # CLI interface
│   ├── telemetry.py         # Structured logging & metrics
│   ├── tools/               # Ablation, analysis, dashboard tools
│   └── validators/          # Per-agent output validators
├── shared/deutsch-framework/ # Epistemological foundation docs
├── deutsch-framework/       # Conjecture & criticism methods
├── tests/                   # Unit + integration test suite
├── CONTENT-FACTORY-v2.3-DESIGN.md   # Architecture spec
├── PARALLEL-ARCHITECTURE-v4.md      # Parallel pipeline design
├── HOW-THE-WORKFLOW-WORKS.md        # Full workflow explainer
├── EXECUTION_CHECKLIST.md           # Run checklist
├── EXTERNAL-REVIEW-LESSONS.md       # System improvement learnings
└── run-content-factory.md           # Quick-start guide
```

## Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

```bash
# Run the full pipeline for a topic
content-factory run "Why goal-setting fails" \
    --formats article,twitter-thread,linkedin-post \
    --brief "Analyse why most goal-setting frameworks fail to produce results"

# Validate pipeline outputs
content-factory validate "why-goal-setting-fails"

# Open the monitoring dashboard
content-factory dashboard --view full
```

## Supported Output Formats

- Long-form article
- Twitter/X thread
- LinkedIn post
- Newsletter section
- YouTube script
- Podcast notes

## Design Principles

- **Conjecture → Criticism → Error Elimination** — each agent is a specialised error-detection system
- **Sequential, not parallel** — order matters; later agents build on validated output from earlier ones
- **Validators on every stage** — structured checks prevent bad output from propagating downstream
- **Full telemetry** — timing, token counts, quality scores, and error types logged per run
- **Fault-tolerant** — checkpointing and recovery so long runs can resume after failure

## Key Docs

| Doc | Purpose |
|-----|---------|
| `HOW-THE-WORKFLOW-WORKS.md` | Why the pipeline is designed this way |
| `CONTENT-FACTORY-v2.3-DESIGN.md` | Architecture and agent specs |
| `EXTERNAL-REVIEW-LESSONS.md` | What broke in external review and how the system was upgraded to v2.1 |
| `AGENTS.md` | Agent orchestration instructions for Claude |
| `GEMINI.md` | Agent orchestration instructions for Gemini |
