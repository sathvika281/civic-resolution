from app.db.repository import Repository
from app.models.domain import (
    Authority,
    Case,
    Citizen,
    CommunityReport,
    Escalation,
    Evidence,
    Problem,
    Service,
    TimelineEntry,
)
from app.models.enums import ServiceCategory


class InMemoryRepository(Repository):
    def __init__(self):
        self._citizens: dict[str, Citizen] = {}
        self._authorities: dict[str, Authority] = {}
        self._services: dict[str, Service] = {}
        self._problems: dict[str, Problem] = {}
        self._cases: dict[str, Case] = {}
        self._timeline: dict[str, TimelineEntry] = {}
        self._evidence: dict[str, Evidence] = {}
        self._community_reports: dict[str, CommunityReport] = {}
        self._escalations: dict[str, Escalation] = {}

    # Citizens
    def upsert_citizen(self, citizen: Citizen) -> Citizen:
        self._citizens[citizen.id] = citizen
        return citizen

    def get_citizen(self, citizen_id: str) -> Citizen | None:
        return self._citizens.get(citizen_id)

    def get_citizen_by_persona_key(self, persona_key: str) -> Citizen | None:
        return next((c for c in self._citizens.values() if c.persona_key == persona_key), None)

    def list_citizens(self) -> list[Citizen]:
        return list(self._citizens.values())

    # Authorities
    def upsert_authority(self, authority: Authority) -> Authority:
        self._authorities[authority.id] = authority
        return authority

    def get_authority(self, authority_id: str) -> Authority | None:
        return self._authorities.get(authority_id)

    def get_authority_by_name(self, name: str) -> Authority | None:
        return next((a for a in self._authorities.values() if a.name == name), None)

    def list_authorities(self) -> list[Authority]:
        return list(self._authorities.values())

    # Services
    def upsert_service(self, service: Service) -> Service:
        self._services[service.id] = service
        return service

    def get_service(self, service_id: str) -> Service | None:
        return self._services.get(service_id)

    def get_service_by_category(self, category: ServiceCategory) -> Service | None:
        return next((s for s in self._services.values() if s.category == category), None)

    def list_services(self) -> list[Service]:
        return list(self._services.values())

    # Problems
    def create_problem(self, problem: Problem) -> Problem:
        self._problems[problem.id] = problem
        return problem

    def get_problem(self, problem_id: str) -> Problem | None:
        return self._problems.get(problem_id)

    def list_problems(self) -> list[Problem]:
        return list(self._problems.values())

    # Cases
    def create_case(self, case: Case) -> Case:
        self._cases[case.id] = case
        return case

    def get_case(self, case_id: str) -> Case | None:
        return self._cases.get(case_id)

    def get_case_by_number(self, case_number: str) -> Case | None:
        return next((c for c in self._cases.values() if c.case_number == case_number), None)

    def update_case(self, case: Case) -> Case:
        self._cases[case.id] = case
        return case

    def list_cases_for_citizen(self, citizen_id: str) -> list[Case]:
        return [c for c in self._cases.values() if c.citizen_id == citizen_id]

    def list_all_cases(self) -> list[Case]:
        return list(self._cases.values())

    # Timeline
    def create_timeline_entry(self, entry: TimelineEntry) -> TimelineEntry:
        self._timeline[entry.id] = entry
        return entry

    def update_timeline_entry(self, entry: TimelineEntry) -> TimelineEntry:
        self._timeline[entry.id] = entry
        return entry

    def list_timeline_for_case(self, case_id: str) -> list[TimelineEntry]:
        entries = [t for t in self._timeline.values() if t.case_id == case_id]
        return sorted(entries, key=lambda t: t.sequence_order)

    # Evidence
    def create_evidence(self, evidence: Evidence) -> Evidence:
        self._evidence[evidence.id] = evidence
        return evidence

    def list_evidence_for_case(self, case_id: str) -> list[Evidence]:
        entries = [e for e in self._evidence.values() if e.case_id == case_id]
        return sorted(entries, key=lambda e: e.created_at)

    # Community
    def create_community_report(self, report: CommunityReport) -> CommunityReport:
        self._community_reports[report.id] = report
        return report

    def list_community_reports_for_problem(self, problem_id: str) -> list[CommunityReport]:
        return [r for r in self._community_reports.values() if r.problem_id == problem_id]

    def list_all_community_reports(self) -> list[CommunityReport]:
        return list(self._community_reports.values())

    # Escalations
    def create_escalation(self, escalation: Escalation) -> Escalation:
        self._escalations[escalation.id] = escalation
        return escalation

    def list_escalations_for_case(self, case_id: str) -> list[Escalation]:
        entries = [e for e in self._escalations.values() if e.case_id == case_id]
        return sorted(entries, key=lambda e: e.created_at)

    # Similarity
    def find_similar_problems(
        self, category: ServiceCategory, location_text: str | None, exclude_problem_id: str
    ) -> list[Problem]:
        results = []
        for problem in self._problems.values():
            if problem.id == exclude_problem_id:
                continue
            understanding = problem.ai_understanding
            if understanding is None or understanding.category != category:
                continue
            if location_text and problem.location_text:
                loc_a = location_text.lower()
                loc_b = problem.location_text.lower()
                if loc_a not in loc_b and loc_b not in loc_a:
                    continue
            results.append(problem)
        return results
