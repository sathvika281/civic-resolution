from supabase import Client, create_client

from app.config import Settings
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


def _dump(model) -> dict:
    return model.model_dump(mode="json")


class SupabaseRepository(Repository):
    def __init__(self, settings: Settings):
        self._client: Client = create_client(settings.supabase_url, settings.supabase_service_role_key)

    # Citizens
    def upsert_citizen(self, citizen: Citizen) -> Citizen:
        self._client.table("citizens").upsert(_dump(citizen), on_conflict="persona_key").execute()
        return citizen

    def get_citizen(self, citizen_id: str) -> Citizen | None:
        res = self._client.table("citizens").select("*").eq("id", citizen_id).limit(1).execute()
        return Citizen(**res.data[0]) if res.data else None

    def get_citizen_by_persona_key(self, persona_key: str) -> Citizen | None:
        res = self._client.table("citizens").select("*").eq("persona_key", persona_key).limit(1).execute()
        return Citizen(**res.data[0]) if res.data else None

    def list_citizens(self) -> list[Citizen]:
        res = self._client.table("citizens").select("*").execute()
        return [Citizen(**row) for row in res.data]

    # Authorities
    def upsert_authority(self, authority: Authority) -> Authority:
        self._client.table("authorities").upsert(_dump(authority), on_conflict="name").execute()
        return authority

    def get_authority(self, authority_id: str) -> Authority | None:
        res = self._client.table("authorities").select("*").eq("id", authority_id).limit(1).execute()
        return Authority(**res.data[0]) if res.data else None

    def get_authority_by_name(self, name: str) -> Authority | None:
        res = self._client.table("authorities").select("*").eq("name", name).limit(1).execute()
        return Authority(**res.data[0]) if res.data else None

    def list_authorities(self) -> list[Authority]:
        res = self._client.table("authorities").select("*").execute()
        return [Authority(**row) for row in res.data]

    # Services
    def upsert_service(self, service: Service) -> Service:
        self._client.table("services").upsert(_dump(service), on_conflict="category").execute()
        return service

    def get_service(self, service_id: str) -> Service | None:
        res = self._client.table("services").select("*").eq("id", service_id).limit(1).execute()
        return Service(**res.data[0]) if res.data else None

    def get_service_by_category(self, category: ServiceCategory) -> Service | None:
        res = self._client.table("services").select("*").eq("category", category.value).limit(1).execute()
        return Service(**res.data[0]) if res.data else None

    def list_services(self) -> list[Service]:
        res = self._client.table("services").select("*").execute()
        return [Service(**row) for row in res.data]

    # Problems
    def create_problem(self, problem: Problem) -> Problem:
        self._client.table("problems").upsert(_dump(problem)).execute()
        return problem

    def get_problem(self, problem_id: str) -> Problem | None:
        res = self._client.table("problems").select("*").eq("id", problem_id).limit(1).execute()
        return Problem(**res.data[0]) if res.data else None

    def list_problems(self) -> list[Problem]:
        res = self._client.table("problems").select("*").execute()
        return [Problem(**row) for row in res.data]

    # Cases
    def create_case(self, case: Case) -> Case:
        self._client.table("cases").upsert(_dump(case)).execute()
        return case

    def get_case(self, case_id: str) -> Case | None:
        res = self._client.table("cases").select("*").eq("id", case_id).limit(1).execute()
        return Case(**res.data[0]) if res.data else None

    def get_case_by_number(self, case_number: str) -> Case | None:
        res = self._client.table("cases").select("*").eq("case_number", case_number).limit(1).execute()
        return Case(**res.data[0]) if res.data else None

    def update_case(self, case: Case) -> Case:
        self._client.table("cases").upsert(_dump(case)).execute()
        return case

    def list_cases_for_citizen(self, citizen_id: str) -> list[Case]:
        res = self._client.table("cases").select("*").eq("citizen_id", citizen_id).execute()
        return [Case(**row) for row in res.data]

    def list_all_cases(self) -> list[Case]:
        res = self._client.table("cases").select("*").execute()
        return [Case(**row) for row in res.data]

    # Timeline
    def create_timeline_entry(self, entry: TimelineEntry) -> TimelineEntry:
        self._client.table("case_timeline").upsert(_dump(entry)).execute()
        return entry

    def update_timeline_entry(self, entry: TimelineEntry) -> TimelineEntry:
        self._client.table("case_timeline").upsert(_dump(entry)).execute()
        return entry

    def list_timeline_for_case(self, case_id: str) -> list[TimelineEntry]:
        res = (
            self._client.table("case_timeline")
            .select("*")
            .eq("case_id", case_id)
            .order("sequence_order")
            .execute()
        )
        return [TimelineEntry(**row) for row in res.data]

    # Evidence
    def create_evidence(self, evidence: Evidence) -> Evidence:
        self._client.table("evidence").upsert(_dump(evidence)).execute()
        return evidence

    def list_evidence_for_case(self, case_id: str) -> list[Evidence]:
        res = self._client.table("evidence").select("*").eq("case_id", case_id).order("created_at").execute()
        return [Evidence(**row) for row in res.data]

    # Community
    def create_community_report(self, report: CommunityReport) -> CommunityReport:
        self._client.table("community_reports").upsert(_dump(report)).execute()
        return report

    def list_community_reports_for_problem(self, problem_id: str) -> list[CommunityReport]:
        res = self._client.table("community_reports").select("*").eq("problem_id", problem_id).execute()
        return [CommunityReport(**row) for row in res.data]

    def list_all_community_reports(self) -> list[CommunityReport]:
        res = self._client.table("community_reports").select("*").execute()
        return [CommunityReport(**row) for row in res.data]

    # Escalations
    def create_escalation(self, escalation: Escalation) -> Escalation:
        self._client.table("escalations").upsert(_dump(escalation)).execute()
        return escalation

    def list_escalations_for_case(self, case_id: str) -> list[Escalation]:
        res = self._client.table("escalations").select("*").eq("case_id", case_id).order("created_at").execute()
        return [Escalation(**row) for row in res.data]

    # Similarity
    def find_similar_problems(
        self, category: ServiceCategory, location_text: str | None, exclude_problem_id: str
    ) -> list[Problem]:
        res = self._client.table("problems").select("*").neq("id", exclude_problem_id).execute()
        results = []
        for row in res.data:
            problem = Problem(**row)
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
