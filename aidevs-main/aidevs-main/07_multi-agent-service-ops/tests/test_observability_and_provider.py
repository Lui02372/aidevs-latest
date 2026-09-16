from shared import travel_llm
from shared.travel_contracts import SpecialistResult
from shared.travel_observability import classify_failure, evaluate_travel_result


def specialist() -> SpecialistResult:
    return SpecialistResult(
        agent_id="weather_agent",
        goal="날씨 확인",
        summary="비 가능성",
        recommendations=["우산"],
        completed=True,
    )


def test_failure_policy_is_explicit() -> None:
    assert classify_failure(TimeoutError()) == "retry"
    assert classify_failure(ValueError()) == "replan"
    assert classify_failure(PermissionError()) == "block"
    assert classify_failure(RuntimeError()) == "human"


def test_scenario_checks_only_requested_optional_constraints() -> None:
    result = {
        "itinerary": {"summary": "제주 여행 일정"},
        "completed_agents": ["weather_agent", "place_agent", "budget_agent", "itinerary_agent"],
        "unapproved_write": False,
    }
    evaluation = evaluate_travel_result(
        result,
        expected_destination="제주",
        expected_budget=None,
        expected_food_restriction=None,
        expected_transport=None,
    )
    assert evaluation.passed is True


def test_scenario_detects_constraint_missing_from_final_itinerary() -> None:
    result = {
        "itinerary": {"summary": "부산 대중교통 여행, 예산 60만원"},
        "completed_agents": ["weather_agent", "place_agent", "budget_agent", "itinerary_agent"],
        "unapproved_write": False,
    }
    evaluation = evaluate_travel_result(result)
    assert evaluation.checks["food_restriction_kept"] is False
    assert evaluation.passed is False


def test_provider_metadata_never_claims_fallback(monkeypatch) -> None:
    monkeypatch.setattr(travel_llm, "run_structured", lambda provider, prompt, schema: specialist())
    output = travel_llm.run_with_metadata("openai", "날씨", SpecialistResult)
    assert output["provider_requested"] == "openai"
    assert output["provider_used"] == "openai"
    assert output["fallback_used"] is False
    assert output["error"] is None


def test_provider_error_is_visible(monkeypatch) -> None:
    def fail(*args, **kwargs):
        raise ConnectionError("provider unavailable")

    monkeypatch.setattr(travel_llm, "run_structured", fail)
    output = travel_llm.run_with_metadata("gemini", "날씨", SpecialistResult)
    assert output["provider_used"] is None
    assert output["fallback_used"] is False
    assert "ConnectionError" in output["error"]
