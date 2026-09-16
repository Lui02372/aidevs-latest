"""
[시나리오]
Supervisor Agent가 Weather Agent와 Place Agent에 작업을 나누어 줍니다.

1. 전체 Context에는 여행지, 날짜, 취향, 예산, 내부 메모가 들어 있습니다.
2. 각 Worker Agent에는 YAML에 허용된 필드만 전달합니다.
3. Tool 요청도 같은 사용자의 요청인지 다시 검사합니다.
4. 다른 사용자 ID를 넣은 Agent 요청은 내부에서 왔더라도 차단합니다.

[기대 결과]
- Weather Agent와 Place Agent가 받는 Context가 서로 다르게 출력됩니다.
- 올바른 사용자 요청은 허용되고 다른 사용자 요청은 차단됩니다.

[학습 포인트]
멀티 Agent 내부 통신도 신뢰 경계입니다. Agent마다 필요한 최소 Context만 전달하고
모든 Tool 요청에서 사용자 범위와 역할 권한을 다시 확인합니다.
"""

from security_registry import load_security_policies
from shared.travel_safety import ToolRequest, authorize_tool


def context_guard_agent(agent_id: str, full_context: dict[str, object]) -> dict[str, object]:
    allowed_fields = load_security_policies()["context_access"][agent_id]
    return {field: full_context[field] for field in allowed_fields if field in full_context}


full_context = {
    "destination": "부산",
    "travel_dates": ["2026-10-01", "2026-10-03"],
    "preferences": ["바다", "맛집"],
    "budget": 500000,
    "internal_note": "운영자 전용 메모",
}

print("Weather Agent Context:", context_guard_agent("weather_agent", full_context))
print("Place Agent Context:", context_guard_agent("place_agent", full_context))


# Supervisor나 다른 Agent가 만들었다고 해도 신뢰하지 않고 같은 Tool Guard를 적용합니다.
requests = [
    ToolRequest(
        task_id="travel-001",
        user_id="user-101",
        agent_id="budget_agent",
        tool_name="calculate_budget",
        arguments={"days": 3},
    ),
    ToolRequest(
        task_id="travel-001",
        user_id="user-999",
        agent_id="place_agent",
        tool_name="search_places",
        arguments={"city": "부산"},
    ),
]

for request in requests:
    try:
        authorize_tool(request, expected_user_id="user-101")
        print("허용:", request.agent_id, request.tool_name)
    except PermissionError as error:
        print("차단:", error)
