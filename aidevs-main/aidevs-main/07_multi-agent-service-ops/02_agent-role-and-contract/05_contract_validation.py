"""Lab 02-05: Agent 결과의 형식과 업무 의미를 차례로 검증합니다.

시나리오:
    외부 Agent가 필수 필드를 빠뜨리거나 다른 역할의 ID를 반환했습니다. 어떤 결과는
    정수 타입을 지켰지만 항목 합계가 total과 다릅니다. Orchestrator는 이런 결과를
    다음 Agent에게 전달하기 전에 차단해야 합니다.

학습 질문:
    JSON 형식과 타입이 올바르면 업무 결과도 올바르다고 볼 수 있을까요?

확인할 내용:
    Pydantic의 필드 검증은 형식 오류를, model_validator는 필드 사이의 업무 규칙을
    검사합니다. 의도적으로 만든 오류 데이터이며 실제 LLM 성공을 흉내 내지 않습니다.
"""

from pydantic import ValidationError

from shared.travel_contracts import BudgetResult, SpecialistResult, ValidationResult, WeatherResult


CASES = [
    (
        "정상 예산",
        BudgetResult,
        {"breakdown": {"교통": 100_000, "숙박": 300_000}, "total": 400_000},
        True,
    ),
    (
        "필수 필드 누락",
        WeatherResult,
        {"agent_id": "weather_agent", "cautions": []},
        False,
    ),
    (
        "다른 역할로 위장",
        WeatherResult,
        {"agent_id": "budget_agent", "forecast_summary": "맑음", "source_confirmed": True},
        False,
    ),
    (
        "허용되지 않은 Agent",
        SpecialistResult,
        {"agent_id": "payment_agent", "goal": "결제", "summary": "완료", "recommendations": ["실행"], "completed": True},
        False,
    ),
    (
        "예산 합계 불일치",
        BudgetResult,
        {"breakdown": {"교통": 100_000, "숙박": 300_000}, "total": 350_000},
        False,
    ),
    (
        "음수 예산",
        BudgetResult,
        {"breakdown": {"할인": -10_000, "숙박": 300_000}, "total": 290_000},
        False,
    ),
    (
        "통과 상태와 Issue 모순",
        ValidationResult,
        {"passed": True, "issues": ["알레르기 조건 누락"]},
        False,
    ),
]


def contract_validation_agent(schema, payload: dict) -> tuple[bool, str]:
    try:
        schema.model_validate(payload)
        return True, "계약 통과"
    except ValidationError as error:
        first_error = error.errors()[0]
        return False, f"위치={first_error['loc']} / 이유={first_error['msg']}"


if __name__ == "__main__":
    matched_count = 0
    for case_name, schema, payload, expected in CASES:
        actual, detail = contract_validation_agent(schema, payload)
        matches = actual == expected
        if matches:
            matched_count += 1
        print(f"{case_name}: {'통과' if actual else '차단'} / {detail} / 예상과 일치: {matches}")

    print(f"\n예상과 일치한 사례: {matched_count}/{len(CASES)}")
    print("형식 검증과 업무 의미 검증을 모두 확인:", matched_count == len(CASES))
