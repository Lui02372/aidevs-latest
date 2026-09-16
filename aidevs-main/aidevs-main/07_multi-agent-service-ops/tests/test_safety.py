import pytest

from shared.travel_safety import Approval, IdempotencyRegistry, ToolRequest, authorize_tool


def write_request() -> ToolRequest:
    return ToolRequest(
        task_id="task-1",
        user_id="user-1",
        agent_id="itinerary_agent",
        tool_name="save_itinerary",
        idempotency_key="save-task-1",
    )


def test_read_tool_uses_agent_allowlist() -> None:
    allowed = ToolRequest(
        task_id="task-1",
        user_id="user-1",
        agent_id="weather_agent",
        tool_name="get_weather",
    )
    authorize_tool(allowed, expected_user_id="user-1")

    forbidden = allowed.model_copy(update={"tool_name": "save_itinerary"})
    with pytest.raises(PermissionError, match="허용되지 않은"):
        authorize_tool(forbidden, expected_user_id="user-1")


def test_write_requires_matching_approval() -> None:
    request = write_request()
    with pytest.raises(PermissionError, match="승인 전"):
        authorize_tool(request, expected_user_id="user-1")

    wrong = Approval(
        task_id="task-other",
        user_id="user-1",
        tool_name="save_itinerary",
        approved=True,
    )
    with pytest.raises(PermissionError, match="일치하지 않는"):
        authorize_tool(request, expected_user_id="user-1", approval=wrong)

    valid = wrong.model_copy(update={"task_id": "task-1"})
    authorize_tool(request, expected_user_id="user-1", approval=valid)


def test_idempotency_is_scoped_by_user() -> None:
    registry = IdempotencyRegistry()
    calls = 0

    def action() -> str:
        nonlocal calls
        calls += 1
        return f"result-{calls}"

    first, first_executed = registry.execute_once("user-1", "key-1", action)
    repeated, repeated_executed = registry.execute_once("user-1", "key-1", action)
    other, other_executed = registry.execute_once("user-2", "key-1", action)
    assert (first, first_executed) == ("result-1", True)
    assert (repeated, repeated_executed) == ("result-1", False)
    assert (other, other_executed) == ("result-2", True)
