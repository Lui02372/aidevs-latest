"""
[시나리오]
Itinerary Agent가 완성한 부산 일정을 저장하려고 합니다.

1. 승인 정보가 없는 요청을 먼저 검사합니다.
2. 다른 task_id에 발급된 승인을 붙여 다시 검사합니다.
3. 마지막으로 사용자·Task·Tool이 모두 일치하는 승인을 사용합니다.

[기대 결과]
앞의 두 요청은 차단되고, 현재 요청과 정확히 연결된 승인만 허용됩니다.

[학습 포인트]
"승인됨"이라는 Boolean 하나만 확인하면 승인을 다른 작업에 재사용할 수 있습니다.
승인은 사용자, Task, Tool과 함께 묶어서 검증해야 합니다.
"""

from shared.travel_safety import Approval, ToolRequest, authorize_tool


request = ToolRequest(
    task_id="travel-001",
    user_id="user-101",
    agent_id="itinerary_agent",
    tool_name="save_itinerary",
    arguments={"title": "부산 2박 3일"},
    idempotency_key="travel-001-save-v1",
)

for approval in [
    None,
    Approval(task_id="travel-999", user_id="user-101", tool_name="save_itinerary", approved=True),
    Approval(task_id="travel-001", user_id="user-101", tool_name="save_itinerary", approved=True),
]:
    try:
        authorize_tool(request, expected_user_id="user-101", approval=approval)
        print("허용: 현재 요청과 일치하는 승인")
    except PermissionError as error:
        print("차단:", error)
