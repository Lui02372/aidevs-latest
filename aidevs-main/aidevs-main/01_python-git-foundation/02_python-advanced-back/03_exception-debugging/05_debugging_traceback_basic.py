"""오류 종류와 메시지를 읽는 방법을 이해하는 예제입니다."""


def get_first_item(items: list[str]) -> str:
    """리스트의 첫 번째 값을 반환합니다."""

    # items가 빈 리스트이면 IndexError가 발생합니다.
    return items[0]


try:
    # 일부러 빈 리스트를 전달해 오류 상황을 만듭니다.
    first_item = get_first_item([])
    print("첫 번째 값:", first_item)

except IndexError as error:
    # type(error).__name__은 오류 종류 이름을 보여줍니다.
    print("오류 종류:", type(error).__name__)

    # error 자체를 출력하면 오류 메시지를 볼 수 있습니다.
    print("오류 메시지:", error)

    # 실제 traceback에서는 오류 메시지의 마지막 줄과 파일의 줄 번호를 먼저 확인합니다.
    print("확인 방법: 오류 종류, 오류 메시지, 발생한 줄 번호를 차례대로 확인합니다.")
