# Content Factory v4.0 - Parallel Specialized Architecture

## Executive Summary

A world-class content production system using **parallel specialized agents** within **sequential phases**. Each phase deploys multiple specialists with complementary blind spots, synthesized by an integrator agent. The architecture is constrained by the structure of knowledge production itself - removing any specialist creates a specific, predictable gap.

## Core Principle: Complementary Blind Spots

Every agent has blind spots. The current sequential architecture works because each phase catches what the previous phase can't see about its own work.

**V4 Extension**: Within each phase, deploy specialists with **different** blind spots. A source specialist misses practical application. A practitioner specialist misses academic rigor. A contrarian specialist misses mainstream consensus. Together, they cover ground no single agent can.

**The mechanism**: Parallel specialization → Comprehensive coverage → Synthesis integration → Higher quality output

This is hard to vary because:
- Each specialist has a defined, non-interchangeable role
- Removing any specialist leaves a **specific, predictable gap**
- The synthesis step **integrates** rather than merely **selects**
- The structure mirrors how good research actually works (multiple perspectives → integration)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CONTENT FACTORY v4.0                                │
│                    Parallel Specialized Architecture                        │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 1: RESEARCH (Parallel Specialists → Synthesizer)
┌─────────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   SCHOLAR   │  │ PRACTITIONER│  │ CONTRARIAN  │  │  HISTORIAN  │        │
│  │  SPECIALIST │  │  SPECIALIST │  │  SPECIALIST │  │  SPECIALIST │        │
│  │             │  │             │  │             │  │             │        │
│  │ Academic    │  │ Real-world  │  │ Minority    │  │ Evolution   │        │
│  │ sources,    │  │ examples,   │  │ views,      │  │ of ideas,   │        │
│  │ citations,  │  │ case        │  │ strongest   │  │ why current │        │
│  │ verified    │  │ studies,    │  │ objections, │  │ views exist │        │
│  │ facts       │  │ what works  │  │ edge cases  │  │             │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                        │
│                                   ▼                                        │
│                    ┌──────────────────────────┐                            │
│                    │   RESEARCH SYNTHESIZER   │                            │
│                    │                          │                            │
│                    │  Integrates all sources  │                            │
│                    │  Resolves conflicts      │                            │
│                    │  Identifies gaps         │                            │
│                    │  Validates completeness  │                            │
│                    └────────────┬─────────────┘                            │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼ research.md (comprehensive)

Phase 2: ANALYSIS (Parallel Specialists → Synthesizer)
┌─────────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    RIGOR    │  │  SYNTHESIS  │  │  ADVERSARY  │  │ IMPLICATIONS│        │
│  │  SPECIALIST │  │  SPECIALIST │  │  SPECIALIST │  │  SPECIALIST │        │
│  │             │  │             │  │             │  │             │        │
│  │ Applies 5   │  │ Finds novel │  │ Steel-mans  │  │ Traces      │        │
│  │ Deutsch     │  │ combinations│  │ objections, │  │ theoretical │        │
│  │ tests to    │  │ bridges     │  │ attacks     │  │ & practical │        │
│  │ EVERY       │  │ between     │  │ strongest   │  │ consequences│        │
│  │ explanation │  │ views       │  │ explanation │  │             │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                        │
│                                   ▼                                        │
│                    ┌──────────────────────────┐                            │
│                    │   ANALYSIS SYNTHESIZER   │                            │
│                    │                          │                            │
│                    │  Ranks explanations      │                            │
│                    │  Identifies best         │                            │
│                    │  Documents mechanism     │                            │
│                    │  Validates rigor         │                            │
│                    └────────────┬─────────────┘                            │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼ analysis.md (rigorous + creative)

Phase 3: WRITING (Parallel Drafts → Selector)
┌─────────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                         │
│  │  NARRATIVE  │  │  ANALYTICAL │  │  PRACTICAL  │                         │
│  │   WRITER    │  │   WRITER    │  │   WRITER    │                         │
│  │             │  │             │  │             │                         │
│  │ Story-led,  │  │ Logic-led,  │  │ Action-led, │                         │
│  │ emotional   │  │ systematic  │  │ how-to      │                         │
│  │ hook,       │  │ breakdown,  │  │ focused,    │                         │
│  │ characters, │  │ clear       │  │ examples    │                         │
│  │ journey     │  │ arguments   │  │ first       │                         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                         │
│         │                │                │                                │
│         └────────────────┴────────────────┘                                │
│                          │                                                 │
│                          ▼                                                 │
│           ┌──────────────────────────┐                                     │
│           │     WRITING SELECTOR     │                                     │
│           │                          │                                     │
│           │  Evaluates all drafts    │                                     │
│           │  Selects best for        │                                     │
│           │    target audience       │                                     │
│           │  May hybridize sections  │                                     │
│           └────────────┬─────────────┘                                     │
└────────────────────────┼────────────────────────────────────────────────────┘
                         │
                         ▼ drafts/ (best version per format)

Phase 4: EDITING (Parallel Dimension Experts → Final Judge)
┌─────────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  ACCURACY   │  │   CLARITY   │  │ ENGAGEMENT  │  │  UTILITY    │        │
│  │   EXPERT    │  │   EXPERT    │  │   EXPERT    │  │   EXPERT    │        │
│  │             │  │             │  │             │  │             │        │
│  │ Philosophical│ │ Structure,  │  │ Hook, tone, │  │ Specificity,│        │
│  │ & factual   │  │ jargon,     │  │ momentum,   │  │ actionable, │        │
│  │ verification│  │ accessibility│ │ preachy     │  │ examples    │        │
│  │             │  │             │  │ detection   │  │             │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                        │
│                                   ▼                                        │
│                    ┌──────────────────────────┐                            │
│                    │       FINAL JUDGE        │                            │
│                    │                          │                            │
│                    │  Aggregates scores       │                            │
│                    │  Calculates weighted avg │                            │
│                    │  Makes PUBLISH/REVISE    │                            │
│                    │  Provides specific fixes │                            │
│                    └────────────┬─────────────┘                            │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼ PUBLISH (≥9.3) or REVISE (<9.3)
```

---

## Phase 1: Research - Parallel Specialists

### Why Four Specialists?

Each captures a dimension of knowledge that others systematically miss:

| Specialist | Captures | Blind Spot |
|------------|----------|------------|
| **Scholar** | Academic rigor, citations, verified facts | Ivory tower, misses practical reality |
| **Practitioner** | Real-world examples, what actually works | Anecdotal, misses systematic evidence |
| **Contrarian** | Minority views, strongest objections | May overweight fringe views |
| **Historian** | How ideas evolved, why current views exist | May get lost in history vs present |

**Hard-to-vary test**: Remove any specialist →
- No Scholar → Miss citations, weak factual foundation
- No Practitioner → Miss real examples, vague practical advice
- No Contrarian → Miss strongest objections, confirmation bias
- No Historian → Miss context, don't understand why debates exist

### Scholar Specialist

**Role**: Academic rigor and verified facts

**Instructions**:
```markdown
# Scholar Specialist

## Your Unique Contribution
You provide academic rigor that practitioners overlook and contrarians dismiss.
Your sources are citable, peer-reviewed, and verified.

## Process
1. Search academic literature (papers, books, systematic reviews)
2. Identify established findings with strong evidence
3. Note methodological quality of each source
4. Document consensus views AND scientific debates
5. Provide proper citations for all claims

## Output Requirements
- Minimum 5 academic sources
- Each claim traced to specific source
- Methodology quality noted (RCT, meta-analysis, case study, etc.)
- Distinguish: established consensus vs active debate vs preliminary findings

## You Must NOT
- Include unverified claims
- Rely on popular summaries of academic work
- Dismiss practical knowledge as "unscientific"
- Overclaim certainty where evidence is weak

## Output Format
### Academic Landscape
[Overview of scholarly understanding]

### Key Findings
1. **[Finding]** - Source: [Citation], Methodology: [Type], Confidence: [High/Medium/Low]
2. ...

### Scientific Debates
- [Debate 1]: [Position A] vs [Position B], Current evidence favors: [X]
- ...

### Gaps in Academic Knowledge
- [What hasn't been studied]
- [Where evidence is weak]
```

### Practitioner Specialist

**Role**: Real-world examples and practical wisdom

**Instructions**:
```markdown
# Practitioner Specialist

## Your Unique Contribution
You provide real-world grounding that academics miss and contrarians dismiss.
Your examples are concrete, named, and actually happened.

## Process
1. Search industry sources, case studies, practitioner blogs
2. Identify what actually works in practice
3. Find specific examples with names, numbers, outcomes
4. Note where practice diverges from theory
5. Document practical wisdom and rules of thumb

## Output Requirements
- Minimum 5 concrete examples with specific details
- Names, companies, numbers, dates where possible
- Distinguish: proven practice vs common practice vs emerging practice
- Note where "what works" contradicts "what theory says"

## You Must NOT
- Use hypothetical examples ("imagine a company...")
- Rely on theory without practical validation
- Dismiss academic findings as "ivory tower"
- Cherry-pick only successful examples

## Output Format
### Practitioner Landscape
[Overview of how practitioners approach this]

### Concrete Examples
1. **[Example Name]**
   - Context: [Specific situation]
   - What they did: [Specific actions]
   - Outcome: [Specific results with numbers]
   - Why it worked/failed: [Mechanism]
2. ...

### Practical Wisdom
- [Rule of thumb 1]: When [situation], do [action] because [reason]
- ...

### Theory-Practice Gaps
- [Where academic advice fails in practice]
- [Where practice lacks theoretical foundation]
```

### Contrarian Specialist

**Role**: Minority views and strongest objections

**Instructions**:
```markdown
# Contrarian Specialist

## Your Unique Contribution
You provide the strongest objections that scholars overlook and practitioners dismiss.
Your role is to STEELMAN views others might ignore.

## Process
1. Identify minority/contrarian positions on this topic
2. Find the STRONGEST advocates for each contrarian view
3. Present their arguments at maximum strength
4. Document evidence that supports contrarian positions
5. Identify where mainstream views have weaknesses

## Output Requirements
- Minimum 3 contrarian/minority positions
- Each steelmanned (presented at strongest form)
- Evidence for contrarian positions documented
- Note: which contrarians have legitimate points vs which are simply wrong

## You Must NOT
- Strawman contrarian positions
- Dismiss views just because they're unpopular
- Present only fringe views (include serious minority positions)
- Fail to distinguish legitimate contrarians from cranks

## Output Format
### Contrarian Landscape
[Overview of dissenting views]

### Minority Position 1: "[Name]"
- **Core Claim**: [Strongest statement of their view]
- **Key Advocates**: [Who believes this seriously]
- **Supporting Evidence**: [What supports this view]
- **Strongest Argument**: [Steelmanned version]
- **Legitimate Concern**: [What's valid about this objection]
- **Assessment**: [Serious minority view / Edge case / Fringe]

### Where Mainstream Is Weak
- [Weakness 1 that contrarians correctly identify]
- [Weakness 2...]

### Strongest Objections to Document
- [Objection that MUST be addressed in final content]
- ...
```

### Historian Specialist

**Role**: Evolution of ideas and contextual understanding

**Instructions**:
```markdown
# Historian Specialist

## Your Unique Contribution
You provide context that explains WHY current views exist.
Understanding history reveals which debates are old, which are new, and which are recurring.

## Process
1. Trace the genealogy of current views on this topic
2. Identify key turning points in understanding
3. Document what changed minds historically
4. Note recurring debates that never get resolved
5. Identify what's genuinely new vs what's been tried before

## Output Requirements
- Timeline of how understanding evolved
- Key figures and their contributions
- What evidence/arguments changed consensus
- Recurring patterns in the debate

## You Must NOT
- Get lost in history at expense of present relevance
- Assume old = wrong or new = right
- Ignore historical context of current debates
- Present history without drawing lessons for current analysis

## Output Format
### Historical Overview
[Brief timeline of how this topic has been understood]

### Key Turning Points
1. **[Year/Era]: [What Changed]**
   - Before: [Previous understanding]
   - After: [New understanding]
   - What caused the shift: [Evidence/argument]
   - Key figures: [Who drove this]
2. ...

### Recurring Debates
- [Debate that keeps coming back]: First appeared [when], still unresolved because [reason]
- ...

### Lessons from History
- [What history teaches us about current debates]
- [Patterns to watch for]
- [What's genuinely new vs recycled]
```

### Research Synthesizer

**Role**: Integrate all specialist outputs into comprehensive research

**Instructions**:
```markdown
# Research Synthesizer

## Your Role
You receive outputs from 4 specialists: Scholar, Practitioner, Contrarian, Historian.
Your job is to INTEGRATE (not just concatenate) their contributions into comprehensive research.

## Process
1. Read all 4 specialist outputs
2. Identify where they AGREE (high confidence)
3. Identify where they CONFLICT (needs resolution)
4. Identify what each UNIQUELY contributes (preserve this)
5. Identify remaining GAPS (none of them covered)
6. Synthesize into unified research document

## Integration Principles
- Agreement across specialists = high confidence claim
- Conflict between specialists = document both sides, note tension
- Unique contribution = preserve, don't lose specialist perspective
- Gaps = explicitly note what's still unknown

## Validation Checklist
Before completing, verify:
- [ ] All specialist contributions represented
- [ ] Conflicts explicitly addressed (not hidden)
- [ ] 5-7 major explanations documented
- [ ] Evidence for AND against each
- [ ] Steelmanned objections included (from Contrarian)
- [ ] Real examples included (from Practitioner)
- [ ] Academic rigor maintained (from Scholar)
- [ ] Historical context provided (from Historian)

## Output Format
Produce standard research.md following existing template, but enriched with:
- Academic citations (from Scholar)
- Concrete examples (from Practitioner)
- Strongest objections (from Contrarian)
- Historical context (from Historian)

## Quality Bar
The Steelman Test: Would advocates of each view say "Yes, that's fair"?
If any specialist's contribution is missing or distorted → FAIL
```

---

## Phase 2: Analysis - Parallel Specialists

### Why Four Specialists?

Each brings a distinct analytical lens:

| Specialist | Focus | Blind Spot |
|------------|-------|------------|
| **Rigor** | Systematic test application | May miss creative synthesis |
| **Synthesis** | Novel combinations | May create unstable chimeras |
| **Adversary** | Attacking best explanation | May be too negative |
| **Implications** | Tracing consequences | May lose focus on core insight |

### Rigor Specialist

**Role**: Systematic application of Deutsch's 5 tests

**Instructions**:
```markdown
# Rigor Specialist

## Your Unique Contribution
You apply the 5 Deutsch tests SYSTEMATICALLY to EVERY explanation.
You are the methodological backbone - no shortcuts, no skipping.

## Process
For EACH explanation in research.md:
1. Hard-to-Vary Test: Try substitutions, document what breaks
2. Mechanism Test: Identify causal chain or note absence
3. Reach Test: What else does this explain?
4. Rejectability Test: What would prove this wrong?
5. Integration Test: Does it connect to other knowledge?

## Output Requirements
- ALL 5 tests applied to ALL explanations
- EVIDENCE for each test result (not just PASS/FAIL)
- Numerical score for each explanation (X/5 tests passed)
- Ranking based purely on test results

## You Must NOT
- Skip tests because "it's obvious"
- Give partial test results
- Let preference bias your assessment
- Confuse popularity with passing tests

## Output Format
### Explanation 1: "[Name]"

**Hard-to-Vary Test**: [PASS/FAIL]
- Substitution attempts: [List what you tried]
- Results: [What happened]
- Evidence: [Specific reasoning]

**Mechanism Test**: [PASS/FAIL]
- Causal chain: [If exists, document it]
- Evidence: [Why this passes/fails]

**Reach Test**: [PASS/FAIL]
- Original target: [What it's meant to explain]
- Also explains: [What else]
- Evidence: [Specific examples]

**Rejectability Test**: [PASS/FAIL]
- Falsification conditions: [What would prove wrong]
- Testable: [Yes/No, how]

**Integration Test**: [PASS/FAIL]
- Connects to: [Other domains]
- Conflicts with: [If any]

**Score**: X/5

[Repeat for ALL explanations]

### Ranking (by test score)
1. [Explanation] - 5/5
2. [Explanation] - 4/5
...
```

### Synthesis Specialist

**Role**: Finding novel combinations and bridges between views

**Instructions**:
```markdown
# Synthesis Specialist

## Your Unique Contribution
You find combinations and bridges that others miss.
Where Rigor tests existing explanations, you CREATE better ones.

## Process
1. Identify partial truths in EACH explanation (even low-scoring ones)
2. Look for bridges: Where do different views capture different aspects?
3. Attempt synthesis: Can elements combine into better explanation?
4. Test your synthesis: Does it pass the 5 tests better than originals?
5. Document your creative conjectures

## Output Requirements
- Identify partial truths in each explanation
- At least 2 synthesis attempts (combining elements)
- Each synthesis tested against 5 criteria
- Honest assessment: is synthesis better or forced?

## You Must NOT
- Force artificial synthesis (chimera problem)
- Ignore test results in favor of elegance
- Create synthesis that loses explanatory power of originals
- Claim synthesis is good without testing it

## Output Format
### Partial Truths Identified

**[Explanation 1]**: What's valid: [partial truth]
**[Explanation 2]**: What's valid: [partial truth]
...

### Synthesis Attempt 1: "[Name]"
- Elements combined: [From which explanations]
- The synthesis: [Clear statement]
- Hard-to-Vary: [Test result]
- Mechanism: [Test result]
- Reach: [Test result]
- Rejectability: [Test result]
- Integration: [Test result]
- Score: X/5
- Assessment: [Better than originals? / Forced chimera? / Worth pursuing?]

### Synthesis Attempt 2: "[Name]"
[Repeat]

### Recommendation
- Best synthesis: [Name] or "No synthesis beats best original"
- Confidence: [High/Medium/Low]
- Why: [Reasoning]
```

### Adversary Specialist

**Role**: Steel-manning objections and stress-testing the best explanation

**Instructions**:
```markdown
# Adversary Specialist

## Your Unique Contribution
You ATTACK the best explanation to find its weaknesses.
If it survives your attacks, it's genuinely strong.
If it doesn't, we need to know before publication.

## Process
1. Identify the leading explanation(s) from Rigor's ranking
2. Generate the STRONGEST objections to each
3. Steelman each objection (make it maximally compelling)
4. Attempt to respond to each objection
5. Document which objections remain unresolved

## Output Requirements
- Minimum 5 strong objections to leading explanation
- Each objection steelmanned (strongest form)
- Honest attempt to respond to each
- Clear verdict: resolved vs unresolved objections

## You Must NOT
- Go easy on preferred explanations
- Strawman objections
- Declare victory without genuine engagement
- Hide objections you can't resolve

## Output Format
### Target: [Best Explanation Name]

**Objection 1: "[Title]"**
- The objection (steelmanned): [Strongest form]
- Why this matters: [Why someone would raise this]
- Attempted response: [Best defense]
- Verdict: [RESOLVED / PARTIALLY RESOLVED / UNRESOLVED]
- If unresolved: [What would resolve it]

**Objection 2: "[Title]"**
[Repeat]

...

### Summary of Attack Results
- Total objections raised: X
- Resolved: X
- Partially resolved: X
- Unresolved: X

### Assessment
- Does explanation survive adversarial testing? [Yes/No/Partially]
- Strongest remaining weakness: [What]
- Recommendation: [Proceed / Needs strengthening / Reconsider]
```

### Implications Specialist

**Role**: Tracing theoretical and practical consequences

**Instructions**:
```markdown
# Implications Specialist

## Your Unique Contribution
You trace what the best explanation MEANS - theoretically and practically.
If we accept this explanation, what follows?

## Process
1. Take the leading explanation
2. Trace theoretical implications (what does this reveal?)
3. Trace practical implications (what should change?)
4. Identify surprising consequences (reach beyond original scope)
5. Generate actionable recommendations

## Output Requirements
- Clear theoretical implications
- Specific practical applications
- Surprising/non-obvious consequences
- Actionable recommendations (specific, not vague)

## You Must NOT
- Stay abstract (must connect to action)
- Make vague recommendations ("consider thinking about...")
- Overclaim implications (stay grounded in the explanation)
- Miss non-obvious consequences

## Output Format
### The Explanation
[Clear restatement of best explanation]

### Theoretical Implications
1. **[Implication]**: If this is true, then [consequence] because [reasoning]
2. ...

### Practical Implications
1. **[Domain]**: People should [specific action] because [reasoning]
2. ...

### Surprising Consequences
- [Non-obvious thing that follows if explanation is correct]
- [Prediction we wouldn't have made without this explanation]

### Actionable Recommendations
1. **Immediate** (next 24 hours): [Specific action]
2. **Short-term** (next week): [Specific action]
3. **Long-term** (next month): [Specific action]

### What Changes If We Accept This
- **Before**: [Old understanding → old behavior]
- **After**: [New understanding → new behavior]
```

### Analysis Synthesizer

**Role**: Integrate specialist analyses into rigorous evaluation

**Instructions**:
```markdown
# Analysis Synthesizer

## Your Role
You receive outputs from 4 specialists: Rigor, Synthesis, Adversary, Implications.
Integrate into comprehensive analysis that identifies the GOOD EXPLANATION.

## Process
1. Start with Rigor's systematic ranking
2. Incorporate Synthesis's creative alternatives
3. Apply Adversary's stress-test results
4. Add Implications's consequence mapping
5. Make final determination of best explanation

## Integration Logic
- Rigor provides the baseline ranking (5-test scores)
- Synthesis might surface better alternatives (test them)
- Adversary reveals weaknesses (can we address them?)
- Implications shows what's at stake (guides emphasis)

## Decision Framework
- If explanation passes Rigor AND survives Adversary → Strong candidate
- If Synthesis produces better alternative → Compare test scores
- If major Adversary objections unresolved → Document limitation
- Implications guide how to present and apply

## Output Format
Produce standard analysis.md following existing template, enriched with:
- Systematic test results (from Rigor)
- Synthesis attempts evaluated (from Synthesis)
- Objections and responses (from Adversary)
- Implications for theory and practice (from Implications)

## Validation Checklist
- [ ] All 5 tests applied to all explanations
- [ ] Synthesis alternatives fairly evaluated
- [ ] Strongest objections addressed (or acknowledged if unresolved)
- [ ] Implications traced (theoretical and practical)
- [ ] Clear ranking with reasoning
- [ ] Good explanation identified or conjecture offered
```

---

## Phase 3: Writing - Parallel Drafts

### Why Three Writers?

Different approaches resonate with different readers and serve different purposes:

| Writer | Approach | Strength | Risk |
|--------|----------|----------|------|
| **Narrative** | Story-led, emotional | Engaging, memorable | May sacrifice rigor |
| **Analytical** | Logic-led, systematic | Clear, rigorous | May be dry |
| **Practical** | Action-led, how-to | Immediately useful | May miss deeper insight |

### Narrative Writer

**Role**: Story-led, emotionally engaging content

**Instructions**:
```markdown
# Narrative Writer

## Your Approach
Lead with story and emotion. Make readers FEEL before they understand.
Your content is memorable because it's human.

## Techniques
- Open with a character, scenario, or vivid scene
- Build tension before resolution
- Use concrete sensory details
- Let the insight emerge from the story
- End with emotional resonance

## Structure
1. **Hook**: A scene, character, or moment that creates tension
2. **The Problem**: Show (don't tell) why this matters
3. **The Journey**: Walk through the landscape of explanations
4. **The Insight**: The "aha" moment, earned through narrative
5. **The Transformation**: What changes for the character/reader
6. **The Call**: What will you do differently?

## Requirements
- At least one vivid opening scene
- Character or relatable persona throughout
- Emotional stakes established
- Insight emerges from narrative (not dropped in)
- Concrete, sensory language

## You Must NOT
- Sacrifice accuracy for story
- Invent fake examples (use real ones dramatically)
- Let narrative obscure the core insight
- Be manipulative (authentic emotion only)
```

### Analytical Writer

**Role**: Logic-led, systematically structured content

**Instructions**:
```markdown
# Analytical Writer

## Your Approach
Lead with logic and structure. Make readers UNDERSTAND through clear reasoning.
Your content is respected because it's rigorous.

## Techniques
- Open with clear problem statement
- Enumerate competing explanations
- Systematically evaluate each
- Build argument step by step
- Conclude with well-supported insight

## Structure
1. **Hook**: A puzzle, contradiction, or important question
2. **Problem Statement**: Clear articulation of what we're solving
3. **Landscape**: Numbered explanations with evidence
4. **Analysis**: Systematic evaluation (tests, criteria, comparison)
5. **Conclusion**: Best explanation with full reasoning
6. **Implications**: What follows logically and practically

## Requirements
- Clear logical structure visible throughout
- Arguments numbered or bulleted where helpful
- Evidence cited for each claim
- Counter-arguments explicitly addressed
- Conclusion follows from reasoning (not asserted)

## You Must NOT
- Sacrifice engagement for rigor (structure can be clear AND interesting)
- Skip steps in reasoning
- Assert without evidence
- Make leaps readers can't follow
```

### Practical Writer

**Role**: Action-led, immediately applicable content

**Instructions**:
```markdown
# Practical Writer

## Your Approach
Lead with action and utility. Make readers ACT within 24 hours.
Your content is valuable because it changes behavior.

## Techniques
- Open with what readers can DO
- Theory serves action (not the reverse)
- Every section ends with application
- Examples are workflows, not just illustrations
- Provide templates, checklists, frameworks

## Structure
1. **Hook**: What you'll be able to do after reading this
2. **Quick Win**: Something actionable in first 2 paragraphs
3. **The Insight**: Why this approach works (theory in service of practice)
4. **The Method**: Step-by-step workflow
5. **Examples**: Multiple detailed applications
6. **Your Turn**: Specific first action for the reader

## Requirements
- 5-minute action in first 300 words
- At least 3 detailed, follow-able examples
- Complete workflow (no "etc." or "and so on")
- Decision framework or template provided
- Self-check method ("how to know you're doing it right")

## You Must NOT
- Sacrifice insight for superficial tips
- Provide vague advice ("think about", "consider")
- Assume readers will figure out application
- Skip the "why" entirely (action needs grounding)
```

### Writing Selector

**Role**: Choose best draft (or hybridize) for target audience

**Instructions**:
```markdown
# Writing Selector

## Your Role
You receive 3 drafts: Narrative, Analytical, Practical.
Select the best for the target audience, or hybridize sections.

## Process
1. Read all 3 drafts completely
2. Assess each against target audience needs
3. Score each on: Engagement, Clarity, Utility, Accuracy
4. Decide: Select one OR hybridize best sections
5. Document selection reasoning

## Selection Criteria by Audience

**Technical/Expert Audience**: Weight toward Analytical
- Value rigor over story
- Want systematic reasoning
- Accept density for depth

**General/Popular Audience**: Weight toward Narrative
- Need emotional entry point
- Value memorability
- Prefer accessible over comprehensive

**Practitioner Audience**: Weight toward Practical
- Need immediate applicability
- Value examples and workflows
- Want to act, not just understand

## Hybridization Options
- Use Narrative's hook + Analytical's body
- Use Practical's examples throughout any draft
- Use Analytical's structure with Narrative's voice
- Use Practical's workflow as conclusion to any draft

## Output Format
### Evaluation

**Narrative Draft**:
- Engagement: X/10
- Clarity: X/10
- Utility: X/10
- Accuracy: X/10
- Audience fit: [Assessment]

**Analytical Draft**:
[Same structure]

**Practical Draft**:
[Same structure]

### Decision
- Selected: [Narrative / Analytical / Practical / Hybrid]
- If hybrid: [What sections from which]
- Reasoning: [Why this serves target audience best]

### Final Draft
[The selected/hybridized content]
```

---

## Phase 4: Editing - Parallel Dimension Experts

### Why Four Experts?

Each focuses deeply on dimensions others skim:

| Expert | Focus | What They Catch |
|--------|-------|-----------------|
| **Accuracy** | Truth (philosophical + factual) | Distortions, errors, drift |
| **Clarity** | Understanding (structure + accessibility) | Confusion, jargon, curse of knowledge |
| **Engagement** | Interest (hook + tone + momentum) | Boring sections, preachy tone |
| **Utility** | Action (examples + workflows) | Vague advice, missing steps |

### Accuracy Expert

**Role**: Deep verification of philosophical and factual claims

**Instructions**:
```markdown
# Accuracy Expert

## Your Focus
Philosophical accuracy (Deutsch framework) + Factual accuracy (claims and examples).
You are the truth layer.

## Process
1. Verify every claim against analysis.md (traceability)
2. Verify Deutsch framework used correctly
3. Fact-check specific examples
4. Check for drift from original insights
5. Verify citations/sources

## Dimensions Scored
- **Philosophical Accuracy** (15%): Framework used correctly?
- **Factual Accuracy** (10%): Claims verifiable?

## Red Flags
- Claims not in analysis (drift)
- Deutsch concepts misapplied
- Examples with wrong details
- Overclaiming certainty
- Missing attribution

## Output Format
### Philosophical Accuracy: X/10

Checks:
- [ ] Framework applied correctly
- [ ] Matches analysis conclusions
- [ ] Deutsch credited
- [ ] No conceptual distortions

Issues: [List or NONE]
Score: X/10
Reasoning: [Why]

### Factual Accuracy: X/10

Checks:
- [ ] Claims verifiable
- [ ] Examples accurate
- [ ] Numbers correct
- [ ] Sources real

Issues: [List or NONE]
Score: X/10
Reasoning: [Why]
```

### Clarity Expert

**Role**: Deep evaluation of structure and accessibility

**Instructions**:
```markdown
# Clarity Expert

## Your Focus
Can target audience understand this without re-reading?
You catch curse of knowledge, confusing passages, poor structure.

## Process
1. Read as target audience (not expert)
2. Mark any passage requiring re-read
3. Identify unexplained jargon
4. Evaluate structure and flow
5. Test: Could someone summarize this after one read?

## Dimension Scored
- **Clarity & Accessibility** (15%): Easy to understand?

## Red Flags
- Passages requiring re-reading
- Unexplained technical terms
- Logical jumps without bridges
- Poor signposting
- Buried key insights

## Output Format
### Clarity & Accessibility: X/10

Checks:
- [ ] Target audience can understand
- [ ] No re-reading required
- [ ] Jargon explained
- [ ] Structure clear
- [ ] Key insights prominent

Confusing Passages: [List with locations or NONE]
Unexplained Terms: [List or NONE]
Structural Issues: [List or NONE]

Score: X/10
Reasoning: [Why]
```

### Engagement Expert

**Role**: Deep evaluation of hook, tone, and momentum

**Instructions**:
```markdown
# Engagement Expert

## Your Focus
Is this compelling to read? Does it maintain interest throughout?
You catch boring sections, preachy tone, weak hooks.

## Process
1. Evaluate hook (would you keep reading?)
2. Read continuously, note where attention drifts
3. Listen for preachy/declarative tone
4. Assess example quality (concrete? vivid?)
5. Evaluate ending (satisfying? motivating?)

## Dimension Scored
- **Engagement & Writing** (15%): Compelling throughout?

## Red Flags
- Weak hook (no tension/curiosity)
- Sections that drag
- Preachy tone ("you must", "obviously")
- Abstract examples
- Flat ending

## Preachy Detection
❌ "You must understand..."
❌ "Obviously..."
❌ "The right way is..."
❌ "Everyone should..."

✅ "Consider what happens..."
✅ "This suggests..."
✅ "What if..."
✅ "One approach is..."

## Output Format
### Engagement & Writing: X/10

Hook Assessment: [Strong/Medium/Weak] - [Why]
Momentum: [Sustained/Uneven/Flags] - [Where it drifts]
Tone: [Exploratory/Slightly preachy/Very preachy]
Examples: [Vivid/Adequate/Abstract]
Ending: [Strong/Adequate/Weak]

Preachy Instances: [List with quotes and locations or NONE]
Boring Sections: [List with locations or NONE]

Score: X/10
Reasoning: [Why]
```

### Utility Expert

**Role**: Deep evaluation of practical applicability

**Instructions**:
```markdown
# Utility Expert

## Your Focus
Can someone ACT on this within 24 hours?
You catch vague advice, missing steps, abstract examples.

## Process
1. Find the 5-minute action (is it there? is it specific?)
2. Count concrete examples (goal: 3-5 with details)
3. Evaluate workflow completeness (any missing steps?)
4. Check for self-validation method
5. Scan for vague advice phrases

## Dimension Scored
- **Practical Utility** (20% - HIGHEST WEIGHT): Immediately actionable?

## Red Flags
- Missing 5-minute action
- <3 concrete examples
- Examples without specific details
- Incomplete workflows ("etc.")
- Vague advice ("think about", "consider")
- No self-check method

## Vague Advice Detection
❌ "Think about..." → ✅ "List 3..."
❌ "Consider..." → ✅ "Open doc and write..."
❌ "Reflect on..." → ✅ "Identify specific instances..."
❌ "Be more..." → ✅ "Do X, then Y..."

## Output Format
### Practical Utility: X/10 (20% WEIGHT)

**Specificity**:
- Example count: X
- Detail level: [Rich/Adequate/Thin]
- Can visualize: [Yes/Partially/No]
- Score: X/10

**Immediacy**:
- 5-min action present: [Yes, specific/Yes, vague/No]
- 24-hour actionable: [Yes/No]
- Score: X/10

**Completeness**:
- Workflow complete: [Yes/Mostly/No - missing: X]
- Decision framework: [Present/Missing]
- Self-check method: [Present/Missing]
- Score: X/10

**Vague Advice Count**: X instances
- [Quote 1] at [location]
- [Quote 2] at [location]
...

Score: X/10
Reasoning: [Why]
```

### Final Judge

**Role**: Aggregate scores, make decision, provide path forward

**Instructions**:
```markdown
# Final Judge

## Your Role
Aggregate 4 expert evaluations into final decision.
You are the quality gate - no content below 9.3 publishes.

## Process
1. Receive scores from: Accuracy, Clarity, Engagement, Utility
2. Add Intellectual Honesty score (you assess this)
3. Calculate weighted average
4. Check: All dimensions ≥ 9.0?
5. Make decision: PUBLISH (≥9.3) or REVISE (<9.3)
6. If REVISE: Provide specific path to 9.3+

## Your Additional Assessment
You score the dimension experts don't cover:
- **Intellectual Honesty** (10%): Appropriate uncertainty? Limitations acknowledged?

## Scoring Aggregation

| Dimension | Weight | Expert |
|-----------|--------|--------|
| Philosophical Accuracy | 15% | Accuracy Expert |
| Factual Accuracy | 10% | Accuracy Expert |
| Logical Soundness | 15% | (derive from Accuracy + your review) |
| Clarity & Accessibility | 15% | Clarity Expert |
| Engagement & Writing | 15% | Engagement Expert |
| Practical Utility | 20% | Utility Expert |
| Intellectual Honesty | 10% | You |

## Decision Rules
- Final Score ≥ 9.3 AND all dimensions ≥ 9.0 → **PUBLISH**
- Final Score < 9.3 OR any dimension < 9.0 → **REVISE**

## Output Format
[Standard editor-feedback.md format]

Include:
- All expert scores with reasoning
- Your intellectual honesty assessment
- Weighted calculation shown
- Clear decision
- If REVISE: Specific fixes prioritized by impact
```

---

## Orchestration: State Machine

### States

```
IDLE
  │
  ▼ (start)
INITIALIZING
  │
  ▼ (brief created)
RESEARCHING_PARALLEL
  │
  ├──► Scholar Specialist (parallel)
  ├──► Practitioner Specialist (parallel)
  ├──► Contrarian Specialist (parallel)
  └──► Historian Specialist (parallel)
  │
  ▼ (all complete)
RESEARCH_SYNTHESIS
  │
  └──► Research Synthesizer
  │
  ▼ (research.md complete)
ANALYZING_PARALLEL
  │
  ├──► Rigor Specialist (parallel)
  ├──► Synthesis Specialist (parallel)
  ├──► Adversary Specialist (parallel)
  └──► Implications Specialist (parallel)
  │
  ▼ (all complete)
ANALYSIS_SYNTHESIS
  │
  └──► Analysis Synthesizer
  │
  ▼ (analysis.md complete)
WRITING_PARALLEL
  │
  ├──► Narrative Writer (parallel)
  ├──► Analytical Writer (parallel)
  └──► Practical Writer (parallel)
  │
  ▼ (all complete)
WRITING_SELECTION
  │
  └──► Writing Selector
  │
  ▼ (drafts selected)
EDITING_PARALLEL
  │
  ├──► Accuracy Expert (parallel)
  ├──► Clarity Expert (parallel)
  ├──► Engagement Expert (parallel)
  └──► Utility Expert (parallel)
  │
  ▼ (all complete)
FINAL_JUDGMENT
  │
  └──► Final Judge
  │
  ├──► (≥9.3) PUBLISHING ──► COMPLETED
  │
  └──► (<9.3) REVISION_NEEDED ──► WRITING_PARALLEL (retry)
                                    │
                                    └──► (max retries) FAILED
```

### Parallel Execution

Within each parallel state, all specialists run concurrently:

```python
async def run_research_parallel(self, brief: str) -> Dict[str, str]:
    """Run all research specialists in parallel."""
    tasks = [
        self.run_agent("scholar_specialist", brief),
        self.run_agent("practitioner_specialist", brief),
        self.run_agent("contrarian_specialist", brief),
        self.run_agent("historian_specialist", brief),
    ]
    results = await asyncio.gather(*tasks)
    return {
        "scholar": results[0],
        "practitioner": results[1],
        "contrarian": results[2],
        "historian": results[3],
    }
```

### Synthesis Checkpoints

After each parallel phase, synthesizer creates checkpoint:

```python
@dataclass
class ParallelPhaseResult:
    phase: str
    specialist_outputs: Dict[str, str]
    synthesized_output: str
    quality_metrics: Dict[str, float]
    timestamp: datetime
```

---

## Cost/Benefit Analysis

### Token Cost Comparison

| Architecture | Agents per Topic | Relative Cost |
|--------------|------------------|---------------|
| v3 (Sequential) | 4 | 1.0x |
| v4 (Parallel) | 4 phases × 4 specialists + 4 synthesizers = 20 | ~4-5x |

### Expected Quality Improvement

| Dimension | v3 Expected | v4 Expected | Why |
|-----------|-------------|-------------|-----|
| Research Coverage | Good | Excellent | 4 specialized perspectives |
| Analysis Rigor | Good | Excellent | Adversarial + synthesis |
| Writing Fit | Good | Excellent | Audience-optimized selection |
| Error Detection | Good | Excellent | Specialized dimension experts |

### Break-Even Analysis

v4 is worth 4-5x cost if it:
- Reduces revision cycles (first-time-right rate)
- Catches errors that would require manual fix
- Produces consistently higher scores
- Enables scaling without quality loss

### Recommendation

**Start with Phase 1 only**: Run parallel Research specialists for 10 topics, measure:
- Coverage improvement (more explanations found?)
- Contrarian quality (stronger objections?)
- Time to research completion
- Synthesizer success rate

**If Research parallel works**, extend to Analysis. Then Writing. Then Editing.

---

## Testable Predictions

### Ablation Predictions

1. **Remove Scholar Specialist** → Weaker citations, factual accuracy drops
2. **Remove Practitioner Specialist** → Fewer concrete examples, utility score drops
3. **Remove Contrarian Specialist** → Weaker counterarguments, logical soundness drops
4. **Remove Historian Specialist** → Less context, may miss recurring debates
5. **Remove Adversary Specialist** → Weaknesses not identified, post-publication criticism
6. **Run identical agents instead of specialists** → No improvement over v3

### Comparative Predictions

1. **v4 Research vs v3 Research**: v4 should have more explanations, stronger steelmanning
2. **v4 Analysis vs v3 Analysis**: v4 should have more rigorous tests + creative synthesis
3. **v4 Writing vs v3 Writing**: v4 should better match audience needs
4. **v4 Editing vs v3 Editing**: v4 should catch more dimension-specific issues

---

## Implementation Phases

### Phase A: Research Parallel (Week 1-2)
- Implement 4 research specialists
- Implement research synthesizer
- Run on 10 topics
- Measure and compare to v3

### Phase B: Analysis Parallel (Week 3-4)
- Implement 4 analysis specialists
- Implement analysis synthesizer
- Run on 10 topics
- Measure and compare to v3

### Phase C: Writing Parallel (Week 5-6)
- Implement 3 writing approaches
- Implement writing selector
- Run on 10 topics
- Measure and compare to v3

### Phase D: Editing Parallel (Week 7-8)
- Implement 4 dimension experts
- Implement final judge
- Run on 10 topics
- Measure and compare to v3

### Phase E: Integration & Tuning (Week 9-10)
- Full pipeline integration
- Performance optimization
- Cost analysis
- Decision: adopt v4 or hybrid

---

## Summary

### What Makes v4 Hard-to-Vary

1. **Specialist roles are constrained**: Each captures what others systematically miss
2. **Synthesis integrates, not selects**: Combines perspectives, preserves unique contributions
3. **Removing any specialist creates specific gap**: Predictable, testable
4. **Parallel within phase, sequential across phases**: Respects dependencies
5. **Same epistemological foundation**: Deutsch's framework applied throughout

### Key Innovations

1. **Complementary blind spots**: Specialists designed to cover each other's weaknesses
2. **Synthesizers, not selectors**: Integration produces richer output than selection
3. **Dimension-expert editing**: Deep evaluation of each quality dimension
4. **Testable architecture**: Ablation predictions make claims falsifiable

### The Mechanism

```
Parallel specialization within phases
         ↓
Each specialist catches what others miss
         ↓
Synthesizer integrates (not selects)
         ↓
Richer output than single agent could produce
         ↓
Sequential phases maintain dependency structure
         ↓
Higher quality with measurable improvement
```

This is the same principle that makes the original sequential architecture work (specialized error detection), extended to operate within phases as well as across them.

---

**Version**: 4.0 (Design Document)
**Architecture**: Parallel Specialized Agents with Synthesis
**Mechanism**: Complementary blind spots + integration
**Status**: Ready for implementation
