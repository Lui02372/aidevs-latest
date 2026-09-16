"""잘못 입력하면 다시 입력받는 안전한 반복 입력 예제입니다."""


def ask_number_until_valid() -> int:
    """숫자가 입력될 때까지 반복해서 입력받습니다."""

    while True:
        # input으로 받은 값은 항상 문자열입니다.
        text = input("숫자를 입력하세요. 종료하려면 q 입력: ")

        # q를 입력하면 반복을 끝냅니다.
        if text.lower() == "q":
            print("입력을 취소했습니다.")
            return 0

        try:
            # 숫자로 변환할 수 없으면 ValueError가 발생합니다.
            number = int(text)

        except ValueError:
            # 잘못 입력해도 프로그램을 종료하지 않고 다시 입력받습니다.
            print("숫자만 입력할 수 있습니다. 다시 입력해 주세요.")
            continue

        # 숫자 변환에 성공하면 값을 반환하고 반복을 끝냅니다.
        return number


value = ask_number_until_valid()
print("최종 입력값:", value)
