"""Deterministic keyword rules used when no OpenAI key is configured.

Each entry drives problem classification, authority resolution, and default
service metadata for the fallback path. The seed demo scenario texts are
written to match these keyword lists so classification is correct by
construction.
"""

from app.models.enums import AuthorityType, ServiceCategory, UrgencyLevel

CATEGORY_KEYWORDS: dict[ServiceCategory, list[str]] = {
    ServiceCategory.STREETLIGHT: ["streetlight", "street light", "lamp post", "light outside", "light not working", "light isn't working", "no light on"],
    ServiceCategory.POTHOLE: ["pothole", "road damage", "broken road", "crater", "road caved"],
    ServiceCategory.WATER_SUPPLY: ["water supply", "no water", "water stopped", "water pressure", "brown water", "dirty water", "water tanker"],
    ServiceCategory.PF_CLAIM: ["pf claim", "provident fund", "epfo", "pf withdrawal", "pf transfer", "uan"],
    ServiceCategory.PENSION: ["pension", "pensioner", "pension amount", "pension payment"],
    ServiceCategory.SCHOLARSHIP: ["scholarship", "scholarship amount", "scholarship credited", "scholarship disbursed"],
    ServiceCategory.CERTIFICATE: ["certificate", "caste certificate", "income certificate", "domicile certificate", "birth certificate", "application stuck", "certificate application"],
}

EMERGENCY_KEYWORDS = ["fire", "on fire", "someone is dying", "medical emergency", "heart attack", "accident happening now", "being attacked", "assault in progress", "life threat", "life-threatening"]

PRIVATE_DISPUTE_KEYWORDS = ["my neighbor", "my landlord", "my ex", "my husband", "my wife", "family dispute", "personal dispute", "my roommate", "custody", "divorce"]

URGENCY_KEYWORDS: dict[UrgencyLevel, list[str]] = {
    UrgencyLevel.HIGH: ["urgent", "emergency", "immediately", "danger", "unsafe", "accident", "months", "three months", "for months"],
    UrgencyLevel.MEDIUM: ["weeks", "two weeks", "delayed", "still waiting", "rejected"],
    UrgencyLevel.LOW: ["minor", "small issue", "whenever possible"],
}


CATEGORY_META: dict[ServiceCategory, dict] = {
    ServiceCategory.STREETLIGHT: {
        "display_name": "Streetlight Outage",
        "description": "A public streetlight is not functioning.",
        "authority_type": AuthorityType.MUNICIPAL,
        "authority_name": "Greater Municipal Corporation",
        "department": "Public Lighting / Engineering",
        "responsible_role": "Junior Engineer",
        "jurisdiction_area": "Ward 17",
        "required_evidence": ["Photo of the streetlight", "Nearby landmark or pole number"],
        "sla_days": 5,
        "stage_template": ["Submitted", "Assigned", "Site Inspection", "Repair", "Citizen Verification"],
        "case_prefix": "CIV",
    },
    ServiceCategory.POTHOLE: {
        "display_name": "Road / Pothole Damage",
        "description": "A pothole or road damage poses a hazard.",
        "authority_type": AuthorityType.MUNICIPAL,
        "authority_name": "Greater Municipal Corporation",
        "department": "Roads / Engineering",
        "responsible_role": "Junior Engineer",
        "jurisdiction_area": "Ward 9",
        "required_evidence": ["Photo of the pothole", "Nearby landmark"],
        "sla_days": 7,
        "stage_template": ["Submitted", "Assigned", "Site Inspection", "Repair", "Citizen Verification"],
        "case_prefix": "CIV",
    },
    ServiceCategory.WATER_SUPPLY: {
        "display_name": "Water Supply Disruption",
        "description": "Water supply is stopped, low-pressure, or discoloured.",
        "authority_type": AuthorityType.MUNICIPAL,
        "authority_name": "Municipal Water Board",
        "department": "Water Supply / Distribution",
        "responsible_role": "Assistant Engineer",
        "jurisdiction_area": "Ward 12",
        "required_evidence": ["Photo of water sample or tap", "Time of disruption"],
        "sla_days": 3,
        "stage_template": ["Submitted", "Assigned", "Field Inspection", "Repair", "Citizen Verification"],
        "case_prefix": "CIV",
    },
    ServiceCategory.PF_CLAIM: {
        "display_name": "PF Claim Issue",
        "description": "A Provident Fund claim was rejected or delayed.",
        "authority_type": AuthorityType.EPFO,
        "authority_name": "EPFO Regional Office",
        "department": "Claims Verification",
        "responsible_role": "Claims Officer",
        "jurisdiction_area": "Regional PF Office",
        "required_evidence": ["Claim rejection notice", "UAN number"],
        "sla_days": 20,
        "stage_template": ["Submitted", "Validated", "Employer Verification", "Approval", "Payment"],
        "case_prefix": "PF",
    },
    ServiceCategory.PENSION: {
        "display_name": "Pension Delay",
        "description": "A pension payment has not been credited.",
        "authority_type": AuthorityType.PENSION_DEPT,
        "authority_name": "Directorate of Pensions",
        "department": "Pension Disbursement",
        "responsible_role": "Pension Officer",
        "jurisdiction_area": "District Treasury",
        "required_evidence": ["Pension Payment Order (PPO) number", "Last credited date"],
        "sla_days": 15,
        "stage_template": ["Submitted", "Verified", "Treasury Processing", "Bank Credit", "Citizen Verification"],
        "case_prefix": "PEN",
    },
    ServiceCategory.SCHOLARSHIP: {
        "display_name": "Scholarship Payment Delay",
        "description": "A scholarship amount has not been credited.",
        "authority_type": AuthorityType.EDUCATION_DEPT,
        "authority_name": "State Scholarship Directorate",
        "department": "Scholarship Disbursement",
        "responsible_role": "Scholarship Verification Officer",
        "jurisdiction_area": "District Education Office",
        "required_evidence": ["Application ID", "Bank account confirmation"],
        "sla_days": 30,
        "stage_template": ["Submitted", "Verified", "Sanctioned", "Bank Credit", "Citizen Verification"],
        "case_prefix": "SCH",
    },
    ServiceCategory.CERTIFICATE: {
        "display_name": "Certificate / Application Delay",
        "description": "A certificate or application has been stuck in process.",
        "authority_type": AuthorityType.REVENUE_DEPT,
        "authority_name": "Revenue Department",
        "department": "Certificate Issuance",
        "responsible_role": "Revenue Inspector",
        "jurisdiction_area": "Taluk Office",
        "required_evidence": ["Application ID", "Supporting documents"],
        "sla_days": 21,
        "stage_template": ["Submitted", "Document Verification", "Field Verification", "Approval", "Certificate Issued"],
        "case_prefix": "CERT",
    },
    ServiceCategory.OTHER: {
        "display_name": "General Civic Issue",
        "description": "A civic issue that does not match a known category.",
        "authority_type": AuthorityType.MUNICIPAL,
        "authority_name": "Municipal Grievance Cell",
        "department": "General Administration",
        "responsible_role": "Grievance Officer",
        "jurisdiction_area": "Local Ward",
        "required_evidence": ["Photo or document related to the issue"],
        "sla_days": 10,
        "stage_template": ["Submitted", "Assigned", "Under Review", "Action Taken", "Citizen Verification"],
        "case_prefix": "GEN",
    },
}
