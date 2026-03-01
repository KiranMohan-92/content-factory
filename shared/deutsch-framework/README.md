# Shared Deutsch Framework

**Version**: 1.0
**Last Updated**: 2025-02-05
**Purpose**: Centralized documentation of David Deutsch's epistemological framework for use across all systems

---

## Overview

This directory contains the core philosophical and methodological foundation for all Deutsch-based systems in the codebase. All systems should reference this framework to ensure consistency and avoid duplication.

---

## Framework Documents

### 1. epistemology.md
**David Deutsch's epistemological foundation**

Contents:
- Fallibilism
- Conjecture and criticism
- Primacy of explanations
- Objective truth
- Demarcation criterion
- Realism about abstract entities
- Problem of induction
- Knowledge creation process
- Common misconceptions
- Practical implications

**When to use**: As the authoritative reference for Deutsch's epistemology. When explaining WHY we do what we do.

**Citation**: "This analysis applies David Deutsch's epistemological framework from *The Beginning of Infinity* (2011)."

---

### 2. 5-test-framework.md
**The five independent tests for good explanations**

Contents:
- Test 1: Hard-to-Vary (ad-hoc detection)
- Test 2: Mechanism (causal chains)
- Test 3: Reach (explanatory power)
- Test 4: Rejectability (falsifiability)
- Test 5: Integration (connection to knowledge)

**When to use**: When evaluating any explanation for quality. Apply all 5 tests systematically.

**Citation**: "Explanations are evaluated using David Deutsch's 5-test framework: hard-to-vary, mechanism, reach, rejectability, and integration."

---

### 3. criticism-methods.md
**Seven forms of systematic criticism for error elimination**

Contents:
- Form 1: Logical criticism (contradictions, fallacies)
- Form 2: Empirical criticism (contradicting evidence)
- Form 3: Alternative explanations (better options)
- Form 4: Edge cases (boundary testing)
- Form 5: Counterexamples (disproving instances)
- Form 6: Assumptions audit (unjustified premises)
- Form 7: Reach criticism (overreach detection)

**When to use**: When criticizing explanations (self or others). Apply all 7 forms systematically.

**Citation**: "This analysis applies seven forms of systematic criticism based on David Deutsch's conjecture-and-criticism epistemology."

---

## How Systems Use This Framework

### Opus-CF
- **Primary user**: References all three documents
- **epistemology.md**: Philosophical foundation
- **5-test-framework.md**: Analysis phase (5 tests)
- **criticism-methods.md**: Criticism phase (7 forms)

### Content Factory v2.2
- **Primary user**: References epistemology.md, 5-test-framework.md
- **Use**: Analyzer agent applies 5 tests, Editor enforces quality

### deutsch_agent
- **Primary user**: References 5-test-framework.md
- **Use**: Hard-to-vary rating (0-10 scale) based on Test 1

---

## Core Principles

### All Systems Agree On These Foundations

1. **Conjecture and Criticism** - Knowledge grows through this cycle
2. **Hard-to-Vary** - Good explanations resist variation
3. **Problems Are Soluble** - No fundamental barriers to knowledge
4. **Primacy of Explanations** - Understanding > prediction
5. **Fallibilism** - We can never be certain, only progressively less wrong

### Each System Applies These Differently

| System | Primary Focus | How It Applies Framework |
|--------|---------------|-------------------------|
| Opus-CF | Knowledge creation | Full pipeline with all tests and criticism |
| Content Factory v2.2 | Content production | 5 tests in Analysis, quality gates |
| deutsch_agent | App ideation | Hard-to-vary rating for ideas |

---

## Citation Guide

### For the Framework (General)

"When applying David Deutsch's epistemological framework, we prioritize explanations over predictions, criticism over justification, and hard-to-vary explanations over arbitrary ones."

### For Specific Tests

**5 Tests**: "This explanation was evaluated using David Deutsch's 5-test framework for good explanations (hard-to-vary, mechanism, reach, rejectability, integration)."

**7 Criticism Forms**: "This explanation was subjected to seven forms of systematic criticism (logical, empirical, alternatives, edge cases, counterexamples, assumptions, reach)."

### For Specific Principles

**Conjecture & Criticism**: "Following Popper and Deutsch, knowledge grows through conjecture and criticism, not through induction from observation."

**Hard-to-Vary**: "A good explanation is hard-to-vary—its components cannot be substituted without losing explanatory power."

**Problems Soluble**: "Deutsch argues that all problems are soluble given the right knowledge, excluding only what is forbidden by the laws of physics."

---

## Maintenance

**Version Control**: When updating framework documents, update version number and date.

**Consistency**: All systems should adapt to framework changes to maintain compatibility.

**Feedback**: If you identify gaps or errors in framework documentation, document them for future improvement.

---

## Related Systems

- **Opus-CF**: `/Opus-CF/` - Complete knowledge creation engine
- **Content Factory v2.2**: `/content-factory/` - Content production system
- **deutsch_agent**: `/App idea/agents/` - App ideation system

---

**Note**: This is a shared resource. When using framework documents, maintain citation practices and intellectual honesty.

**Primary Sources**:
- *The Beginning of Infinity* by David Deutsch (2011)
- *The Fabric of Reality* by David Deutsch (1997)
- *Conjectures and Refutations* by Karl Popper (1963)

---

**Last Review**: 2025-02-05
**Next Review**: As needed when systems evolve or new Deutsch works are incorporated.
