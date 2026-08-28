import logging

from pydantic import BaseModel

from app.config import Settings

log = logging.getLogger("civic_resolution.ai")


class OpenAIClientWrapper:
    """Thin wrapper around the OpenAI client with graceful degradation.

    Every intelligence module calls `complete_structured`; a `None` return
    (missing key, network error, timeout, bad response) is the caller's
    signal to fall back to the deterministic rules path.
    """

    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = None
        if settings.openai_api_key:
            try:
                from openai import OpenAI

                self._client = OpenAI(api_key=settings.openai_api_key)
            except Exception:
                log.warning("Failed to initialize OpenAI client", exc_info=True)
                self._client = None

    def is_available(self) -> bool:
        return self._client is not None

    def complete_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type[BaseModel],
        timeout: float = 8.0,
    ) -> BaseModel | None:
        if self._client is None:
            return None
        try:
            response = self._client.beta.chat.completions.parse(
                model=self._settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=response_model,
                timeout=timeout,
            )
            parsed = response.choices[0].message.parsed
            return parsed
        except Exception:
            log.warning("OpenAI structured completion failed, falling back", exc_info=True)
            return None


_client_instance: OpenAIClientWrapper | None = None


def get_ai_client() -> OpenAIClientWrapper:
    global _client_instance
    if _client_instance is None:
        from app.config import settings

        _client_instance = OpenAIClientWrapper(settings)
    return _client_instance
