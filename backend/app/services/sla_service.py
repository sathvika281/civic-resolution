from datetime import date, datetime, timedelta, timezone

from app.models.domain import Case, SlaOut


def compute_expected_resolution_date(opened_at: datetime, sla_days: int) -> date:
    return (opened_at + timedelta(days=sla_days)).date()


def build_sla_out(case: Case, sla_days: int) -> SlaOut:
    now = datetime.now(timezone.utc)
    current_days = (now - case.opened_at).days
    days_overdue = max(0, (now.date() - case.expected_resolution_date).days)
    return SlaOut(
        expected_days=sla_days,
        current_days=current_days,
        is_overdue=days_overdue > 0,
        days_overdue=days_overdue,
    )


def days_at_current_stage(last_status_change_at: datetime) -> int:
    now = datetime.now(timezone.utc)
    return max(0, (now - last_status_change_at).days)
