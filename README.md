# Content Factory v2

A production-grade agentic content system built on David Deutsch's epistemological framework — creating explanatory content through systematic error elimination rather than single-shot generation.

---

## Core Pipeline

```mermaid
flowchart TD
    INPUT(["📝 Topic Brief"])

    subgraph PHASE1["Phase 1 — Research"]
        R1["🔍 Prompt Generator\nAnalyses topic domain,\ndepth & controversy level"]
        R2["🌐 Gemini CLI\nLive web search +\nmulti-modal sources"]
        R3[("research.md")]
        R1 --> R2 --> R3
    end

    subgraph PHASE2["Phase 2 — Analysis"]
        A1["🧠 Analyzer Agent\nApplies Deutsch's 5-test\nepistemological framework"]
        A2{"Validator"}
        A3[("analysis.md")]
        A1 --> A2
        A2 -->|"Pass"| A3
        A2 -->|"Fail"| A1
    end

    subgraph PHASE3["Phase 3 — Writing"]
        W1["✍️ Writer Agent\nTranslates analysis into\naccessible prose per format"]
        W2{"Validator"}
        W3[("drafts/")]
        W1 --> W2
        W2 -->|"Pass"| W3
        W2 -->|"Fail"| W1
    end

    subgraph PHASE4["Phase 4 — Editing"]
        E1["✂️ Editor Agent\nFact-check, logic,\nstyle & quality gates"]
        E2{"Validator\n≥ 9.5 / 10"}
        E3[("final/")]
        E1 --> E2
        E2 -->|"Pass"| E3
        E2 -->|"Fail"| E1
    end

    OUTPUT(["🚀 Published Content\nArticle · Thread · LinkedIn\nNewsletter · YouTube · Podcast"])

    INPUT --> PHASE1
    PHASE1 --> PHASE2
    PHASE2 --> PHASE3
    PHASE3 --> PHASE4
    PHASE4 --> OUTPUT
```

---

## Why Sequential, Not Parallel?

Each agent is a **specialised error-detection system** that can only do its job once the previous phase is complete. Error correction requires criticism, and criticism requires completed work to criticise.

| Agent | Error Type Caught | Requires |
|---|---|---|
| Researcher | Ignorance, selection bias, missing perspectives | Topic brief |
| Analyzer | Bad explanations, arbitrary claims, unfalsifiable theories | Complete research |
| Writer | Structural failures, inaccessible prose, format mismatch | Validated analysis |
| Editor | Factual errors, logic gaps, quality below threshold | Full draft |

---

## Orchestrator State Machine

```mermaid
stateDiagram-v2
    [*] --> IDLE
    IDLE --> INITIALIZING : START
    INITIALIZING --> RESEARCHING : init complete

    RESEARCHING --> ANALYZING : phase complete
    RESEARCHING --> RESEARCHING : retry (backoff)
    RESEARCHING --> FAILED : max retries exceeded

    ANALYZING --> WRITING : phase complete
    ANALYZING --> ANALYZING : retry (backoff)
    ANALYZING --> FAILED : max retries exceeded

    WRITING --> EDITING : phase complete
    WRITING --> WRITING : retry (backoff)
    WRITING --> FAILED : max retries exceeded

    EDITING --> AWAITING_USER : score < 9.5
    EDITING --> PUBLISHING : score ≥ 9.5
    EDITING --> EDITING : retry (backoff)
    EDITING --> FAILED : max retries exceeded

    AWAITING_USER --> EDITING : USER_REJECT
    AWAITING_USER --> PUBLISHING : USER_APPROVE

    PUBLISHING --> COMPLETED : published
    FAILED --> INITIALIZING : resume from checkpoint
    COMPLETED --> [*]
```

---

## v2.3 Research Phase — Gemini CLI Integration

```mermaid
flowchart LR
    BRIEF["Topic Brief"]

    subgraph PROMPTGEN["Dynamic Prompt Generator"]
        direction TB
        PG1["Classify domain\ntechnical · philosophical\npractical · scientific"]
        PG2["Assess depth\nsurface · intermediate · deep"]
        PG3["Flag controversy\nsettled · debated · polarized"]
        PG4["Set temporal sensitivity\ntimeless · evolving · breaking"]
        PG1 --> PG2 --> PG3 --> PG4
    end

    subgraph GEMINI["Gemini CLI — Research Agent"]
        direction TB
        G1["Live web search\n+ knowledge graph"]
        G2["Multi-modal sources\nPDFs · images · video"]
        G3["Academic + industry\n+ primary sources"]
        G1 & G2 & G3
    end

    subgraph VALIDATION["Research Validator"]
        V1{"Source diversity\ncheck"}
        V2{"Steelman\nrequirement"}
        V3{"Evidence\nhygiene"}
    end

    OUT[("research.md\nComprehensive · Cited\nConflicts documented")]

    BRIEF --> PROMPTGEN --> GEMINI --> VALIDATION
    VALIDATION -->|"All pass"| OUT
    VALIDATION -->|"Fail"| GEMINI
```

---

## Phase 4.5 — CODEX Brutal Critic Agent

The CODEX Brutal Critic Agent is the **final gatekeeper before publication**. It sits between Editor approval and the publication step, powered by OpenAI's `codex` CLI running in headless mode. Its single purpose: find what the Editor missed and refuse to let anything mediocre through.

```mermaid
flowchart TD
    EDITOR_PASS["✂️ Editor Agent\nApproves at ≥ 9.3/10"]

    subgraph CODEX_PHASE["Phase 4.5 — CODEX Brutal Critic"]
        CB1["Execute codex CLI\nin headless mode"]

        subgraph DIMENSIONS["7 Evaluation Dimensions"]
            D1["Argument Strength · 20%"]
            D2["Factual Precision · 15%"]
            D3["Logical Structure · 15%"]
            D4["Counterargument Depth · 15%"]
            D5["Practical Value · 15%"]
            D6["Original Insight · 10%"]
            D7["Prose Quality · 10%"]
        end

        CB2["Hostile stress-test\nevery claim"]
        CB3{"CODEX Score\n≥ 9.5 / 10?"}
        FEEDBACK[("codex-feedback.md\nJSON + ranked issues\n+ path to 9.5")]
    end

    PUBLISH(["🚀 Final Publication"])
    REVISE["↩ Return to Writer\nwith specific fixes"]
    ESCALATE["⚠️ Escalate to Human\nafter 3 failed iterations"]

    EDITOR_PASS --> CB1
    DIMENSIONS --> CB2 --> CB3
    CB1 --> DIMENSIONS
    CB3 -->|"APPROVE ≥ 9.5"| FEEDBACK --> PUBLISH
    CB3 -->|"REJECT < 9.5 · Iter 1-2"| REVISE
    CB3 -->|"REJECT < 9.5 · Iter 3"| ESCALATE
```

### Why a second quality gate?

The Editor approves at **9.3** — excellent, publishable. The CODEX Critic requires **9.5** — world-class, survives hostile review. The gap between the two is where real excellence lives. The Editor catches surface issues (structure, tone, engagement); the CODEX Critic runs a forensic evaluation that an expert hostile to the piece would run.

| Check | What it finds |
|---|---|
| Claim stress-test | What a hostile expert would immediately attack |
| Counterexample search | Generalisations that break under real cases |
| Evidence sufficiency | Strong claims without proportionate support |
| Alternative explanations | Whether objections are genuinely considered or performative |
| Hard-to-vary test | Whether the explanation would survive detail changes |
| Falsifiability | Whether there exists any evidence that could prove it wrong |
| Originality test | Whether the insight is genuinely new or rearranged familiarity |

### Iteration mechanics

The agent runs up to **3 CODEX evaluation loops**. Each rejected iteration returns specific, ranked fixes to the Writer. After 3 failures, the system escalates to a human with options: revise further, return to an earlier phase, or abandon the piece. There is no automatic approval below 9.5 — no exceptions.

---

## Repo Structure

```
content-factory/
├── agents/                  # Agent prompt definitions (v1 + v2)
│   ├── researcher-agent-v2.md
│   ├── analyzer-agent-v2.md
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
│   ├── tools/               # Ablation, analysis, dashboard
│   └── validators/          # Per-agent output validators
├── shared/deutsch-framework/ # Epistemological foundation
├── tests/                   # Unit + integration test suite
├── CONTENT-FACTORY-v2.3-DESIGN.md
├── HOW-THE-WORKFLOW-WORKS.md
├── EXECUTION_CHECKLIST.md
└── run-content-factory.md
```

---

## Installation & Quick Start

```bash
pip install -e ".[dev]"
```

```bash
# Run the full pipeline
content-factory run "Why goal-setting fails" \
    --formats article,twitter-thread,linkedin-post \
    --brief "Analyse why most goal-setting frameworks fail"

# Validate outputs
content-factory validate "why-goal-setting-fails"

# Open monitoring dashboard
content-factory dashboard --view full
```

---

## Supported Output Formats

| Format | Template | Agent |
|---|---|---|
| Long-form article | `article-template.md` | Writer → Editor |
| Twitter/X thread | `twitter-thread-template-v2.md` | Thread Agent → Editor |
| LinkedIn post | `linkedin-post-template.md` | Writer → Editor |
| Newsletter section | `newsletter-template.md` | Writer → Editor |
| YouTube script | `youtube-script-template.md` | Writer → Editor |
| Podcast notes | `podcast-notes-template.md` | Writer → Editor |

---

## Key Docs

| Doc | What it covers |
|---|---|
| `HOW-THE-WORKFLOW-WORKS.md` | Why the pipeline is designed this way |
| `CONTENT-FACTORY-v2.3-DESIGN.md` | v2.3 architecture with Gemini CLI research and Codex brutal Critic agent|
| `EXTERNAL-REVIEW-LESSONS.md` | What broke in external review & how the system was upgraded |
| `AGENTS.md` | Orchestration instructions for Claude |
| `GEMINI.md` | Orchestration instructions for Gemini |
| `agents/codex-brutal-critic-agent.md` | CODEX Brutal Critic — Phase 4.5 final gatekeeper |
