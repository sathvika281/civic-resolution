from fastapi import APIRouter, Depends, HTTPException

from app.db.repository import Repository
from app.deps import get_case_or_404, repo_dep
from app.models.domain import CaseDetailOut, VerifyResolutionIn
from app.services import case_service

router = APIRouter(prefix="/api/cases", tags=["resolution"])


@router.post("/{case_number}/verify", response_model=CaseDetailOut)
def verify_resolution(case_number: str, payload: VerifyResolutionIn, repo: Repository = Depends(repo_dep)) -> CaseDetailOut:
    case = get_case_or_404(repo, case_number)
    try:
        updated_case = case_service.verify_resolution(repo, case.id, payload.is_actually_fixed, payload.explanation_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return case_service.build_case_detail(repo, updated_case)
