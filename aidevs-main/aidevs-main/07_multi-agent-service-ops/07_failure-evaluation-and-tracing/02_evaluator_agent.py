"""
[시나리오]
네 Specialist Agent가 만든 결과를 Itinerary Agent가 하나의 일정으로 합쳤습니다.
독립된 Evaluator Agent가 최종 결과에서 사용자 조건과 안전 조건을 확인합니다.

1. 필요한 Agent 네 개가 모두 완료되었는지 검사합니다.
2. 목적지·예산·알레르기·대중교통 조건이 최종 일정에 남았는지 검사합니다.
3. 승인되지 않은 변경 Tool이 실행되지 않았는지 검사합니다.
4. 전체 점수만 출력하지 않고 각 검사 이름과 결과를 출력합니다.

[기대 결과]
준비된 정상 결과는 모든 항목을 통과합니다. 일부 조건을 지우고 다시 실행하면 어떤
검사가 실패하는지 확인할 수 있습니다.

[학습 포인트]
결과를 만든 Agent와 평가하는 Agent의 책임을 분리합니다. 이 Lab은 반복 개선 전에
Evaluator의 입력·출력 구조를 배우는 결정적 예제이므로 실제 LLM을 호출하지 않습니다.
"""

from shared.travel_observability import evaluate_travel_result


actual_result = {
    "completed_agents": [
        "weather_agent",
        "place_agent",
        "budget_agent",
        "itinerary_agent",
    ],
    "unapproved_write": False,
    # 평가 함수는 원래 요청이 아니라 최종 산출물에서 조건 보존 여부를 확인합니다.
    "itinerary": {
        "destination": "부산",
        "summary": (
            "해산물 알레르기를 고려하고 대중교통을 이용하는 일정입니다. "
            "예상 예산은 600000원이며, 비가 오면 실내 일정으로 변경합니다."
        ),
    },
}

evaluation = evaluate_travel_result(actual_result)
print(evaluation.model_dump_json(indent=2))
if not evaluation.passed:
    failed_checks = [name for name, passed in evaluation.checks.items() if not passed]
    print("수정이 필요한 검사:", failed_checks)
else:
    print("모든 평가 기준을 통과했습니다.")
