"""
Unit tests for Content Factory validators.

Tests each validator's ability to detect:
- Structural issues (missing sections)
- Quality issues (vague language, preachy tone)
- Completeness issues (missing tests, counterarguments)
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from content_factory.validators import (
    ResearchValidator,
    AnalysisValidator,
    WriterValidator,
    EditorValidator,
    ValidationResult,
)
from content_factory.validators.writer_validator import ContentFormat


class TestResearchValidator:
    """Tests for ResearchValidator."""

    @pytest.fixture
    def validator(self):
        return ResearchValidator(min_explanations=3, max_explanations=7)

    @pytest.fixture
    def valid_research(self):
        """Load sample valid research."""
        fixtures_dir = Path(__file__).parent.parent / "fixtures"
        return (fixtures_dir / "sample_research.md").read_text()

    def test_valid_research_passes(self, validator, valid_research):
        """Valid research should pass validation."""
        result = validator.validate(valid_research)
        assert result.valid, f"Expected valid, got errors: {result.errors}"
        assert result.metrics.get("explanation_count", 0) >= 3

    def test_detects_missing_problem_statement(self, validator):
        """Should detect missing problem statement."""
        content = """
# Research: Test Topic

## Landscape of Explanations

### Explanation 1: "Test"
**Core Claim**: Something
**Supporting Evidence**: Evidence
**Counter-Evidence**: Counter
**Prevalence**: Mainstream
        """
        result = validator.validate(content)
        assert any(e.code == "MISSING_PROBLEM_STATEMENT" for e in result.errors)

    def test_detects_too_few_explanations(self, validator):
        """Should detect when fewer than 3 explanations."""
        content = """
# Research: Test

## The Problem
This is the problem statement.

## Landscape of Explanations

### Explanation 1: "Only One"
**Core Claim**: Something
**Supporting Evidence**: Evidence
**Counter-Evidence**: Counter
        """
        result = validator.validate(content)
        assert any(e.code == "TOO_FEW_EXPLANATIONS" for e in result.errors)

    def test_detects_missing_evidence(self, validator):
        """Should detect missing supporting or counter evidence."""
        content = """
# Research: Test

## The Problem
This is a test problem that needs investigation.

## Landscape of Explanations

### Explanation 1: "Missing Counter"
**Core Claim**: This is what people believe.
**Supporting Evidence**: This is why they believe it.

### Explanation 2: "Missing Support"
**Core Claim**: Another view.
**Counter-Evidence**: This challenges it.

### Explanation 3: "Complete"
**Core Claim**: A third view.
**Supporting Evidence**: Support here.
**Counter-Evidence**: Counter here.
        """
        result = validator.validate(content)
        # Should flag missing evidence
        assert any("EVIDENCE" in e.code for e in result.issues)

    def test_detects_evaluation_in_research(self, validator):
        """Should warn about evaluation language in research."""
        content = """
# Research: Test

## The Problem
This is the test problem.

## Landscape of Explanations

### Explanation 1: "Test"
**Core Claim**: This is clearly the best explanation.
**Supporting Evidence**: Evidence
**Counter-Evidence**: Counter

### Explanation 2: "Test2"
**Core Claim**: This is obviously wrong.
**Supporting Evidence**: Evidence
**Counter-Evidence**: Counter

### Explanation 3: "Test3"
**Core Claim**: Claim.
**Supporting Evidence**: Evidence
**Counter-Evidence**: Counter
        """
        result = validator.validate(content)
        # Should warn about evaluation
        assert any("EVALUATION" in e.code for e in result.warnings)

    def test_metrics_computed(self, validator, valid_research):
        """Should compute metrics correctly."""
        result = validator.validate(valid_research)
        assert "total_words" in result.metrics
        assert "explanation_count" in result.metrics
        assert "completeness_score" in result.metrics
        assert result.metrics["completeness_score"] > 0


class TestAnalysisValidator:
    """Tests for AnalysisValidator."""

    @pytest.fixture
    def validator(self):
        return AnalysisValidator(require_all_tests=True)

    def test_detects_missing_tests(self, validator):
        """Should detect when not all 5 tests are applied."""
        content = """
# Analysis: Test

## Systematic Evaluation

### Explanation 1: "Test"

**Test Results**:

1. **Hard-to-Vary**: PASS ✓
   - Evidence: Can't swap components

2. **Mechanism**: PASS ✓
   - Evidence: Clear causal chain

3. **Reach**: PASS ✓
   - Evidence: Explains multiple phenomena

# Missing Rejectability and Integration tests
        """
        result = validator.validate(content)
        assert any("MISSING_TESTS" in e.code for e in result.errors)

    def test_detects_missing_good_explanation(self, validator):
        """Should detect missing good explanation section."""
        content = """
# Analysis: Test

## Systematic Evaluation

### Explanation 1: "Test"
**Score**: 5/5

## Ranking
1. Test - 5/5
        """
        result = validator.validate(content)
        assert any("GOOD_EXPLANATION" in e.code for e in result.errors)

    def test_valid_analysis_with_all_tests(self, validator):
        """Full analysis with all 5 tests should pass."""
        content = """
# Analysis: Test

## Systematic Evaluation

### Explanation 1: "Complete Example"

**Test Results**:

1. **Hard-to-Vary**: PASS ✓
   - Evidence: Components are tightly constrained.
   - Reasoning: Changing any element breaks the explanation.

2. **Mechanism**: PASS ✓
   - Evidence: A causes B which causes C.
   - Reasoning: Clear causal chain identified.

3. **Reach**: PASS ✓
   - Evidence: Also explains X, Y, and Z phenomena.
   - Reasoning: Extends beyond original target.

4. **Rejectability**: PASS ✓
   - Evidence: Would be falsified if A didn't cause B.
   - Reasoning: Testable prediction.

5. **Integration**: PASS ✓
   - Evidence: Consistent with physics and psychology.
   - Reasoning: No conflicts with established knowledge.

**Score**: 5/5 tests passed

## Ranking

1. **Complete Example** - 5/5 ✓✓✓✓✓
   - This is a GOOD explanation

## The Good Explanation

**The Explanation**: The complete example passes all tests.

**Why It's Hard-to-Vary**: Components constrained.

**The Mechanism**: A → B → C

**The Reach**: Explains X, Y, Z

**Testability**: Falsifiable predictions

**Integration**: Consistent with existing knowledge

## Implications

### Theoretical Understanding
New insight revealed.

### Practical Application
Changed behavior recommended.
        """
        result = validator.validate(content)
        # Should be valid or only have minor issues
        assert result.error_count == 0, f"Unexpected errors: {result.errors}"


class TestWriterValidator:
    """Tests for WriterValidator."""

    @pytest.fixture
    def article_validator(self):
        return WriterValidator(content_format=ContentFormat.ARTICLE)

    @pytest.fixture
    def twitter_validator(self):
        return WriterValidator(content_format=ContentFormat.TWITTER_THREAD)

    def test_detects_preachy_tone(self, article_validator):
        """Should detect preachy/lecturing language."""
        content = """
# Why You Must Change

You must understand this. Obviously, everyone knows that goal-setting is important.
The truth is that you need to do this. You should always focus on what matters.

Clearly, this is simple if you just do it. Everyone knows the answer.
""" * 50  # Repeat to meet word count
        result = article_validator.validate(content)
        # Should flag preachy tone
        assert result.metrics.get("preachy_score", 0) > 0

    def test_detects_insufficient_counterarguments(self, article_validator):
        """Should detect missing counterarguments."""
        content = """
# Test Article

This is a test article about something important. We will discuss the topic
at length without addressing any potential objections or counterarguments.

The framework works like this and there are no problems with it at all.
Everyone should just use it and everything will be fine.
""" * 100  # Repeat to meet word count
        result = article_validator.validate(content)
        assert any("COUNTERARGUMENT" in e.code for e in result.errors)

    def test_detects_vague_language(self, article_validator):
        """Should detect vague language."""
        content = """
# Test Article

Think about your goals. Consider your options. Reflect on what matters.
Some people say this, many experts believe that. In general, things work out.

Think about it more. Consider the alternatives. Reflect on the implications.
""" * 50
        result = article_validator.validate(content)
        assert result.metrics.get("vague_phrases", 0) > 0

    def test_validates_twitter_format(self, twitter_validator):
        """Should validate Twitter thread format."""
        content = """
1/ Thread on goal-setting (THREAD)

2/ Here's what most people get wrong about goals...

3/ The key insight is this: frameworks are arbitrary.

4/ But there's a better way. Here's the mechanism:

5/ Apply the hard-to-vary test. If you can swap components, it's bad.

6/ Sarah tried this and saw results in 90 days.

7/ The counterargument: "But structure helps!"

8/ True, but structure without mechanism is just ritual.

9/ Try this today: Write your goal. Swap one word. Does it still work?

10/ That's how you know if your goal is real.
"""
        result = twitter_validator.validate(content)
        assert result.metrics.get("tweet_count", 0) >= 5

    def test_detects_low_practical_utility(self, article_validator):
        """Should detect low practical utility."""
        content = """
# Theoretical Treatise

This is a purely theoretical exploration of goal-setting frameworks.
We will examine the philosophical underpinnings without any practical application.

The metaphysics of goals is complex and nuanced. One must consider the
ontological status of intentions and the epistemological challenges of
self-knowledge.

There are no specific steps here, no examples, no actions you can take.
Just pure theory and abstraction.
""" * 50
        result = article_validator.validate(content)
        assert any("PRACTICAL" in e.code for e in result.errors)


class TestEditorValidator:
    """Tests for EditorValidator."""

    @pytest.fixture
    def validator(self):
        return EditorValidator(min_score_to_publish=9.3)

    @pytest.fixture
    def valid_feedback(self):
        """Load sample valid editor feedback."""
        fixtures_dir = Path(__file__).parent.parent / "fixtures"
        return (fixtures_dir / "sample_editor_feedback.md").read_text()

    def test_valid_feedback_passes(self, validator, valid_feedback):
        """Valid editor feedback should pass validation."""
        result = validator.validate(valid_feedback)
        assert result.valid, f"Errors: {result.errors}"
        assert result.metrics.get("effective_score", 0) >= 9.0

    def test_extracts_dimension_scores(self, validator, valid_feedback):
        """Should extract all dimension scores."""
        result = validator.validate(valid_feedback)
        scores = result.metrics.get("scores", {})
        assert len(scores) >= 5, f"Only extracted {len(scores)} scores"

    def test_detects_missing_decision(self, validator):
        """Should detect missing editorial decision."""
        content = """
# Editorial Review

## Dimensional Scores

| Dimension | Score |
|-----------|-------|
| Philosophical Accuracy | 9.5/10 |
| Factual Accuracy | 9.0/10 |

## Final Score: 9.3/10

# No decision stated
        """
        result = validator.validate(content)
        assert any("DECISION" in e.code for e in result.errors)

    def test_detects_score_below_threshold(self, validator):
        """Should detect when score is below publish threshold."""
        content = """
# Editorial Review

## DECISION: MAJOR REVISION

## Final Score: 8.5/10

## Dimensional Scores

| Dimension | Score |
|-----------|-------|
| Philosophical Accuracy | 8.5/10 |
| Factual Accuracy | 8.5/10 |
| Logical Soundness | 8.5/10 |
| Clarity | 8.5/10 |
| Engagement | 8.5/10 |
| Practical Utility | 8.5/10 |
| Intellectual Honesty | 8.5/10 |
        """
        result = validator.validate(content)
        # Should flag below threshold
        assert result.metrics.get("meets_threshold") == False

    def test_detects_missing_actionable_feedback(self, validator):
        """Should require actionable feedback when score is low."""
        content = """
# Editorial Review

## DECISION: MAJOR REVISION

## Final Score: 8.0/10

## Dimensional Scores
Philosophical Accuracy: 8.0/10
Factual Accuracy: 8.0/10

# No specific fixes or improvement path
        """
        result = validator.validate(content)
        assert any("ACTIONABLE" in e.code or "IMPROVEMENT" in e.code for e in result.issues)


class TestValidationResult:
    """Tests for ValidationResult helper class."""

    def test_error_tracking(self):
        """Should track errors correctly."""
        result = ValidationResult(valid=True)
        assert result.valid == True

        result.add_error("TEST_ERROR", "Test message")
        assert result.valid == False
        assert result.error_count == 1

    def test_warning_tracking(self):
        """Should track warnings without affecting validity."""
        result = ValidationResult(valid=True)
        result.add_warning("TEST_WARNING", "Test warning")
        assert result.valid == True
        assert result.warning_count == 1

    def test_to_dict(self):
        """Should export to dictionary correctly."""
        result = ValidationResult(valid=True)
        result.add_error("E1", "Error 1")
        result.add_warning("W1", "Warning 1")
        result.metrics = {"test": 123}

        d = result.to_dict()
        assert d["valid"] == False
        assert d["error_count"] == 1
        assert d["warning_count"] == 1
        assert d["metrics"]["test"] == 123


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
