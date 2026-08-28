from fastapi import APIRouter, Depends

from app.db.repository import Repository
from app.deps import get_case_or_404, repo_dep
from app.models.domain import CaseDetailOut, EvidenceIn
from app.services import case_service

router = APIRouter(prefix="/api/cases", tags=["evidence"])


@router.post("/{case_number}/evidence", response_model=CaseDetailOut)
def add_evidence(case_number: str, payload: EvidenceIn, repo: Repository = Depends(repo_dep)) -> CaseDetailOut:
    case = get_case_or_404(repo, case_number)
    case_service.add_evidence(
        repo, case.id, payload.uploaded_by, payload.file_name, payload.description_text, payload.stage_context
    )
    return case_service.build_case_detail(repo, case)
