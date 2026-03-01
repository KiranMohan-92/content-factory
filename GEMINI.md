# GEMINI.md

This file provides guidance to Gemini when working with code in this repository.

---

## Project Overview

**David Deutsch Content Factory** - A systematic content production system that applies David Deutsch's epistemological framework (from *The Beginning of Infinity*) to analyze problems and create high-quality explanatory content.

**Core Principle**: Good explanations are hard-to-vary, mechanistic, and have reach. This system uses a sequential 4-agent workflow to identify, analyze, and communicate good explanations while systematically eliminating errors.

---

## Architecture

### Sequential Agent Workflow

The system uses **4 specialized agents in strict sequence**. Each agent criticizes and improves upon previous work:

```
Research → Analysis → Writing → Editing → Publication
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

3. **Writer Agent** (`/agents/writer-agent.md`)
   - **FIRST**: Checks `/CONTENT-CONTEXT.md` for previously explained concepts
   - **Asks user** whether to repeat, reference, or skip previously explained concepts
   - Translates analysis into accessible content with **substantial counterarguments**
   - Creates drafts for multiple formats (article, thread, post, etc.)
   - Maintains philosophical rigor while optimizing for engagement
   - Uses **exploratory, non-preachy tone** (questions, not lectures)
   - **Output**: Format-specific draft files (`article.md`, `twitter-thread.md`, etc.)

4. **Editor Agent** (`/agents/editor-agent.md`)
   - **WORLD-CLASS QUALITY GATE**: Minimum score 9.3/10, preferably >9.5/10
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
   - **Output**: `editor-feedback.md` with numerical scores OR approved final content in `/final/`

---

## Directory Structure

```
/content-factory/
├── GEMINI.md                          # This file - start here
├── CONTENT-CONTEXT.md                 # Track explained concepts across topics (CHECK BEFORE WRITING)
├── HOW-THE-WORKFLOW-WORKS.md          # Deep explanation of the workflow
│
├── deutsch-framework/                 # Epistemological framework reference
│   ├── epistemology.md               # Core principles
│   ├── explanations.md               # Good vs bad explanations
│   ├── problem-solving.md            # Problems inevitable/soluble
│   └── examples.md                   # Concrete applications
│
├── agents/                            # Agent instructions (read before invoking)
│   ├── researcher-agent.md
│   ├── analyzer-agent.md
│   ├── writer-agent.md
│   ├── editor-agent.md
│   └── scoring-rubric.md             # World-class scoring system (9.3+ to publish)
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
        ├── research.md
        ├── analysis.md
        ├── [format].md               # article, twitter-thread, linkedin-post, etc.
        ├── editor-feedback.md
        └── final/                    # Publication-ready content
            └── [all approved formats]
```

---

## Common Commands

### Starting New Content Project

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

2. **Run the workflow**:

```
# Phase 1: Research
Read: /agents/researcher-agent.md
Invoke Researcher with input brief
Review output: /outputs/[topic]/research.md

# Phase 2: Analysis
Read: /agents/analyzer-agent.md
Invoke Analyzer with research.md
Review output: /outputs/[topic]/analysis.md

# Phase 3: Writing
FIRST: Writer checks /CONTENT-CONTEXT.md for previously explained concepts
THEN: Writer asks user about repeating vs referencing those concepts
Read: /agents/writer-agent.md
Invoke Writer with analysis.md + requested formats
Writer includes 2-3 strong counterarguments and uses exploratory tone
Review output: /outputs/[topic]/[format].md

# Phase 4: Editing
Read: /agents/editor-agent.md
Invoke Editor with all drafts
Review output: /outputs/[topic]/editor-feedback.md or /final/

# Phase 5: Iterate if needed
If Editor requests revisions, make changes and re-submit
```

### Example Invocation

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
- **World-class quality score of 9.3+/10** (see scoring rubric)

**Never**:
- Claim certainty (only "survives criticism so far")
- Skip research phase (even on familiar topics)
- Combine agents or run in parallel (breaks error correction)
- Ignore Editor feedback (quality enforcement is essential)
- Strawman opposing views (steelman instead)
- **Use preachy/lecturing tone** (be exploratory and humble)
- **Skip counterarguments** (minimum 2-3 substantial objections)
- **Repeat explanations unnecessarily** (checked CONTENT-CONTEXT.md first, ask user)

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
- [ ] **Editor scored ≥9.3/10** (with breakdown by dimension)
- [ ] Editor approved after rigorous review

---

## For Continuing Work

**If returning to existing project**:

1. Check `/outputs/[topic]/` to see what's been completed
2. **Check `/CONTENT-CONTEXT.md`** to see what's been explained in other pieces
3. Identify current phase (research/analysis/writing/editing)
4. Read relevant agent instructions in `/agents/`
5. Review previous phase output to understand context
6. Continue with next sequential phase

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
- Numerical score ≥9.3/10 (preferably >9.5)
- Presents competing explanations fairly
- Identifies hard-to-vary explanation
- Makes testable claims
- **Provides specific, immediately actionable steps** (not vague advice)
- Acknowledges limitations with intellectual honesty

**Reader-level**:
- Understands hard-to-vary test
- Can apply framework to other domains
- **Has taken specific action within 24 hours** (immediate first step)
- **Uses provided workflow/framework repeatedly**
- Wants to learn more and shares content

**System-level**:
- Consistent 9.3+ scores across all topics
- Reproducible world-class process
- Building library of proven practical examples
- Reader testimonials about usefulness

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
- Editor → catches everything previous agents missed

Combined roles force tradeoffs. Specialized roles maximize error detection per dimension.

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

---

## The Ultimate Test

Would David Deutsch read this and say, "Yes, that's right, and it's well explained"?

- If yes → publish
- If no → iterate until yes

---

**Version**: 2.0
**Purpose**: Systematic error elimination produces quality content
**Core Mechanism**: Sequential specialized criticism

Welcome to the David Deutsch Content Factory. Let's create some good explanations.
