from app.ai.client import get_ai_client
from app.ai.fallback.rules import understand_problem_fallback
from app.ai.prompts import INTENT_SYSTEM_PROMPT
from app.ai.schemas import ProblemUnderstandingPayload
from app.models.domain import ProblemUnderstanding
from app.models.enums import AiSource


def understand_problem(raw_text: str, location_text: str | None) -> ProblemUnderstanding:
    client = get_ai_client()
    if client.is_available():
        user_prompt = raw_text if not location_text else f"{raw_text}\n\nLocation: {location_text}"
        result = client.complete_structured(INTENT_SYSTEM_PROMPT, user_prompt, ProblemUnderstandingPayload)
        if result is not None:
            return ProblemUnderstanding(
                **result.model_dump(),
                location_text=location_text,
                source=AiSource.OPENAI,
            )
    return understand_problem_fallback(raw_text, location_text)
