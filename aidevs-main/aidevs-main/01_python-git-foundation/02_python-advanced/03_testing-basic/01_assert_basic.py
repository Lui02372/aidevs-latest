r"""assert 기본 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\03_testing-basic\01_assert_basic.py

이 예제의 목표:
    assert는 "이 조건은 반드시 True여야 한다"는 뜻입니다.
    조건이 False이면 Python이 AssertionError를 발생시킵니다.
"""


def add(a: int, b: int) -> int:
    return a + b


def main() -> None:
    result = add(2, 3)

    print("계산 결과:", result)

    assert result == 5
    print("assert 통과: add(2, 3)은 5입니다.")


main()
