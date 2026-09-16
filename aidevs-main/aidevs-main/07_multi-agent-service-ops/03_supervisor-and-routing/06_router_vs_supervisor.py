"""Lab 03-06: Router와 Supervisor가 적합한 업무를 결정적으로 비교합니다.

시나리오:
    고객지원 단일 문의와 여러 단계가 필요한 코드 변경 요청이 섞여 있습니다. 각 사례에
    필요한 선택 횟수, State, 종료 조건과 실패 지점을 비교해 더 단순한 구조를 고릅니다.

학습 질문:
    LLM이 여러 Agent 중 하나를 선택한다는 이유만으로 모두 Supervisor일까요?

확인할 내용:
    한 번의 담당자 선택은 Router, 중간 결과를 보고 다음 행동을 반복하면 Supervisor가
    적합합니다. 이 단계는 구조 비교 예제이므로 실제 LLM을 호출하지 않습니다.
"""


CASES = [
    {"request": "배송 상태를 알려 주세요.", "needs_multiple_steps": False, "needs_state": False},
    {"request": "환불 정책을 알려 주세요.", "needs_multiple_steps": False, "needs_state": False},
    {"request": "요구사항을 분석하고 구현 방법을 작성한 뒤 검토해 주세요.", "needs_multiple_steps": True, "needs_state": True},
    {"request": "여행 예산만 계산해 주세요.", "needs_multiple_steps": False, "needs_state": False},
]


def architecture_selection_agent(case: dict[str, object]) -> dict[str, object]:
    use_supervisor = bool(case["needs_multiple_steps"] and case["needs_state"])
    return {
        "request": case["request"],
        "selected_structure": "supervisor" if use_supervisor else "router",
        "selection_count": "반복" if use_supervisor else "1회",
        "state_required": use_supervisor,
        "termination_rule": "완료 또는 최대 단계" if use_supervisor else "Worker 선택 후 종료",
    }


if __name__ == "__main__":
    for case in CASES:
        result = architecture_selection_agent(case)
        print(result)
