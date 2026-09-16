# FastAPI 기본 프로젝트 구조

처음에는 `main.py` 하나로 시작합니다.

```text
project
└─ main.py
```

하지만 기능이 늘어나면 파일을 역할별로 나누는 것이 좋습니다.

```text
app
├─ main.py
├─ routers
│  └─ memo_router.py
├─ schemas
│  └─ memo_schema.py
└─ services
   └─ memo_service.py

tests
└─ test_memo_api.py
```

## 폴더 역할

```text
main.py:
  FastAPI 앱을 만들고 서버의 시작점을 담당합니다.

routers:
  /memos, /users 같은 API 주소를 기능별로 나누어 둡니다.

schemas:
  Pydantic 모델을 둡니다. 요청 데이터와 응답 데이터의 모양을 정의합니다.

services:
  실제 처리 로직을 둡니다. 예를 들어 메모 생성, 질문 검증, 외부 API 호출 같은 작업입니다.

tests:
  API가 예상대로 동작하는지 확인하는 테스트 코드를 둡니다.
```

## 이 단원에서는 어디까지 하나요?

이번 첫 단원에서는 `main.py` 하나로 시작합니다.

```text
main.py
-> app = FastAPI()
-> @app.get("/")
-> @app.get("/health")
```

라우터, 스키마, 서비스 분리는 이후 Request Body, Pydantic, CRUD API를 배우면서 천천히 확장합니다.

## 이 구조를 어디서 실습하나요?

이 구조는 `10_labs/lab-100_project-structure-refactor`에서 직접 실습합니다.

이 과정의 초반 목표는 폴더 분리보다 FastAPI의 기본 동작을 먼저 이해하는 것입니다. 그래서 먼저 아래 단원들은 대부분 하나의 `main.py` 또는 `solution.py` 파일 안에서 개념을 익힙니다.

```text
01_fastapi-project-setup
-> main.py 하나로 FastAPI 앱 실행

02_routing-and-request
-> 라우팅, path/query/request body를 단일 파일에서 실습

03_pydantic-and-response
-> Pydantic 요청/응답 모델을 단일 파일에서 실습

05_error-handling-and-testing
-> 오류 처리와 테스트 흐름을 작은 예제로 실습

10_labs/lab-99_mini-memo-api-server
-> 라우팅, Pydantic 모델, 메모리 저장소, async 응답을 하나의 미니 API 서버로 통합

10_labs/lab-100_project-structure-refactor
-> lab-99에서 만든 미니 API 서버를 app/main.py, routers, schemas, services, tests 구조로 분리
```

즉, `lab-99_mini-memo-api-server`에서는 API 기능을 한 파일 흐름으로 완성하고, 바로 다음 `lab-100_project-structure-refactor`에서 같은 기능을 실제 프로젝트 폴더 구조로 나누어 봅니다.

이 순서로 진행하면 수강생이 먼저 API 동작을 이해한 뒤, 왜 `router`, `schema`, `service`, `test`를 분리하는지 자연스럽게 연결할 수 있습니다.
