"""Lab 04-03: 서로 독립적인 실제 LLM Worker를 병렬 실행합니다.

시나리오:
    Weather, Place, Budget Agent는 같은 부산 여행 요청을 받지만 서로의 결과가 없어도
    작업을 시작할 수 있습니다. Gemini, Llama, GPT를 ThreadPool에서 동시에 실행하고
    완료되는 순서대로 결과를 수집합니다.

학습 질문:
    병렬 Worker가 하나의 Shared State를 동시에 직접 수정해도 안전할까요?

확인할 내용:
    Worker는 독립 결과만 반환하고 Orchestrator가 Main Thread에서 결과를 State에
    저장합니다. 실제 LLM을 3회 호출하며 완료 순서는 매번 달라질 수 있습니다.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from shared.travel_contracts import BudgetResult, PlaceResult, WeatherResult
from shared.travel_llm import provider_for_agent, run_with_metadata


REQUEST = "부산 2박 3일, 대중교통, 총예산 60만 원"
JOBS = {
    "weather_agent": (WeatherResult, "여행 기간의 날씨 위험과 준비 사항을 정리하세요."),
    "place_agent": (PlaceResult, "대중교통으로 방문할 장소 후보와 선택 근거를 작성하세요."),
    "budget_agent": (BudgetResult, "60만 원을 항목별로 나누고 합계를 정확히 맞추세요."),
}


def parallel_worker_agent(agent_id: str) -> dict:
    schema, instruction = JOBS[agent_id]
    prompt = f"""당신은 {agent_id}입니다. 다른 Agent의 결과를 추측하지 마세요.
요청: {REQUEST}
담당 업무: {instruction}
{schema.__name__} 계약으로 반환하고 agent_id는 {agent_id}로 작성하세요."""
    return run_with_metadata(provider_for_agent(agent_id), prompt, schema)


def parallel_orchestrator_agent() -> dict[str, object]:
    results: dict[str, object] = {}
    errors: dict[str, str] = {}
    completion_order: list[str] = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(parallel_worker_agent, agent_id): agent_id for agent_id in JOBS}
        for future in as_completed(futures):
            agent_id = futures[future]
            try:
                response = future.result()
            except Exception as error:
                errors[agent_id] = f"{type(error).__name__}: {error}"
                completion_order.append(agent_id)
                continue
            completion_order.append(agent_id)
            if response["error"]:
                errors[agent_id] = response["error"]
            else:
                results[agent_id] = response
    return {"status": "completed" if not errors else "partial_failure", "results": results, "errors": errors, "completion_order": completion_order}


if __name__ == "__main__":
    output = parallel_orchestrator_agent()
    print(output)
    print("완료 순서:", output["completion_order"])
    print("성공 Agent:", list(output["results"]))
    print("실패 Agent:", list(output["errors"]))
