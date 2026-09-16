"""Lab 04-04: 검증된 여러 Agent 결과를 Join한 뒤 실제 Itinerary Agent를 실행합니다.

시나리오:
    Weather, Place, Budget Agent의 역할별 결과가 이미 계약 검증을 통과했습니다. Join
    Guard가 세 필수 결과를 확인한 뒤 최소 Context만 Gemma Itinerary Agent에 전달합니다.

학습 질문:
    병렬 Agent가 모두 끝났다는 사실만으로 안전하게 결과를 통합할 수 있을까요?

확인할 내용:
    필수 결과 존재와 역할별 계약을 먼저 확인하고 Join 성공 후에만 실제 Gemma를 1회
    호출합니다. 앞 단계는 고정된 계약 예제이며 LLM 성공을 흉내 내는 결과가 아닙니다.
"""

import json

from shared.travel_contracts import BudgetResult, ItineraryResult, PlaceResult, WeatherResult
from shared.travel_llm import provider_for_agent, run_with_metadata


VERIFIED_RESULTS = {
    "weather_agent": WeatherResult(forecast_summary="둘째 날 비 가능성", cautions=["우산 준비", "실내 일정 준비"], source_confirmed=True),
    "place_agent": PlaceResult(places=["영화의전당", "부산시립미술관"], selection_reason="대중교통과 실내 대체 일정 고려"),
    "budget_agent": BudgetResult(breakdown={"교통": 100000, "숙박": 300000, "식비": 150000, "예비비": 50000}, total=600000),
}


def join_guard_agent(results: dict[str, object]) -> dict[str, object]:
    required = {"weather_agent", "place_agent", "budget_agent"}
    missing = sorted(required - set(results))
    if missing:
        raise ValueError(f"Join 필수 결과가 없습니다: {missing}")
    return {agent_id: result.model_dump() for agent_id, result in results.items()}


def itinerary_agent(joined_context: dict[str, object]) -> dict:
    prompt = f"""당신은 itinerary_agent입니다.
요청: 부산 2박 3일, 대중교통, 총예산 60만 원
계약 검증을 통과한 Context: {json.dumps(joined_context, ensure_ascii=False)}
세 결과를 반영한 3일 일정을 ItineraryResult 계약으로 반환하세요."""
    return run_with_metadata(provider_for_agent("itinerary_agent"), prompt, ItineraryResult)


if __name__ == "__main__":
    joined = join_guard_agent(VERIFIED_RESULTS)
    print("Join된 Agent:", list(joined))
    result = itinerary_agent(joined)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Itinerary 실행 조건 충족:", result["result"] is not None)
