import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.factory import force_in_memory_fallback, get_active_db_mode, get_repository
from app.routers import admin, cases, citizens, community, escalation, evidence, health, registry, resolution
from app.services.seed_service import seed_all

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("civic_resolution")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.demo_seed_on_startup:
        repo = get_repository()
        try:
            seed_all(repo)
        except Exception:
            if settings.supabase_url:
                log.warning(
                    "Supabase backend unreachable or not migrated yet — falling back to in-memory storage.",
                    exc_info=True,
                )
                repo = force_in_memory_fallback()
                seed_all(repo)
            else:
                raise
        log.info("Seeded demo data (ai_mode=%s, db_mode=%s)", settings.ai_mode, get_active_db_mode())
    yield


app = FastAPI(title="Civic Resolution API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(cases.router)
app.include_router(resolution.router)
app.include_router(escalation.router)
app.include_router(evidence.router)
app.include_router(community.router)
app.include_router(admin.router)
app.include_router(registry.router)
app.include_router(citizens.router)
