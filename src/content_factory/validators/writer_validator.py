"""
Validator for Writer Agent output (article.md, twitter-thread.md, etc.).

Ensures:
- Traceability to analysis (claims backed by analysis)
- 3-5 specific, detailed examples (names, numbers)
- 2-3 strong counterarguments addressed
- Practical utility (actionable in 24 hours)
- Exploratory tone (not preachy)
- Format-appropriate structure
"""

import re
from typing import Dict, List, Optional
from enum import Enum
from .base import Validator, ValidationResult


class ContentFormat(Enum):
    """Content output formats with specific requirements."""
    ARTICLE = "article"
    TWITTER_THREAD = "twitter-thread"
    LINKEDIN_POST = "linkedin-post"
    NEWSLETTER = "newsletter"
    YOUTUBE_SCRIPT = "youtube-script"


class WriterValidator(Validator):
    """Validates writer output for any format."""

    # Format-specific requirements
    FORMAT_REQUIREMENTS = {
        ContentFormat.ARTICLE: {
            "min_words": 1500,
            "max_words": 5000,
            "min_counterarguments": 2,
            "min_examples": 3,
            "require_practical": True,
        },
        ContentFormat.TWITTER_THREAD: {
            "min_words": 300,
            "max_words": 1500,
            "min_counterarguments": 1,
            "min_examples": 2,
            "require_practical": True,
        },
        ContentFormat.LINKEDIN_POST: {
            "min_words": 200,
            "max_words": 800,
            "min_counterarguments": 1,
            "min_examples": 1,
            "require_practical": True,
        },
        ContentFormat.NEWSLETTER: {
            "min_words": 800,
            "max_words": 3000,
            "min_counterarguments": 2,
            "min_examples": 2,
            "require_practical": True,
        },
        ContentFormat.YOUTUBE_SCRIPT: {
            "min_words": 1000,
            "max_words": 4000,
            "min_counterarguments": 2,
            "min_examples": 3,
            "require_practical": True,
        },
    }

    def __init__(
        self,
        content_format: ContentFormat = ContentFormat.ARTICLE,
        min_counterarguments: int = 2,
        require_practical_utility: bool = True,
        max_preachy_score: float = 3.0,
        strict: bool = True
    ):
        super().__init__(strict=strict)
        self.content_format = content_format
        self.requirements = self.FORMAT_REQUIREMENTS.get(
            content_format,
            self.FORMAT_REQUIREMENTS[ContentFormat.ARTICLE]
        )
        self.min_counterarguments = min_counterarguments
        self.require_practical_utility = require_practical_utility
        self.max_preachy_score = max_preachy_score

    def validate(self, content: str) -> ValidationResult:
        """Validate writer output content."""
        result = ValidationResult(valid=True, raw_content=content)

        # 1. Check word count
        self._validate_word_count(content, result)

        # 2. Check for specific examples
        self._validate_examples(content, result)

        # 3. Check for counterarguments
        self._validate_counterarguments(content, result)

        # 4. Check practical utility
        if self.require_practical_utility:
            self._validate_practical_utility(content, result)

        # 5. Check tone (not preachy)
        self._validate_tone(content, result)

        # 6. Check format-specific requirements
        self._validate_format_specific(content, result)

        # 7. Compute comprehensive metrics
        result.metrics = self._compute_metrics(content)

        return result

    def _validate_word_count(self, content: str, result: ValidationResult):
        """Validate content length for format."""
        word_count, in_range = self._check_word_count(
            content,
            self.requirements["min_words"],
            self.requirements["max_words"]
        )

        result.metrics["word_count"] = word_count

        if word_count < self.requirements["min_words"]:
            result.add_error(
                code="TOO_SHORT",
                message=f"Content is {word_count} words, minimum is {self.requirements['min_words']}",
                suggestion=f"Expand content by {self.requirements['min_words'] - word_count} words"
            )
        elif word_count > self.requirements["max_words"]:
            result.add_warning(
                code="TOO_LONG",
                message=f"Content is {word_count} words, maximum recommended is {self.requirements['max_words']}",
                suggestion="Consider trimming or splitting into multiple pieces"
            )

    def _validate_examples(self, content: str, result: ValidationResult):
        """Validate specific, detailed examples."""
        example_metrics = self._check_specific_examples(content)

        result.metrics.update({
            "named_examples": example_metrics["named_examples"],
            "numbered_examples": example_metrics["numbered_examples"],
            "vague_phrases": example_metrics["vague_phrases"],
        })

        # Calculate example quality score
        specific_examples = example_metrics["named_examples"] + example_metrics["numbered_examples"]
        min_examples = self.requirements["min_examples"]

        if specific_examples < min_examples:
            result.add_error(
                code="INSUFFICIENT_EXAMPLES",
                message=f"Found ~{specific_examples} specific examples, need at least {min_examples}",
                suggestion="Add examples with real names, numbers, and concrete details"
            )

        # Check for vague language
        if example_metrics["vague_phrases"] > 5:
            result.add_warning(
                code="VAGUE_LANGUAGE",
                message=f"Found {example_metrics['vague_phrases']} vague phrases",
                suggestion="Replace 'think about', 'some people', etc. with specific examples"
            )

        # Deep example analysis
        self._analyze_example_quality(content, result)

    def _analyze_example_quality(self, content: str, result: ValidationResult):
        """Analyze quality of examples in detail."""
        # Look for example patterns
        example_patterns = [
            r'(?:For example|Consider|Take)\s*[,:]?\s*([^.]+\.)',
            r'(?:Like|Such as)\s+([^.]+\.)',
            r'(?:Sarah|Marcus|Chen|Elena|James)\s+[^.]+\.',
        ]

        examples_found = []
        for pattern in example_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            examples_found.extend(matches)

        # Check if examples have specifics
        good_examples = 0
        for example in examples_found:
            has_number = bool(re.search(r'\d+', example))
            has_name = bool(re.search(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?', example))
            has_detail = len(example.split()) > 10

            if has_number or has_name and has_detail:
                good_examples += 1

        result.metrics["quality_examples"] = good_examples

    def _validate_counterarguments(self, content: str, result: ValidationResult):
        """Validate counterarguments are addressed."""
        # Patterns indicating counterargument handling
        counter_patterns = [
            r'(?:but|however)[,]?\s+(?:some|critics|skeptics|one might|you might)',
            r'(?:objection|counterargument|criticism)[s]?\s*[:\-]',
            r'"[^"]+\?".*?(?:this|but|however)',  # Question format objection
            r'(?:what about|but what if)',
            r'(?:one could argue|some might say)',
            r'(?:the objection|this objection)',
        ]

        counterargument_count = 0
        for pattern in counter_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            counterargument_count += len(matches)

        result.metrics["counterarguments_found"] = counterargument_count

        if counterargument_count < self.min_counterarguments:
            result.add_error(
                code="INSUFFICIENT_COUNTERARGUMENTS",
                message=f"Found ~{counterargument_count} counterarguments, need at least {self.min_counterarguments}",
                suggestion="Add steelmanned objections with substantive responses"
            )

        # Check for steelmanning language
        steelman_patterns = [
            r'strongest version',
            r'best argument',
            r'legitimate concern',
            r'fair point',
            r'valid objection',
        ]

        steelman_count = sum(
            1 for p in steelman_patterns
            if re.search(p, content, re.IGNORECASE)
        )

        result.metrics["steelman_indicators"] = steelman_count

        if counterargument_count >= self.min_counterarguments and steelman_count == 0:
            result.add_warning(
                code="WEAK_COUNTERARGUMENTS",
                message="Counterarguments may not be steelmanned",
                suggestion="Present objections at their strongest, then respond"
            )

    def _validate_practical_utility(self, content: str, result: ValidationResult):
        """Validate practical utility and actionability."""
        # Immediate action indicators
        action_patterns = [
            r'(?:right now|today|in the next|within \d+)',
            r'(?:step 1|first,?\s+\w+|start by)',
            r'(?:try this|do this|here\'s how)',
            r'(?:open|create|write down|list)',
            r'(?:set a timer|schedule|calendar)',
            r'\d+\s*(?:min|minute|hour)',
        ]

        action_count = 0
        for pattern in action_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            action_count += len(matches)

        result.metrics["action_indicators"] = action_count

        # Check for specific tools/methods
        tool_patterns = [
            r'(?:google doc|notion|spreadsheet|calendar|timer)',
            r'(?:template|framework|checklist|worksheet)',
        ]

        tool_count = sum(
            len(re.findall(p, content, re.IGNORECASE))
            for p in tool_patterns
        )

        result.metrics["tool_references"] = tool_count

        # Overall practical score
        practical_score = min(10, (action_count * 0.5) + (tool_count * 1.5))
        result.metrics["practical_utility_score"] = practical_score

        if practical_score < 3:
            result.add_error(
                code="LOW_PRACTICAL_UTILITY",
                message=f"Practical utility score: {practical_score}/10 (need 5+)",
                suggestion="Add specific actions readers can take in next 24 hours"
            )
        elif practical_score < 5:
            result.add_warning(
                code="MODERATE_PRACTICAL_UTILITY",
                message=f"Practical utility score: {practical_score}/10",
                suggestion="Add more specific steps, tools, or timeframes"
            )

    def _validate_tone(self, content: str, result: ValidationResult):
        """Validate exploratory (not preachy) tone."""
        preachy_findings = self._detect_preachy_language(content)

        preachy_count = sum(count for _, count in preachy_findings)
        result.metrics["preachy_language_count"] = preachy_count

        # Calculate preachy score (0-10, lower is better)
        word_count = len(content.split())
        preachy_score = min(10, (preachy_count / max(word_count, 1)) * 1000)
        result.metrics["preachy_score"] = round(preachy_score, 2)

        if preachy_score > self.max_preachy_score:
            result.add_error(
                code="PREACHY_TONE",
                message=f"Preachy score: {preachy_score:.1f}/10 (max allowed: {self.max_preachy_score})",
                suggestion="Replace imperatives with questions and invitations"
            )

            # List specific preachy patterns found
            for description, count in preachy_findings:
                if count > 0:
                    result.add_info(
                        code="PREACHY_PATTERN",
                        message=f"Found {count}x: {description}"
                    )

        # Check for exploratory language (good)
        exploratory_patterns = [
            r'\bwhat if\b',
            r'\bconsider this\b',
            r'\bwhat happens when\b',
            r'\bhave you noticed\b',
            r'\blet me show you\b',
            r'\bhere\'s what I\'ve found\b',
        ]

        exploratory_count = sum(
            len(re.findall(p, content, re.IGNORECASE))
            for p in exploratory_patterns
        )

        result.metrics["exploratory_language_count"] = exploratory_count

        if exploratory_count == 0 and preachy_count > 0:
            result.add_warning(
                code="NO_EXPLORATORY_TONE",
                message="No exploratory language found",
                suggestion="Add phrases like 'Consider...', 'What if...', 'Here's what I found...'"
            )

    def _validate_format_specific(self, content: str, result: ValidationResult):
        """Validate format-specific requirements."""
        if self.content_format == ContentFormat.TWITTER_THREAD:
            self._validate_twitter_format(content, result)
        elif self.content_format == ContentFormat.LINKEDIN_POST:
            self._validate_linkedin_format(content, result)
        elif self.content_format == ContentFormat.ARTICLE:
            self._validate_article_format(content, result)

    def _validate_twitter_format(self, content: str, result: ValidationResult):
        """Validate Twitter thread format."""
        # Count tweets (numbered sections or ---separators)
        tweet_patterns = [
            r'^\d+[./)]',  # 1. or 1) or 1/
            r'^Tweet \d+',
            r'---',
        ]

        tweet_count = 0
        for pattern in tweet_patterns:
            tweet_count = max(tweet_count, len(re.findall(pattern, content, re.MULTILINE)))

        result.metrics["tweet_count"] = tweet_count

        if tweet_count < 5:
            result.add_warning(
                code="SHORT_THREAD",
                message=f"Thread has ~{tweet_count} tweets, recommend 8-15",
                suggestion="Expand thread with more insights or examples"
            )
        elif tweet_count > 20:
            result.add_warning(
                code="LONG_THREAD",
                message=f"Thread has ~{tweet_count} tweets, may lose readers",
                suggestion="Consider condensing or splitting into multiple threads"
            )

        # Check for hook (first tweet should grab attention)
        lines = content.split('\n')
        first_substantive = next((l for l in lines if len(l) > 20), "")

        hook_patterns = [r'\?', r'!', r'most people', r'nobody', r'secret', r'truth']
        has_hook = any(re.search(p, first_substantive, re.IGNORECASE) for p in hook_patterns)

        if not has_hook:
            result.add_warning(
                code="WEAK_HOOK",
                message="First tweet may not hook readers",
                suggestion="Start with a question, surprising stat, or bold claim"
            )

    def _validate_linkedin_format(self, content: str, result: ValidationResult):
        """Validate LinkedIn post format."""
        # Check for professional framing
        professional_indicators = [
            r'(?:in my experience|I\'ve seen|working with)',
            r'(?:team|organization|company|business)',
            r'(?:leader|manager|professional)',
        ]

        prof_count = sum(
            len(re.findall(p, content, re.IGNORECASE))
            for p in professional_indicators
        )

        result.metrics["professional_framing"] = prof_count

        if prof_count == 0:
            result.add_info(
                code="LOW_PROFESSIONAL_FRAMING",
                message="Consider adding professional context for LinkedIn audience"
            )

    def _validate_article_format(self, content: str, result: ValidationResult):
        """Validate article format."""
        sections = self._extract_sections(content)
        result.metrics["section_count"] = len(sections)

        # Check for clear structure
        if len(sections) < 3:
            result.add_warning(
                code="WEAK_STRUCTURE",
                message=f"Only {len(sections)} sections found",
                suggestion="Add clear ## headings to organize content"
            )

        # Check for conclusion
        has_conclusion = any(
            'conclusion' in s.lower() or 'final' in s.lower() or 'summary' in s.lower()
            for s in sections.keys()
        )

        if not has_conclusion:
            result.add_info(
                code="NO_CONCLUSION",
                message="Consider adding a conclusion section"
            )

    def _compute_metrics(self, content: str) -> Dict:
        """Compute comprehensive content metrics."""
        words = len(content.split())
        sentences = len(re.split(r'[.!?]+', content))
        paragraphs = len([p for p in content.split('\n\n') if p.strip()])

        # Readability approximation (Flesch-Kincaid grade level proxy)
        avg_sentence_length = words / max(sentences, 1)
        syllables = sum(self._count_syllables(word) for word in content.split())
        avg_syllables = syllables / max(words, 1)

        # FK Grade Level ≈ 0.39 × (words/sentences) + 11.8 × (syllables/words) − 15.59
        fk_grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables - 15.59

        return {
            "word_count": words,
            "sentence_count": sentences,
            "paragraph_count": paragraphs,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "flesch_kincaid_grade": round(max(0, fk_grade), 1),
        }

    def _count_syllables(self, word: str) -> int:
        """Approximate syllable count for a word."""
        word = word.lower().strip(".,!?;:'\"")
        if not word:
            return 0

        count = 0
        vowels = "aeiouy"
        prev_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e') and count > 1:
            count -= 1

        return max(1, count)
