# Criticism Methods: 7 Forms of Systematic Error Correction

**Based on**: David Deutsch's epistemology (conjecture & criticism)
**Part of**: Shared Deutsch Framework v1.0
**Last Updated**: 2025-02-05

---

## Overview

Knowledge grows through systematic criticism. This document defines 7 forms of criticism that can be applied to any explanation to eliminate errors and improve knowledge.

**Philosophical Foundation**: Conjecture and criticism - we create explanations and then ruthlessly attack them to find errors. The best explanations survive.

---

## The 7 Forms of Criticism

### 1. Logical Criticism

**What It Tests**: Internal consistency and logical validity

**What It Finds**: Contradictions, fallacies, invalid inferences, circular reasoning

**How to Apply**:
1. Check for internal contradictions: Does any part contradict another?
2. Check for fallacies: circular reasoning, false dichotomy, ad hominem, etc.
3. Check inference chain: Does conclusion actually follow from premises?
4. Check definitions: Are key terms used consistently?

**Examples**:
- **Internal Contradiction**: "This statement is false" (if true, then false; if false, then true)
- **Circular Reasoning**: "X is true because the source of X says so" (source depends on X being true)
- **False Dichotomy**: "Either you believe X or you don't care" (ignores possibility of caring but disagreeing)

**Severity Levels**:
- **CRITICAL**: Contradiction at core of explanation
- **MAJOR**: Fallacy in supporting argument
- **MINOR**: Inconsistency in peripheral detail

**Survival**: Explanation survives if no contradictions or fallacies found.

---

### 2. Empirical Criticism

**What It Tests**: Contradiction by evidence

**What It Finds**: Claims that don't match reality, evidence that refutes the explanation

**How to Apply**:
1. Search for evidence that would contradict the explanation
2. Check if Research phase addressed contradictory evidence
3. Look for real-world cases that don't fit the explanation
4. Check if data exists that contradicts predictions

**Examples**:
- **Contradicting Evidence**: Explanation says "X always leads to Y" but documented cases show X leading to Z
- **Counterexample**: "All swans are white" - black swan discovered
- **Failed Prediction**: Explanation predicts X will happen under Y conditions; it doesn't

**Severity Levels**:
- **CRITICAL**: Core claim contradicted by strong evidence
- **MAJOR**: Peripheral claim contradicted by evidence
- **MINOR**: Evidence ambiguous or weak

**Survival**: Explanation survives if no contradicting evidence exists OR explanation accommodates evidence.

---

### 3. Alternative Explanations

**What It Tests**: Whether better explanations exist

**What It Finds**: Competing explanations that work better than ours

**How to Apply**:
1. Review existing explanations (from Discovery phase or elsewhere)
2. Ask: Does any alternative explain things better?
3. Ask: Does any alternative handle edge cases better?
4. Ask: Is ours genuinely the best available?

**Examples**:
- **Better Mechanism**: Alternative explains HOW, ours only explains WHAT
- **Simpler**: Alternative achieves same result with less complexity
- **More Comprehensive**: Alternative explains more phenomena

**Severity Levels**:
- **CRITICAL**: Much better alternative exists
- **MAJOR**: Alternative is somewhat better
- **MINOR**: Alternative is comparable but different

**Survival**: Explanation survives if it's genuinely the best available.

---

### 4. Edge Cases

**What It Tests**: Boundary conditions and extreme values

**What It Finds**: Explanations that work in typical cases but break at boundaries

**How to Apply**:
1. Identify boundary conditions of the explanation
2. Test: What happens at extreme values?
3. Test: What happens with zero/null input?
4. Test: What happens with contradictory inputs?
5. Test: Where does the mechanism break down?

**Examples**:
- **Boundary**: "Supply curves slope downward" - at zero quantity, what happens?
- **Extreme**: "This algorithm is O(n²)" - at n=0, does it still work?
- **Contradictory**: "This model handles conflict" - what with mutually exclusive goals?

**Severity Levels**:
- **CRITICAL**: Explanation fails at common boundary
- **MAJOR**: Explanation fails at extreme but rare case
- **MINOR**: Explanation has limits but domains where it works well

**Survival**: Explanation survives if it handles edge cases appropriately OR clearly defines its scope.

---

### 5. Counterexamples

**What It Tests**: Specific cases that would disprove the explanation

**What It Finds**: Individual instances that contradict general claims

**How to Apply**:
1. For each claim, ask: What would disprove it?
2. Search for documented counterexamples
3. Consider hypothetical counterexamples
4. Test: Does explanation accommodate or break?

**Examples**:
- **Documented**: "All mammals have live birth" - Platypus discovered
- **Hypothetical**: "This algorithm always terminates" - but what if input has infinite loop?
- **Edge Case**: "This model predicts X for Y > 0" - what at Y = 0.0001?

**Severity Levels**:
- **CRITICAL**: Counterexample disproves core claim
- **MAJOR**: Counterexample requires qualification
- **MINOR**: Counterexample is edge case that can be accommodated

**Survival**: Explanation survives if no genuine counterexamples exist OR counterexamples are addressed.

---

### 6. Assumptions Audit

**What It Tests**: Unjustified premises

**What It Finds**: Implicit assumptions that may not hold

**How to Apply**:
1. Extract all implicit assumptions from explanation
2. For each: Is it justified? What evidence supports it?
3. For each: What if it's false? What happens?
4. For each: Does the explanation depend on it?

**Examples**:
- **Assumption**: "People act rationally" - What if they don't? Does explanation fail?
- **Assumption**: "Market is efficient" - What if there are frictions?
- **Assumption**: "Technology continues improving" - What if it plateaus?

**Severity Levels**:
- **CRITICAL**: Explanation depends on unjustified assumption
- **MAJOR**: Assumption plausible but untested
- **MINOR**: Assumption reasonable with caveats

**Survival**: Explanation survives if all assumptions are justified OR explanation doesn't depend on unjustified assumptions.

---

### 7. Reach Criticism

**What It Tests**: Whether claimed reach is legitimate

**What It Finds**: Overreaching claims, failure to apply where it should work

**How to Apply**:
1. Based on the mechanism, where else should this apply?
2. Check: Does it actually work there?
3. Identify: Domains where it should apply but doesn't
4. Assess: Is the claimed reach legitimate or overstated?

**Examples**:
- **Claimed Reach**: "This principle explains all learning" - but does it apply to statistical learning?
- **Overreach**: "This economic model works in all markets" - but fails in command economies
- **Legitimate Reach**: "Evolution explains all biological adaptation" - does apply across all species

**Severity Levels**:
- **CRITICAL**: Claimed reach but doesn't deliver
- **MAJOR**: Reach is narrower than claimed
- **MINOR**: Reach is legitimate but needs qualification

**Survival**: Explanation survives if claimed reach is legitimate OR reach is appropriately limited.

---

## Using the 7 Forms

### For Critiquing Explanations

**Process**:
1. Extract the explanation and its claims
2. Apply all 7 forms systematically
3. Rate severity of each issue found
4. Assess overall survival

**Output Template**:
```markdown
### Criticism Report: [Explanation]

#### Form 1: Logical Criticism
- [Issue 1]: [description] - Severity: [CRITICAL/MAJOR/MINOR]
- [Issue 2]: [description] - Severity: [CRITICAL/MAJOR/MINOR]
Survival: [YES/NO]

#### Form 2: Empirical Criticism
- [Contradicting Evidence 1]: [description] - Severity: [CRITICAL/MAJOR/MINOR]
Survival: [YES/NO - how addressed]

[Continue for all 7 forms]

#### Overall Survival
Critical Issues: [count]
Major Issues: [count]
Minor Issues: [count]
Verdict: [SURVIVES / NEEDS REVISION / FAILS]
```

### For Self-Criticism (Creating Explanations)

**Process**:
1. Create your explanation
2. Apply all 7 forms to your own work
3. Address all issues found
4. Repeat until satisfied or explanation fails

**This is how knowledge grows**: Conjecture → Criticism → Error elimination → Better conjecture.

---

## Severity Guidelines

### CRITICAL Issues

Must be fixed before explanation can proceed. These are fatal flaws.

**Examples**:
- Internal contradiction
- Core claim contradicted by evidence
- Much better alternative exists
- Explanation fails at common boundary
- Counterexample to core claim
- Depends on unjustified assumption
- Claimed reach is false

### MAJOR Issues

Should be addressed if possible. May require revision or qualification.

**Examples**:
- Logical fallacy in supporting argument
- Peripheral claim contradicted
- Alternative is somewhat better
- Explanation fails at edge case
- Counterexample requires qualification
- Assumption untested
- Reach is overstated

### MINOR Issues

Optional to fix. May represent limitations rather than flaws.

**Examples**:
- Minor inconsistency in detail
- Evidence ambiguous but not contradictory
- Alternative is different but not better
- Edge case handled with caveat
- Counterexample accommodated with note
- Assumption reasonable but could be tested
- Reach is legitimate but narrower than claimed

---

## Relationship to Deutsch Framework

### Connection to Conjecture & Criticism

These 7 forms operationalize "criticism" - the systematic error elimination that drives knowledge growth.

### Connection to 5-Test Framework

The 5-test framework evaluates explanations. The 7-form criticism tests them. They work together:

- **5-Test**: Is this a good explanation? (Evaluation)
- **7-Form Criticism**: Does this explanation survive attack? (Testing)

### Connection to Fallibilism

We never achieve certainty. Criticism is never complete. These 7 forms help us approach truth asymptotically by eliminating errors, but we never arrive at final, justification-proof certainty.

---

## Practical Examples

### Example 1: "Supply and Demand Determines Price"

**Logical Criticism**: ✓ (internally consistent)
**Empirical Criticism**: ✗ (ignores market power, information asymmetry)
**Alternative Explanations**: ✓ (Price setting models explain better)
**Edge Cases**: ✗ (what with zero price? infinite price?)
**Counterexamples**: ✓ (Veblen goods, Giffen goods)
**Assumptions**: ✓ (rational actors, perfect information)
**Reach Criticism**: ✗ (fails in many real markets)

**Result**: FAILS multiple tests - bad explanation in many domains

### Example 2: Evolution by Natural Selection

**Logical Criticism**: ✓ (internally consistent)
**Empirical Criticism**: ✓ (massive evidence, no contradictions)
**Alternative Explanations**: ✗ (no better explanation found)
**Edge Cases**: ✓ (handles transition cases, etc.)
**Counterexamples**: ✗ (no genuine counterexamples found)
**Assumptions**: ✓ (mechanism depends on variation, which exists)
**Reach Criticism**: ✓ (explains all biological adaptation)

**Result**: PASSES all tests - good explanation

---

## Citation

When using this framework:

**Short**: "This analysis applies 7 forms of systematic criticism based on David Deutsch's conjecture-and-criticism epistemology."

**Detailed**: "The explanation was subjected to seven forms of criticism: logical, empirical, alternatives, edge cases, counterexamples, assumptions, and reach. Each form targets specific failure modes: internal contradictions (Form 1), contradicting evidence (Form 2), superior alternatives (Form 3), boundary failures (Form 4), disconfirming instances (Form 5), unjustified premises (Form 6), and overreach (Form 7). This operationalizes Popper's and Deutsch's criticism mechanism for error elimination."

---

**Note**: This is a shared framework document. When applying criticism, be thorough and specific. Vague criticism misses the point. The goal is error elimination, not fault-finding.
