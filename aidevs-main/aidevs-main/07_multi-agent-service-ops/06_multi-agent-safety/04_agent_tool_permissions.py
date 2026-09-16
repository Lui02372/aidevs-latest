"""
[시나리오]
Supervisor Agent가 두 개의 Tool 요청을 전달합니다.

1. Weather Agent는 자신에게 허용된 get_weather Tool을 요청합니다.
2. 같은 Weather Agent가 일정 저장 Tool인 save_itinerary도 요청합니다.
3. Tool Guard는 Agent 이름을 믿지 않고 서버의 allowlist와 요청을 비교합니다.

[기대 결과]
- 날씨 조회는 허용됩니다.
- Weather Agent의 일정 저장은 권한 밖이므로 차단됩니다.

[학습 포인트]
LLM 프롬프트의 역할 설명은 권한 통제가 아닙니다. 실제 Tool 실행 직전에 Python이
Agent별 최소 권한을 강제해야 Prompt Injection이나 잘못된 Routing도 피해를 줄입니다.
"""

from shared.travel_safety import ToolRequest, authorize_tool


weather_read = ToolRequest(
    task_id="travel-001",
    user_id="user-101",
    agent_id="weather_agent",
    tool_name="get_weather",
    arguments={"city": "부산"},
)
authorize_tool(weather_read, expected_user_id="user-101")
print("허용: Weather Agent의 날씨 조회")

forbidden_write = ToolRequest(
    task_id="travel-001",
    user_id="user-101",
    agent_id="weather_agent",
    tool_name="save_itinerary",
    idempotency_key="save-001",
)
try:
    authorize_tool(forbidden_write, expected_user_id="user-101")
except PermissionError as error:
    print("차단:", error)
