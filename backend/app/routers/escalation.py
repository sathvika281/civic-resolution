from fastapi import APIRouter, Depends, HTTPException

from app.db.repository import Repository
from app.deps import get_case_or_404, repo_dep
from app.models.domain import CaseDetailOut, EscalateIn
from app.services import case_service, sla_service

router = APIRouter(prefix="/api/cases", tags=["escalation"])


@router.post("/{case_number}/escalate", response_model=CaseDetailOut)
def escalate_case(case_number: str, payload: EscalateIn, repo: Repository = Depends(repo_dep)) -> CaseDetailOut:
    case = get_case_or_404(repo, case_number)
    service = repo.get_service(case.service_id)
    sla = sla_service.build_sla_out(case, service.sla_days)
    if not sla.is_overdue:
        raise HTTPException(status_code=400, detail="Case is not overdue yet, escalation is not available.")
    existing = repo.list_escalations_for_case(case.id)
    if any(e.status == "submitted" for e in existing):
        raise HTTPException(status_code=400, detail="This case has already been escalated and is awaiting a response.")
    case_service.escalate_case(repo, case.id)
    return case_service.build_case_detail(repo, case)
