"""Lab 02-06: 정보가 부족한 Agent 결과를 실패가 아닌 상태로 표현합니다.

시나리오:
    Budget Agent가 여행 요청을 받았지만 숙박 가격과 출발지 교통비가 없습니다. Agent가
    값을 추측하거나 단순 오류를 내는 대신 completed와 missing_information으로 다음
    행동에 필요한 정보를 알려 줍니다.

학습 질문:
    실행 실패와 사용자 정보 부족을 같은 오류로 처리해야 할까요?

확인할 내용:
    Orchestrator는 completed=False를 보고 사용자에게 추가 정보를 요청할 수 있습니다.
    이 단계는 상태 계약 예제이므로 실제 LLM을 호출하지 않습니다.
"""

from shared.travel_contracts import SpecialistResult


def budget_agent(has_hotel_price: bool) -> SpecialistResult:
    if not has_hotel_price:
        return SpecialistResult(
            agent_id="budget_agent",
            goal="여행 예산 항목과 계산 입력 확인",
            summary="정확한 총액을 계산하기에는 정보가 부족합니다.",
            recommendations=["숙박 가격을 먼저 확인하세요."],
            missing_information=["1박 숙박 가격", "출발지 교통비"],
            completed=False,
        )
    return SpecialistResult(
        agent_id="budget_agent",
        goal="여행 예산 항목과 계산 입력 확인",
        summary="필요한 가격 정보가 준비되었습니다.",
        recommendations=["항목별 예산 계산을 진행하세요."],
        missing_information=[],
        completed=True,
    )


if __name__ == "__main__":
    result = budget_agent(has_hotel_price=False)
    print(result.model_dump_json(indent=2))
    print("\n실행 오류가 아님: Agent 결과 객체가 존재합니다.")
    print("작업 완료:", result.completed)
    print("다음 행동: 사용자에게 추가 정보 요청" if result.missing_information else "다음 Agent 실행")
