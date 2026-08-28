from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    supabase_anon_key: str | None = None

    env: str = "development"
    cors_allow_origins: str = "http://localhost:5173"
    demo_seed_on_startup: bool = True

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]

    @property
    def ai_mode(self) -> str:
        return "openai" if self.openai_api_key else "fallback"

    @property
    def db_mode(self) -> str:
        return "supabase" if self.supabase_url else "in_memory"


settings = Settings()
