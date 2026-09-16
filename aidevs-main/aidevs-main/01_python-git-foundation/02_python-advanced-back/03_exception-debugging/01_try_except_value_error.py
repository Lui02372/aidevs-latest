"""ValueError를 try/except로 처리하는 기본 예제입니다."""


def convert_to_number(value: str) -> int:
    """문자열을 숫자로 변환하고, 실패하면 0을 반환합니다."""

    try:
        # int("10")은 성공하지만 int("abc")는 ValueError가 발생합니다.
        number = int(value)

    except ValueError:
        # 숫자로 바꿀 수 없는 값이 들어오면 여기로 이동합니다.
        print(f"'{value}' 값은 숫자로 변환할 수 없습니다.")

        # 프로그램을 중단하지 않고 기본값 0을 반환합니다.
        return 0

    # 변환에 성공하면 숫자를 반환합니다.
    return number


print("정상 입력:", convert_to_number("10"))
print("잘못된 입력:", convert_to_number("abc"))
print("빈 문자열:", convert_to_number(""))
