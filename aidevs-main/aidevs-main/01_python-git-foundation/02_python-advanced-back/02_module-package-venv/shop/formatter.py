"""주문 출력 문장을 만드는 모듈입니다."""


def format_order_message(customer: str, total: int) -> str:
    """주문자 이름과 총 금액을 받아 출력 문장을 만듭니다."""

    # f-string을 사용하면 변수 값을 문자열 안에 쉽게 넣을 수 있습니다.
    return f"{customer}님의 주문 총액은 {total}원입니다."
