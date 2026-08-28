from datetime import datetime, timedelta, timezone

from app.models.domain import Case
from app.models.enums import CaseStatus
from app.services.sla_service import build_sla_out, compute_expected_resolution_date


def _make_case(opened_days_ago: int, sla_days: int) -> Case:
    now = datetime.now(timezone.utc)
    opened_at = now - timedelta(days=opened_days_ago)
    return Case(
        id="case-1",
        case_number="TEST-1",
        problem_id="problem-1",
        citizen_id="citizen-1",
        authority_id="authority-1",
        service_id="service-1",
        status=CaseStatus.IN_PROGRESS,
        current_stage="Assigned",
        opened_at=opened_at,
        expected_resolution_date=compute_expected_resolution_date(opened_at, sla_days),
        last_status_change_at=opened_at,
        created_at=opened_at,
        updated_at=now,
    )


def test_case_within_sla_is_not_overdue():
    case = _make_case(opened_days_ago=2, sla_days=5)
    sla = build_sla_out(case, sla_days=5)
    assert sla.is_overdue is False
    assert sla.days_overdue == 0


def test_case_past_sla_is_overdue_with_correct_day_count():
    case = _make_case(opened_days_ago=9, sla_days=5)
    sla = build_sla_out(case, sla_days=5)
    assert sla.is_overdue is True
    assert sla.days_overdue == 4
