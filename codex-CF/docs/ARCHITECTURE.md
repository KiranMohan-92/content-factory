# Architecture

## Objective Function

Maximize explanatory knowledge quality:

`KQ = f(HTV, Mechanism, Reach, Rejectability, Integration, Evidence Hygiene)`

Where:
- `HTV`: Hard-to-Vary resilience under adversarial substitutions
- `Mechanism`: Causal explanatory depth
- `Reach`: Explanatory generality beyond narrow case
- `Rejectability`: Concrete falsifiers and measurable failure conditions
- `Integration`: Coherence with adjacent good explanations
- `Evidence Hygiene`: Source quality, verifiability, and calibration

## Two-Rail Design

1. Knowledge Rail
- Input: topic + candidate explanations from internet research.
- Process: evaluate each explanation against all tests.
- Failure mode handling: if no candidate survives, synthesize a conjecture from strongest partial truths.
- Output: best explanation with scorecard and explicit falsification triggers.

2. Publication Rail
- Input: knowledge rail output.
- Gate: epistemic threshold and critical minimums.
- Output: publication package including:
  - core claim
  - mechanism
  - assumptions
  - falsifiers
  - what would change my mind

## Hard-to-Vary Attack

The system performs deterministic variation attacks:
- replace abstract performance terms ("better", "effective", "success")
- remove constrained qualifiers
- check whether explanation still appears to "work"

If many variations survive with little loss of specificity, HTV score drops.

## Synthesis Rule

When all candidates are below threshold:
- pick top two by weighted score
- merge strongest causal mechanism from one with strongest rejectability structure from another
- produce synthesized conjecture
- re-evaluate as a normal candidate

## Publication Gate (default)

- weighted epistemic score `>= 8.0`
- no critical test (`HTV`, `Mechanism`, `Rejectability`) below `6.5`

## Why This Is Hard to Vary

- Explanations must survive independent tests with explicit failure conditions.
- Vague claims are penalized by both HTV and Evidence Hygiene.
- Publishability depends on falsifiability, not prose quality.
