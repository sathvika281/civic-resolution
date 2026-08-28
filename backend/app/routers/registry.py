from fastapi import APIRouter, Depends

from app.db.repository import Repository
from app.deps import repo_dep
from app.models.domain import Authority, Service

router = APIRouter(prefix="/api/registry", tags=["registry"])


@router.get("/services", response_model=list[Service])
def list_services(repo: Repository = Depends(repo_dep)) -> list[Service]:
    return repo.list_services()


@router.get("/authorities", response_model=list[Authority])
def list_authorities(repo: Repository = Depends(repo_dep)) -> list[Authority]:
    return repo.list_authorities()
