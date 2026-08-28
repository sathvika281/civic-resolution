from app.ai.fallback.rules import build_escalation_summary_fallback
from app.models.domain import EscalationSummary


def build_escalation_summary(issue_summary: str, days_overdue: int) -> EscalationSummary:
    return build_escalation_summary_fallback(issue_summary, days_overdue)
