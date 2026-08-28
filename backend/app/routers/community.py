from fastapi import APIRouter, Depends

from app.db.repository import Repository
from app.deps import get_case_or_404, repo_dep
from app.models.domain import CaseDetailOut, ConfirmIn, NearbyProblemOut
from app.services import case_service, community_service

router = APIRouter(prefix="/api", tags=["community"])


@router.get("/community/nearby", response_model=list[NearbyProblemOut])
def nearby_problems(exclude_citizen_id: str | None = None, repo: Repository = Depends(repo_dep)) -> list[NearbyProblemOut]:
    return community_service.list_nearby_problems(repo, exclude_citizen_id)


@router.post("/cases/{case_number}/confirm", response_model=CaseDetailOut)
def confirm_case(case_number: str, payload: ConfirmIn, repo: Repository = Depends(repo_dep)) -> CaseDetailOut:
    case = get_case_or_404(repo, case_number)
    community_service.confirm_problem(repo, case.id, payload.citizen_id, payload.comment_text)
    return case_service.build_case_detail(repo, case)
