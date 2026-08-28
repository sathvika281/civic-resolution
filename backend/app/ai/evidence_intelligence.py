from app.ai.client import get_ai_client
from app.ai.fallback.rules import interpret_evidence_fallback
from app.ai.prompts import EVIDENCE_SYSTEM_PROMPT
from app.ai.schemas import EvidenceInterpretationPayload
from app.models.domain import EvidenceInterpretation
from app.models.enums import AiSource, ServiceCategory


def interpret_evidence(
    file_name: str, description_text: str | None, category: ServiceCategory
) -> EvidenceInterpretation:
    client = get_ai_client()
    if client.is_available():
        user_prompt = f"Category: {category.value}\nFile name: {file_name}\nDescription: {description_text or '(none provided)'}"
        result = client.complete_structured(EVIDENCE_SYSTEM_PROMPT, user_prompt, EvidenceInterpretationPayload)
        if result is not None:
            return EvidenceInterpretation(**result.model_dump(), source=AiSource.OPENAI)
    return interpret_evidence_fallback(file_name, description_text, category)
