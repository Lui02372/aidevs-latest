"""Lab 03-03: Router의 선택 범위와 정보 부족 상태를 계약으로 제한합니다.

시나리오:
    외부 Router가 존재하지 않는 payment_agent를 선택하거나, 추가 정보가 필요하다고
    하면서 어떤 정보가 필요한지는 반환하지 않았습니다. 반대로 Worker를 선택하면서
    missing_information도 함께 반환한 모순 사례가 있습니다.

학습 질문:
    LLM Router의 선택을 Prompt 지시만으로 안전하게 제한할 수 있을까요?

확인할 내용:
    Pydantic Literal과 의미 검증이 허용 목록 및 상태 모순을 차단합니다. 의도적으로
    만든 오류 입력이며 실제 LLM을 호출하지 않습니다.
"""

from pydantic import ValidationError

from shared.travel_contracts import SupportRouteDecision


CASES = [
    ("정상 배송 선택", {"selected_agent": "delivery_agent", "reason": "배송 상태 문의"}, True),
    ("존재하지 않는 Agent", {"selected_agent": "payment_agent", "reason": "결제 처리"}, False),
    ("선택 이유 누락", {"selected_agent": "refund_agent"}, False),
    ("추가 정보 목록 누락", {"selected_agent": "request_information", "reason": "문의가 모호함"}, False),
    ("Worker 선택과 정보 요청 모순", {"selected_agent": "delivery_agent", "reason": "배송 문의", "missing_information": ["주문 번호"]}, False),
]


def routing_contract_agent(payload: dict) -> tuple[bool, str]:
    try:
        SupportRouteDecision.model_validate(payload)
        return True, "계약 통과"
    except ValidationError as error:
        first_error = error.errors()[0]
        return False, f"위치={first_error['loc']} / 이유={first_error['msg']}"


if __name__ == "__main__":
    for name, payload, expected in CASES:
        actual, detail = routing_contract_agent(payload)
        print(f"{name}: {'통과' if actual else '차단'} / 예상과 일치: {actual == expected}")
        print(" ", detail)
