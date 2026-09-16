"""Lab 02-04: Agent 역할마다 다른 출력 계약을 사용합니다.

시나리오:
    Weather Agent는 사용자가 제공한 확인된 날씨를 받고, Budget Agent는 확정된 총예산을
    항목별로 배분합니다. 두 Agent는 서로 다른 업무 결과를 반환해야 합니다.

학습 질문:
    모든 Agent가 summary 하나만 반환하면 다음 Agent가 필요한 정보를 안전하게 사용할
    수 있을까요?

확인할 내용:
    역할별 계약은 Agent의 책임을 코드로 드러냅니다. 이 단계는 계약 비교 예제이므로
    실제 LLM을 호출하지 않습니다.
"""

from shared.travel_contracts import BudgetResult, WeatherResult


def weather_agent(confirmed_forecast: str) -> WeatherResult:
    return WeatherResult(
        forecast_summary=confirmed_forecast,
        cautions=["작은 우산 준비", "실내 대체 일정 준비"],
        source_confirmed=True,
    )


def budget_agent() -> BudgetResult:
    return BudgetResult(
        breakdown={"교통": 100_000, "숙박": 300_000, "식비": 150_000, "예비비": 50_000},
        total=600_000,
    )


if __name__ == "__main__":
    weather_result = weather_agent("사용자가 제공한 정보: 둘째 날 비 가능성이 있습니다.")
    budget_result = budget_agent()
    print("=== Weather Agent 전용 계약 ===")
    print(weather_result.model_dump_json(indent=2))
    print("\n=== Budget Agent 전용 계약 ===")
    print(budget_result.model_dump_json(indent=2))
    print("\n서로 다른 Agent ID:", weather_result.agent_id, "/", budget_result.agent_id)
    print("Budget 합계 확인:", sum(budget_result.breakdown.values()) == budget_result.total)
