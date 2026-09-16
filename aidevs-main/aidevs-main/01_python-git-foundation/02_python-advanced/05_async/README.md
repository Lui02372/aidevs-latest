# async/await 아주 쉬운 예제

이 폴더에서는 `async`와 `await`으로 여러 작업을 기다리는 방법을 연습합니다.

## 실행 방법

`05_async` 폴더에서 아래 명령을 실행합니다.

```bash
python 01_async_await_basics.py
python 01_sync_basics.py
python 02_async_api_request.py
python 02_sync_api_request.py
```

## 파일 안내

- `01_async_await_basics.py`: `asyncio.sleep()`을 이용해 두 작업을 동시에 기다립니다. 전체 시간은 약 2초입니다.
- `01_sync_basics.py`: 같은 작업을 동기 방식으로 실행합니다. 두 작업이 차례대로 실행되어 약 3초가 걸립니다.
- `02_async_api_request.py`: 무료 연습용 API 두 곳에 동시에 요청을 보냅니다.
- `02_sync_api_request.py`: 같은 API 요청을 하나씩 보냅니다. 앞 요청의 응답을 받기 전까지 다음 요청을 보낼 수 없습니다.

API 예제는 인터넷 연결이 필요하며, Python 3.9 이상에서 실행하세요. 네트워크 상태에 따라 정확한 시간은 달라질 수 있습니다.

## 비교해 보기

먼저 `01_sync_basics.py`를 실행한 뒤 `01_async_await_basics.py`를 실행해 보세요. 출력된 걸린 시간을 비교하면, 기다리는 작업은 동시에 처리할 때 전체 시간이 줄어드는 것을 볼 수 있습니다.

그다음 `02_sync_api_request.py`와 `02_async_api_request.py`도 같은 방식으로 비교해 보세요. API 응답을 기다리는 동안에도 다른 요청을 진행할 수 있다는 점이 핵심입니다.

## 핵심만 기억하기

- `async def`: 비동기 함수를 만든다.
- `await`: 비동기 작업이 끝날 때까지 기다린다. 그동안 다른 비동기 작업은 실행될 수 있다.
- `asyncio.run(main())`: 비동기 프로그램의 시작점이다.
