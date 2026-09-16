"""Lab 01-3: 여러 업무를 같은 기준으로 평가해 Agent 분리를 판단합니다.

시나리오:
    여행, 고객지원, 코드검토, 콘텐츠 검사, 장애대응 사례를 독립 Goal·Context·권한·
    평가·Handoff 기준으로 판정합니다. Tool이나 단계가 많다는 이유만으로 분리하지
    않습니다.

학습 질문:
    도메인이 달라져도 반복해서 사용할 수 있는 Agent 분리 기준은 무엇일까요?
"""

from dataclasses import dataclass


criteria = {
    "single_ai_agent": [
        "사용자 Goal이 하나다",
        "같은 Context와 Tool 권한을 사용한다",
        "하나의 완료·평가 기준으로 충분하다",
    ],
    "multi_ai_agent": [
        "독립적인 전문 Goal이 있다",
        "Context 또는 Tool 권한을 격리해야 한다",
        "Agent별 완료·평가 기준이 다르다",
        "결과를 병렬로 만들거나 Handoff해야 한다",
    ],
}


@dataclass(frozen=True)
class DesignCase:
    name: str
    independent_goals: bool
    isolated_context_or_permissions: bool
    separate_evaluation: bool
    handoff_or_parallelism: bool


CASES = [
    DesignCase("여행 초안 한 번 작성", False, False, False, False),
    DesignCase("한 Agent가 날씨와 장소 Tool 사용", False, False, False, False),
    DesignCase("날씨·예산·장소를 독립 평가", True, False, True, True),
    DesignCase("조회 Agent와 결제 Agent 권한 격리", True, True, True, False),
    DesignCase("고객 문의 분류와 일반 답변", False, False, False, False),
    DesignCase("상담 분석 후 실제 환불", True, True, True, True),
    DesignCase("코드 생성 후 독립 보안 검토", True, True, True, True),
    DesignCase("초안 작성 후 맞춤법 규칙 검사", False, False, False, False),
    DesignCase("장애 분석 후 운영 서버 재시작", True, True, True, True),
]


def architecture_decision_agent(case: DesignCase) -> tuple[str, list[str]]:
    reasons = []
    if case.independent_goals:
        reasons.append("독립 Goal")
    if case.isolated_context_or_permissions:
        reasons.append("Context 또는 권한 격리")
    if case.separate_evaluation:
        reasons.append("별도 평가 기준")
    if case.handoff_or_parallelism:
        reasons.append("Handoff 또는 병렬 실행")

    # Tool이나 단계의 개수가 아니라 책임을 분리할 근거가 둘 이상인지 확인합니다.
    decision = "multi_agent_candidate" if len(reasons) >= 2 else "start_single_agent"
    return decision, reasons


if __name__ == "__main__":
    print("판단 기준:", criteria)
    for case in CASES:
        decision, reasons = architecture_decision_agent(case)
        print(f"{case.name}: {decision} / 근거={reasons or ['분리 근거 없음']}")

    expected = ["start_single_agent", "start_single_agent", "multi_agent_candidate", "multi_agent_candidate", "start_single_agent", "multi_agent_candidate", "multi_agent_candidate", "start_single_agent", "multi_agent_candidate"]
    actual = [architecture_decision_agent(case)[0] for case in CASES]
    print("예상 판정과 일치:", actual == expected)
    print("주의: 후보로 판정돼도 비용과 실패 지점이 늘어나는지 비교한 뒤 분리합니다.")
