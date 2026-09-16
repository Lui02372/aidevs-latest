"""02_async_api_request.py와 비교하는 동기 방식 API 호출 예제.

실행: python 02_sync_api_request.py
"""

import json
import time
from urllib.request import urlopen


URLS = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
]


def get_json(url: str) -> dict:
    with urlopen(url, timeout=10) as response:
        return json.load(response)


started_at = time.perf_counter()
print("API 요청을 하나씩 보냅니다...")

# 앞 요청의 응답을 받을 때까지 다음 요청을 보내지 못한다.
for url in URLS:
    todo = get_json(url)
    print(f"- {todo['title']}")

print(f"걸린 시간: {time.perf_counter() - started_at:.2f}초")
print("여러 API 요청이 필요하면 async 예제처럼 동시에 기다리는 편이 유리합니다.")
