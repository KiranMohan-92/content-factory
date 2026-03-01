# Opus-CF Quick Reference

## One-Page Summary

**Opus-CF** is a Popper-Deutsch knowledge creation engine powered by Opus 4.6.

---

## The 7-Phase Pipeline

```
0. Setup → Create brief, directory structure
0.5. DISCOVERY → Find & test existing explanations (5-15 found, all 5 tests applied)
1. Research → Fill gaps identified by Discovery
2. Analysis → Create best explanation (apply all 5 tests)
2.5. CRITICISM → 7 forms of systematic error correction
3. Writing → Translate to accessible content (address criticisms, examples, counterarguments)
4. Editing → 7-pass review, score 9.3+ to publish
5. Publication → Move to /final/, update database
```

---

## The 5 Deutsch Tests

| Test | Detects | Good | Bad |
|------|---------|------|-----|
| Hard-to-Vary | Ad-hoc | Can't swap components | Can swap freely |
| Mechanism | "Just-so" | Explains HOW | Describes WHAT |
| Reach | Narrow | Explains more | Only target |
| Rejectability | Unfalsifiable | Can state what's wrong | No test possible |
| Integration | Isolated | Connects to knowledge | Conflicts/alone |

---

## The 7 Forms of Criticism

| Form | What It Tests |
|------|---------------|
| 1. Logical | Internal contradictions, fallacies |
| 2. Empirical | Contradicting evidence |
| 3. Alternatives | Better explanations exist |
| 4. Edge Cases | Breaks at boundaries |
| 5. Counterexamples | Specific disproofs |
| 6. Assumptions | Unjustified premises |
| 7. Reach | Fails where should work |

---

## The 7 Editorial Dimensions

| Dimension | Weight | Min Score |
|-----------|--------|-----------|
| 1. Accuracy | 20% | 9.0 |
| 2. Criticism Survival | 15% | 9.0 |
| 3. Logical Soundness | 15% | 9.0 |
| 4. Clarity | 15% | 9.0 |
| 5. Engagement | 10% | 9.0 |
| 6. Practical Utility | 15% | 9.0 |
| 7. Intellectual Honesty | 10% | 9.0 |

**Threshold**: 9.3/10 to publish

---

## File Locations

**Input**: `/Opus-CF/inputs/[topic].md`
**Agents**: `/Opus-CF/agents/[agent-name].md`
**Output**: `/Opus-CF/outputs/[topic]/[phase-file].md`
**Published**: `/Opus-CF/outputs/[topic]/final/`
**Database**: `/Opus-CF/EXPLANATION-DATABASE.md`

---

## Key Innovations

1. **Discovery First** - Find existing explanations before creating new ones
2. **Systematic Criticism** - 7 forms of error correction
3. **Database Accumulation** - Knowledge persists across topics
4. **Opus + Structure** - Intelligence within hard-to-vary constraints

---

## How to Use

### Create Content

1. Copy `/Opus-CF/templates/input-brief-template.md` to `/Opus-CF/inputs/your-topic.md`
2. Fill out the brief
3. Run: Read `/Opus-CF/run-opus-cf.md` with your brief details
4. Find output in `/Opus-CF/outputs/your-topic/final/`

### Run Synthesis (Periodic)

1. After 10+ topics published
2. Run: Read `/Opus-CF/agents/synthesis-agent-v1.md`
3. Output: `/Opus-CF/UNIVERSAL-EXPLAINERS.md`

---

## Philosophy Corner

**Knowledge grows through**:
- Conjecture (create explanations)
- Criticism (test against reality)
- Error elimination (discard what fails)
- Better conjecture (improve from wreckage)

**Good explanations are**:
- Hard-to-vary (can't change details without breaking)
- Mechanistic (explain HOW not just WHAT)
- Have reach (explain more than intended)
- Falsifiable (can state what's wrong)
- Integrated (connect to other knowledge)

**We never reach certainty** - only explanations that "survive criticism so far."

---

## Quick Checklist

**Before starting**:
- [ ] Brief filled out with specific topic, audience, formats
- [ ] Reviewed agents for understanding of pipeline

**During execution**:
- [ ] Each phase completes before next starts
- [ ] Each agent produces required output file
- [ ] Execution log tracks progress

**After completion**:
- [ ] Score ≥9.3/10
- [ ] All formats created
- [ ] Database updated
- [ ] Content in /final/

---

## Version

**Opus-CF v1.0** - Complete knowledge creation engine

---

**For full details**, see `/Opus-CF/CLAUDE.md`
