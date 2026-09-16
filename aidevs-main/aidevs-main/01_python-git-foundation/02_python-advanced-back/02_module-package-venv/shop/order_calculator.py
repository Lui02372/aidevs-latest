"""주문 금액 계산 기능을 담은 모듈입니다."""


def calculate_total(prices: list[int]) -> int:
    """상품 가격 목록을 받아 총 금액을 계산합니다."""

    # total은 누적 합계를 저장하는 변수입니다.
    total = 0

    # 가격 목록에서 가격을 하나씩 꺼냅니다.
    for price in prices:
        # 현재 가격을 total에 더합니다.
        total += price

    # 최종 합계를 반환합니다.
    return total
