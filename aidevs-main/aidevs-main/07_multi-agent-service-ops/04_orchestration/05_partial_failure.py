"""Lab 04-05: 병렬 Agent 일부가 실패했을 때 세 가지 계속 실행 정책을 비교합니다.

시나리오:
    Weather와 Budget Agent는 성공했지만 Place Agent는 실패했습니다. Fail Fast,
    Best Effort, Required/Optional 정책이 같은 실패를 어떻게 다르게 처리하는지 봅니다.

학습 질문:
    Agent 하나가 실패하면 항상 전체 Workflow를 실패시켜야 할까요?

확인할 내용:
    실패 정책은 LLM이 즉석에서 정하지 않고 업무 요구사항으로 미리 정의합니다. 이
    단계는 결정적인 정책 비교 예제이므로 실제 LLM을 호출하지 않습니다.
"""


RESULTS = {"weather_agent": {"status": "completed"}, "budget_agent": {"status": "completed"}}
ERRORS = {"place_agent": "Provider timeout"}
REQUIRED_AGENTS = {"weather_agent", "budget_agent"}


def partial_failure_policy_agent(policy: str) -> dict[str, object]:
    successful = set(RESULTS)
    failed = set(ERRORS)
    missing_required = sorted(REQUIRED_AGENTS - successful)
    if policy == "fail_fast":
        can_continue = not failed
        failure_reason = "any_agent_failed"
    elif policy == "best_effort":
        can_continue = bool(successful)
        failure_reason = "no_successful_result"
    elif policy == "required_optional":
        can_continue = not missing_required
        failure_reason = "required_result_failed"
    else:
        raise ValueError(f"지원하지 않는 정책입니다: {policy}")
    return {
        "policy": policy,
        "successful_agents": sorted(successful),
        "failed_agents": sorted(failed),
        "missing_required": missing_required,
        "can_continue": can_continue,
        "termination_reason": "continue_with_available_results" if can_continue else failure_reason,
    }


if __name__ == "__main__":
    for policy_name in ("fail_fast", "best_effort", "required_optional"):
        print(partial_failure_policy_agent(policy_name))
