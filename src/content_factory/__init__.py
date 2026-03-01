"""
Content Factory v3.0 - World-Class Agentic Content System

A production-grade implementation of David Deutsch's epistemological framework
for creating explanatory content through systematic error elimination.

Architecture:
- Sequential 4-agent pipeline (Research → Analysis → Writing → Editing)
- State machine orchestrator with checkpointing
- Output validators with JSON schemas
- Telemetry and structured logging
- Guardrails (budget, time, quality)
- Empirical validation framework

Author: Content Factory Team
Version: 3.0.0
"""

__version__ = "3.0.0"
__author__ = "Content Factory Team"

from .orchestrator import ContentFactoryOrchestrator
from .config import Config, PipelineConfig
from .telemetry import TelemetryCollector

__all__ = [
    "ContentFactoryOrchestrator",
    "Config",
    "PipelineConfig",
    "TelemetryCollector",
]
