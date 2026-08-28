from fastapi import APIRouter, Depends, HTTPException

from app.db.repository import Repository
from app.deps import get_case_or_404, repo_dep
from app.models.domain import CaseDetailOut, CaseSummaryOut, CreateCaseResponse, ProblemIn
from app.services import case_service, sla_service

router = APIRouter(prefix="/api/cases", tags=["cases"])


@router.post("", response_model=CreateCaseResponse)
def create_case(payload: ProblemIn, repo: Repository = Depends(repo_dep)) -> CreateCaseResponse:
    if not payload.raw_text.strip():
        raise HTTPException(status_code=400, detail="raw_text is required")
    return case_service.create_case(repo, payload.citizen_id, payload.raw_text, payload.location_text)


@router.get("", response_model=list[CaseSummaryOut])
def list_cases(citizen_id: str, repo: Repository = Depends(repo_dep)) -> list[CaseSummaryOut]:
    cases = repo.list_cases_for_citizen(citizen_id)
    summaries: list[CaseSummaryOut] = []
    for case in cases:
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


@router.get("/{case_number}", response_model=CaseDetailOut)
def get_case_detail(case_number: str, repo: Repository = Depends(repo_dep)) -> CaseDetailOut:
    case = get_case_or_404(repo, case_number)
    return case_service.build_case_detail(repo, case)
