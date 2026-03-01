# Content Factory AGENTS.md

## OVERVIEW
Sequential 4-agent workflow producing world-class explanatory content via David Deutsch's epistemological framework.

## STRUCTURE
- `agents/`: Core logic for Research, Analysis, Writing, and Editing phases.
- `inputs/`: Content briefs and user requirements for each topic.
- `outputs/`: Phase-specific artifacts and approved `/final/` content.
- `src/content_factory/`: Python orchestrator for automated execution.
- `deutsch-framework/`: Reference documents for "Hard-to-Vary" explanations.
- `templates/`: Markdown templates for articles, threads, and posts.

## WHERE TO LOOK
- **Logic**: `src/content_factory/orchestrator.py` manages the agent handoffs.
- **Prompts**: `agents/*-agent-v2.md` contains the primary instructions for LLMs.
- **Quality**: `agents/scoring-rubric.md` defines the 9.3/10 gate criteria.
- **Knowledge**: `CONTENT-CONTEXT.md` tracks explained concepts to prevent repetition.
- **Framework**: `deutsch-framework/explanations.md` defines "Good Explanations."

## CONVENTIONS
- **Sequential Flow**: Mandatory order: Research → Analysis → Writing → Editing.
- **Quality Gate**: Editor has absolute authority; minimum 9.3/10 score to publish to `/final/`.
- **Context Check**: Writer MUST check `CONTENT-CONTEXT.md` and ask user before repeating concepts.
- **Deutschian Tests**: Analyzer applies 5 tests: Hard-to-Vary, Mechanism, Reach, Rejectability, Integration.
- **Socratic Testing**: Vitest tests must verify responses contain questions (no direct answers).
- **Coverage**: Maintain 80% Vitest coverage for all validator logic.
- **Actionable Output**: Must provide specific, immediate steps (e.g., "5-minute action," "decision framework").

## ANTI-PATTERNS
- **Parallel Execution**: Never run agents in parallel; error correction requires sequential criticism.
- **Preachy Tone**: Reject content that lectures; use exploratory, humble language with contractions.
- **Vague Advice**: "Think about X" is a failure; "Apply Y checklist to Z" is required.
- **One-Sidedness**: Rejects any draft lacking 2-3 strong, steelmanned counterarguments.
- **Skipping Phases**: Never jump to Writing without a completed `analysis.md`.
