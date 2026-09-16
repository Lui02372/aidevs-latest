from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.models import TaskRecord
from shared.travel_contracts import RouteDecision, SPECIALIST_GOALS, SpecialistResult
from shared.travel_llm import run_structured


def provider_for(agent_id: str) -> str:
    name = agent_id.removesuffix("_agent").upper()
    return os.getenv(f"{name}_AGENT_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))


def append_trace(task: TaskRecord, actor: str, action: str, status: str, **details: object) -> None:
    task.trace.append({"actor": actor, "action": action, "status": status, **details})


def route(task: TaskRecord) -> RouteDecision:
    provider = os.getenv("SUPERVISOR_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
    prompt = f"""당신은 Travel Supervisor입니다.
사용자 요청: {task.request}
weather_agent, place_agent, budget_agent 중 필요한 Agent를 선택하세요.
최종 일정은 별도의 itinerary_agent가 구성하므로 selected_agents에 넣지 마세요.
RouteDecision 계약으로 답하세요."""
    return run_structured(provider, prompt, RouteDecision)


def specialist(task: TaskRecord, agent_id: str) -> SpecialistResult:
    prompt = f"""당신은 {agent_id}입니다.
목표: {SPECIALIST_GOALS[agent_id]}
사용자 요청: {task.request}
자신의 전문 범위만 수행하고 SpecialistResult로 답하세요.
agent_id는 반드시 {agent_id}, completed는 true로 반환하세요."""
    result = run_structured(provider_for(agent_id), prompt, SpecialistResult)
    if result.agent_id != agent_id or not result.completed:
        raise RuntimeError(f"{agent_id} 결과가 계약과 일치하지 않습니다.")
    return result


def itinerary(task: TaskRecord, results: dict[str, SpecialistResult]) -> SpecialistResult:
    prompt = f"""당신은 itinerary_agent입니다.
사용자 요청: {task.request}
검증된 전문 Agent 결과: { {name: value.model_dump() for name, value in results.items()} }
이 결과만 근거로 여행 일정 초안을 SpecialistResult로 구성하세요.
해산물 알레르기 같은 안전 조건을 유지하세요.
agent_id는 itinerary_agent, completed는 true로 반환하세요."""
    result = run_structured(provider_for("itinerary_agent"), prompt, SpecialistResult)
    if result.agent_id != "itinerary_agent" or not result.completed:
        raise RuntimeError("itinerary_agent 결과가 계약과 일치하지 않습니다.")
    return result


def run_multi_agent(task: TaskRecord) -> TaskRecord:
    max_steps = int(os.getenv("MAX_ORCHESTRATION_STEPS", "8"))
    task.status = "running"
    task.progress = 10
    append_trace(task, "supervisor", "route", "started")
    decision = route(task)
    append_trace(
        task,
        "supervisor",
        "route",
        "completed",
        selected_agents=decision.selected_agents,
        reason=decision.reason,
    )

    selected = [name for name in decision.selected_agents if name != "itinerary_agent"]
    if not selected:
        raise RuntimeError("Supervisor가 전문 Agent를 선택하지 않았습니다.")
    if len(selected) + 2 > max_steps:
        raise RuntimeError("최대 Orchestration 단계를 초과합니다.")

    results: dict[str, SpecialistResult] = {}
    with ThreadPoolExecutor(max_workers=min(3, len(selected))) as executor:
        futures = {executor.submit(specialist, task, agent_id): agent_id for agent_id in selected}
        for future in as_completed(futures):
            agent_id = futures[future]
            try:
                results[agent_id] = future.result()
                append_trace(task, agent_id, "specialist", "completed")
            except Exception as error:
                append_trace(
                    task,
                    agent_id,
                    "specialist",
                    "failed",
                    error_type=type(error).__name__,
                    error=str(error),
                )
                raise

    task.progress = 70
    append_trace(task, "orchestrator", "join", "completed", agents=list(results))
    final = itinerary(task, results)
    append_trace(task, "itinerary_agent", "compose", "completed")
    task.result = {
        "route": decision.model_dump(),
        "specialists": {name: value.model_dump() for name, value in results.items()},
        "itinerary": final.model_dump(),
        "notice": "교육용 일정 초안이며 실제 예약이나 결제를 수행하지 않았습니다.",
    }
    task.current_agent = None
    task.progress = 90
    task.status = "waiting_approval"
    append_trace(task, "orchestrator", "wait_for_approval", "waiting_human")
    return task
