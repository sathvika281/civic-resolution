from app.ai.client import get_ai_client
from app.ai.fallback.rules import screen_safety_fallback
from app.ai.prompts import SAFETY_SYSTEM_PROMPT
from app.ai.schemas import SafetyScreenPayload
from app.models.domain import SafetyScreenResult
from app.models.enums import AiSource


def screen(raw_text: str) -> SafetyScreenResult:
    client = get_ai_client()
    if client.is_available():
        result = client.complete_structured(SAFETY_SYSTEM_PROMPT, raw_text, SafetyScreenPayload)
        if result is not None:
            return SafetyScreenResult(**result.model_dump(), source=AiSource.OPENAI)
    return screen_safety_fallback(raw_text)
