"""Structured-output payload models used ONLY for parsing OpenAI responses.

These deliberately omit the `source` field (the LLM shouldn't be asked to
decide that) — callers wrap the parsed payload into the full domain model
with source="openai" themselves.
"""

from pydantic import BaseModel

from app.models.enums import AuthorityType, ServiceCategory, UrgencyLevel


class SafetyScreenPayload(BaseModel):
    is_safe_for_workflow: bool
    reason: str | None = None
    redirect_message: str | None = None


class ProblemUnderstandingPayload(BaseModel):
    issue_summary: str
    category: ServiceCategory
    urgency: UrgencyLevel
    likely_required_evidence: list[str]
    likely_next_action: str


class AuthorityResolutionPayload(BaseModel):
    authority_name: str
    authority_type: AuthorityType
    department: str
    jurisdiction_area: str
    responsible_role: str


class CaseExplanationPayload(BaseModel):
    whats_happening: str
    current_blocker: str
    who_needs_to_act: str
    what_you_should_do: str
    next_step_label: str
    then_step_label: str


class EvidenceInterpretationPayload(BaseModel):
    likely_shows: str
    missing_info_hint: str | None = None
    consistent_with_original_issue: bool | None = None


class ClusterResultPayload(BaseModel):
    possible_common_issue: bool
    summary: str


class EscalationSummaryPayload(BaseModel):
    reason_text: str
