"""Plain-language case-state explanation. Template-driven by design — the
(category, stage) space is small and enumerable, so a deterministic lookup
is both cheaper and more demo-reliable than an LLM call here."""

from app.ai.fallback.rules import explain_case_state_fallback
from app.models.domain import CaseExplanation
from app.models.enums import ServiceCategory


def explain_case_state(category: ServiceCategory, stage_name: str) -> CaseExplanation:
    return explain_case_state_fallback(category, stage_name)
