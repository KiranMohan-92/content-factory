# Opus-CF: Opus-Powered Content Factory

## Project Overview

**Opus-CF** is a Popper-Deutsch knowledge creation engine that:
1. **Discovers** existing explanations and tests them with hard-to-vary criteria
2. **Researches** gaps to find evidence no existing explanation addresses
3. **Creates** the best possible explanation using 5 Deutsch tests
4. **Critiques** with 7 forms of systematic error correction
5. **Translates** to accessible, actionable content
6. **Accumulates** knowledge in a persistent database

**Core Philosophy**: Knowledge grows through conjecture and criticism. Good explanations are hard-to-vary. We never reach certainty, only better explanations.

---

## Quick Start

### For Users

**To create content**:

1. Create input brief:
   ```bash
   cp /Opus-CF/templates/input-brief-template.md /Opus-CF/inputs/your-topic.md
   # Edit and fill out the brief
   ```

2. Run the orchestrator with your brief:
   ```
   Topic: [your topic from brief]
   Audience: [from brief]
   Formats: [from brief]
   ```

3. The system runs 7 phases automatically:
   - Setup → Discovery → Research → Analysis → Criticism → Writing → Editing → Publication

4. Find published content in: `/Opus-CF/outputs/[topic]/final/`

---

## System Architecture

```
Phase 0: Setup
   ↓
Phase 0.5: DISCOVERY (Find & test existing explanations)
   ↓
Phase 1: RESEARCH (Fill gaps from Discovery)
   ↓
Phase 2: ANALYSIS (Create best explanation with 5 Deutsch tests)
   ↓
Phase 2.5: CRITICISM (7 forms of systematic error correction)
   ↓
Phase 3: WRITING (Translate to accessible content)
   ↓
Phase 4: EDITING (7-pass review, 9.3+ to publish)
   ↓
Phase 5: PUBLICATION + DATABASE UPDATE
```

---

## The Agents

All agents are powered by Opus 4.6:

1. **Discovery Agent** (`/agents/discovery-agent-v1.md`)
   - Finds 5-15 existing explanations
   - Applies all 5 Deutsch tests to each
   - Identifies gaps
   - Output: `discovery-report.md`

2. **Research Agent** (`/agents/research-agent-v1.md`)
   - Researches gaps from Discovery
   - Tests shared assumptions
   - Finds new explanations
   - Output: `research.md`

3. **Analysis Agent** (`/agents/analysis-agent-v1.md`)
   - Creates or selects best explanation
   - Applies all 5 Deutsch tests
   - Output: `analysis.md`

4. **Criticism Engine** (`/agents/criticism-engine-v1.md`)
   - 7 forms of systematic criticism
   - Tests for survival
   - Output: `criticism-report.md`

5. **Writer Agent** (`/agents/writer-agent-v1.md`)
   - Translates to accessible content
   - Addresses all criticisms
   - 3-5 examples, 2-3 counterarguments
   - Practical utility included
   - Output: `drafts/[format].md`

6. **Editor Agent** (`/agents/editor-agent-v1.md`)
   - 7-pass systematic review
   - Numerical scoring (9.3+ to publish)
   - Output: `editor-feedback.md`

---

## The 5 Deutsch Tests

1. **Hard-to-Vary**: Can components vary without breaking explanation?
2. **Mechanism**: Does it explain HOW (causal chain)?
3. **Reach**: Does it explain more than intended?
4. **Rejectability**: Can it be falsified?
5. **Integration**: Does it connect to other knowledge?

---

## The 7 Forms of Criticism

1. **Logical**: Internal contradictions, fallacies
2. **Empirical**: Contradicted by evidence
3. **Alternatives**: Better explanations exist
4. **Edge Cases**: Breaks at boundaries
5. **Counterexamples**: Specific cases disprove it
6. **Assumptions**: Unjustified assumptions
7. **Reach**: Fails where should work

---

## Quality Standards

**7 Editorial Dimensions**:
1. Accuracy (20%) - Traceability to sources
2. Criticism Survival (15%) - Objections addressed
3. Logical Soundness (15%) - No fallacies
4. Clarity (15%) - Target audience understands
5. Engagement (10%) - Hook, momentum, voice
6. Practical Utility (15%) - Specific, actionable
7. Intellectual Honesty (10%) - Limitations acknowledged

**Minimum to publish**: 9.3/10
**Each dimension minimum**: 9.0/10

---

## Key Innovations

1. **Discovery Phase**: Systematically find and test existing explanations FIRST
2. **Criticism Engine**: 7 forms of error correction before publication
3. **Explanation Database**: Persistent knowledge accumulation
4. **Opus 4.6 Integration**: Each agent uses Opus within structural constraints

---

## Directory Structure

```
/Opus-CF/
├── README.md                    # This file
├── run-opus-cf.md                # Orchestrator instructions
├── EXPLANATION-DATABASE.md       # Knowledge base
├── CLAUDE.md                     # This file
├── agents/                       # All agent instructions
│   ├── discovery-agent-v1.md
│   ├── research-agent-v1.md
│   ├── analysis-agent-v1.md
│   ├── criticism-engine-v1.md
│   ├── writer-agent-v1.md
│   └── editor-agent-v1.md
├── templates/
│   └── input-brief-template.md   # User brief template
├── inputs/                       # User briefs
│   └── [topic].md
└── outputs/                      # Generated content
    └── [topic]/
        ├── discovery-report.md
        ├── research.md
        ├── analysis.md
        ├── criticism-report.md
        ├── drafts/
        │   ├── article.md
        │   ├── thread.md
        │   └── post.md
        ├── editor-feedback.md
        ├── execution-log.md
        └── final/                 # Published content
```

---

## Using Opus-CF

### Starting a New Topic

1. Create your input brief from the template
2. Run the orchestrator (or invoke agents sequentially)
3. Review execution-log.md for progress
4. Find published content in `/final/`

### Monitoring Progress

Check execution status:
- `/Opus-CF/outputs/[topic]/execution-log.md` - Phase-by-phase progress
- `/Opus-CF/EXPLANATION-DATABASE.md` - All published topics

### Troubleshooting

**If Discovery fails**: Topic may be too obscure - manual research needed
**If Research fails**: Discovery gaps too vague - refine brief
**If Analysis fails**: Research insufficient - more evidence needed
**If Criticism rejects**: Return to Analysis - create better explanation
**If Writer fails**: Analysis unclear - provide more guidance
**If Editor rejects**: Return to Writer with specific fixes

---

## Philosophy

**Based on**:
- Karl Popper's *Conjectures and Refutations*
- David Deutsch's *The Beginning of Infinity*

**Core Principles**:
- Knowledge grows through conjecture and criticism
- Problems are inevitable AND soluble
- Good explanations are hard-to-vary
- We never reach certainty, only better explanations
- Reach indicates truth
- Objective truth exists but certainty doesn't

---

## Version

**Opus-CF v1.0** - Complete knowledge creation engine

**Changes from Content Factory v2.2**:
- NEW: Discovery Phase (find existing explanations first)
- NEW: Criticism Engine (7 forms of systematic error correction)
- NEW: Explanation Database (persistent knowledge tracking)
- Simplified: 7 editorial dimensions (adapted from original)
- All agents Opus-Powered
- Focus on best explanation achievable now (not infinite iteration)

---

## Credits

**Framework**: David Deutsch's epistemology
**Implementation**: Opus-CF agentic system
**Intelligence**: Opus 4.6 (Claude)

---

**Welcome to Opus-CF. Let's create some hard-to-vary explanations.**
