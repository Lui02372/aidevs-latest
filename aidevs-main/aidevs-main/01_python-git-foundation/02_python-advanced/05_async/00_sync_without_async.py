"""async/await 없이 순차 실행되는 예제.

실행: python 00_sync_without_async.py
"""

import time


def say_hello(name: str, seconds: int) -> str:
    """지정한 시간만큼 기다린 뒤 인사말을 반환합니다."""
    print(f"{name}: 기다리기 시작")
    time.sleep(seconds)
    return f"{name}: 안녕하세요"


def main() -> None:
    started_at = time.monotonic()
    print("프로그램 시작")

    # 첫 번째 작업이 완전히 끝난 뒤 두 번째 작업을 시작합니다.
    first = say_hello("첫 번째 작업", 2)
    second = say_hello("두 번째 작업", 1)

    print(first)
    print(second)
    elapsed = time.monotonic() - started_at
    print(f"프로그램 종료 (걸린 시간: {elapsed:.1f}초)")


main()
