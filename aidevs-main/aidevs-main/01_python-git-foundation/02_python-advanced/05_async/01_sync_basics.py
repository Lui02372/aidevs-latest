"""01_async_await_basics.py와 비교하는 동기 방식 예제.

실행: python 01_sync_basics.py
"""

import time


def say_hello(name: str, seconds: int) -> str:
    """기다리는 동안 프로그램 전체가 멈춘다."""
    print(f"{name}: 기다리기 시작")
    time.sleep(seconds)
    return f"{name}: 안녕하세요!"


started_at = time.perf_counter()
print("프로그램 시작")

# 첫 번째 작업이 완전히 끝난 뒤에 두 번째 작업이 시작된다.
first = say_hello("첫 번째 작업", 2)
second = say_hello("두 번째 작업", 1)

print(first)
print(second)
print(f"프로그램 종료 (걸린 시간: {time.perf_counter() - started_at:.1f}초)")

# 2초 + 1초이므로 약 3초가 걸린다.
