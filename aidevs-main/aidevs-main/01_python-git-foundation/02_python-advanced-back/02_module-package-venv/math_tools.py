"""계산과 관련된 함수를 모아 둔 직접 만든 모듈입니다."""


def add(a: int, b: int) -> int:
    """두 숫자를 더합니다."""

    # a와 b를 더한 값을 반환합니다.
    return a + b


def subtract(a: int, b: int) -> int:
    """첫 번째 숫자에서 두 번째 숫자를 뺍니다."""

    # a에서 b를 뺀 값을 반환합니다.
    return a - b


def multiply(a: int, b: int) -> int:
    """두 숫자를 곱합니다."""

    # a와 b를 곱한 값을 반환합니다.
    return a * b


def divide(a: int, b: int) -> float:
    """첫 번째 숫자를 두 번째 숫자로 나눕니다."""

    # 이 예제에서는 예외 처리를 아직 자세히 다루지 않습니다.
    # b가 0이면 오류가 발생할 수 있다는 점만 기억합니다.
    return a / b
