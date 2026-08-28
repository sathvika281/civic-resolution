from enum import StrEnum


class ServiceCategory(StrEnum):
    STREETLIGHT = "streetlight"
    POTHOLE = "pothole"
    WATER_SUPPLY = "water_supply"
    PF_CLAIM = "pf_claim"
    PENSION = "pension"
    SCHOLARSHIP = "scholarship"
    CERTIFICATE = "certificate"
    OTHER = "other"


class AuthorityType(StrEnum):
    MUNICIPAL = "municipal"
    EPFO = "epfo"
    EDUCATION_DEPT = "education_dept"
    PENSION_DEPT = "pension_dept"
    REVENUE_DEPT = "revenue_dept"


class UrgencyLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CaseStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED_PENDING_VERIFICATION = "resolved_pending_verification"
    CLOSED = "closed"
    REOPENED = "reopened"


class StageStatus(StrEnum):
    COMPLETED = "completed"
    CURRENT = "current"
    PENDING = "pending"
    BLOCKED = "blocked"


class ActorType(StrEnum):
    CITIZEN = "citizen"
    AUTHORITY = "authority"
    SYSTEM = "system"


class AiSource(StrEnum):
    OPENAI = "openai"
    FALLBACK = "fallback"


class ConfirmationType(StrEnum):
    CONFIRM = "confirm"
    COMMENT = "comment"
