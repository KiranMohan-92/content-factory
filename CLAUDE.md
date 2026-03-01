# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**David Deutsch Content Factory** - A systematic content production system that applies David Deutsch's epistemological framework (from *The Beginning of Infinity*) to analyze problems and create high-quality explanatory content.

**Core Principle**: Good explanations are hard-to-vary, mechanistic, and have reach. This system uses a sequential 5-agent workflow to identify, analyze, and communicate good explanations while systematically eliminating errors.

**SYSTEM VERSION: 2.2** (CODEX Brutal Critic Integration)
- **v2.0**: Automated orchestrator, hard-to-vary agents, error handling
- **v2.1**: External Review pre-pass - addresses 2.9-point internal/external scoring gap
- **v2.2**: **NEW CODEX Brutal Critic agent** - uses OpenAI `codex` CLI for final quality gate
- **NEW**: 9.5/10 minimum score (raised from 9.3)
- **NEW**: Dual-gate quality control (Editor 9.3 → CODEX 9.5)
- **NEW**: Maximum 3 CODEX revision iterations before escalation
- **KEPT**: All v2.1 features (external verification, agents, logging)
- **KEPT**: Manual workflow option

---

## Architecture

### Sequential Agent Workflow

The system uses **5 specialized agents in strict sequence**. Each agent criticizes and improves upon previous work:

```
Research → Analysis → Writing → Editing → CODEX Brutal Critic → Publication
```

**Why Sequential?** Each phase depends on the previous phase's output. This enables cumulative error correction through specialized criticism - the core mechanism for quality.

**Critical Rule**: Never skip phases or combine agents. The sequential structure is not arbitrary; it's constrained by dependencies.

### Agent Responsibilities

1. **Researcher Agent** (`/agents/researcher-agent.md`)
   - Maps landscape of competing explanations (5-7 major views)
   - Gathers evidence for/against each
   - Identifies gaps, contradictions, patterns
   - **Output**: `research.md` with fair representation of all views

2. **Analyzer Agent** (`/agents/analyzer-agent.md`)
   - Applies 5 Deutsch tests to each explanation:
     - Hard-to-Vary Test
     - Mechanism Test
     - Reach Test
     - Rejectability Test
     - Integration Test
   - Identifies or creates "good explanation"
   - **Output**: `analysis.md` with systematic evaluation and insights

3. **Writer Agent** (`/agents/writer-agent-v2.md`)
   - **FIRST**: Checks `/CONTENT-CONTEXT.md` for previously explained concepts
   - **Asks user** whether to repeat, reference, or skip previously explained concepts
   - Translates analysis into accessible content with **substantial counterarguments**
   - Creates drafts for multiple formats (article, thread, post, etc.)
   - Maintains philosophical rigor while optimizing for engagement
   - Uses **exploratory, non-preachy tone** (questions, not lectures)
   - **Output**: Format-specific draft files (`article.md`, `twitter-thread.md`, etc.)

4. **Editor Agent** (`/agents/editor-agent-v2.md`)
   - **PRELIMINARY QUALITY GATE**: Minimum score 9.3/10 to qualify for CODEX review
   - **7-pass deep review** (see `/agents/scoring-rubric.md`):
     - Philosophical accuracy (+ checks for repetition via CONTENT-CONTEXT.md)
     - Factual accuracy
     - Logical coherence (+ **verifies 2-3 strong counterarguments included**)
     - Clarity
     - Engagement
     - Format & style (+ **tone check: rejects preachy content**)
     - **Practical utility (20% of score)** - specific examples, actionable steps, immediate applicability
   - **Ruthlessly critical**: Be harsh, not encouraging; enforce excellence, not "good enough"
   - **Authority**: REJECT anything <9.3/10, demand multiple revisions, send back to Analysis if needed
   - **WILL REJECT** if: score <9.3, preachy tone, insufficient counterarguments, vague advice, or unnecessary repetition
   - **Output**: `editor-feedback.md` with numerical scores
   - **Forward**: Content scoring ≥9.3 proceeds to CODEX Brutal Critic

5. **CODEX Brutal Critic Agent** (`/agents/codex-brutal-critic-agent.md`) - **NEW in v2.2**
   - **FINAL QUALITY GATE**: Minimum score 9.5/10 for true world-class publication
   - **Executes OpenAI `codex` CLI** in headless mode for external hostile review
   - **7-dimension CODEX evaluation**:
     - Argument Strength (20%): Survives hostile stress-testing
     - Factual Precision (15%): Every claim verifiable, no overreach
     - Logical Structure (15%): No gaps, valid inference chain
     - Original Insight (10%): Says something genuinely new
     - Prose Quality (10%): Precise, clear, elegant
     - Counterargument Depth (15%): Genuine steelmanning
     - Practical Value (15%): Reader can act immediately
   - **Hostile cross-examination**: Claim stress-test, counterexample search, evidence forensics
   - **Brutal standards**: Top 0.01% quality, finds issues Editor missed
   - **Iteration loop**: Maximum 3 revision attempts to reach 9.5
   - **Authority**: REJECT anything <9.5, no exceptions
   - **Output**: `codex-feedback.md` with CODEX scores and specific fixes
   - **Decision**: APPROVE (≥9.5) → Publication, REJECT (<9.5) → Revision loop

---

## Directory Structure

```
/content-factory/
├── CLAUDE.md                          # This file - start here
├── CONTENT-CONTEXT.md                 # Track explained concepts across topics (CHECK BEFORE WRITING)
├── HOW-THE-WORKFLOW-WORKS.md          # Deep explanation of the workflow
├── run-content-factory.md             # NEW: Orchestrator for automated workflow
│
├── deutsch-framework/                 # Epistemological framework reference
│   ├── epistemology.md               # Core principles
│   ├── explanations.md               # Good vs bad explanations
│   ├── problem-solving.md            # Problems inevitable/soluble
│   └── examples.md                   # Concrete applications
│
├── agents/                            # Agent instructions (read before invoking)
│   ├── researcher-agent-v2.md        # Hard-to-vary researcher (automated)
│   ├── analyzer-agent-v2.md          # Hard-to-vary analyzer (automated)
│   ├── writer-agent-v2.md            # Hard-to-vary writer (automated)
│   ├── editor-agent-v2.md            # Hard-to-vary editor (automated)
│   ├── codex-brutal-critic-agent.md  # NEW v2.2: CODEX CLI brutal critic (final gatekeeper)
│   ├── researcher-agent.md           # V1: Manual invocation (deprecated but available)
│   ├── analyzer-agent.md             # V1: Manual invocation (deprecated but available)
│   ├── writer-agent.md               # V1: Manual invocation (deprecated but available)
│   ├── editor-agent.md               # V1: Manual invocation (deprecated but available)
│   └── scoring-rubric.md             # World-class scoring system (9.5+ to publish via CODEX)
│
├── templates/                         # Output format templates
│   ├── article-template.md
│   ├── twitter-thread-template.md
│   ├── linkedin-post-template.md
│   ├── newsletter-template.md
│   ├── youtube-script-template.md
│   └── podcast-notes-template.md
│
├── inputs/                            # User briefs (create one per topic)
│   └── [topic-name].md
│
└── outputs/                           # Generated content
    └── [topic-name]/
        ├── research.md                # Phase 1 output
        ├── analysis.md                # Phase 2 output
        ├── drafts/                    # Phase 3 output
        │   ├── article.md
        │   ├── twitter-thread.md
        │   └── linkedin-post.md
        ├── editor-feedback.md         # Phase 4 output
        ├── codex-feedback.md          # NEW v2.2: Phase 4.5 CODEX output
        ├── execution-log.md           # Orchestrator tracking (automated mode)
        └── final/                     # Publication-ready content (Phase 5 - after CODEX ≥9.5)
            └── [all approved formats]
```

---

## Critical System Lesson: External Review Gap (February 2026)

### The Problem

**Internal Review Score**: 9.4/10 (Editor Agent v2.1)
**External Review Score**: 6.5/10 (Independent fact-check)
**Gap**: 2.9 points

The internal review process systematically **over-scored content** by missing critical factual errors that external reviewers caught immediately.

### What Internal Review Missed

**Checked** (correctly):
- ✓ Traceability to analysis (all claims traced to research)
- ✓ Tone (exploratory, not preachy)
- ✓ Practical utility (specific examples, actionable)
- ✓ Counterarguments (2-3 substantial objections)
- ✓ Structure and flow

**Missed** (critical gaps):
- ✗ **Founder attribution**: Said "Peter Steinberger" → Actually Matt Schlicht
- ✗ **Specific numbers**: "150,000 in 48 hours", "43 prophets" → Not verifiable from sources
- ✗ **Absolute claims**: "without human programming" → Technically wrong
- ✗ **Testability**: Core explanation not falsifiable
- ✗ **Overconfident timelines**: "6-24 months" without mechanism

### Root Cause Analysis

**Internal review assumes**: If it traces to analysis and follows framework, it's accurate.
**External review verifies**: Are the actual FACTS correct?

The Researcher documented what sources said, but:
1. **No primary source verification** - Did we actually check Wikipedia/Reuters?
2. **No paywall access** - Forbes sources were paywalled, couldn't verify
3. **No number validation** - Precise numbers treated as facts without verification
4. **No claim-strength audit** - Absolute language not tested against reality

### System Improvements (v2.1 → v2.2)

#### v2.1: External Fact-Check Pre-Pass (MANDATORY)

**Before any content scores ≥9.3, must verify:**

1. **Named Entities**
   - [ ] People's names match primary sources (Wikipedia, official bios)
   - [ ] Organization names correct
   - [ ] Dates/timeline verifiable

2. **Numerical Claims**
   - [ ] Specific numbers (X, 48 hours) have non-paywalled sources
   - [ ] If paywalled: Use ranges ("tens to hundreds of thousands")
   - [ ] If sources vary: Report range, not precise middle

3. **Absolute Language**
   - [ ] "Never/will always/definitely" → Rigorously defend OR soften
   - [ ] "Without any X" → Usually false; hedge as "minimal" or "claimed"

4. **Source Verification**
   - [ ] Actually open and read cited sources
   - [ ] Verify characterization matches what source actually says
   - [ ] If can't verify: Either remove claim OR soften to "reported as"

#### v2.2: CODEX Brutal Critic Agent (NEW)

**After Editor approves (≥9.3), CODEX Brutal Critic must approve (≥9.5):**

**Installation**:
```bash
npm install -g @openai/codex
codex configure
```

**Evaluation**:
- Executes OpenAI `codex` CLI in headless mode
- Applies hostile cross-examination framework
- Tests all claims for counterexamples
- Verifies evidence forensically
- Steelmans counterarguments
- Checks falsifiability
- Returns JSON output with scores and specific fixes

**Quality Gates**:
- Editor: 9.3/10 minimum (qualifies for CODEX review)
- CODEX: 9.5/10 minimum (required for publication)

**Iteration**:
- Maximum 3 CODEX revision attempts
- Each iteration re-runs `codex` CLI on revised content
- After 3 failures: Escalate to human

#### NEW: External Review Standards (v2.2)

**Before publication, content must survive:**

| Check | Internal | External |
|-------|----------|----------|
| Framework application | ✓ | - |
| Tone and clarity | ✓ | - |
| Practical utility | ✓ | ✓ |
| **Factual accuracy** | Partial check | **Full verification** |
| **Named entities** | Assumed correct | **Verified against sources** |
| **Specific numbers** | Not validated | **Source-checked OR converted to ranges** |

### Implementation

**For Orchestrator (run-content-factory.md)**:
- Add external verification phase before Phase 5 (Publication)
- All named entities must be verified against primary sources
- All numerical claims must have non-paywalled sources OR use ranges
- All absolute language must pass "rigorous defense OR soften" test

**For Editor Agent (editor-agent-v2.md)**:
- Add "External Verification" pass before 7-pass review
- Flag any content that fails verification
- Return to Writer with specific fixes

### Lessons Documented in CONTENT-CONTEXT.md

See "Systems Thinking Deep Explanation" section for the original lesson that prompted v2.1 hostile cross-examination pre-pass.

**Key Insight**: Internal review checks surface features (structure, tone, flow). External review tests claims against reality. Both are needed.

---

## Common Commands

### Two Workflow Options

**NEW: Automated Orchestrator** (Recommended for most topics)
- Fully automated pipeline
- Spawns agents sequentially
- Enforces quality gates automatically
- One command runs entire workflow

**Classic: Manual Invocation** (For fine control or special cases)
- Step-by-step agent invocation
- Review each phase before proceeding
- More control but more manual work

---

### Option A: Automated Workflow (Recommended)

**One-command execution using the orchestrator:**

```
Read the orchestrator instructions:
/run-content-factory.md

Then provide your content brief:

"Topic: [Your topic/problem]
Audience: [Target audience]
Formats: [article, thread, post, etc.]
Requirements: [Any specific needs]"

The orchestrator will:
1. Create brief and directory structure
2. Spawn Researcher agent → research.md
3. Spawn Analyzer agent → analysis.md
4. Check CONTENT-CONTEXT and ask about repetition
5. Spawn Writer agent(s) → drafts for each format
6. Spawn Editor agent → score and approve/reject
7. If ≥9.3: Publish to /final/ and update context
8. If <9.3: Auto-retry once, then ask for intervention
```

**Example**:

```
Read: /run-content-factory.md

Then:

"Topic: Why most productivity advice fails
Audience: Ambitious professionals juggling multiple priorities
Formats: Article (2500 words), Twitter thread, LinkedIn post
Requirements: Apply hard-to-vary test to show popular frameworks are arbitrary. Include specific workplace examples."
```

**The orchestrator handles everything** - spawning agents, managing handoffs, enforcing quality gates, tracking execution.

**Output**: Complete content in `/outputs/[topic]/final/` or specific feedback if revision needed.

---

### Option B: Manual Workflow (Step-by-Step)

**For fine control or when you want to review each phase:**

1. **Create input brief** at `/inputs/[topic-name].md`:

```markdown
# Content Brief: [Topic]

## Problem/Topic
[Specific issue to analyze - be concrete]

## Target Audience
- Primary: [Who needs this most]
- Knowledge level: [What can we assume they know]

## Output Formats Requested
- [ ] Long-form article (2000-3000 words)
- [ ] Twitter/X thread (8-12 tweets)
- [ ] LinkedIn post (300-500 words)
- [ ] Email newsletter
- [ ] YouTube script
- [ ] Podcast talking points

## Deutschian Angle
[Which framework concepts to emphasize]

## Specific Goals
[What should readers be able to do after consuming this?]
```

2. **Run the workflow manually**:

```
# Phase 1: Research
Read: /agents/researcher-agent-v2.md (or v1 if preferred)
Invoke Researcher with input brief
Review output: /outputs/[topic]/research.md

# Phase 2: Analysis
Read: /agents/analyzer-agent-v2.md
Invoke Analyzer with research.md
Review output: /outputs/[topic]/analysis.md

# Phase 3: Writing
FIRST: Writer checks /CONTENT-CONTEXT.md for previously explained concepts
THEN: Writer asks user about repeating vs referencing those concepts
Read: /agents/writer-agent-v2.md
Invoke Writer with analysis.md + requested formats
Writer includes 2-3 strong counterarguments and uses exploratory tone
Review output: /outputs/[topic]/drafts/[format].md

# Phase 4: Editing
Read: /agents/editor-agent-v2.md
Invoke Editor with all drafts
Review output: /outputs/[topic]/editor-feedback.md or /final/

# Phase 5: Iterate if needed
If Editor requests revisions, make changes and re-submit
```

**Example Manual Invocation**:

```
"I want to analyze: 'Why most productivity advice fails'

Target: Ambitious professionals
Formats: Article (2000 words) + Twitter thread + LinkedIn post
Angle: Apply hard-to-vary test to show popular frameworks are arbitrary

Let's start with research phase. Researcher agent, please:
1. Find 5-7 popular productivity frameworks
2. Document core claims and evidence for each
3. Identify where they conflict and common failure modes
4. Create research.md"
```

---

## Key Principles for Working in This System

### David Deutsch's Framework (Quick Reference)

1. **Good explanations are hard to vary** - Can't change details without losing explanatory power
2. **Knowledge grows through conjecture & criticism** - Not through observation or proof
3. **Problems are inevitable AND soluble** - Both matter equally
4. **Reach indicates truth** - Good explanations explain more than intended
5. **Objective truth exists but certainty doesn't** - We improve through error elimination

### Content Quality Requirements

**Every piece must demonstrate**:
- Clear problem statement
- 2+ competing explanations presented fairly
- Systematic Deutschian analysis (5 tests applied)
- Good explanation identified or created
- **2-3 strong counterarguments addressed substantially** (dedicated section or integrated)
- **Specific, actionable practical examples** (5-minute action, step-by-step workflow, 3-5 concrete examples, decision framework, self-check method)
- Intellectual honesty (limitations acknowledged, uncertainty expressed)
- **Exploratory, non-preachy tone** (questions not lectures)
- **Authentic conversational voice** (contractions, varied rhythm, personality through asides)
- **World-class quality score of 9.3+/10** (see scoring rubric)

**Never**:
- Claim certainty (only "survives criticism so far")
- Skip research phase (even on familiar topics)
- Combine agents or run in parallel (breaks error correction)
- Ignore Editor feedback (quality enforcement is essential)
- Strawman opposing views (steelman instead)
- **Use preachy/lecturing tone** (be exploratory and humble)
- **Write robotic, formal prose** (use contractions, vary rhythm, show personality)
- **Skip counterarguments** (minimum 2-3 substantial objections)
- **Repeat explanations unnecessarily** (check CONTENT-CONTEXT.md first, ask user)

### Process Rules

1. **Sequential workflow is mandatory** - Dependencies require this order
2. **Quality gates matter** - Each agent must meet standards before handoff
3. **Editor has final authority** - Can veto or require any previous phase restart
4. **Context preservation is critical** - Each agent builds on previous work
5. **Iteration improves output** - First draft is rarely best; accept revision requests
6. **No skipping phases** - Every phase catches specific error types

---

## Common Mistakes to Avoid

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Skipping Research | Bias, strawmanning, missing strong counterarguments | Always document landscape first |
| Rushing Analysis | Superficial content, no genuine insights | Apply 5 tests rigorously |
| Writing Before Analysis | Arbitrary claims, weak logic, no grounding | Complete analysis before drafting |
| Vague Practical Advice | Kills Practical Utility score (20% of total) | Specific steps, concrete examples, actionable in 24hrs |
| Accepting <9.3 Score | Publishing mediocrity instead of world-class | Demand revisions until ≥9.3, reject if unfixable |
| Skipping Editor | Blind spots, errors slip through, quality drift | Always run Editor with real authority |
| Combining Agents | Confirmation bias, no fresh perspective, no error correction | Keep agents separate and sequential |

---

## Philosophy Pitfalls to Avoid

- ❌ Claiming certainty → ✓ "Survives criticism so far"
- ❌ "Data proves theory" → ✓ "Evidence fails to refute conjecture"
- ❌ "Deutsch says so" → ✓ Show the reasoning
- ❌ All views equally valid → ✓ Some explanations objectively better
- ❌ Starting abstract → ✓ Begin with concrete problem
- ❌ Vague implications → ✓ Specific action items

---

## Quality Checklist

Before considering content complete, verify:

- [ ] Research documented 5-7 explanations fairly with evidence
- [ ] Analysis applied all 5 Deutsch tests systematically
- [ ] Good explanation is hard-to-vary with clear mechanism
- [ ] **2-3 strong counterarguments addressed substantially** (not just mentioned)
- [ ] Content accessible to target audience with concrete examples
- [ ] Limitations and counterarguments addressed honestly
- [ ] **Tone is exploratory, not preachy** (questions not lectures)
- [ ] **Practical utility: immediate action, workflow, 3-5 examples, framework, self-check**
- [ ] **NO vague advice** ("think about" → specific steps)
- [ ] **No unnecessary repetition** (checked CONTENT-CONTEXT.md, asked user)
- [ ] **Editor scored ≥9.3/10** (with breakdown by dimension) - qualifies for CODEX
- [ ] **CODEX scored ≥9.5/10** (via CLI execution) - required for publication
- [ ] All hostile objections from CODEX addressed or acknowledged

---

## For Continuing Work

**If returning to existing project**:

1. Check `/outputs/[topic]/` to see what's been completed
2. **Check `/outputs/[topic]/execution-log.md`** (if using orchestrator) to see exact status
3. **Check `/CONTENT-CONTEXT.md`** to see what's been explained in other pieces
4. Identify current phase (research/analysis/writing/editing)
5. Two options to continue:
   - **Automated**: Read `/run-content-factory.md` - orchestrator can resume from last phase
   - **Manual**: Read relevant agent instructions in `/agents/` and invoke next agent
6. Review previous phase output to understand context
7. Continue with next sequential phase

**If starting NEW project**:

**Recommended**: Use automated orchestrator
```
Read: /run-content-factory.md
Provide: Topic, Audience, Formats, Requirements
```

**Alternative**: Use manual workflow (see "Option B: Manual Workflow" above)

**If Editor requested revisions**:

1. Read `editor-feedback.md` carefully
2. Address specific issues identified (common: preachy tone, weak counterarguments, repetition)
3. Don't batch fixes - handle systematically
4. Re-submit to Editor for approval
5. Iterate until approved

**After publishing any piece**:

1. Update `/CONTENT-CONTEXT.md` with concepts explained
2. Add examples used
3. Note tone learnings
4. This prevents repetition in future pieces

---

## Success Metrics

**Content-level**:
- Editor score ≥9.3/10 (qualifies for CODEX review)
- **CODEX score ≥9.5/10** (required for publication - via CLI execution)
- Presents competing explanations fairly
- Identifies hard-to-vary explanation
- Makes testable claims
- **Provides specific, immediately actionable steps** (not vague advice)
- Acknowledges limitations with intellectual honesty
- Survives hostile cross-examination

**Reader-level**:
- Understands hard-to-vary test
- Can apply framework to other domains
- **Has taken specific action within 24 hours** (immediate first step)
- **Uses provided workflow/framework repeatedly**
- Wants to learn more and shares content

**System-level**:
- Consistent CODEX scores ≥9.5 across all published topics
- Reproducible world-class process
- Building library of proven practical examples
- Reader testimonials about usefulness
- **Internal/external scoring gap eliminated**

---

## Advanced Notes

### This System Is Itself a "Good Explanation"

The workflow demonstrates Deutsch's principles:
- **Hard to vary**: Change order → breaks dependencies; remove agents → specific errors go uncaught
- **Has mechanism**: Sequential specialized error correction
- **Has reach**: Pattern applies to any knowledge creation (software dev, scientific research, product development)
- **Testable**: Predicts skipping phases produces specific error types
- **Integrates**: Consistent with Popper, cognitive science, software engineering best practices

### Why Not Parallel?

Error correction requires criticism of completed work. Parallel structure breaks this:
- Agents can't critique each other
- Can't build on previous insights
- Errors don't get caught
- Knowledge accumulates rather than compounds

### Specialization Enables Quality

Each agent optimizes for specific error detection:
- Researcher → catches bias, ignorance, strawmanning
- Analyzer → catches bad explanations, arbitrary claims
- Writer → catches inaccessibility, format issues
- Editor → catches surface issues previous agents missed
- **CODEX Brutal Critic → catches deep issues via hostile CLI review** (v2.2)

Combined roles force tradeoffs. Specialized roles maximize error detection per dimension.

**v2.2 Dual-Gate Quality Control**:
1. **Editor (9.3 threshold)**: Catches surface issues—structure, tone, basic logic
2. **CODEX (9.5 threshold)**: Catches deep issues—argument stress-testing, counterexamples, evidence forensics

The gap between 9.3 and 9.5 is where true world-class quality lives.

---

## Quick Reference Commands

| Need | Action |
|------|--------|
| Start new piece | Create brief in `/inputs/`, invoke Researcher |
| Continue work | Check `/outputs/[topic]/` for latest, invoke next agent |
| Need framework guidance | Review `/deutsch-framework/` files |
| Need process guidance | Review `/agents/` for specific agent |
| Need format guidance | Review `/templates/` for output format |
| Quality question | Check Quality Checklist section, invoke Editor if uncertain |
| CODEX not working | Run `npm install -g @openai/codex && codex configure` |

---

## The Ultimate Test

Would David Deutsch read this and say, "Yes, that's right, and it's well explained"?

- If yes → proceed to CODEX review
- If CODEX says yes (≥9.5) → publish
- If no → iterate until yes

---

**Version**: 2.2 (CODEX Brutal Critic Integration)
**Purpose**: Sequential 5-agent specialized error elimination with dual-gate quality control (Editor 9.3 → CODEX 9.5)
**Core Mechanism**: Specialized criticism + external hostile review via `codex` CLI
**Quality Threshold**: 9.5/10 (true world-class standard via OpenAI CODEX)

Welcome to the David Deutsch Content Factory v2.2. Let's create some good explanations.
