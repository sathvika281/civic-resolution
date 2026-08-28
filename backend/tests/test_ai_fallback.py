from app.ai.fallback.rules import classify_category_fallback, understand_problem_fallback
from app.ai.jurisdiction import resolve_authority
from app.models.enums import AuthorityType, ServiceCategory

SCENARIOS = [
    ("The streetlight outside my house hasn't worked for two weeks.", ServiceCategory.STREETLIGHT, AuthorityType.MUNICIPAL),
    ("My PF claim was rejected and I don't understand why.", ServiceCategory.PF_CLAIM, AuthorityType.EPFO),
    ("My scholarship hasn't been credited even though it was approved months ago.", ServiceCategory.SCHOLARSHIP, AuthorityType.EDUCATION_DEPT),
    ("My pension hasn't come for three months.", ServiceCategory.PENSION, AuthorityType.PENSION_DEPT),
    ("I applied for my income certificate but it has been stuck for months.", ServiceCategory.CERTIFICATE, AuthorityType.REVENUE_DEPT),
]


def test_classify_category_fallback_matches_demo_scenarios():
    for raw_text, expected_category, _ in SCENARIOS:
        assert classify_category_fallback(raw_text) == expected_category


def test_understand_and_resolve_authority_fallback_end_to_end():
    for raw_text, expected_category, expected_authority_type in SCENARIOS:
        understanding = understand_problem_fallback(raw_text, "Some City")
        assert understanding.category == expected_category
        assert understanding.source == "fallback"

        authority = resolve_authority(understanding.category)
        assert authority.authority_type == expected_authority_type
        assert authority.source == "fallback"


def test_unrelated_text_falls_back_to_other_category():
    understanding = understand_problem_fallback("My internet bill seems too high this month.", None)
    assert understanding.category == ServiceCategory.OTHER
