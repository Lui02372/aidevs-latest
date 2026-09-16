"""async/await 기초 예제.

실행: python 01_async_await_basics.py
"""

import asyncio

# asyncio는 파이썬 표준 비동기 도구입니다.
# 일반 파이썬 파일에서는 asyncio.run()으로 이벤트 루프를 시작합니다.
# FastAPI에서는 Uvicorn/FastAPI가 이벤트 루프를 이미 실행하므로,
# 보통 asyncio.run()을 직접 쓰지 않고 async def 안에서 await를 사용합니다.
# 실제 FastAPI에서는 asyncio.sleep()보다 외부 API 호출이나 비동기 DB 호출을
# await 하는 경우가 더 많습니다.


async def say_hello(name: str, seconds: int) -> str:
    """지정한 시간만큼 비동기로 기다린 뒤 인사말을 반환합니다."""
    print(f"{name}: 기다리기 시작")
    await asyncio.sleep(seconds)
    return f"{name}: 안녕하세요"


async def main() -> None:
    started_at = asyncio.get_running_loop().time()
    print("프로그램 시작")

    # 두 작업을 동시에 시작합니다.
    first, second = await asyncio.gather(
        say_hello("첫 번째 작업", 2),
        say_hello("두 번째 작업", 1),
    )

    print(first)
    print(second)
    elapsed = asyncio.get_running_loop().time() - started_at
    print(f"프로그램 종료 (걸린 시간: {elapsed:.1f}초)")


asyncio.run(main())
