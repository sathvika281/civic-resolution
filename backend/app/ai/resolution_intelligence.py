from app.ai.fallback.rules import determine_next_action_fallback


def determine_next_action(is_overdue: bool, awaiting_verification: bool) -> str:
    return determine_next_action_fallback(is_overdue, awaiting_verification)
