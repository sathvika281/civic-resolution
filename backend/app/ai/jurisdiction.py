"""Authority/jurisdiction resolution.

Deterministic by design: once a category is known, the responsible synthetic
authority is a registry lookup, not something worth spending an LLM call on.
"""

from app.ai.fallback.rules import resolve_authority_fallback
from app.models.domain import AuthorityResolution
from app.models.enums import ServiceCategory


def resolve_authority(category: ServiceCategory) -> AuthorityResolution:
    return resolve_authority_fallback(category)
