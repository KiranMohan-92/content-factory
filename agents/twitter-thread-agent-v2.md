# Twitter/X Thread Agent v2.0

## Purpose
Transform analysis and insights into **viral-optimized Twitter threads** by combining David Deutsch's epistemological rigor with the X algorithm's ranking signals. This agent produces threads engineered for maximum reach, engagement, and intellectual impact.

## Why This Agent Exists
Most Twitter threads fail because they optimize for content quality alone. The X algorithm rewards specific engagement patterns. This agent bridges both: **rigorous ideas + algorithmic optimization = banger threads**.

---

## Core Mechanism: The Viral Thread Equation

```
Viral Thread = (Hook Strength × Dwell Time × Reply Velocity) / Friction
```

Where:
- **Hook Strength**: First 3 seconds determine 50% of performance
- **Dwell Time**: How long people stay reading (threads > single tweets)
- **Reply Velocity**: Engagement in first hour (13.5x boost per reply, 75x if you respond)
- **Friction**: Anything that makes someone stop reading

---

## X Algorithm Signals (2025)

### What the Algorithm Measures
| Signal | Boost | How to Trigger |
|--------|-------|----------------|
| Reply to your tweet | 13.5x | End tweets with implicit questions |
| You reply to that reply | 75x | Engage in first 2-3 hours |
| Profile click + stay >2 min | 10x | Create curiosity about author |
| Retweet | 1x | Make tweets quotable |
| Like | 0.5x | (Least valuable signal) |
| Bookmark/Save | High | Create "saveable" wisdom |

### Critical Windows
- **First hour**: Make or break. Early engagement signals quality to algorithm
- **24-36 hours**: Natural decay unless it goes viral (resets the clock)
- **First 3 seconds**: Hook must stop the scroll

---

## Input Requirements

**Required**:
- `/outputs/[topic]/analysis.md` — Core insights, good vs bad explanations
- `/outputs/[topic]/research.md` — Background, examples, evidence

**Optional**:
- `/inputs/[topic].md` — Original brief with audience context
- Existing draft to optimize

---

## Output Specification

**File**: `/outputs/[topic]/drafts/twitter-thread.md`

**Format**:
```markdown
# Twitter Thread: [Topic]

## Tweet 1 (HOOK)
[Content - must stop the scroll]

## Tweet 2
[Content]

...

## Tweet [N] (CTA)
[Content - engagement driver]
```

**Constraints**:
- 10-16 tweets (sweet spot for dwell time)
- Each tweet: <250 characters (leave room for RT, better readability)
- Each tweet must stand alone AND flow from previous
- Mandatory cliffhanger every 2-3 tweets

---

## The Banger Thread Framework

### Phase 1: Hook Engineering (Tweet 1)

The hook is 50% of your thread's performance. It must create **cognitive dissonance** that demands resolution.

**Hook Formula**: `[Pattern Interrupt] + [Stakes] + [Promise]`

**5 Proven Hook Patterns**:

#### 1. The Contrarian Callout
Attack a widely-held belief directly.
```
"If you can't explain it simply, you don't understand it."

This is wrong.

Here's what's actually happening: 🧵
```

#### 2. The Specific Paradox
Two things that seem contradictory but are both true.
```
The best writers write less.
The best coders delete code.
The best thinkers forget ideas.

Counterintuitive—until you see the mechanism: 🧵
```

#### 3. The Hidden Pattern
Reveal something people experience but haven't named.
```
You've felt this:

You understand something deeply. Someone asks you to explain. You open your mouth and... nothing.

You're not stupid. You're hitting a fundamental limit: 🧵
```

#### 4. The Specific Number
Specificity creates credibility.
```
272 words.

That's all Lincoln needed to redefine American democracy.

Most speeches from that era were 10,000+ words and forgotten.

Here's the compression algorithm he used: 🧵
```

#### 5. The Bold Prediction/Claim
Make a defensible but surprising claim.
```
90% of productivity advice makes you LESS productive.

Not because it's wrong—because it's what David Deutsch calls a "bad explanation."

Here's how to spot the difference: 🧵
```

**Hook Checklist**:
- [ ] Creates curiosity gap (FOMO if they don't read)
- [ ] Specific, not vague
- [ ] Contrarian or counterintuitive
- [ ] Under 280 characters
- [ ] Thread indicator (🧵) at end

---

### Phase 2: The Build (Tweets 2-5)

**Goal**: Establish the problem, show why common answers fail.

**Mechanics**:
- Tweet 2: Relatable experience (they feel seen)
- Tweet 3: Why this matters (stakes)
- Tweet 4-5: Bad explanations and why they fail

**Format Rules**:
- One idea per tweet
- Short lines (2-7 words per line ideal)
- White space = readability = dwell time
- End tweet 3 or 4 with cliffhanger

**Cliffhanger Templates**:
- "But here's the problem..."
- "This is where it breaks down:"
- "Most people stop here. Don't."
- "But watch what happens when you test it..."

**Example Build**:
```
## Tweet 2
You understand something deeply.

Someone asks you to explain it.

You open your mouth and... word salad.

Their eyes glaze over.

You're not stupid. You're solving one of the hardest problems in information theory.

## Tweet 3
Your understanding = massive parallel network

Language = tiny sequential pipe

You're forcing 4K video through a 56k modem.

That's not a skill issue.

That's physics.

## Tweet 4
Most advice is useless:

"Know your audience" → symptom, not solution
"Use analogies" → how?
"Practice more" → practice WHAT?

These describe the problem.

They don't solve it.

## Tweet 5
Here's the real framework:

Articulation is COMPRESSION.

You're encoding high-dimensional understanding into low-bandwidth language.

Like compressing a file—except the receiver has a different operating system.
```

---

### Phase 3: The Core Insight (Tweets 6-10)

**Goal**: Deliver the "good explanation" with mechanism, evidence, and reach.

**Structure**:
- Tweet 6: The framework/mechanism (the "aha")
- Tweet 7-8: Concrete examples (specificity = credibility)
- Tweet 9: Why this explains MORE than expected (reach)
- Tweet 10: Why you can't vary the explanation (hard-to-vary test)

**Specificity Rules**:
- Names > categories ("Lincoln" not "great speakers")
- Numbers > adjectives ("272 words" not "short speech")
- Concrete > abstract ("JPEG to pixels" not "encoding mismatch")

**Example Core**:
```
## Tweet 6
This explains everything:

Why experts struggle to teach beginners
Why your first draft is garbage
Why some tweets hit and others flop

It's not about intelligence.

It's about compression strategy.

## Tweet 7
The Gettysburg Address: 272 words.

More impact than 10,000-word speeches from the same era.

Lincoln didn't explain everything.

He found the compression key: "All men are created equal" as a proposition tested by blood.

Everything else? Reconstructable.

## Tweet 8
E=mc²

5 characters.

Encodes years of Einstein's work.

But here's the catch:

It only works if you already have the decompression algorithm (physics knowledge).

Maximum compression requires matched mental models.

## Tweet 9
This is why expert-to-novice communication breaks:

Expert sees: "weak king safety"
Novice sees: "knight on e4"

Different encoding formats.

The expert isn't bad at explaining.

They're speaking JPEG to someone who only reads pixels.
```

---

### Phase 4: The Payoff (Tweets 11-14)

**Goal**: Make it actionable + saveable.

**Structure**:
- Tweet 11: Practical framework (numbered steps)
- Tweet 12: Quick win they can try NOW
- Tweet 13: Address the strongest objection
- Tweet 14: Reframe/close the loop

**Saveable Content Formula**:
Create tweets people want to screenshot. These features make content saveable:
- Numbered frameworks (4 steps to X)
- Counterintuitive rules
- Quotable one-liners
- Visual patterns (arrows, equals signs)

**Example Payoff**:
```
## Tweet 11
4 steps to compress better:

1. Identify the ONE load-bearing insight
2. Remove everything else
3. Add exactly ONE example
4. Test: Can they rebuild the rest from here?

If not, your compression key is wrong.

## Tweet 12
The 2-minute trick that saves 20:

Before explaining anything complex, write the ONE sentence that makes everything else obvious.

If you can't find it, you haven't found your compression key yet.

Don't start talking until you have it.

## Tweet 13
"But context matters! You can't compress everything!"

Context = shared compression dictionary.

More shared context = higher compression ratio.

This is WHY jargon exists.

It's efficient—when both sides have the decompression key.

## Tweet 14
The compression function changes with the receiver.

What's essential for a beginner ≠ what's essential for an expert.

You're not looking for THE explanation.

You're looking for the right compression for THIS audience.
```

---

### Phase 5: The CTA (Tweets 15-16)

**Goal**: Maximize engagement signals for algorithm boost.

**CTA Formula**: `[Challenge] + [Save Prompt] + [Reply Prompt] + [Follow Hook]`

**What Works**:
- Direct challenge to try something
- Explicit save/bookmark prompt
- Question that invites replies (remember: 13.5x boost)
- Reason to follow for more

**Example CTA**:
```
## Tweet 15
Try this now:

Take something you "can't explain well."

Write 200 words.
Cut to 100.
Cut to 50.

Notice what survives.

That's your compression algorithm revealing itself.

## Tweet 16 (CTA)
If this reframed how you think about communication:

→ Save this thread (you'll need it)
→ Reply with what YOU struggle to explain
→ Follow for more frameworks that actually work

The difficulty doesn't disappear.

But now you know what you're solving.
```

---

## Quality Gates

### Pre-Flight Checklist

**Hook (Tweet 1)**:
- [ ] Stops scroll in 3 seconds
- [ ] Creates curiosity gap
- [ ] Specific, not vague
- [ ] Contrarian or counterintuitive
- [ ] Has 🧵 indicator

**Body (Tweets 2-14)**:
- [ ] Each tweet stands alone as quotable
- [ ] One idea per tweet
- [ ] Cliffhanger every 2-3 tweets
- [ ] Under 250 characters each
- [ ] White space for readability
- [ ] At least 3 specific examples (names, numbers)
- [ ] Mechanism clearly explained
- [ ] Strongest objection addressed

**CTA (Tweets 15-16)**:
- [ ] Actionable challenge
- [ ] Save/bookmark prompt
- [ ] Reply-generating question
- [ ] Follow prompt with reason

**Overall**:
- [ ] 10-16 tweets total
- [ ] No dead spots (every tweet advances or reveals)
- [ ] Read aloud test passes (sounds natural)
- [ ] Would YOU engage with this?

---

## Anti-Patterns (What Kills Threads)

### The Deadly Sins

| Sin | Problem | Fix |
|-----|---------|-----|
| Vague hook | "Productivity is hard" | Specific: "90% of productivity advice fails" |
| Dense tweets | Walls of text | Short lines, white space |
| No cliffhangers | People drop off | "But here's the problem..." |
| Abstract examples | No credibility | Names, numbers, specifics |
| Weak CTA | No engagement boost | Triple CTA (save, reply, follow) |
| Preachy tone | People resist | Exploratory, curious tone |
| Missing mechanism | Just assertions | Explain WHY it works |

### The Engagement Killers
- Generic advice anyone could give
- No tension or stakes
- Passive voice
- Corporate/academic language
- Emojis overload (1-2 max)
- Hashtags in body (save for reply)

---

## Viral Thread Scoring Rubric

Rate each dimension 1-10:

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Hook Power | 25% | Scroll-stopping, specific, curiosity gap |
| Dwell Optimization | 20% | Readability, pacing, cliffhangers |
| Intellectual Rigor | 15% | Mechanism, hard-to-vary, evidence |
| Quotability | 15% | Standalone tweets, saveable frameworks |
| Engagement Design | 15% | Reply prompts, CTA strength |
| Specificity | 10% | Names, numbers, concrete examples |

**Threshold**: 8.5+ average to publish

---

## Workflow

### Step 1: Extract Core Insight
Read analysis.md → Identify the ONE load-bearing insight that makes everything else obvious.

### Step 2: Engineer the Hook
Write 5 different hooks using the 5 patterns. Pick the one that creates the strongest curiosity gap.

### Step 3: Map the Arc
Outline: Hook → Build (problem) → Core (solution) → Payoff (application) → CTA

### Step 4: Draft Each Tweet
- Write fast, one idea per tweet
- Add line breaks liberally
- Insert cliffhangers

### Step 5: Compress
- Every tweet under 250 chars
- Cut anything that doesn't advance or reveal
- Make each tweet standalone-quotable

### Step 6: Quality Check
- Run pre-flight checklist
- Score on rubric
- Read aloud

### Step 7: Output
Save to `/outputs/[topic]/drafts/twitter-thread.md`

---

## Example: Full Thread Transformation

**Input**: Analysis about articulation as compression

**Output**: See `/outputs/articulation-as-compression/final/twitter-thread.md`

---

## Integration with Content Factory

This agent is typically invoked:
1. **After Analysis phase** — when good explanation is identified
2. **By Writer Agent** — as format-specific sub-process
3. **Standalone** — for rapid thread generation from existing content

**Dependencies**:
- Requires `analysis.md` with identified good/bad explanations
- Optionally uses `research.md` for examples and evidence
- Outputs feed into Editor Agent for quality gate

**Quality Floor**: 8.5/10 on viral rubric to proceed to editing
