"""Lab 03-05: 실제 Supervisor가 Worker 결과를 확인하며 제한된 Loop를 실행합니다.

시나리오:
    입력 검증 기능의 요구사항을 분석하고 안전성 검토까지 수행합니다. GPT Supervisor는
    현재 State를 보고 Gemini Analyst와 Gemma Reviewer를 차례로 선택하며, 각 Worker
    결과가 계약을 통과한 경우에만 다음 결정을 내립니다.

학습 질문:
    Supervisor가 다음 Agent를 선택한다면 최대 단계와 허용 순서도 LLM에 맡겨야 할까요?

확인할 내용:
    Python이 Worker Allowlist, 의존 순서, 중복 실행, 최대 5회 LLM 호출과 실패 종료를
    보장합니다. 정상 흐름은 Supervisor 3회와 Worker 2회로 최대 5회 호출합니다.
"""

from shared.travel_contracts import SupervisorDecision
from shared.travel_llm import provider_for_agent, run_learning_agent, run_with_metadata


WORKER_PLAN = ["analyst_agent", "reviewer_agent"]
WORKER_GOALS = {
    "analyst_agent": "사용자 입력 검증 요구사항과 위험을 분석한다.",
    "reviewer_agent": "분석 결과에서 누락된 보안 조건을 검토한다.",
}


def supervisor_agent(request: str, state: dict[str, object], expected_next: str) -> dict:
    prompt = f"""당신은 supervisor_agent입니다. Worker 업무를 직접 수행하지 마세요.
이번 실습의 허용 순서: analyst_agent → reviewer_agent → finish
현재 State: {state}
현재 허용된 다음 행동: {expected_next}
사용자 요청: {request}
SupervisorDecision 계약으로 반환하고 agent_id는 supervisor_agent로 작성하세요."""
    return run_with_metadata(provider_for_agent("supervisor_agent"), prompt, SupervisorDecision)


def selected_worker_agent(agent_id: str, request: str, state: dict[str, object]) -> dict:
    if agent_id not in WORKER_GOALS:
        raise ValueError(f"허용되지 않은 Worker입니다: {agent_id}")
    return run_learning_agent(agent_id, WORKER_GOALS[agent_id], request, state["outputs"])


def supervisor_loop_agent(request: str, max_llm_calls: int = 5) -> dict[str, object]:
    state: dict[str, object] = {"completed_agents": [], "outputs": {}}
    trace: list[dict[str, object]] = []
    llm_calls = 0

    while llm_calls < max_llm_calls:
        completed_agents = state["completed_agents"]
        expected_next = WORKER_PLAN[len(completed_agents)] if len(completed_agents) < len(WORKER_PLAN) else "finish"
        decision = supervisor_agent(request, state, expected_next)
        llm_calls += 1
        trace.append({"call": llm_calls, "actor": "supervisor_agent", "expected": expected_next, "result": decision["result"], "error": decision["error"]})
        if decision["error"]:
            return {"status": "failed", "reason": "supervisor_failed", "state": state, "trace": trace}

        selected = decision["result"]["next_agent"]
        if selected != expected_next:
            return {"status": "blocked", "reason": "invalid_transition", "state": state, "trace": trace}
        if selected == "finish":
            return {"status": "completed", "reason": "all_workers_completed", "state": state, "trace": trace}
        if selected in completed_agents:
            return {"status": "blocked", "reason": "duplicate_worker", "state": state, "trace": trace}
        if llm_calls >= max_llm_calls:
            break

        worker = selected_worker_agent(selected, request, state)
        llm_calls += 1
        trace.append({"call": llm_calls, "actor": selected, "result": worker["result"], "error": worker["error"]})
        if worker["error"]:
            return {"status": "failed", "reason": "worker_failed", "state": state, "trace": trace}
        completed_agents.append(selected)
        state["outputs"][selected] = worker["result"]

    return {"status": "failed", "reason": "max_llm_calls", "state": state, "trace": trace}


if __name__ == "__main__":
    result = supervisor_loop_agent("사용자 입력 길이와 허용 문자를 검증하는 기능을 설계해 주세요.")
    print(result)
    print("전체 상태:", result["status"])
    print("종료 이유:", result["reason"])
    print("실제 LLM 호출 수:", len(result["trace"]))
