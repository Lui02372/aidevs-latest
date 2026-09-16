"""Git/GitHub 실습용 작은 Python 파일입니다.

이 파일은 복잡한 프로그램을 만들기 위한 파일이 아닙니다.
VS Code에서 파일을 수정하고, 테스트하고, Git에 commit하는 흐름을 연습하기 위한 예제입니다.
"""


def add(a: int, b: int) -> int:
    """두 숫자를 더한 값을 반환합니다."""

    return a + b


if __name__ == "__main__":
    result = add(2, 3)
    print("2 + 3 =", result)
