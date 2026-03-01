# How the Content Factory Agentic Workflow Works
## A Complete Guide to Creating Quality Content Through Systematic Error Correction

---

## The Problem with "Just Ask AI"

You've probably done this: opened Claude, typed a topic, and asked for an article. Minutes later, you have 1000 words of seemingly sophisticated content. Done, right?

Not quite.

Here's what's missing: **systematic error correction**. That single-shot content might have:
- Factual errors you didn't catch
- Logical fallacies you didn't notice
- Bad explanations that sound plausible
- Blind spots you share with the AI
- Arbitrary claims with no grounding

A skilled human editor would catch these. But you're not a skilled editor in every domain. And neither is AI, despite its sophistication.

**This is where the Content Factory's agentic workflow comes in.**

It's not just a process—it's a good explanation of how to create quality content. By "good explanation," I mean one that's hard to vary, has a clear mechanism, and actually tells you *why* it works, not just *what* to do.

Let me show you how it works, why it's designed this way, and how to use it effectively.

---

## The Core Insight: Quality Comes from Error Elimination

David Deutsch, in *The Beginning of Infinity*, explains that knowledge grows not through certainty or proof, but through **conjecture and criticism**. You create explanations (conjectures), criticize them systematically, eliminate errors, and iterate. What survives criticism is closer to truth—not proven, but less wrong.

The Content Factory embodies this principle.

Instead of trying to create perfect content in one shot (impossible), it creates a system for **systematic error elimination**:

1. **Researcher Agent** — Gathers competing explanations and evidence
2. **Analyzer Agent** — Criticizes explanations systematically using Deutsch's framework
3. **Writer Agent** — Translates analysis into accessible content
4. **Editor Agent** — Catches remaining errors and enforces quality standards

Each agent is a specialized error-detection system. Each catches specific error types that previous agents either create or can't see.

The magic isn't in any single agent—it's in the **sequential structure** that enables cumulative error correction.

---

## Why This Order? Why Not Parallel?

Here's a crucial insight: **The sequence is not arbitrary.**

You might think: "Why not run all agents in parallel for speed? Why not combine agents for efficiency?"

The answer lies in dependencies.

### The Dependency Chain

**Analyzer needs Researcher's output**:
- Can't evaluate explanations you haven't documented
- Can't criticize views you don't understand
- Can't identify patterns you haven't surveyed

**Writer needs Analyzer's output**:
- Can't write compellingly about insights you haven't identified
- Can't explain mechanisms you haven't understood
- Can't show why one explanation is better without systematic evaluation

**Editor needs Writer's output**:
- Can't review content that hasn't been written
- Can't check clarity without seeing how analysis was communicated
- Can't enforce format standards without drafts

Try to reverse the order, and you'll find yourself stuck:
- Edit before writing? Nothing to edit.
- Write before analysis? No insight to communicate.
- Analyze before research? No explanations to evaluate.

**The structure is constrained by what each agent produces and requires.** That's what makes it "hard to vary"—it's not a preference, it's causal.

### Why Not Parallel?

Parallel sounds efficient: run all agents at once, combine results. But parallel structure breaks the error-correction mechanism.

Error correction requires **criticism**, which requires **completed work to criticize**.

If agents work simultaneously:
- They can't critique each other's work
- They can't build on previous insights
- They can't catch each other's errors
- Knowledge doesn't compound—it just accumulates

Think about software development: you don't write code, compile, and test *in parallel*. You can't test code that hasn't been written. You can't compile code that hasn't been designed. Dependencies matter.

The same applies here.

---

## The Four Agents: What Each Does and Why

### Agent 1: The Researcher

**Role**: Map the landscape of existing explanations

**What It Does**:
- Identifies the problem or topic clearly
- Documents 5-7 major competing explanations
- Gathers evidence for and against each
- Identifies gaps, contradictions, patterns
- Notes prevalence and advocates for each view

**Why It's Necessary**:

You can't evaluate explanations you don't know about. You can't criticize what you haven't fairly represented.

Without research:
- You'll strawman opposing views (representing them weakly)
- You'll miss the strongest counterarguments
- You'll reinvent wheels instead of building on existing work
- Your analysis will be biased toward your pre-existing views

**Example** (from the goal-setting-frameworks project):
The Researcher documented 6 frameworks—SMART goals, OKRs, 12-Week Year, WOOP, Commando Planning, GTD. For each:
- Core claims
- Supporting evidence
- Why people believe it
- Where it fails
- How prevalent it is

This gave the Analyzer a comprehensive landscape to evaluate, not just "my opinion about goal-setting."

**Error Type Prevented**: Ignorance, bias, strawmanning, cherry-picking

---

### Agent 2: The Analyzer

**Role**: Apply David Deutsch's philosophical framework systematically to evaluate explanations

**What It Does**:

For each explanation, applies **five tests**:
1. **Hard-to-Vary Test**: Can you swap components arbitrarily without losing explanatory power?
2. **Mechanism Test**: Does it explain *how* (causal mechanism) or just *what*?
3. **Reach Test**: Does it explain more than intended?
4. **Rejectability Test**: What would show it's wrong? Is it testable?
5. **Integration Test**: Does it connect to other good explanations?

Then:
- Identifies or creates a "good explanation" (hard to vary, mechanistic, with reach)
- Applies Deutsch's problem-solving framework (problems inevitable/soluble)
- Identifies theoretical and practical implications
- Shows what becomes possible with better understanding

**Why It's Necessary**:

Without systematic analysis, evaluation is arbitrary. "I like this framework better" isn't an explanation—it's a preference.

The Analyzer provides **criteria** for evaluating explanations. Not just opinions, but reasons grounded in epistemology.

**Example** (from goal-setting-frameworks):
Applied hard-to-vary test to SMART goals: found you could swap the letters (Specific → Detailed, Measurable → Trackable, etc.) without changing explanatory power. This means SMART is "easy to vary"—a procedural checklist, not an explanation of why goals succeed or fail.

The Analyzer then identified a better explanation: Goal achievement isn't about frameworks, it's about understanding change and applying conjecture-and-criticism to your own efforts.

**Error Type Prevented**: Arbitrary preferences, bad explanations, superficial analysis, missing philosophical grounding

---

### Agent 3: The Writer

**Role**: Translate philosophical analysis into compelling, accessible content across formats

**What It Does**:
- Absorbs the analysis and identifies core insights
- Finds the hook, the "aha" moment, the emotional core
- Creates drafts for multiple formats:
  - Long-form articles (2000-4000 words)
  - Twitter/X threads (8-12 tweets)
  - LinkedIn posts (professional framing)
  - Newsletters, video scripts, podcast notes
- Optimizes for engagement while maintaining accuracy
- Uses concrete examples, clear structure, memorable language

**Why It's Necessary**:

Good analysis is often dense and inaccessible. If only philosophers can understand it, your insight doesn't spread.

The Writer makes analysis **available** to real humans on real platforms.

Without this phase:
- You'd publish raw analysis (too dense for general audience)
- You'd lose engagement (boring, academic tone)
- You'd miss platform-specific best practices (article-style content in tweets doesn't work)

**Example** (from goal-setting-frameworks):
- **Article**: Full 2000-word explanatory arc from "why do frameworks fail?" to "here's a better understanding of change"
- **Twitter thread**: 10-tweet version with hook about SMART goals' failure
- **LinkedIn post**: Professional framing about organizational goal-setting

Same core insight, three different packages—each optimized for its platform.

**Error Type Prevented**: Inaccessibility, poor engagement, format mismatches, losing general audience

---

### Agent 4: The Editor

**Role**: Final quality assurance—catch all remaining errors before publication

**What It Does**:

**Six-pass review**:
1. **Philosophical Accuracy**: Does content reflect analysis correctly? Are Deutsch concepts used precisely?
2. **Factual Accuracy**: Verify all claims, check sources, confirm quotes
3. **Logical Coherence**: Are arguments valid? Any fallacies? Counterarguments addressed?
4. **Clarity**: Would target audience understand? Technical terms explained?
5. **Engagement**: Does hook work? Does content hold attention? Strong ending?
6. **Format & Style**: Platform requirements met? No typos? Consistent voice?

Then makes a decision:
- **Publish as-is** (meets all standards)
- **Minor revisions** (small fixes, <30 min)
- **Major revision** (substantive rewrite)
- **Return to Analysis** (fundamental issues, restart)

**Why It's Necessary**:

Writers have blind spots. We know what we meant to say, so we don't see where it's unclear. We become fond of our own phrasings. We overlook our own errors.

The Editor is the **last line of defense** and the **reader's advocate**.

**Example** (from goal-setting-frameworks):
- Caught overstatement ("proves" → "suggests")
- Requested example clarification (vague reference made specific)
- Verified adoption statistics
- Confirmed Deutsch framework applied accurately
- Approved after minor revisions

**Error Type Prevented**: Factual errors, logical fallacies, unclear writing, unnoticed blind spots, quality drift

---

## Why This Structure Works: The Mechanism

Let's get specific about *how* this produces quality.

### Specialization Enables Error Detection

Each agent optimizes for a specific type of error detection:

- **Researcher**: Optimizes for comprehensive, fair representation (catches bias, ignorance)
- **Analyzer**: Optimizes for philosophical rigor (catches bad explanations, arbitrary claims)
- **Writer**: Optimizes for accessibility and engagement (catches inaccessibility, format issues)
- **Editor**: Optimizes for catching everything previous agents missed (catches blind spots, errors)

If one person did all four roles simultaneously, they'd make tradeoffs:
- Research comprehensiveness vs. time
- Analytical depth vs. accessibility
- Rigor vs. engagement

By specializing, each agent can **maximize** its dimension without compromise.

### Sequential Structure Enables Cumulative Error Correction

Here's the key: **Each agent improves on previous work.**

```
Research (has errors: bias, gaps)
    ↓ [criticized by]
Analysis (catches research errors, adds philosophical rigor)
    ↓ [has errors: may be inaccessible, dense]
Writing (catches accessibility issues, optimizes communication)
    ↓ [has errors: may distort analysis, miss edge cases]
Editing (catches writing errors, verifies accuracy, enforces standards)
    ↓
Quality Content (errors minimized through multiple rounds of criticism)
```

Each agent acts as a **critic** of previous work. This is Popperian error elimination in action.

If you combined agents (e.g., Research + Analysis), you'd lose this criticism:
- Confirmation bias: find research that supports your analysis
- No fresh perspective to catch your blind spots
- Tradeoffs between depth and breadth

If you ran agents in parallel:
- Can't critique what hasn't been completed
- Can't build on insights not yet identified
- Errors compound instead of being corrected

### Editor Authority Prevents Quality Drift

Without enforcement, quality standards become suggestions. "Good enough" becomes the standard.

The Editor has **veto power**: can require additional research, request different angle, send back for major revision, or reject entirely.

This creates a quality gate: **nothing published without passing standards.**

Over time, this prevents quality drift—the gradual erosion of standards that happens when no one enforces them.

---

## This Workflow Is a "Good Explanation"

Using Deutsch's own criteria:

### 1. Hard to Vary ✓

The structure is constrained by dependencies:
- Change the order → breaks dependencies
- Remove an agent → specific errors go uncaught
- Combine agents → lose specialization and criticism
- Skip quality gates → errors slip through

It's not arbitrary—it follows from the mechanism of error correction.

### 2. Has a Mechanism ✓

The mechanism is **sequential, specialized error correction**:
- Specialization → better error detection for specific types
- Sequential structure → enables criticism of previous work
- Multiple agents → catch different error types
- Quality enforcement → prevents drift

This explains *how* quality emerges, not just *what* to do.

### 3. Has Reach ✓

Designed for content creation, but explains:
- Why peer review works (specialized criticism)
- Why code review catches bugs (fresh perspective)
- Why manufacturing has quality gates (sequential error detection)
- Why science uses observation → hypothesis → test → review
- Why "move fast and break things" creates quality problems (skips error correction)

The pattern appears wherever quality matters and errors are costly.

### 4. Testable (Rejectability) ✓

Makes risky predictions:
- Full workflow will have fewer errors than single-shot AI (testable)
- Skipping agents will produce specific error types (testable)
- Parallel structure will reduce quality (testable)
- Combined agents will catch fewer errors (testable)

Could be shown wrong if these predictions fail.

### 5. Integrates with Other Knowledge ✓

Consistent with:
- Popper's epistemology (error elimination)
- Cognitive science (blind spots, bias)
- Software engineering (separation of concerns, code review)
- Manufacturing (quality control at multiple stages)
- Economics (early error detection is cheaper)

Not isolated—connects to multiple domains of knowledge.

---

## How to Use This Workflow: Practical Guidance

### Running a Content Project

**Step 1: Create Input Brief** (`/inputs/[topic].md`)

Specify:
- Problem or topic to explore
- Target audience
- Desired output formats
- Any specific angles or constraints

**Step 2: Invoke Researcher Agent**

Give it the brief. Ask it to:
- Find 5-7 competing explanations
- Gather evidence for/against each
- Identify gaps and contradictions
- Create research.md file

**Step 3: Invoke Analyzer Agent**

Give it the research. Ask it to:
- Apply five tests to each explanation
- Identify or create good explanation
- Apply Deutsch's problem-solving framework
- Identify implications
- Create analysis.md file

**Step 4: Invoke Writer Agent**

Give it the analysis. Ask it to:
- Create drafts in requested formats
- Optimize for each platform
- Maintain philosophical accuracy
- Use concrete examples
- Create draft files (article.md, twitter-thread.md, etc.)

**Step 5: Invoke Editor Agent**

Give it all drafts plus original research and analysis. Ask it to:
- Review against quality standards (six-pass review)
- Check philosophical accuracy, facts, logic, clarity, engagement, format
- Provide detailed feedback or approve
- Create editor-feedback.md or final/ directory

**Step 6: Iterate if Needed**

If Editor requests revisions:
- Make changes as specified
- Re-submit to Editor
- Repeat until approved

### Common Mistakes to Avoid

**Mistake 1: Skipping Research**

"I already know the landscape."

**Why it's a problem**: You have bias. You'll strawman opposing views. You'll miss strong counterarguments.

**Fix**: Always run Researcher phase, even on familiar topics. Document what you think you know, then verify.

**Mistake 2: Rushing Analysis**

"Let's just apply the framework quickly."

**Why it's a problem**: Mechanical application without insight produces superficial content. Defeats the purpose.

**Fix**: Take time with Analysis. Apply tests rigorously. Look for genuine insights, not just checking boxes.

**Mistake 3: Writing Before Analysis**

"I'll figure it out as I write."

**Why it's a problem**: Results in arbitrary claims, weak logic, no philosophical grounding. You'll make it up as you go.

**Fix**: Don't start writing until Analysis is complete. Know your good explanation first.

**Mistake 4: Skipping Editor**

"Looks good to me."

**Why it's a problem**: You can't see your own blind spots. Errors will slip through. Quality will drift.

**Fix**: Always run Editor phase. Give Editor real authority. Accept revision requests.

**Mistake 5: Combining Agents for Speed**

"I'll research and analyze at the same time."

**Why it's a problem**: Confirmation bias, no fresh perspective, no error correction, combined blind spots.

**Fix**: Keep agents separate. Let each complete before starting next. Trust the sequential structure.

---

## Why This Matters: What You Gain

### For Content Quality

- **Fewer errors**: Multiple layers of error detection
- **Better explanations**: Systematic application of Deutsch's criteria
- **Greater reach**: Accessible to general audience while maintaining rigor
- **Consistency**: Quality standards enforced systematically

### For Your Understanding

- **Deeper insight**: Systematic analysis forces you to understand, not just opine
- **Clearer thinking**: Making explanations explicit clarifies your own thoughts
- **Better criticism**: Learning to criticize systematically improves all thinking
- **Pattern recognition**: Seeing Deutsch's principles in action builds intuition

### For Scaling

- **Reproducible**: Same process works across topics
- **Teachable**: Clear methodology can be learned
- **Systematic**: Doesn't depend on inspiration or genius
- **Improvable**: Process can be refined based on results

---

## Beyond Content: The Template for Knowledge Creation

Here's the deepest insight: **This workflow is a template for any knowledge-creation system where quality matters.**

The pattern:
1. Identify what quality means in your domain
2. Identify error types that prevent quality
3. Create specialized roles for catching each error type
4. Structure sequence based on dependencies
5. Separate creation from criticism
6. Enforce quality standards

**Examples of the same pattern**:

**Software Development**:
- Requirements (Research) → Design (Analysis) → Implementation (Writing) → Code Review + Testing (Editing)
- Sequential, specialized error correction

**Scientific Research**:
- Observation (Research) → Hypothesis (Analysis) → Experiment (Writing) → Peer Review (Editing)
- Sequential, specialized error correction

**Product Development**:
- User Research → Design → Prototype → Testing & Iteration
- Sequential, specialized error correction

**Legal Work**:
- Investigation → Case Building → Argument Preparation → Review
- Sequential, specialized error correction

Wherever you need to create knowledge and minimize errors, you see this structure emerge. **Why?** Because it's a good explanation of how error correction works.

---

## Final Thoughts: Quality Through Error Elimination

The traditional view of quality is that it comes from talent, inspiration, or genius. Great content comes from great writers having great ideas.

The Deutschian view is different: **Quality comes from error elimination.**

You start with conjectures (any will do). You criticize them systematically. You eliminate errors. You iterate. What survives is closer to truth—not perfect, not proven, but less wrong.

The Content Factory's agentic workflow embodies this principle. It doesn't try to create perfection from the start (impossible). It creates a system for **systematic error correction**.

Four agents. Four specialized error-detection functions. One sequential structure that enables cumulative error elimination.

Simple in concept. Powerful in execution. Grounded in philosophy. Applicable far beyond content creation.

That's how you turn knowledge creation into a systematic process. Not by avoiding errors (impossible), but by catching them before they reach your audience.

---

## Getting Started

**Your Next Steps**:

1. **Read the system documentation**: Start with `/content-factory/CLAUDE.md`
2. **Review the example**: Check `/content-factory/outputs/goal-setting-frameworks/` to see the full workflow
3. **Create an input brief**: Pick a topic and create `/content-factory/inputs/[your-topic].md`
4. **Run the workflow**: Invoke each agent in sequence
5. **Learn from results**: See what works, what doesn't, refine your process

**Remember**:
- Follow the sequence (don't skip phases)
- Let each agent specialize (don't combine roles)
- Trust the process (quality emerges through iteration)
- Use Editor authority (accept revision requests)
- Apply quality standards rigorously

Quality isn't magic. It's systematic error elimination.

Now you know how.

---

*This guide was created using the Content Factory's own workflow—research, analysis, writing, and editing phases all applied to document the workflow itself. Meta, but effective.*
