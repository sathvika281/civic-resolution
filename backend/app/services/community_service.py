import uuid
from datetime import datetime, timezone

from app.db.repository import Repository
from app.models.domain import CommunityReport, NearbyProblemOut
from app.models.enums import ConfirmationType
from app.services import sla_service


def confirm_problem(repo: Repository, case_id: str, citizen_id: str, comment_text: str | None) -> CommunityReport:
    case = repo.get_case(case_id)
    if case is None:
        raise LookupError("Case not found")
    return repo.create_community_report(
        CommunityReport(
            id=str(uuid.uuid4()),
            problem_id=case.problem_id,
            case_id=case.id,
            reporter_citizen_id=citizen_id,
            confirmation_type=ConfirmationType.CONFIRM if comment_text is None else ConfirmationType.COMMENT,
            comment_text=comment_text,
            created_at=datetime.now(timezone.utc),
        )
    )


def list_nearby_problems(repo: Repository, exclude_citizen_id: str | None = None) -> list[NearbyProblemOut]:
    results: list[NearbyProblemOut] = []
    for case in repo.list_all_cases():
        if exclude_citizen_id and case.citizen_id == exclude_citizen_id:
            continue
        problem = repo.get_problem(case.problem_id)
        service = repo.get_service(case.service_id)
        if problem is None or service is None or problem.ai_understanding is None:
            continue
        similar = repo.find_similar_problems(problem.ai_understanding.category, problem.location_text, problem.id)
        reports = repo.list_community_reports_for_problem(problem.id)
        confirmed_count = sum(1 for r in reports if r.confirmation_type == ConfirmationType.CONFIRM)
        sla = sla_service.build_sla_out(case, service.sla_days)
        results.append(
            NearbyProblemOut(
                case_number=case.case_number,
                issue_summary=problem.ai_understanding.issue_summary,
                category=problem.ai_understanding.category,
                location_text=problem.location_text,
                status=case.status,
                affected_count=len(similar) + 1 + confirmed_count,
                confirmed_count=confirmed_count,
                is_overdue=sla.is_overdue,
            )
        )
    return results
