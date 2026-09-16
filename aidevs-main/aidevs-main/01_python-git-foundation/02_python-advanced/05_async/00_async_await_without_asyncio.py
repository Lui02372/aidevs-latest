"""asyncio를 직접 import하지 않는 async/await 예제.

실행: python 00_async_await_without_asyncio.py

anyio는 asyncio, Trio 등의 비동기 실행 환경을 공통 방식으로 다룰 수 있게 하는
라이브러리입니다. 이 예제에서는 asyncio 대신 anyio가 비동기 실행을 시작합니다.
"""

import anyio


async def say_hello(name: str, seconds: int) -> str:
    """지정한 시간만큼 기다린 뒤 인사말을 반환합니다."""
    print(f"{name}: 기다리기 시작")
    await anyio.sleep(seconds)
    return f"{name}: 안녕하세요"


async def main() -> None:
    print("프로그램 시작")

    # async/await는 asyncio 전용 문법이 아닙니다.
    # await 할 수 있는 비동기 함수라면 사용할 수 있습니다.
    first = await say_hello("첫 번째 작업", 2)
    second = await say_hello("두 번째 작업", 1)

    print(first)
    print(second)
    print("프로그램 종료")


# 일반 파이썬 파일에서는 비동기 함수를 실행할 도구가 필요합니다.
# 여기서는 asyncio.run() 대신 anyio.run()을 사용합니다.
anyio.run(main)
