from fastapi import APIRouter, Depends

from app.db.repository import Repository
from app.deps import repo_dep
from app.models.domain import Citizen

router = APIRouter(prefix="/api/citizens", tags=["citizens"])


@router.get("", response_model=list[Citizen])
def list_citizens(repo: Repository = Depends(repo_dep)) -> list[Citizen]:
    return repo.list_citizens()
