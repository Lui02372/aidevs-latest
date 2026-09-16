"""asyncio로 외부 API를 호출하는 쉬운 예제.

별도 패키지 설치 없이 Python 표준 라이브러리만 사용한다.
실행: python 02_async_api_request.py
"""

import asyncio
import json
from urllib.request import urlopen


URLS = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
]


def get_json(url: str) -> dict:
    """동기 방식으로 URL의 JSON 응답을 가져온다."""
    with urlopen(url, timeout=10) as response:
        return json.load(response)


async def main() -> None:
    started_at = asyncio.get_running_loop().time()
    print("API 요청을 동시에 보냅니다...")

    # urlopen은 동기 함수다. to_thread로 별도 스레드에서 실행해
    # 이벤트 루프가 멈추지 않도록 한다.
    todos = await asyncio.gather(
        *(asyncio.to_thread(get_json, url) for url in URLS)
    )

    print("받은 할 일:")
    for todo in todos:
        print(f"- {todo['title']} (완료: {todo['completed']})")
    print(f"걸린 시간: {asyncio.get_running_loop().time() - started_at:.2f}초")


asyncio.run(main())
