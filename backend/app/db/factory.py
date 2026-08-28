from app.config import settings
from app.db.memory_repo import InMemoryRepository
from app.db.repository import Repository

_repository_instance: Repository | None = None


def get_repository() -> Repository:
    global _repository_instance
    if _repository_instance is None:
        if settings.supabase_url:
            from app.db.supabase_repo import SupabaseRepository

            _repository_instance = SupabaseRepository(settings)
        else:
            _repository_instance = InMemoryRepository()
    return _repository_instance


def force_in_memory_fallback() -> Repository:
    """Called when a configured Supabase backend is unreachable at startup
    (e.g. migration not yet run). Swaps the active repository to an
    in-memory one so the app stays usable rather than crashing."""
    global _repository_instance
    _repository_instance = InMemoryRepository()
    return _repository_instance


def get_active_db_mode() -> str:
    if _repository_instance is not None and not isinstance(_repository_instance, InMemoryRepository):
        return "supabase"
    return "in_memory"
