from abc import ABC, abstractmethod

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


class Repository(ABC):
    """Storage-agnostic interface. Routers/services depend only on this so the
    active backend (in-memory today, Supabase once credentials land) can be
    swapped via app.db.factory without touching business logic."""

    # Citizens
    @abstractmethod
    def upsert_citizen(self, citizen: Citizen) -> Citizen: ...

    @abstractmethod
    def get_citizen(self, citizen_id: str) -> Citizen | None: ...

    @abstractmethod
    def get_citizen_by_persona_key(self, persona_key: str) -> Citizen | None: ...

    @abstractmethod
    def list_citizens(self) -> list[Citizen]: ...

    # Authorities
    @abstractmethod
    def upsert_authority(self, authority: Authority) -> Authority: ...

    @abstractmethod
    def get_authority(self, authority_id: str) -> Authority | None: ...

    @abstractmethod
    def get_authority_by_name(self, name: str) -> Authority | None: ...

    @abstractmethod
    def list_authorities(self) -> list[Authority]: ...

    # Services
    @abstractmethod
    def upsert_service(self, service: Service) -> Service: ...

    @abstractmethod
    def get_service(self, service_id: str) -> Service | None: ...

    @abstractmethod
    def get_service_by_category(self, category: ServiceCategory) -> Service | None: ...

    @abstractmethod
    def list_services(self) -> list[Service]: ...

    # Problems
    @abstractmethod
    def create_problem(self, problem: Problem) -> Problem: ...

    @abstractmethod
    def get_problem(self, problem_id: str) -> Problem | None: ...

    @abstractmethod
    def list_problems(self) -> list[Problem]: ...

    # Cases
    @abstractmethod
    def create_case(self, case: Case) -> Case: ...

    @abstractmethod
    def get_case(self, case_id: str) -> Case | None: ...

    @abstractmethod
    def get_case_by_number(self, case_number: str) -> Case | None: ...

    @abstractmethod
    def update_case(self, case: Case) -> Case: ...

    @abstractmethod
    def list_cases_for_citizen(self, citizen_id: str) -> list[Case]: ...

    @abstractmethod
    def list_all_cases(self) -> list[Case]: ...

    # Timeline
    @abstractmethod
    def create_timeline_entry(self, entry: TimelineEntry) -> TimelineEntry: ...

    @abstractmethod
    def update_timeline_entry(self, entry: TimelineEntry) -> TimelineEntry: ...

    @abstractmethod
    def list_timeline_for_case(self, case_id: str) -> list[TimelineEntry]: ...

    # Evidence
    @abstractmethod
    def create_evidence(self, evidence: Evidence) -> Evidence: ...

    @abstractmethod
    def list_evidence_for_case(self, case_id: str) -> list[Evidence]: ...

    # Community
    @abstractmethod
    def create_community_report(self, report: CommunityReport) -> CommunityReport: ...

    @abstractmethod
    def list_community_reports_for_problem(self, problem_id: str) -> list[CommunityReport]: ...

    @abstractmethod
    def list_all_community_reports(self) -> list[CommunityReport]: ...

    # Escalations
    @abstractmethod
    def create_escalation(self, escalation: Escalation) -> Escalation: ...

    @abstractmethod
    def list_escalations_for_case(self, case_id: str) -> list[Escalation]: ...

    # Similarity / clustering support
    @abstractmethod
    def find_similar_problems(
        self, category: ServiceCategory, location_text: str | None, exclude_problem_id: str
    ) -> list[Problem]: ...
