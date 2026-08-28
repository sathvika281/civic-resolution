"""Hidden demo-only route: simulates an authority marking a case resolved.

Not linked from any citizen-facing navigation. Exists solely so the
resolution-verification loop can be triggered live during a demo.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.db.repository import Repository
from app.deps import get_case_or_404, repo_dep
from app.models.domain import CaseDetailOut, CaseSummaryOut
from app.services import case_service, sla_service

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/cases", response_model=list[CaseSummaryOut])
def list_all_cases(repo: Repository = Depends(repo_dep)) -> list[CaseSummaryOut]:
    summaries: list[CaseSummaryOut] = []
    for case in repo.list_all_cases():
        problem = repo.get_problem(case.problem_id)
        service = repo.get_service(case.service_id)
        if problem is None or service is None or problem.ai_understanding is None:
            continue
        sla = sla_service.build_sla_out(case, service.sla_days)
        summaries.append(
            CaseSummaryOut(
                case_number=case.case_number,
                issue_summary=problem.ai_understanding.issue_summary,
                category=problem.ai_understanding.category,
                status=case.status,
                is_overdue=sla.is_overdue,
                updated_at=case.updated_at,
            )
        )
    return sorted(summaries, key=lambda s: s.updated_at, reverse=True)


@router.post("/cases/{case_number}/mark-resolved", response_model=CaseDetailOut)
def mark_resolved(case_number: str, repo: Repository = Depends(repo_dep)) -> CaseDetailOut:
    case = get_case_or_404(repo, case_number)
    try:
        updated_case = case_service.mark_resolved(repo, case.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return case_service.build_case_detail(repo, updated_case)
