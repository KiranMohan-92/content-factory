# Opus-CF: Opus-Powered Content Factory

## Mission

A Popper-Deutsch knowledge creation engine that:
1. **Discovers** existing explanations and subjects them to hard-to-vary tests
2. **Critiques** candidate explanations with systematic error correction
3. **Creates** the best hard-to-vary explanation achievable with current knowledge
4. **Accumulates** knowledge in a persistent database

## Core Philosophy

Based on Karl Popper and David Deutsch's epistemology:
- Knowledge grows through **conjecture and criticism**
- Problems are the engine of knowledge creation
- Good explanations are **hard-to-vary**
- We never reach certainty, only better explanations

## Architecture

```
Phase 0: Setup
  ↓
Phase 0.5: DISCOVERY (Find and test existing explanations)
  ↓
Phase 1: RESEARCH (Fill gaps identified by Discovery)
  ↓
Phase 2: ANALYSIS (Create best explanation using 5 Deutsch tests)
  ↓
Phase 2.5: CRITICISM (Systematic error correction)
  ↓
Phase 3: WRITING (Translate to accessible content)
  ↓
Phase 4: EDITING (7-pass review + CODEX brutal critic)
  ↓
Phase 5: PUBLICATION + DATABASE UPDATE
```

## Key Innovations

1. **Discovery Phase**: Systematically find and test existing explanations BEFORE creating new ones
2. **Criticism Engine**: 7 forms of systematic criticism (logical, empirical, alternatives, edge cases, counterexamples, assumptions, reach)
3. **Explanation Database**: Persistent tracking of all explanations with version history
4. **Opus 4.6 Integration**: Each agent uses Opus 4.6's intelligence within structural constraints

## Version

**Opus-CF v1.0** - Complete knowledge creation engine

## Usage

See `/Opus-CF/run-opus-cf.md` for orchestrator instructions.
