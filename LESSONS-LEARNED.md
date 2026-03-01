# Content Factory: Lessons Learned

This document captures hard-won lessons from content that failed external review. Every entry represents a real failure that led to system improvements.

---

## Lesson 001: Evidence Hygiene Failure (January 2025)

**Topic**: "Judgment at Scale: The Real Skill in the AI Era"

**What Happened**: Article passed internal 7-pass review with 9.42/10 score. External review scored it 7.2/10, identifying multiple evidence hygiene failures.

**Failure Mode**: Claims were stronger than evidence supported. Specifically:

| Claim Made | What Evidence Actually Showed | Error Type |
|------------|-------------------------------|------------|
| "Hybrid teams outperformed AI by 68.7%" | Teaming improved efficiency by 68.7% on *tasks agents failed* in *specific setup* | **Mischaracterization** |
| "AI fundamentally cannot do judgment" | Current AI is unreliable at self-evaluation without external feedback | **Overclaiming** |
| "Nova Spivack found 90%+ confirmation rate" | Research exists but attribution to specific person without primary citation | **Weak attribution** |
| "Zach Seward described semantic fingerprinting" | No verifiable source for this specific quote | **Unverifiable quote** |
| "Catastrophic rework" | Phrase not found in cited study | **Fabricated terminology** |

**Root Causes**:
1. Research synthesis created composite claims from multiple sources
2. Secondary summaries trusted over primary sources
3. Precision inflation (vague findings stated with false precision)
4. Pattern observations presented as direct quotes
5. Internal editor didn't verify claims against primary sources

**System Changes Made**:
1. **Researcher Agent**: Added "Evidence Hygiene Standards" section requiring source classification, numerical claim verification, and quote attribution levels
2. **Writer Agent**: Added "Claim Strength & Attribution Guardrails" with forbidden absolute language table and study citation requirements
3. **Editor Agent**: Expanded Pass 2 to "Factual Accuracy & Evidence Hygiene" with study citation audit, quote/attribution audit, and claim strength audit

**Detection Heuristics Added**:
- Any claim with specific percentage must include context (% of what? compared to what?)
- Any "fundamentally" or "cannot" requires rigorous architectural/physical defense
- Any "[Person] told me" or "[Person] said" requires verifiable publication link
- Any study citation must include conditions/limitations

**Validation**: Future content must pass the "Would the original researchers agree with my summary?" test for every cited study.

---

## Lesson 002: Counterargument Defeat vs. Assertion (January 2025)

**Topic**: Same as above

**What Happened**: Counterarguments were "addressed" but not "defeated." Specifically, Objection 1 ("AI is improving rapidly—this is temporary") was asserted against using "it's an architecture problem" without establishing why architecture is a permanent barrier.

**Failure Mode**: Asserting the opposite of an objection instead of providing mechanism-based rebuttal.

**Better Approach**: The external reviewer suggested:
> "Even if evaluators improve, evaluation is inherently costly because it requires interaction with reality (tests, feedback loops, real-world outcomes), not just token prediction."

This is a harder-to-vary rebuttal because:
- It identifies a structural cost (reality interaction) not dependent on AI capability
- It aligns with Kahneman/Klein's boundary conditions for expertise
- It explains the 17.7% slowdown finding (verification overhead)

**System Changes Made**:
- Writer Agent: Added "Counterargument Response Standards" requiring mechanism-based rebuttals
- Emphasized "Use evidence, not authority" and "Explain WHY your position survives"

**Detection Heuristic**: If a counterargument response contains "but" without "because [mechanism]", it's probably assertion not defeat.

---

## Lesson 003: Internal Editor Grade Inflation (January 2025)

**What Happened**: Internal review scored 9.42/10. External review scored 7.2/10. That's a 2.2 point gap—significant grade inflation.

**Root Cause**: Internal editor didn't independently verify factual claims. Trusted that research → analysis → writing chain preserved accuracy.

**System Changes Made**:
- Editor Pass 2 now requires explicit verification count: "Studies cited: [N], Verified against primary source: [N]"
- Added "CRITICAL" warning that this pass catches most publication-blocking errors
- Lowered threshold: Mischaracterization of supporting claim now scores ≤7/10

**Meta-Lesson**: The traceability chain (research → analysis → writing) doesn't prevent evidence mischaracterization—it can actually amplify it by adding legitimacy to mischaracterized claims.

---

## Patterns to Watch

### High-Risk Claim Types
1. **Specific percentages** - Rarely as clean as they sound
2. **"Study found"** - Study probably found something more nuanced
3. **"Fundamentally/cannot/never"** - Almost always overclaims
4. **"[Person] said"** - Often unverifiable or paraphrased
5. **Combined findings** - Two true things combined into one false thing

### High-Risk Situations
1. **Time pressure** - Shortcuts on verification
2. **Compelling narrative** - Bending evidence to fit story
3. **Secondary sources** - Trusting summaries over primaries
4. **Synthesis** - Creating composite claims from multiple sources

### Quality Signals That DON'T Indicate Accuracy
- Well-written prose
- Clear argument structure
- Compelling examples
- High confidence tone
- Specific-sounding numbers

### Quality Signals That DO Indicate Accuracy
- Links to primary sources
- Context for every statistic
- Hedged language ("suggests", "in this context")
- Acknowledgment of limitations
- "Would the source agree?" test passed

---

## Process Improvement Log

| Date | Change | Reason |
|------|--------|--------|
| Jan 2025 | Added Evidence Hygiene Standards to Researcher | Mischaracterized study findings |
| Jan 2025 | Added Claim Strength Guardrails to Writer | Overclaiming, absolute language |
| Jan 2025 | Expanded Editor Pass 2 to Evidence Hygiene Audit | Grade inflation, unverified claims |
| Jan 2025 | Created LESSONS-LEARNED.md | Institutional memory |

---

## How to Use This Document

1. **Before researching**: Review "High-Risk Claim Types" and "High-Risk Situations"
2. **Before writing**: Review "Claim Strength Guardrails" in Writer Agent
3. **Before editing**: Review "Detection Heuristics" from each lesson
4. **After external review fails**: Add new lesson to this document

**The goal is not to avoid mistakes—it's to avoid the SAME mistake twice.**
