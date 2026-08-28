import random
import uuid
from datetime import datetime, timezone

from app.ai import case_intelligence, community_intelligence, escalation_intelligence, intent, jurisdiction, resolution_intelligence, safety_check
from app.db.repository import Repository
from app.models.domain import (
    Case,
    CaseDetailOut,
    CaseExplanation,
    CommunityOut,
    CreateCaseResponse,
    CurrentResponsibilityOut,
    Escalation,
    EscalationOut,
    Evidence,
    EvidenceOut,
    Problem,
    RedirectOut,
    RelatedCaseOut,
    SlaOut,
    TimelineEntry,
    TimelineEntryOut,
)
from app.models.enums import ActorType, CaseStatus, StageStatus
from app.services import registry_service, sla_service

VERIFICATION_STAGE_NAME = "Citizen Verification"


def _new_id() -> str:
    return str(uuid.uuid4())


def _generate_case_number(repo: Repository, prefix: str) -> str:
    for _ in range(20):
        candidate = f"{prefix}-{random.randint(10000, 99999)}"
        if repo.get_case_by_number(candidate) is None:
            return candidate
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


def create_case(repo: Repository, citizen_id: str, raw_text: str, location_text: str | None) -> CreateCaseResponse:
    screen = safety_check.screen(raw_text)
    if not screen.is_safe_for_workflow:
        return CreateCaseResponse(
            redirected=True,
            redirect=RedirectOut(reason=screen.reason or "not_applicable", message=screen.redirect_message or ""),
        )

    understanding = intent.understand_problem(raw_text, location_text)
    service = registry_service.get_service_for_category(repo, understanding.category)
    authority_resolution = jurisdiction.resolve_authority(understanding.category)
    authority = registry_service.get_authority_for_name(repo, authority_resolution.authority_name)

    now = datetime.now(timezone.utc)
    problem = repo.create_problem(
        Problem(
            id=_new_id(),
            citizen_id=citizen_id,
            raw_text=raw_text,
            location_text=location_text,
            service_id=service.id,
            ai_understanding=understanding,
            created_at=now,
        )
    )

    from app.ai.fallback.keywords import CATEGORY_META

    prefix = CATEGORY_META[understanding.category]["case_prefix"]
    case_number = _generate_case_number(repo, prefix)
    expected_resolution_date = sla_service.compute_expected_resolution_date(now, service.sla_days)

    case = repo.create_case(
        Case(
            id=_new_id(),
            case_number=case_number,
            problem_id=problem.id,
            citizen_id=citizen_id,
            authority_id=authority.id,
            service_id=service.id,
            status=CaseStatus.IN_PROGRESS,
            current_stage=service.stage_template[1] if len(service.stage_template) > 1 else service.stage_template[0],
            opened_at=now,
            expected_resolution_date=expected_resolution_date,
            last_status_change_at=now,
            created_at=now,
            updated_at=now,
        )
    )

    for index, stage_name in enumerate(service.stage_template):
        if index == 0:
            status = StageStatus.COMPLETED
        elif index == 1:
            status = StageStatus.CURRENT
        else:
            status = StageStatus.PENDING
        repo.create_timeline_entry(
            TimelineEntry(
                id=_new_id(),
                case_id=case.id,
                stage_name=stage_name,
                status=status,
                actor_type=ActorType.SYSTEM if index == 0 else ActorType.AUTHORITY,
                actor_name=None if index == 0 else authority_resolution.responsible_role,
                note=None,
                occurred_at=now,
                sequence_order=index,
            )
        )

    return CreateCaseResponse(redirected=False, case=build_case_detail(repo, case))


def build_case_detail(repo: Repository, case: Case) -> CaseDetailOut:
    problem = repo.get_problem(case.problem_id)
    service = repo.get_service(case.service_id)
    authority = repo.get_authority(case.authority_id)
    understanding = problem.ai_understanding
    authority_resolution = jurisdiction.resolve_authority(understanding.category)

    timeline_entries = repo.list_timeline_for_case(case.id)
    timeline_out = [
        TimelineEntryOut(
            stage_name=t.stage_name,
            status=t.status,
            actor_name=t.actor_name,
            note=t.note,
            occurred_at=t.occurred_at,
        )
        for t in timeline_entries
    ]

    sla = sla_service.build_sla_out(case, service.sla_days)
    awaiting_verification = case.status == CaseStatus.RESOLVED_PENDING_VERIFICATION

    if awaiting_verification:
        explanation = CaseExplanation(
            whats_happening=f"{authority.name} has marked this case resolved. We're waiting for you to confirm it's actually fixed.",
            current_blocker="Your confirmation is the only remaining step.",
            who_needs_to_act="You",
            what_you_should_do="Check the issue and tell us whether it's actually resolved.",
            next_step_label="Case Closed",
            then_step_label="-",
        )
    elif case.status == CaseStatus.REOPENED:
        explanation = CaseExplanation(
            whats_happening=f"You told us this wasn't actually fixed, so we've sent it back to {authority.name} for another look.",
            current_blocker=f"{authority.name} needs to re-inspect and act on your update.",
            who_needs_to_act=authority.name,
            what_you_should_do="No action is required from you right now. You can escalate if it stays unresolved.",
            next_step_label="Re-inspection",
            then_step_label="Citizen Verification",
        )
    elif case.status == CaseStatus.CLOSED:
        explanation = CaseExplanation(
            whats_happening="You confirmed this issue is resolved, so this case is now closed.",
            current_blocker="None — there is nothing left to do.",
            who_needs_to_act="No one",
            what_you_should_do="Nothing further is needed. Thanks for confirming the outcome.",
            next_step_label="-",
            then_step_label="-",
        )
    else:
        explanation = case_intelligence.explain_case_state(understanding.category, case.current_stage)

    days_at_stage = sla_service.days_at_current_stage(case.last_status_change_at)
    current_responsibility = CurrentResponsibilityOut(
        authority_name=authority.name,
        role=authority.contact_role,
        jurisdiction_area=authority.jurisdiction_area,
        days_at_current_stage=days_at_stage,
    )

    similar_problems = repo.find_similar_problems(understanding.category, problem.location_text, problem.id)
    related_cases_out: list[RelatedCaseOut] = []
    for sim_problem in similar_problems:
        sim_case = next((c for c in repo.list_all_cases() if c.problem_id == sim_problem.id), None)
        if sim_case:
            related_cases_out.append(
                RelatedCaseOut(
                    case_number=sim_case.case_number,
                    issue_summary=sim_problem.ai_understanding.issue_summary if sim_problem.ai_understanding else sim_problem.raw_text,
                    location_text=sim_problem.location_text,
                    status=sim_case.status,
                )
            )

    community_reports = repo.list_community_reports_for_problem(problem.id)
    confirmed_count = sum(1 for r in community_reports if r.confirmation_type.value == "confirm")
    affected_count = len(similar_problems) + 1 + confirmed_count
    cluster = community_intelligence.cluster_related(len(similar_problems) + confirmed_count)

    evidence_list = repo.list_evidence_for_case(case.id)
    evidence_out = [
        EvidenceOut(
            id=e.id,
            file_name=e.file_name,
            description_text=e.description_text,
            interpretation=e.ai_interpretation,
            created_at=e.created_at,
        )
        for e in evidence_list
    ]

    escalations = repo.list_escalations_for_case(case.id)
    escalation_out = [
        EscalationOut(
            id=e.id,
            case_number=case.case_number,
            reason_text=e.reason_text,
            escalated_to_authority_name=repo.get_authority(e.escalated_to_authority_id).name,
            status=e.status,
            created_at=e.created_at,
        )
        for e in escalations
    ]

    return CaseDetailOut(
        case_number=case.case_number,
        status=case.status,
        understanding=understanding,
        authority=authority_resolution,
        explanation=explanation,
        current_responsibility=current_responsibility,
        timeline=timeline_out,
        sla=sla,
        community=CommunityOut(affected_count=affected_count, confirmed_count=confirmed_count, cluster=cluster),
        evidence=evidence_out,
        related_cases=related_cases_out,
        escalations=escalation_out,
        can_escalate=sla.is_overdue and case.status != CaseStatus.CLOSED,
        awaiting_citizen_verification=awaiting_verification,
    )


def mark_resolved(repo: Repository, case_id: str) -> Case:
    case = repo.get_case(case_id)
    if case is None:
        raise LookupError("Case not found")
    if case.status == CaseStatus.RESOLVED_PENDING_VERIFICATION:
        return case
    if case.status == CaseStatus.CLOSED:
        raise ValueError("Case is already closed")
    now = datetime.now(timezone.utc)

    existing_entries = repo.list_timeline_for_case(case.id)
    resolved_note = "The authority marked this case resolved. Awaiting citizen confirmation."
    reused_entry = next(
        (e for e in existing_entries if e.stage_name == VERIFICATION_STAGE_NAME and e.status != StageStatus.COMPLETED),
        None,
    )

    for entry in existing_entries:
        if entry.status == StageStatus.CURRENT and entry is not reused_entry:
            entry.status = StageStatus.COMPLETED
            repo.update_timeline_entry(entry)

    if reused_entry is not None:
        reused_entry.status = StageStatus.CURRENT
        reused_entry.actor_type = ActorType.AUTHORITY
        reused_entry.actor_name = "Authority"
        reused_entry.note = resolved_note
        reused_entry.occurred_at = now
        repo.update_timeline_entry(reused_entry)
    else:
        next_order = max((e.sequence_order for e in existing_entries), default=-1) + 1
        repo.create_timeline_entry(
            TimelineEntry(
                id=_new_id(),
                case_id=case.id,
                stage_name=VERIFICATION_STAGE_NAME,
                status=StageStatus.CURRENT,
                actor_type=ActorType.AUTHORITY,
                actor_name="Authority",
                note=resolved_note,
                occurred_at=now,
                sequence_order=next_order,
            )
        )

    case.status = CaseStatus.RESOLVED_PENDING_VERIFICATION
    case.current_stage = VERIFICATION_STAGE_NAME
    case.last_status_change_at = now
    case.updated_at = now
    return repo.update_case(case)


def verify_resolution(
    repo: Repository, case_id: str, is_actually_fixed: bool, explanation_text: str | None
) -> Case:
    case = repo.get_case(case_id)
    if case is None:
        raise LookupError("Case not found")
    if case.status != CaseStatus.RESOLVED_PENDING_VERIFICATION:
        raise ValueError("This case is not currently awaiting your verification.")
    now = datetime.now(timezone.utc)

    existing_entries = repo.list_timeline_for_case(case.id)
    verification_entry = next((e for e in existing_entries if e.stage_name == VERIFICATION_STAGE_NAME and e.status == StageStatus.CURRENT), None)

    if is_actually_fixed:
        if verification_entry:
            verification_entry.status = StageStatus.COMPLETED
            verification_entry.note = "Citizen confirmed the issue is resolved."
            repo.update_timeline_entry(verification_entry)
        case.status = CaseStatus.CLOSED
        case.current_stage = "Case Closed"
    else:
        if verification_entry:
            verification_entry.status = StageStatus.BLOCKED
            verification_entry.note = explanation_text or "Citizen reported the issue is still happening."
            repo.update_timeline_entry(verification_entry)
        next_order = max((e.sequence_order for e in existing_entries), default=-1) + 1
        repo.create_timeline_entry(
            TimelineEntry(
                id=_new_id(),
                case_id=case.id,
                stage_name="Reopened",
                status=StageStatus.CURRENT,
                actor_type=ActorType.CITIZEN,
                actor_name="You",
                note=explanation_text or "Citizen reported the issue is still happening. Case reopened for further action.",
                occurred_at=now,
                sequence_order=next_order,
            )
        )
        case.status = CaseStatus.REOPENED
        case.current_stage = "Reopened"

    case.resolution_verification_count += 1
    case.last_status_change_at = now
    case.updated_at = now
    return repo.update_case(case)


def escalate_case(repo: Repository, case_id: str) -> Escalation:
    case = repo.get_case(case_id)
    if case is None:
        raise LookupError("Case not found")
    problem = repo.get_problem(case.problem_id)
    service = repo.get_service(case.service_id)
    sla = sla_service.build_sla_out(case, service.sla_days)
    summary = escalation_intelligence.build_escalation_summary(
        problem.ai_understanding.issue_summary if problem.ai_understanding else problem.raw_text,
        sla.days_overdue,
    )
    escalation = repo.create_escalation(
        Escalation(
            id=_new_id(),
            case_id=case.id,
            escalated_to_authority_id=case.authority_id,
            reason_text=summary.reason_text,
            payload_snapshot={
                "case_number": case.case_number,
                "problem": problem.raw_text,
                "days_overdue": sla.days_overdue,
                "current_stage": case.current_stage,
            },
            status="submitted",
            created_at=datetime.now(timezone.utc),
        )
    )
    return escalation


def add_evidence(
    repo: Repository, case_id: str, uploaded_by: str, file_name: str, description_text: str | None, stage_context: str | None
) -> Evidence:
    from app.ai import evidence_intelligence

    case = repo.get_case(case_id)
    if case is None:
        raise LookupError("Case not found")
    problem = repo.get_problem(case.problem_id)
    category = problem.ai_understanding.category if problem.ai_understanding else None
    interpretation = evidence_intelligence.interpret_evidence(file_name, description_text, category) if category else None

    return repo.create_evidence(
        Evidence(
            id=_new_id(),
            case_id=case.id,
            uploaded_by=uploaded_by,
            file_name=file_name,
            description_text=description_text,
            ai_interpretation=interpretation,
            stage_context=stage_context,
            created_at=datetime.now(timezone.utc),
        )
    )


def determine_recommended_action(repo: Repository, case: Case) -> str:
    service = repo.get_service(case.service_id)
    sla = sla_service.build_sla_out(case, service.sla_days)
    return resolution_intelligence.determine_next_action(
        sla.is_overdue, case.status == CaseStatus.RESOLVED_PENDING_VERIFICATION
    )
