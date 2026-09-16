"""Lab 04-07: 실제 네 AI Agent의 병렬 실행, Join, State와 Trace를 통합합니다.

시나리오:
    Gemini Weather, Llama Place, GPT Budget Agent가 부산 여행 요청을 병렬 처리합니다.
    Main Thread의 Orchestrator가 결과를 검증해 Shared State에 기록합니다. Weather와
    Budget 필수 결과가 성공하면 선택 결과인 Place가 실패해도 Join을 진행할 수 있습니다.

학습 질문:
    여러 Agent가 동시에 실행돼도 State와 전체 종료를 일관되게 관리하려면 누가 결과를
    기록해야 할까요?

확인할 내용:
    반복 Worker와 Team 구성은 YAML에서 읽지만 병렬 실행, 필수 결과 확인과 종료는
    Python이 통제합니다. 정상 흐름에서는 실제 LLM을 최대 4회 호출합니다.
"""

import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed

from shared.travel_contracts import BudgetResult, ItineraryResult, PlaceResult, WeatherResult
from shared.travel_llm import provider_for_agent, run_with_metadata
from shared.travel_orchestration import CollaborationState, TraceEvent
from worker_registry import load_registry


REQUEST = "부산 2박 3일, 대중교통, 총예산 60만 원"
SCHEMAS = {
    "WeatherResult": WeatherResult,
    "PlaceResult": PlaceResult,
    "BudgetResult": BudgetResult,
}
WORKERS, TEAMS = load_registry()
TEAM = TEAMS["travel_collaboration_team"]


def specialist_agent(agent_id: str) -> dict:
    worker = WORKERS[agent_id]
    schema = SCHEMAS[worker["output_contract"]]
    prompt = f"""당신은 {agent_id}입니다. 다른 Agent 결과를 추측하지 마세요.
요청: {REQUEST}
이름: {worker['name']}
담당 업무: {worker['goal']}
{schema.__name__} 계약으로 반환하고 agent_id는 {agent_id}로 작성하세요."""
    return run_with_metadata(worker["provider"], prompt, schema)


def itinerary_agent(context: dict[str, object]) -> dict:
    prompt = f"""당신은 itinerary_agent입니다.
요청: {REQUEST}
검증된 Specialist 결과: {json.dumps(context, ensure_ascii=False)}
모든 조건을 반영한 3일 일정을 ItineraryResult 계약으로 반환하세요."""
    return run_with_metadata(provider_for_agent("itinerary_agent"), prompt, ItineraryResult)


def add_trace(state: CollaborationState, actor: str, action: str, status: str, response: dict | None = None) -> None:
    response = response or {}
    state.trace.append(TraceEvent(
        step=len(state.trace) + 1,
        actor=actor,
        action=action,
        status=status,
        provider=response.get("provider_requested"),
        model=response.get("model"),
        latency_ms=response.get("latency_ms"),
        details={"error": response.get("error")} if response.get("error") else {},
    ))


def distributed_orchestrator_agent() -> CollaborationState:
    state = CollaborationState(task_id="travel-001", request=REQUEST, status="running", current_step="parallel_research")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for agent_id in TEAM["parallel_workers"]:
            add_trace(state, agent_id, "agent_started", "started")
            futures[executor.submit(specialist_agent, agent_id)] = agent_id
        try:
            for future in as_completed(futures, timeout=TEAM["timeout_seconds"]):
                agent_id = futures[future]
                try:
                    response = future.result()
                except Exception as error:
                    message = f"{type(error).__name__}: {error}"
                    state.errors[agent_id] = message
                    state.failed_agents.append(agent_id)
                    add_trace(state, agent_id, "agent_failed", "failed", {"error": message})
                    continue
                if response["error"]:
                    state.errors[agent_id] = response["error"]
                    state.failed_agents.append(agent_id)
                    add_trace(state, agent_id, "agent_failed", "failed", response)
                else:
                    state.results[agent_id] = response["result"]
                    state.completed_agents.append(agent_id)
                    add_trace(state, agent_id, "agent_completed", "completed", response)
        except TimeoutError:
            for future, agent_id in futures.items():
                if not future.done():
                    future.cancel()
                    state.errors[agent_id] = "Worker timeout"
                    state.failed_agents.append(agent_id)
                    add_trace(state, agent_id, "agent_failed", "failed", {"error": "Worker timeout"})

    required = set(TEAM["required_workers"])
    missing = sorted(required - set(state.results))
    if missing:
        state.status = "failed"
        state.current_step = None
        add_trace(state, "join_guard_agent", "join_blocked", "blocked", {"error": f"필수 결과 누락: {missing}"})
        return state

    state.current_step = "join"
    add_trace(state, "join_guard_agent", "join_completed", "completed")
    joined_context = {
        agent_id: state.results[agent_id]
        for agent_id in TEAM["parallel_workers"]
        if agent_id in state.results
    }
    itinerary = itinerary_agent(joined_context)
    if itinerary["error"]:
        state.errors["itinerary_agent"] = itinerary["error"]
        state.failed_agents.append("itinerary_agent")
        state.status = "failed"
        state.current_step = None
        add_trace(state, "itinerary_agent", "agent_failed", "failed", itinerary)
        return state

    state.results["itinerary_agent"] = itinerary["result"]
    state.completed_agents.append("itinerary_agent")
    add_trace(state, "itinerary_agent", "agent_completed", "completed", itinerary)
    state.status = "partial_failure" if state.errors else "completed"
    state.current_step = None
    add_trace(state, "orchestrator_agent", "workflow_completed", "completed")
    return state


if __name__ == "__main__":
    final_state = distributed_orchestrator_agent()
    print(final_state.model_dump_json(indent=2))
    print("전체 상태:", final_state.status)
    print("완료 Agent:", final_state.completed_agents)
    print("실패 Agent:", final_state.failed_agents)
