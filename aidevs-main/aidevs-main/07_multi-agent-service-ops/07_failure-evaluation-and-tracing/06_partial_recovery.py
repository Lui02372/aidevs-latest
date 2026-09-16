"""
[시나리오]
Weather, Place, Budget Agent가 병렬 실행되었고 Place Agent만 실패했습니다.

1. 이미 성공한 Weather와 Budget 결과는 버리지 않고 보존합니다.
2. 실패한 Agent가 필수 Agent인지 확인합니다.
3. 선택 Agent만 실패했다면 성공 결과로 계획을 다시 구성합니다.
4. 필수 Agent가 실패했다면 자동 완성을 멈추고 사람에게 전달합니다.

[기대 결과]
현재 예제에서 Place Agent는 선택 Agent이므로 성공 결과를 보존하고 Replan합니다.

[학습 포인트]
Multi-Agent 전체를 처음부터 다시 실행하면 비용과 중복 Tool 실행이 늘어납니다.
실패 범위와 의존성을 확인하고 필요한 부분만 복구합니다.
"""

results = {
    "weather_agent": {"status": "completed", "summary": "둘째 날 비"},
    "place_agent": {"status": "failed", "error": "장소 API 연결 실패"},
    "budget_agent": {"status": "completed", "total": 580_000},
}

required_agents = {"weather_agent", "budget_agent"}
failed_required = {
    name
    for name in required_agents
    if results.get(name, {}).get("status") != "completed"
}

if failed_required:
    decision = "human_escalation"
else:
    decision = "replan_with_successful_results"

print("보존한 성공 결과:", [name for name, value in results.items() if value["status"] == "completed"])
print("실패 결과:", [name for name, value in results.items() if value["status"] == "failed"])
print("다음 행동:", decision)
