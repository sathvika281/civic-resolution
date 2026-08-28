from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.models.enums import (
    ActorType,
    AiSource,
    AuthorityType,
    CaseStatus,
    ConfirmationType,
    ServiceCategory,
    StageStatus,
    UrgencyLevel,
)

# ---------------------------------------------------------------------------
# AI module outputs (shared between the real OpenAI path and the fallback)
# ---------------------------------------------------------------------------


class SafetyScreenResult(BaseModel):
    is_safe_for_workflow: bool
    reason: str | None = None
    redirect_message: str | None = None
    source: AiSource = AiSource.FALLBACK


class ProblemUnderstanding(BaseModel):
    issue_summary: str
    category: ServiceCategory
    location_text: str | None = None
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    likely_required_evidence: list[str] = Field(default_factory=list)
    likely_next_action: str
    source: AiSource = AiSource.FALLBACK


class AuthorityResolution(BaseModel):
    authority_name: str
    authority_type: AuthorityType
    department: str
    jurisdiction_area: str
    responsible_role: str
    source: AiSource = AiSource.FALLBACK


class CaseExplanation(BaseModel):
    whats_happening: str
    current_blocker: str
    who_needs_to_act: str
    what_you_should_do: str
    next_step_label: str
    then_step_label: str
    source: AiSource = AiSource.FALLBACK


class EvidenceInterpretation(BaseModel):
    likely_shows: str
    missing_info_hint: str | None = None
    consistent_with_original_issue: bool | None = None
    source: AiSource = AiSource.FALLBACK


class ClusterResult(BaseModel):
    possible_common_issue: bool
    summary: str
    source: AiSource = AiSource.FALLBACK


class EscalationSummary(BaseModel):
    reason_text: str
    source: AiSource = AiSource.FALLBACK


# ---------------------------------------------------------------------------
# Persisted entities
# ---------------------------------------------------------------------------


class Citizen(BaseModel):
    id: str
    display_name: str
    persona_key: str
    phone: str | None = None
    created_at: datetime


class Authority(BaseModel):
    id: str
    name: str
    authority_type: AuthorityType
    jurisdiction_area: str
    contact_person_name: str
    contact_role: str
    escalation_authority_id: str | None = None
    created_at: datetime


class Service(BaseModel):
    id: str
    category: ServiceCategory
    display_name: str
    description: str
    default_authority_type: AuthorityType
    required_evidence: list[str] = Field(default_factory=list)
    sla_days: int
    stage_template: list[str]
    created_at: datetime


class Problem(BaseModel):
    id: str
    citizen_id: str
    raw_text: str
    location_text: str | None = None
    service_id: str | None = None
    ai_understanding: ProblemUnderstanding | None = None
    created_at: datetime


class TimelineEntry(BaseModel):
    id: str
    case_id: str
    stage_name: str
    status: StageStatus
    actor_type: ActorType
    actor_name: str | None = None
    note: str | None = None
    occurred_at: datetime
    sequence_order: int


class Evidence(BaseModel):
    id: str
    case_id: str
    uploaded_by: str
    file_name: str
    description_text: str | None = None
    ai_interpretation: EvidenceInterpretation | None = None
    stage_context: str | None = None
    created_at: datetime


class CommunityReport(BaseModel):
    id: str
    problem_id: str
    case_id: str | None = None
    reporter_citizen_id: str | None = None
    confirmation_type: ConfirmationType
    comment_text: str | None = None
    created_at: datetime


class Escalation(BaseModel):
    id: str
    case_id: str
    escalated_to_authority_id: str
    reason_text: str
    payload_snapshot: dict
    status: str = "submitted"
    created_at: datetime


class Case(BaseModel):
    id: str
    case_number: str
    problem_id: str
    citizen_id: str
    authority_id: str
    service_id: str
    status: CaseStatus
    current_stage: str
    opened_at: datetime
    expected_resolution_date: date
    last_status_change_at: datetime
    resolution_verification_count: int = 0
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# API request/response schemas
# ---------------------------------------------------------------------------


class ProblemIn(BaseModel):
    citizen_id: str
    raw_text: str
    location_text: str | None = None


class RedirectOut(BaseModel):
    redirected: Literal[True] = True
    reason: str
    message: str


class SlaOut(BaseModel):
    expected_days: int
    current_days: int
    is_overdue: bool
    days_overdue: int
    note: str = "Simulated SLA for prototype purposes."


class CurrentResponsibilityOut(BaseModel):
    authority_name: str
    role: str
    jurisdiction_area: str
    days_at_current_stage: int


class TimelineEntryOut(BaseModel):
    stage_name: str
    status: StageStatus
    actor_name: str | None
    note: str | None
    occurred_at: datetime


class RelatedCaseOut(BaseModel):
    case_number: str
    issue_summary: str
    location_text: str | None
    status: CaseStatus


class CommunityOut(BaseModel):
    affected_count: int
    confirmed_count: int
    cluster: ClusterResult | None = None


class EvidenceOut(BaseModel):
    id: str
    file_name: str
    description_text: str | None
    interpretation: EvidenceInterpretation | None
    created_at: datetime


class EscalationOut(BaseModel):
    id: str
    case_number: str
    reason_text: str
    escalated_to_authority_name: str
    status: str
    created_at: datetime


class CaseSummaryOut(BaseModel):
    case_number: str
    issue_summary: str
    category: ServiceCategory
    status: CaseStatus
    is_overdue: bool
    updated_at: datetime


class CaseDetailOut(BaseModel):
    case_number: str
    status: CaseStatus
    understanding: ProblemUnderstanding
    authority: AuthorityResolution
    explanation: CaseExplanation
    current_responsibility: CurrentResponsibilityOut
    timeline: list[TimelineEntryOut]
    sla: SlaOut
    community: CommunityOut
    evidence: list[EvidenceOut]
    related_cases: list[RelatedCaseOut]
    escalations: list[EscalationOut]
    can_escalate: bool
    awaiting_citizen_verification: bool


class CreateCaseResponse(BaseModel):
    redirected: bool
    redirect: RedirectOut | None = None
    case: CaseDetailOut | None = None


class VerifyResolutionIn(BaseModel):
    citizen_id: str
    is_actually_fixed: bool
    explanation_text: str | None = None


class EscalateIn(BaseModel):
    citizen_id: str


class EvidenceIn(BaseModel):
    uploaded_by: str
    file_name: str
    description_text: str | None = None
    stage_context: str | None = None


class ConfirmIn(BaseModel):
    citizen_id: str
    comment_text: str | None = None


class NearbyProblemOut(BaseModel):
    case_number: str
    issue_summary: str
    category: ServiceCategory
    location_text: str | None
    status: CaseStatus
    affected_count: int
    confirmed_count: int
    is_overdue: bool


class HealthOut(BaseModel):
    status: str = "ok"
    ai_mode: str
    db_mode: str
