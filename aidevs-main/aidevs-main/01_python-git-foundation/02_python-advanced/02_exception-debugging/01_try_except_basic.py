r"""try/except 기본 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\02_exception-debugging\01_try_except_basic.py

이 예제의 목표:
    문자열을 숫자로 바꿀 때 발생할 수 있는 ValueError를 처리합니다.
"""


def to_int_or_default(value: str) -> int:
    """문자열을 int로 바꾸고, 실패하면 기본값을 반환합니다."""
    try:
        result = int(value)
    except:
        return None
    return result

def dvided(num1:int, num2:int) ->float:
    try:
        result = num1 / num2
    except:
        return None
    return result

def main() -> None:
    values = ["10", "a", "30"]

    for value in values:
        number = to_int_or_default(value)
        print("변환 결과:", number)

    result = dvided(10,2)
    print(result)


main()
