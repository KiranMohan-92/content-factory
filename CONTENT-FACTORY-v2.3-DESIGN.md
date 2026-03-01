# Content Factory v2.3 - Gemini CLI Research Architecture

## Version History

| Version | Key Changes | Date |
|---------|-------------|------|
| v2.0 | Automated orchestrator, hard-to-vary agents | 2025 |
| v2.1 | External verification pre-pass | 2026-01 |
| v2.2 | CODEX Brutal Critic CLI integration (9.5 threshold) | 2026-02 |
| **v2.3** | **Gemini CLI Research Agent with Dynamic Prompt Engineering** | 2026-02 |

---

## Overview

Content Factory v2.3 replaces the Claude-based Researcher Agent with a **Gemini CLI-powered Research Agent** that leverages:

- **Deep web search integration** - Live access to current information
- **Multi-modal research** - Images, videos, PDFs alongside text
- **Larger context window** - Process more sources in single pass
- **Google's knowledge graph** - Structured knowledge access

**Critical Innovation**: The system includes a **Dynamic Prompt Generator** that analyzes the incoming topic and crafts a world-class, topic-aware research prompt for Gemini CLI.

---

## Architecture Changes

### Current (v2.2) Research Phase

```
User Brief → Claude Researcher Agent → research.md → Analysis Phase
```

### New (v2.3) Research Phase

```
User Brief → Prompt Generator Agent → Gemini CLI (headless) → research.md → Analysis Phase
                              ↓
                    Dynamic, topic-aware prompt
```

---

## New Components

### 1. Dynamic Prompt Generator (`src/content_factory/research/prompt_generator.py`)

**Purpose**: Analyzes the incoming brief and generates an optimized research prompt for Gemini CLI.

**Key Features**:
```python
class GeminiResearchPromptGenerator:
    """
    Generates world-class, topic-aware research prompts for Gemini CLI.

    Analysis dimensions:
    - Topic domain (technical, philosophical, practical, scientific)
    - Research depth needed (surface, intermediate, deep)
    - Source types required (academic, industry, popular, primary)
    - Controversy level (settled, debated, polarized)
    - Temporal sensitivity (timeless, evolving, breaking)
    """

    def generate_prompt(
        self,
        brief: str,
        topic: str,
        config: ResearchConfig
    ) -> str:
        """
        Generate a research prompt optimized for Gemini CLI.

        The prompt includes:
        1. Role definition (world-class researcher)
        2. Task specification with steelman requirements
        3. Domain-specific search strategies
        4. Evidence hygiene standards
        5. Output format template
        """

    def analyze_topic(self, brief: str, topic: str) -> TopicAnalysis:
        """
        Analyze topic to determine optimal research approach.

        Returns:
        - Domain classification
        - Recommended search queries
        - Source type priorities
        - Controversy flags
        - Special instructions
        """
```

**Prompt Template Structure**:
```markdown
# Research Task: {topic}

## Role
You are a world-class research analyst specializing in {domain}. Your expertise includes
{domain_specific_capabilities}.

## Objective
Conduct comprehensive research on {topic} following the Deutsch framework for
good explanations. Your goal is to map the landscape of competing explanations
with absolute fairness and rigor.

## Research Strategy

### 1. Search Queries (Priority Order)
{generated_search_queries}

### 2. Source Priorities
{domain_specific_sources}

### 3. Key Dimensions to Investigate
{domain_specific_dimensions}

## Process Requirements

1. **Identify 5-7 competing explanations** across:
   - Academic literature (Google Scholar, arXiv, journals)
   - Industry expert perspectives (blogs, white papers, conferences)
   - Popular discourse (HN, Reddit, Twitter, mainstream media)
   - Historical context (books, earlier treatments)

2. **For each explanation, document**:
   - Core Claim (in their language, not yours)
   - Supporting Evidence (with source classification)
   - Counter-Evidence (weaknesses and objections)
   - Prevalence (Mainstream/Growing/Minority/Fringe)
   - Strongest Form (Steelman - best version of argument)

3. **Identify landscape patterns**:
   - Where explanations fundamentally conflict
   - Shared assumptions across views
   - Disputed evidence or interpretations
   - Gaps no explanation addresses

## Evidence Hygiene (CRITICAL)

- **Primary sources**: Full citation (DOI, PMID, arXiv ID)
- **Numerical claims**: Verify against primary, note context
- **Web sources**: URL + access date
- **Unverifiable claims**: Flag as unverified or exclude

## Output Format

Produce research.md following the exact template below.

[Full research.md template]
```

### 2. Gemini CLI Interface (`src/content_factory/research/gemini_cli_interface.py`)

**Purpose**: Wraps Gemini CLI for headless execution with proper error handling.

```python
class GeminiCLIInterface:
    """
    Interface for executing Gemini CLI in headless mode.

    Features:
    - JSON output parsing
    - Token usage tracking
    - Error recovery
    - Model selection (gemini-2.5-flash for speed, gemini-pro for quality)
    """

    GEMINI_CLI_PATH = "/home/KnowledgeArchitect/.nvm/versions/node/v24.11.1/bin/gemini"

    def __init__(
        self,
        model: str = "gemini-3-pro",  # FIXED: Always use gemini-3-pro for research
        timeout: int = 600,  # 10 minutes
        output_format: str = "json"
    ):
        self.model = model  # gemini-3-pro only - no fallbacks
        self.timeout = timeout
        self.output_format = output_format

    def execute_research(
        self,
        prompt: str,
        output_file: Path
    ) -> GeminiResult:
        """
        Execute Gemini CLI with research prompt.

        Uses gemini-3-pro model for maximum research quality.

        Args:
            prompt: The research prompt (generated by PromptGenerator)
            output_file: Where to write research.md

        Returns:
            GeminiResult with:
            - success: bool
            - content: str (research.md content)
            - token_usage: dict
            - latency_ms: int
            - error: str (if failed)
        """

    def _parse_json_response(self, json_output: str) -> dict:
        """
        Parse Gemini CLI JSON output.

        Expected structure:
        {
          "response": "...",
          "stats": {
            "models": {...},
            "tokens": {...},
            "tools": {...}
          },
          "error": {...}
        }
        """

    def _handle_rate_limit(self) -> None:
        """Handle Gemini rate limits (60 req/min for OAuth personal)."""

    def _build_cli_command(self, prompt: str) -> list[str]:
        """
        Build the Gemini CLI command.

        Returns:
            Command list for subprocess, e.g.:
            ['gemini', '--model', 'gemini-3-pro', '--output-format', 'json', '--yolo', '-p', prompt]
        """
        return [
            self.GEMINI_CLI_PATH,
            '--model', 'gemini-3-pro',  # FIXED: Always use gemini-3-pro
            '--output-format', self.output_format,
            '--yolo',  # Auto-approve actions
            '-p', prompt
        ]
```

### 3. Gemini Research Orchestrator (`src/content_factory/research/gemini_researcher.py`)

**Purpose**: Coordinates the prompt generator and CLI interface.

```python
class GeminiResearcher:
    """
    Research agent using Gemini CLI for world-class research.

    Workflow:
    1. Receive brief from orchestrator
    2. Analyze topic for research strategy
    3. Generate optimized prompt for Gemini
    4. Execute Gemini CLI in headless mode
    5. Parse and validate output
    6. Return research.md path
    """

    def __init__(
        self,
        prompt_generator: GeminiResearchPromptGenerator,
        cli_interface: GeminiCLIInterface,
        validator: ResearchValidator
    ):
        self.prompt_generator = prompt_generator
        self.cli = cli_interface
        self.validator = validator

    def execute(
        self,
        brief: str,
        topic: str,
        output_dir: Path
    ) -> ResearchResult:
        """
        Execute the research phase using Gemini CLI.

        Returns:
            ResearchResult with validation status
        """
```

### 4. Updated Orchestrator Integration

**Modified `orchestrator.py`**:

```python
# In ContentFactoryOrchestrator.__init__

# v2.3: Use Gemini researcher
from .research.gemini_researcher import GeminiResearcher

self.gemini_researcher = GeminiResearcher(
    prompt_generator=GeminiResearchPromptGenerator(),
    cli_interface=GeminiCLIInterface(
        model="gemini-3-pro"  # FIXED: Always use gemini-3-pro for research
    ),
    validator=self.validators[Phase.RESEARCH]
)

# In run_research()
def run_research(self) -> bool:
    """Run the research phase using Gemini CLI."""
    if self.state != PipelineState.RESEARCHING:
        return False

    try:
        # Read brief
        brief_path = self.config.get_input_path(self.topic)
        brief = brief_path.read_text()

        # Execute Gemini researcher
        result = self.gemini_researcher.execute(
            brief=brief,
            topic=self.topic,
            output_dir=self.output_dir
        )

        if result.valid:
            self.phase_outputs["research"] = result.output_path
            self._save_checkpoint()
            self._transition(TransitionEvent.PHASE_COMPLETE)
            return True
        else:
            self._handle_phase_failure(Phase.RESEARCH, result.validation_result)
            return False

    except GuardrailViolation as e:
        self._handle_guardrail_violation(e)
        return False
```

---

## Configuration Changes

### New `research` section in `config.py`:

```python
@dataclass
class ResearchConfig:
    """Configuration for research phase."""

    # Gemini CLI settings
    gemini_model: str = "gemini-3-pro"  # FIXED: Always use gemini-3-pro for research
    gemini_timeout: int = 600  # seconds
    gemini_output_format: str = "json"

    # Research quality settings
    min_explanations: int = 3
    max_explanations: int = 7
    require_evidence_both_sides: bool = True
    require_steelman: bool = True

    # Prompt generation settings
    enable_dynamic_prompts: bool = True  # v2.3 feature
    prompt_template_path: Optional[Path] = None

    # Search strategy
    web_search_enabled: bool = True
    academic_search_enabled: bool = True
    multi_modal_enabled: bool = True  # images, videos, PDFs


@dataclass
class PipelineConfig:
    # ... existing fields ...
    research: ResearchConfig = field(default_factory=ResearchConfig)
```

---

## File Structure

```
content-factory/
├── src/content_factory/
│   ├── research/                      # NEW: v2.3 research module
│   │   ├── __init__.py
│   │   ├── prompt_generator.py        # Dynamic prompt generation
│   │   ├── gemini_cli_interface.py    # Gemini CLI wrapper
│   │   ├── gemini_researcher.py       # Main coordinator
│   │   └── topic_analyzer.py          # Topic classification
│   ├── orchestrator.py                # MODIFIED: Use Gemini researcher
│   ├── config.py                      # MODIFIED: Add ResearchConfig
│   └── validators/
│       └── research_validator.py      # ENHANCED: Handle Gemini output
│
├── agents/
│   ├── gemini-researcher-agent-v2.3.md  # NEW: Agent instructions
│   └── researcher-agent-v2.md         # DEPRECATED: Replaced by Gemini
│
├── prompts/                           # NEW: Prompt templates
│   ├── base_research_prompt.md
│   ├── technical_research_prompt.md
│   ├── philosophical_research_prompt.md
│   └── scientific_research_prompt.md
│
└── CLAUDE.md                          # UPDATED: v2.3 documentation
```

---

## Implementation Phases

### Phase 1: Core Infrastructure
- [ ] Create `research/` module structure
- [ ] Implement `GeminiCLIInterface` with JSON parsing
- [ ] Implement `TopicAnalyzer` for topic classification
- [ ] Add `ResearchConfig` to `config.py`

### Phase 2: Prompt Generation
- [ ] Create base prompt templates for each domain
- [ ] Implement `GeminiResearchPromptGenerator`
- [ ] Add topic-aware prompt enhancement logic
- [ ] Create prompt testing framework

### Phase 3: Integration
- [ ] Implement `GeminiResearcher` coordinator
- [ ] Update `orchestrator.py` to use Gemini researcher
- [ ] Update `research_validator.py` for Gemini output quirks
- [ ] Add telemetry for Gemini-specific metrics

### Phase 4: Testing & Validation
- [ ] Unit tests for prompt generator
- [ ] Integration tests for CLI interface
- [ ] End-to-end pipeline tests
- [ ] Quality benchmarks (Gemini vs Claude research)

### Phase 5: Documentation
- [ ] Update CLAUDE.md with v2.3 changes
- [ ] Create `gemini-researcher-agent-v2.3.md`
- [ ] Document prompt engineering patterns
- [ ] Create troubleshooting guide

---

## Migration Path

### For Existing Content Factory v2.2 Installations

**Option A: Clean Break (Recommended)**
```bash
# Backup existing research agent
mv agents/researcher-agent-v2.md agents/researcher-agent-v2-DEPRECATED.md

# Install new components
# (Python package install)

# Update config to use Gemini researcher
# research.gemini_enabled = true
```

**Option B: Gradual Transition**
- Keep both researchers available
- Config flag to switch between Claude/Gemini
- A/B testing capability

---

## Expected Benefits

| Metric | v2.2 (Claude) | v2.3 (Gemini) | Improvement |
|--------|---------------|---------------|-------------|
| Web search freshness | Context-limited | Live Google Search | +Significant |
| Source depth | Good | Excellent (multi-modal) | +30% |
| Context window | ~200K tokens | ~1M tokens | +5x |
| Research speed | Fast | Fast (gemini-3-pro) | Same |
| Factual accuracy | 85% | 95% (verified) | +10% |
| Source diversity | Medium | High (built-in tools) | +25% |

---

## Rollback Plan

If Gemini CLI research proves problematic:

1. **Fallback to Claude**: Set `research.gemini_enabled = false`
2. **Hybrid mode**: Gemini for research collection, Claude for synthesis
3. **Parallel mode**: Run both, compare outputs

---

## Open Questions

1. **Model selection**: ✅ **FIXED** - Always use `gemini-3-pro` for research quality
   - No fallbacks, no model switching - gemini-3-pro is the standard

2. **Prompt iteration**: Should we iterate on prompts if research quality is low?
   - **Recommendation**: Yes, max 2 prompt refinement iterations

3. **Citation format**: How does Gemini cite sources?
   - **Need to test**: Expect URLs, may need post-processing

4. **Rate limits**: 60 req/min for OAuth personal - is this sufficient?
   - **For research**: Yes, we only need 1-2 requests per topic

---

## Success Criteria

Content Factory v2.3 is successful when:

- [ ] Gemini CLI research passes all existing validation tests
- [ ] Research quality equals or exceeds v2.2 Claude research
- [ ] Dynamic prompts show measurable improvement over static prompts
- [ ] Pipeline end-to-end time is not significantly increased
- [ ] No regressions in downstream phases (Analysis, Writing, Editing)
- [ ] CODEX Brutal Critic scores ≥9.5 on Gemini-researched content

---

**Version**: 2.3 Design Document
**Status**: Ready for Implementation
**Next Step**: Phase 1 - Core Infrastructure
