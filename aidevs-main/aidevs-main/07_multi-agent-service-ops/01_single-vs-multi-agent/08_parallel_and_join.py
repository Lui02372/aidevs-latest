"""Lab 01-8: Parallel + Join 구조를 실제 LLM 결과로 미리 확인합니다.

시나리오:
    Weather·Place·Budget Agent는 같은 여행 요청만 있으면 서로 기다리지 않고 조사할
    수 있습니다. 세 결과가 모두 준비된 뒤 Itinerary Agent가 하나의 일정으로 합칩니다.

학습 질문:
    어떤 작업이 독립적이며, Join 전에 반드시 준비돼야 하는 결과는 무엇일까요?

범위:
    GPT·Gemini·Llama·Gemma Agent 결과를 사용합니다. Thread 병렬 실행은 04에서
    구현하고 여기서는 독립 호출과 필수 Join 경계에 집중합니다.
"""

from shared.travel_llm import run_learning_agent


def weather_agent(request: str) -> dict:
    return run_learning_agent("weather_agent", "날씨 준비 사항을 조사한다.", request)


def place_agent(request: str) -> dict:
    return run_learning_agent("place_agent", "조건에 맞는 장소 후보를 조사한다.", request)


def budget_agent(request: str) -> dict:
    return run_learning_agent("budget_agent", "예산 항목을 계산한다.", request)


def itinerary_agent(results: dict[str, object], required: set[str]) -> dict[str, object]:
    missing = required - set(results)
    if missing:
        raise ValueError(f"Join 결과 누락: {sorted(missing)}")
    failed = [name for name, value in results.items() if value["error"]]
    if failed:
        raise RuntimeError(f"실패 Agent: {failed}")
    return run_learning_agent("itinerary_agent", "전문 Agent 결과를 하나의 일정으로 종합한다.", "부산 2박 3일 여행", results)


if __name__ == "__main__":
    request = "부산 2박 3일 여행"
    independent_results = {
        "weather": weather_agent(request),
        "places": place_agent(request),
        "budget": budget_agent(request),
    }
    print("독립 결과:", independent_results)
    try:
        itinerary = itinerary_agent(independent_results, {"weather", "places", "budget"})
        print("Join 결과:", itinerary)
        print("Join 결과 생성:", itinerary["result"] is not None)
    except (RuntimeError, ValueError) as error:
        print("Join 실패:", error)

    try:
        itinerary_agent({"weather": "맑음"}, {"weather", "places", "budget"})
    except ValueError as error:
        print("불완전한 Join 차단:", error)
    else:
        print("불완전한 Join 차단: False")
