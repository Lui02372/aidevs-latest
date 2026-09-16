import pytest
from pydantic import ValidationError

from shared.travel_contracts import SpecialistResult
from shared.travel_orchestration import (
    ExecutionPlan,
    PlanStep,
    TravelHandoff,
    guard_handoff,
)


def test_specialist_result_enforces_agent_contract() -> None:
    with pytest.raises(ValidationError):
        SpecialistResult(
            agent_id="unknown_agent",
            goal="테스트",
            summary="결과",
            recommendations=["추천"],
            completed=True,
        )


def test_execution_plan_rejects_unknown_dependency() -> None:
    with pytest.raises(ValidationError, match="의존 단계"):
        ExecutionPlan(
            goal="여행 계획",
            steps=[
                PlanStep(
                    step_id="compose",
                    agents=["itinerary_agent"],
                    depends_on=["research"],
                )
            ],
        )


def test_handoff_allows_minimum_context_and_blocks_secret() -> None:
    valid = TravelHandoff(
        task_id="task-1",
        trace_id="trace-1",
        from_agent="weather_agent",
        to_agent="itinerary_agent",
        responsibility="날씨 정보를 일정에 반영한다.",
        context={"summary": "둘째 날 비"},
        user_id="user-1",
    )
    guard_handoff(valid, expected_user_id="user-1")

    exposed = valid.model_copy(update={"context": {"api_key": "secret"}})
    with pytest.raises(ValueError, match="전달하면 안 되는"):
        guard_handoff(exposed, expected_user_id="user-1")


def test_handoff_blocks_other_user_and_reverse_route() -> None:
    handoff = TravelHandoff(
        task_id="task-1",
        trace_id="trace-1",
        from_agent="itinerary_agent",
        to_agent="weather_agent",
        responsibility="허용되지 않은 역방향 인계이다.",
        context={"summary": "test"},
        user_id="other-user",
    )
    with pytest.raises(PermissionError, match="다른 사용자"):
        guard_handoff(handoff, expected_user_id="user-1")
    same_user = handoff.model_copy(update={"user_id": "user-1"})
    with pytest.raises(PermissionError, match="허용되지 않은"):
        guard_handoff(same_user, expected_user_id="user-1")
