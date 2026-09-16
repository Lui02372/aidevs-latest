"""
[시나리오]
Itinerary Agent가 부산 여행 일정 초안을 만들었습니다. 바로 사용자에게 전달하지 않고
Evaluation Agent가 평가할 기준을 먼저 정의합니다.

1. 목적지 "부산"이 유지되었는지 검사합니다.
2. 사용자의 "해산물 알레르기" 조건이 포함되었는지 검사합니다.
3. "대중교통" 조건과 예산 정보가 포함되었는지 검사합니다.
4. 모든 조건을 하나의 평균 점수로 숨기지 않고 항목별 True/False로 출력합니다.

[기대 결과]
예제 초안에는 알레르기 조건이 빠져 있으므로 전체 평가는 실패합니다. 출력에서
어떤 기준이 실패했는지 바로 확인할 수 있어야 합니다.

[학습 포인트]
Evaluator Agent를 호출하기 전에 사람이 이해할 수 있는 성공 기준을 먼저 정해야 합니다.
형식·필수 문구처럼 코드로 확인할 수 있는 기준은 LLM이 아니라 Python으로 검사합니다.
이 Lab은 개념 설명용이므로 실제 LLM을 호출하지 않습니다.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationCriterion:
    name: str
    expected_text: str
    description: str


CRITERIA = [
    EvaluationCriterion("destination_kept", "부산", "원래 목적지가 유지되어야 합니다."),
    EvaluationCriterion("allergy_kept", "알레르기", "음식 제한 조건이 유지되어야 합니다."),
    EvaluationCriterion("transport_kept", "대중교통", "이동 수단이 일정에 반영되어야 합니다."),
    EvaluationCriterion("budget_present", "600000", "예상 예산이 결과에 포함되어야 합니다."),
]


def criteria_evaluator_agent(draft: str) -> dict[str, object]:
    checks = {criterion.name: criterion.expected_text in draft for criterion in CRITERIA}
    failed = [criterion.name for criterion in CRITERIA if not checks[criterion.name]]
    return {"passed": not failed, "checks": checks, "failed_criteria": failed}


travel_draft = "부산 2박 3일 대중교통 일정이며 예상 예산은 600000원입니다."
evaluation = criteria_evaluator_agent(travel_draft)

print("평가 대상:", travel_draft)
print("항목별 결과:", evaluation["checks"])
print("전체 통과:", evaluation["passed"])
print("수정이 필요한 기준:", evaluation["failed_criteria"])
