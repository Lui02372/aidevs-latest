"""Lab 01-4: Single과 Multi 구조의 호출·Context·실패 범위를 비교합니다.

시나리오:
    같은 여행 요청을 하나의 Agent와 Supervisor·세 Specialist·Join 구조로 각각
    설계했다고 가정합니다. 실제 LLM을 호출하지 않고 호출 수, Context 복사, 실패
    지점과 권한 격리의 차이만 비교합니다.

학습 질문:
    Multi-Agent로 분리해서 얻는 이점은 늘어난 비용과 실패 지점을 감수할 만큼
    구체적인가요?
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitectureEstimate:
    name: str
    llm_calls: int
    context_copies: int
    independent_failure_points: int
    isolated_permissions: bool


def architecture_estimation_agent(agent_count: int, *, orchestrated: bool) -> ArchitectureEstimate:
    if not orchestrated:
        return ArchitectureEstimate(
            name="single_agent",
            llm_calls=1,
            context_copies=1,
            independent_failure_points=1,
            isolated_permissions=False,
        )
    return ArchitectureEstimate(
        name="multi_agent_orchestration",
        # Supervisor 1회 + Specialist N회 + 최종 Join 1회인 단순 추정입니다.
        llm_calls=agent_count + 2,
        context_copies=agent_count,
        independent_failure_points=agent_count + 2,
        isolated_permissions=True,
    )


def architecture_recommendation_agent(single: ArchitectureEstimate, multi: ArchitectureEstimate, *, needs_isolation: bool) -> str:
    if needs_isolation and multi.isolated_permissions:
        return "multi_agent_candidate"
    if multi.llm_calls > single.llm_calls:
        return "start_single_agent"
    return "compare_with_evaluation"


if __name__ == "__main__":
    single = architecture_estimation_agent(agent_count=3, orchestrated=False)
    multi = architecture_estimation_agent(agent_count=3, orchestrated=True)

    print(single)
    print(multi)
    print("권한 격리 불필요:", architecture_recommendation_agent(single, multi, needs_isolation=False))
    print("권한 격리 필요:", architecture_recommendation_agent(single, multi, needs_isolation=True))
    print("Multi 구조의 호출 증가:", multi.llm_calls > single.llm_calls)
    print("Multi 구조의 실패 지점 증가:", multi.independent_failure_points > single.independent_failure_points)
