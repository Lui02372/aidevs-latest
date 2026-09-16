"""Lab 03-07: GPT Supervisor와 Gemini·Llama·Gemma Worker가 한 Team으로 협업합니다.

시나리오:
    사용자 입력 검증 기능을 분석하고 구현 방법을 작성한 뒤 보안 관점에서 검토합니다.
    GPT Supervisor가 State를 확인하며 Gemini Analyst, Llama Developer, Gemma Reviewer를
    순서대로 선택하고 마지막에 finish를 반환합니다.

학습 질문:
    여러 Provider를 사용해도 누가 다음 Worker를 선택하고 언제 종료할지는 어떻게
    일관되게 통제할 수 있을까요?

확인할 내용:
    반복되는 Worker 설정은 YAML에서 읽지만 허용 순서·중복 실행·최대 7회 호출은
    Python이 통제합니다. 실제 네 LLM의 결과와 오류를 Trace에 보존합니다.
"""

from shared.travel_contracts import LearningAgentResult, SupervisorDecision
from shared.travel_llm import run_with_metadata
from worker_registry import load_worker_registry


WORKER_PLAN = ["analyst_agent", "developer_agent", "reviewer_agent"]
WORKERS = load_worker_registry()


def supervisor_agent(request: str, state: dict[str, object], expected_next: str) -> dict:
    prompt = f"""당신은 supervisor_agent입니다. 직접 분석·구현·검토하지 마세요.
허용 순서: analyst_agent → developer_agent → reviewer_agent → finish
현재 State: {state}
현재 허용된 다음 행동: {expected_next}
사용자 요청: {request}
SupervisorDecision 계약으로 반환하고 agent_id는 supervisor_agent로 작성하세요."""
    return run_with_metadata("openai", prompt, SupervisorDecision)


def selected_worker_agent(agent_id: str, request: str, outputs: dict[str, object]) -> dict:
    if agent_id not in WORKERS:
        raise ValueError(f"허용되지 않은 Worker입니다: {agent_id}")
    worker = WORKERS[agent_id]
    prompt = f"""당신은 {agent_id}입니다.
이름: {worker['name']}
Goal: {worker['goal']}
Instructions: {worker['instructions']}
사용자 요청: {request}
이전 Agent Context: {outputs}
LearningAgentResult 계약으로 반환하고 agent_id는 반드시 {agent_id}로 작성하세요."""
    result = run_with_metadata(worker["provider"], prompt, LearningAgentResult)
    if result["result"] and result["result"]["agent_id"] != agent_id:
        result["error"] = f"Agent 역할 불일치: expected={agent_id}, actual={result['result']['agent_id']}"
        result["result"] = None
    return result


def multi_llm_team_agent(request: str, max_llm_calls: int = 7) -> dict[str, object]:
    state: dict[str, object] = {"completed_agents": [], "outputs": {}}
    trace: list[dict[str, object]] = []

    while len(trace) < max_llm_calls:
        completed_agents = state["completed_agents"]
        expected_next = WORKER_PLAN[len(completed_agents)] if len(completed_agents) < len(WORKER_PLAN) else "finish"
        decision = supervisor_agent(request, state, expected_next)
        trace.append({"step": len(trace) + 1, "actor": "supervisor_agent", "provider": decision["provider_requested"], "model": decision["model"], "result": decision["result"], "error": decision["error"]})
        if decision["error"]:
            return {"status": "failed", "reason": "supervisor_failed", "state": state, "trace": trace}
        selected = decision["result"]["next_agent"]
        if selected != expected_next:
            return {"status": "blocked", "reason": "invalid_transition", "state": state, "trace": trace}
        if selected == "finish":
            return {"status": "completed", "reason": "all_workers_completed", "state": state, "trace": trace}
        if selected in completed_agents:
            return {"status": "blocked", "reason": "duplicate_worker", "state": state, "trace": trace}
        if len(trace) >= max_llm_calls:
            break

        worker = selected_worker_agent(selected, request, state["outputs"])
        trace.append({"step": len(trace) + 1, "actor": selected, "provider": worker["provider_requested"], "model": worker["model"], "result": worker["result"], "error": worker["error"]})
        if worker["error"]:
            return {"status": "failed", "reason": "worker_failed", "state": state, "trace": trace}
        completed_agents.append(selected)
        state["outputs"][selected] = worker["result"]

    return {"status": "failed", "reason": "max_llm_calls", "state": state, "trace": trace}


if __name__ == "__main__":
    result = multi_llm_team_agent("사용자 입력 길이와 허용 문자를 검증하는 기능을 설계하고 검토해 주세요.")
    print(result)
    print("전체 상태:", result["status"])
    print("종료 이유:", result["reason"])
    for event in result["trace"]:
        print(event["step"], event["actor"], event["provider"], event["model"], "오류:", event["error"])
