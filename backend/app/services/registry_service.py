"""Mock government service registry, built from the category metadata in
app.ai.fallback.keywords.CATEGORY_META (the single source of truth for
synthetic authorities/services/SLAs/stage templates in this prototype)."""

import uuid
from datetime import datetime, timezone

from app.ai.fallback.keywords import CATEGORY_META
from app.db.repository import Repository
from app.models.domain import Authority, Service
from app.models.enums import ServiceCategory

NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


def _deterministic_id(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "|".join(parts)))


def ensure_registry_seeded(repo: Repository) -> None:
    now = datetime.now(timezone.utc)
    authority_ids_by_name: dict[str, str] = {}

    for category, meta in CATEGORY_META.items():
        authority_name = meta["authority_name"]
        if authority_name not in authority_ids_by_name:
            authority_id = _deterministic_id("authority", authority_name)
            authority_ids_by_name[authority_name] = authority_id
            repo.upsert_authority(
                Authority(
                    id=authority_id,
                    name=authority_name,
                    authority_type=meta["authority_type"],
                    jurisdiction_area=meta["jurisdiction_area"],
                    contact_person_name=_synthetic_contact_name(category),
                    contact_role=meta["responsible_role"],
                    escalation_authority_id=None,
                    created_at=now,
                )
            )

        service_id = _deterministic_id("service", category.value)
        repo.upsert_service(
            Service(
                id=service_id,
                category=category,
                display_name=meta["display_name"],
                description=meta["description"],
                default_authority_type=meta["authority_type"],
                required_evidence=meta["required_evidence"],
                sla_days=meta["sla_days"],
                stage_template=meta["stage_template"],
                created_at=now,
            )
        )


def _synthetic_contact_name(category: ServiceCategory) -> str:
    names = {
        ServiceCategory.STREETLIGHT: "R. Kumar",
        ServiceCategory.POTHOLE: "S. Iyer",
        ServiceCategory.WATER_SUPPLY: "A. Reddy",
        ServiceCategory.PF_CLAIM: "M. Sharma",
        ServiceCategory.PENSION: "K. Nair",
        ServiceCategory.SCHOLARSHIP: "P. Verma",
        ServiceCategory.CERTIFICATE: "T. Rao",
        ServiceCategory.OTHER: "Grievance Desk",
    }
    return names.get(category, "Duty Officer")


def get_service_for_category(repo: Repository, category: ServiceCategory) -> Service:
    service = repo.get_service_by_category(category)
    if service is None:
        raise LookupError(f"No service registered for category {category}")
    return service


def get_authority_for_name(repo: Repository, name: str) -> Authority:
    authority = repo.get_authority_by_name(name)
    if authority is None:
        raise LookupError(f"No authority registered with name {name}")
    return authority
