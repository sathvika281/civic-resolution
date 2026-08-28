import json
import uuid
from datetime import datetime, timedelta, timezone
from importlib import resources

from app.ai.fallback.keywords import CATEGORY_META
from app.ai.fallback.rules import build_escalation_summary_fallback, interpret_evidence_fallback, understand_problem_fallback
from app.db.repository import Repository
from app.models.domain import Case, Citizen, CommunityReport, Escalation, Evidence, Problem, TimelineEntry
from app.models.enums import ActorType, CaseStatus, ConfirmationType, ServiceCategory, StageStatus
from app.services import registry_service, sla_service

SEED_NAMESPACE = uuid.UUID("87654321-4321-8765-4321-876543218765")


def _det_id(*parts: str) -> str:
    return str(uuid.uuid5(SEED_NAMESPACE, "|".join(parts)))


def _load_json(filename: str) -> list[dict]:
    with resources.files("app.seed").joinpath(filename).open("r", encoding="utf-8") as f:
        return json.load(f)


def seed_all(repo: Repository) -> None:
    registry_service.ensure_registry_seeded(repo)
    _seed_citizens(repo)
    _seed_cases(repo)


def _seed_citizens(repo: Repository) -> None:
    now = datetime.now(timezone.utc)
    for entry in _load_json("demo_citizens.json"):
        repo.upsert_citizen(
            Citizen(
                id=_det_id("citizen", entry["persona_key"]),
                display_name=entry["display_name"],
                persona_key=entry["persona_key"],
                phone=entry.get("phone"),
                created_at=now,
            )
        )


def _seed_cases(repo: Repository) -> None:
    now = datetime.now(timezone.utc)
    for scenario in _load_json("demo_cases.json"):
        citizen = repo.get_citizen_by_persona_key(scenario["persona_key"])
        if citizen is None:
            continue

        category = ServiceCategory(scenario["category"])
        service = registry_service.get_service_for_category(repo, category)

        understanding = understand_problem_fallback(scenario["raw_text"], scenario["location_text"])

        problem_id = _det_id("problem", scenario["case_number"])
        problem = repo.create_problem(
            Problem(
                id=problem_id,
                citizen_id=citizen.id,
                raw_text=scenario["raw_text"],
                location_text=scenario["location_text"],
                service_id=service.id,
                ai_understanding=understanding,
                created_at=now - timedelta(days=scenario["opened_days_ago"]),
            )
        )

        authority = repo.get_authority_by_name(CATEGORY_META[category]["authority_name"])

        opened_at = now - timedelta(days=scenario["opened_days_ago"])
        expected_resolution_date = sla_service.compute_expected_resolution_date(opened_at, service.sla_days)
        current_stage = next((s["stage_name"] for s in scenario["stages"] if s["status"] == "current"), service.stage_template[0])
        last_status_change_at = now - timedelta(days=next((s["days_ago"] for s in scenario["stages"] if s["status"] == "current"), 0))

        case = repo.create_case(
            Case(
                id=_det_id("case", scenario["case_number"]),
                case_number=scenario["case_number"],
                problem_id=problem.id,
                citizen_id=citizen.id,
                authority_id=authority.id,
                service_id=service.id,
                status=CaseStatus.IN_PROGRESS,
                current_stage=current_stage,
                opened_at=opened_at,
                expected_resolution_date=expected_resolution_date,
                last_status_change_at=last_status_change_at,
                created_at=opened_at,
                updated_at=now,
            )
        )

        for index, stage in enumerate(scenario["stages"]):
            repo.create_timeline_entry(
                TimelineEntry(
                    id=_det_id("timeline", scenario["case_number"], str(index)),
                    case_id=case.id,
                    stage_name=stage["stage_name"],
                    status=StageStatus(stage["status"]),
                    actor_type=ActorType(stage["actor_type"]),
                    actor_name=stage.get("actor_name"),
                    note=None,
                    occurred_at=now - timedelta(days=stage["days_ago"]),
                    sequence_order=index,
                )
            )

        for e_index, evidence in enumerate(scenario.get("evidence", [])):
            interpretation = interpret_evidence_fallback(evidence["file_name"], evidence["description_text"], category)
            repo.create_evidence(
                Evidence(
                    id=_det_id("evidence", scenario["case_number"], str(e_index)),
                    case_id=case.id,
                    uploaded_by=citizen.display_name,
                    file_name=evidence["file_name"],
                    description_text=evidence["description_text"],
                    ai_interpretation=interpretation,
                    stage_context=current_stage,
                    created_at=now - timedelta(days=evidence["days_ago"]),
                )
            )

        if scenario.get("escalated"):
            sla = sla_service.build_sla_out(case, service.sla_days)
            summary = build_escalation_summary_fallback(understanding.issue_summary, sla.days_overdue)
            repo.create_escalation(
                Escalation(
                    id=_det_id("escalation", scenario["case_number"]),
                    case_id=case.id,
                    escalated_to_authority_id=authority.id,
                    reason_text=summary.reason_text,
                    payload_snapshot={
                        "case_number": case.case_number,
                        "problem": scenario["raw_text"],
                        "days_overdue": sla.days_overdue,
                    },
                    status="submitted",
                    created_at=opened_at + timedelta(days=max(1, scenario["opened_days_ago"] // 2)),
                )
            )

        confirmations = scenario.get("community_confirmations", 0)
        for c_index in range(confirmations):
            repo.create_community_report(
                CommunityReport(
                    id=_det_id("community", scenario["case_number"], str(c_index)),
                    problem_id=problem.id,
                    case_id=case.id,
                    reporter_citizen_id=None,
                    confirmation_type=ConfirmationType.CONFIRM,
                    comment_text=None,
                    created_at=now - timedelta(days=c_index % max(1, scenario["opened_days_ago"])),
                )
            )
