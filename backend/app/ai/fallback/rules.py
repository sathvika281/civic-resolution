"""Deterministic fallback implementations. Mirrors the contract of every
ai/*.py module so routers/services never need to know which path ran."""

from app.ai.fallback.keywords import (
    CATEGORY_KEYWORDS,
    CATEGORY_META,
    EMERGENCY_KEYWORDS,
    PRIVATE_DISPUTE_KEYWORDS,
    URGENCY_KEYWORDS,
)
from app.ai.fallback.templates import get_template
from app.models.domain import (
    AuthorityResolution,
    CaseExplanation,
    ClusterResult,
    EscalationSummary,
    EvidenceInterpretation,
    ProblemUnderstanding,
    SafetyScreenResult,
)
from app.models.enums import AiSource, ServiceCategory, UrgencyLevel


def _matches_any(text: str, phrases: list[str]) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in phrases)


def screen_safety_fallback(raw_text: str) -> SafetyScreenResult:
    if _matches_any(raw_text, EMERGENCY_KEYWORDS):
        return SafetyScreenResult(
            is_safe_for_workflow=False,
            reason="emergency",
            redirect_message=(
                "This sounds like it may involve immediate danger. This prototype cannot help with "
                "emergencies — please contact the appropriate emergency service directly."
            ),
            source=AiSource.FALLBACK,
        )
    if _matches_any(raw_text, PRIVATE_DISPUTE_KEYWORDS):
        return SafetyScreenResult(
            is_safe_for_workflow=False,
            reason="private_dispute",
            redirect_message=(
                "This appears to be a private/personal dispute rather than a government-service issue, "
                "so this platform isn't the right channel for it."
            ),
            source=AiSource.FALLBACK,
        )
    return SafetyScreenResult(is_safe_for_workflow=True, source=AiSource.FALLBACK)


def classify_category_fallback(raw_text: str) -> ServiceCategory:
    lowered = raw_text.lower()
    best_category = ServiceCategory.OTHER
    best_hits = 0
    for category, phrases in CATEGORY_KEYWORDS.items():
        hits = sum(1 for phrase in phrases if phrase in lowered)
        if hits > best_hits:
            best_hits = hits
            best_category = category
    return best_category


def _classify_urgency(raw_text: str) -> UrgencyLevel:
    lowered = raw_text.lower()
    for level in (UrgencyLevel.HIGH, UrgencyLevel.MEDIUM, UrgencyLevel.LOW):
        if _matches_any(lowered, URGENCY_KEYWORDS[level]):
            return level
    return UrgencyLevel.MEDIUM


def understand_problem_fallback(raw_text: str, location_text: str | None) -> ProblemUnderstanding:
    category = classify_category_fallback(raw_text)
    meta = CATEGORY_META[category]
    urgency = _classify_urgency(raw_text)
    return ProblemUnderstanding(
        issue_summary=meta["display_name"],
        category=category,
        location_text=location_text,
        urgency=urgency,
        likely_required_evidence=meta["required_evidence"],
        likely_next_action=f"We'll route this to {meta['authority_name']} ({meta['department']}).",
        source=AiSource.FALLBACK,
    )


def resolve_authority_fallback(category: ServiceCategory) -> AuthorityResolution:
    meta = CATEGORY_META.get(category, CATEGORY_META[ServiceCategory.OTHER])
    return AuthorityResolution(
        authority_name=meta["authority_name"],
        authority_type=meta["authority_type"],
        department=meta["department"],
        jurisdiction_area=meta["jurisdiction_area"],
        responsible_role=meta["responsible_role"],
        source=AiSource.FALLBACK,
    )


def explain_case_state_fallback(category: ServiceCategory, stage_name: str) -> CaseExplanation:
    template = get_template(category, stage_name)
    return CaseExplanation(
        whats_happening=template["whats_happening"],
        current_blocker=template["current_blocker"],
        who_needs_to_act=template["who_needs_to_act"],
        what_you_should_do=template["what_you_should_do"],
        next_step_label=template["next_step_label"],
        then_step_label=template["then_step_label"],
        source=AiSource.FALLBACK,
    )


def determine_next_action_fallback(is_overdue: bool, awaiting_verification: bool) -> str:
    if awaiting_verification:
        return "Confirm whether the issue is actually resolved."
    if is_overdue:
        return "This case is overdue — consider escalating it."
    return "No action needed right now — we'll keep tracking this for you."


def cluster_related_fallback(similar_count: int) -> ClusterResult:
    if similar_count >= 3:
        return ClusterResult(
            possible_common_issue=True,
            summary=f"Possible common issue detected — {similar_count} nearby reports may describe the same underlying problem.",
            source=AiSource.FALLBACK,
        )
    return ClusterResult(
        possible_common_issue=False,
        summary="No strong pattern detected yet across nearby reports.",
        source=AiSource.FALLBACK,
    )


def interpret_evidence_fallback(
    file_name: str, description_text: str | None, category: ServiceCategory
) -> EvidenceInterpretation:
    meta = CATEGORY_META.get(category, CATEGORY_META[ServiceCategory.OTHER])
    lowered = (description_text or file_name).lower()
    likely_shows = f"This appears related to: {meta['display_name'].lower()}."
    if "reject" in lowered or "notice" in lowered:
        likely_shows = "This appears to be a rejection or official notice document."
    elif "photo" in lowered or file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        likely_shows = f"Likely photo evidence of: {meta['display_name'].lower()}."

    missing_info_hint = None
    if "location" not in lowered and category in {ServiceCategory.STREETLIGHT, ServiceCategory.POTHOLE, ServiceCategory.WATER_SUPPLY}:
        missing_info_hint = "Exact location may be needed — consider adding a nearby landmark."

    return EvidenceInterpretation(
        likely_shows=likely_shows,
        missing_info_hint=missing_info_hint,
        consistent_with_original_issue=True,
        source=AiSource.FALLBACK,
    )


def build_escalation_summary_fallback(issue_summary: str, days_overdue: int) -> EscalationSummary:
    return EscalationSummary(
        reason_text=(
            f"This case ('{issue_summary}') has exceeded its expected resolution window by "
            f"{days_overdue} day(s) with no update. Escalating for priority action."
        ),
        source=AiSource.FALLBACK,
    )
