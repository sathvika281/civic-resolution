from fastapi import HTTPException

from app.db.factory import get_repository
from app.db.repository import Repository
from app.models.domain import Case


def repo_dep() -> Repository:
    return get_repository()


def get_case_or_404(repo: Repository, case_number: str) -> Case:
    case = repo.get_case_by_number(case_number)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
