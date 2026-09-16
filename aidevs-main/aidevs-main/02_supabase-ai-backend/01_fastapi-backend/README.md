# 01_fastapi-backend

Python으로 웹 API 서버를 만드는 FastAPI 백엔드 개발 단원입니다.

`01_python-git-foundation/01_python-basic`과 `01_python-git-foundation/02_python-advanced`에서 익힌 Python 문법, 함수, 모듈, 객체지향 개념을 실제 API 서버 개발로 연결합니다.

이 단원에서는 **브라우저나 다른 프로그램이 호출할 수 있는 API 서버**를 직접 만들어 봅니다. 아직 Supabase에 저장하지 않고, 먼저 FastAPI의 기본 구조와 요청/응답 흐름을 익힙니다. 이후 `02_llm-api-integration`에서 AI 모델 API 호출 구조를 연결하고, `03_supabase-db-and-auth`에서 데이터베이스 저장과 인증을 Supabase 기준으로 연결합니다.

## 이 단원에서 먼저 이해할 것

```text
FastAPI:
  Python 함수로 API 주소를 만들 수 있게 해 주는 웹 API 프레임워크입니다.

Endpoint:
  사용자가 호출하는 API 주소입니다. 예를 들어 /health, /users/1 같은 경로입니다.

HTTP Method:
  API 요청의 목적을 나타냅니다. GET은 조회, POST는 생성, PUT은 수정, DELETE는 삭제에 사용합니다.

Request:
  클라이언트가 서버로 보내는 요청입니다. URL, Query Parameter, Path Parameter, JSON Body가 포함될 수 있습니다.

Response:
  서버가 클라이언트에게 돌려주는 응답입니다. 보통 JSON 형태로 반환합니다.

Pydantic:
  요청 데이터와 응답 데이터의 모양을 정하고 검증하는 도구입니다.

Swagger UI:
  FastAPI가 자동으로 만들어 주는 API 테스트 화면입니다. 브라우저에서 /docs로 접속합니다.
```

## 학습 목표

- FastAPI 프로젝트를 만들고 실행할 수 있다.
- HTTP Method, Path Parameter, Query Parameter, Request Body를 이해할 수 있다.
- Pydantic 모델로 요청 데이터를 검증할 수 있다.
- Response Model과 표준 응답 구조를 설계할 수 있다.
- FastAPI의 `Depends`를 사용해 공통 로직을 분리할 수 있다.
- 비동기 엔드포인트와 외부 API 호출 구조를 이해할 수 있다.
- HTTPException, 전역 Exception Handler, Middleware, CORS, Swagger UI, 간단한 테스트 흐름을 익힐 수 있다.
- 메모리 저장소 기반 CRUD API를 만들고 이후 Supabase 저장 구조로 확장할 준비를 할 수 있다.

## 참고 문서

처음부터 모든 문서를 외우지 않아도 됩니다. 예제를 실행하다가 필요한 순간에 아래 문서를 함께 확인합니다.

| 문서 | 언제 보면 좋은가 |
| --- | --- |
| [setup-and-run.md](00_references/setup-and-run.md) | FastAPI 설치, `uvicorn` 실행, `/docs` 접속 방법이 헷갈릴 때 |
| [http-basics.md](00_references/http-basics.md) | GET/POST/PUT/DELETE, URL, 상태 코드가 헷갈릴 때 |
| [fastapi-cheatsheet.md](00_references/fastapi-cheatsheet.md) | FastAPI 기본 문법을 빠르게 다시 보고 싶을 때 |
| [api-design-checklist.md](00_references/api-design-checklist.md) | API 주소와 응답 구조가 적절한지 점검할 때 |
| [common-errors.md](00_references/common-errors.md) | `Error loading ASGI app`, 422 오류, 설치 오류가 날 때 |

## 학습 순서

```text
00_references
-> 01_fastapi-project-setup
-> 02_routing-and-request
-> 03_pydantic-and-response
-> 04_async-and-external-api
-> 05_error-handling-and-testing
-> 10_labs
-> 20_assignments
```

## 챕터별 연결

| 순서 | 폴더 | 핵심 내용 | 이후 연결 |
| --- | --- | --- | --- |
| 1 | `01_fastapi-project-setup` | FastAPI 앱 생성, `/health`, `uvicorn` 실행 | 모든 API 서버의 시작 구조 |
| 2 | `02_routing-and-request` | GET/POST, Path Parameter, Query Parameter, Request Body | REST API 설계 |
| 3 | `03_pydantic-and-response` | Pydantic 요청 검증, Response Model, 표준 응답 | Supabase 저장 전 데이터 모양 정리 |
| 4 | `04_async-and-external-api` | `async def`, 외부 API 호출 구조, 스트리밍 응답 기초 | 이후 LLM API 호출과 SSE 이해 |
| 5 | `05_error-handling-and-testing` | HTTPException, Depends, CORS, Swagger/Postman/TestClient | 프론트엔드 연동과 API 안정성 점검 |
| 6 | `10_labs` | 단계별 실습, 미니 API 서버, 프로젝트 구조 분리 | 직접 구현 |
| 7 | `20_assignments` | 과제형 API 구현 | 미니 프로젝트 준비 |

## 실행 기본 명령

먼저 과정 루트에서 가상환경을 활성화합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

설치가 정상인지 확인합니다.

```powershell
python -c "import fastapi, uvicorn, pydantic; print('fastapi ready')"
```

FastAPI 서버는 `app = FastAPI()`가 있는 파일을 기준으로 실행합니다.

```powershell
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

명령의 의미는 다음과 같습니다.

```text
main:
  main.py 파일을 뜻합니다.

app:
  파일 안에 있는 FastAPI 인스턴스 변수명입니다. 예: app = FastAPI()

--reload:
  코드를 수정하면 서버를 자동으로 다시 시작합니다.
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

서버를 종료하려면 터미널에서 `Ctrl + C`를 누릅니다.

## 파일명과 실행 위치 주의

FastAPI 예제 파일 중에는 학습 순서를 보여주기 위해 `01_hello-fastapi.py`처럼 번호와 하이픈이 들어간 파일이 있습니다. 이런 파일은 실제 프로젝트 파일명으로는 권장하지 않지만, 이 과정에서는 개념을 하나씩 확인할 수 있도록 일부 예제 파일 상단에 개별 실행 명령을 적어 두었습니다.

개별 예제 파일을 실행할 때는 파일 상단의 `실행:` 주석을 먼저 확인합니다. 통합 실습과 Lab은 아래처럼 `starter.py`, `solution.py`, `main.py`처럼 import하기 쉬운 파일명으로 진행합니다.

```powershell
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

정리하면, 개념 예제는 파일 상단의 실행 명령을 따르고, 수업에서 하나의 API 서버로 합쳐 보는 실습은 각 챕터의 `main.py` 또는 Lab의 `starter.py`, `solution.py`를 기준으로 진행합니다.

## 예제 실행 방법

각 챕터의 예제 파일명은 학습 순서를 보여주기 위해 번호와 하이픈을 포함할 수 있습니다. 개별 예제는 파일 상단의 실행 명령으로 확인하고, 통합 실행에서는 import가 쉬운 `main.py`, `solution.py`, `starter.py` 같은 파일명을 사용하는 것을 권장합니다.

### Lab 01 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-01_fastapi-health-check
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

확인:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

PowerShell에서 직접 확인:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

기대 결과:

```json
{
 "status": "ok"
}
```

### Path/Query Parameter 확인

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-02_memo-routing-and-search
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

확인:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/users/1
Invoke-RestMethod "http://127.0.0.1:8000/search?keyword=python&limit=5"
```

### Request Body 확인

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-03_memo-request-validation
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

Swagger UI에서 `POST /users`를 열고 다음 JSON을 입력합니다.

```json
{
 "name": "Alice",
 "email": "alice@example.com",
 "age": 25
}
```

확인할 것:

- 정상 요청은 200 응답을 반환한다.
- 필드를 누락하거나 타입을 틀리게 보내면 422 오류가 발생한다.

### Depends, Exception Handler, Middleware 확인

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
uvicorn dependency_injection_depends:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn dependency_injection_depends:app --reload
```

확인:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/me?token=student-token"
Invoke-RestMethod "http://127.0.0.1:8000/admin?token=student-token"
```

`Depends`는 여러 API에서 반복되는 인증, 설정 확인, DB 연결 준비 같은 공통 작업을 함수로 분리할 때 사용합니다.

전역 예외 처리 예제:

```powershell
uvicorn global_exception_handler:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn global_exception_handler:app --reload
```

확인:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/items/999
```

Middleware와 CORS 예제:

`02_middleware-cors.py`는 파일 상단의 실행 명령으로 서버를 실행해 `/health` 응답을 확인할 수 있습니다. 다만 CORS 효과는 브라우저에서 다른 origin의 프론트엔드가 FastAPI를 호출할 때 드러나므로, 이 단원에서는 설정 구조를 먼저 이해하고 실제 프론트엔드 연동은 `03_supabase-ai-frontend`에서 다시 확인합니다.

확인할 것:

- 모든 요청에 공통 처리를 끼워 넣는 구조가 Middleware입니다.
- 브라우저에서 다른 주소의 API를 호출할 때 CORS 설정이 필요합니다.

### Response Model 확인

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-04_memo-response-model
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

확인:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/users/1
```

확인할 것:

- 응답에 `id`, `name`만 포함된다.
- 내부 데이터의 `password`는 응답에서 제외된다.

### Async API 확인

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-05_async-external-context
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

확인:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/mock-external?keyword=fastapi"
```

### In Memory CRUD API 확인

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-06_memo-crud-review
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

Swagger UI에서 아래 순서로 확인합니다.

```text
GET /memos
POST /memos
GET /memos/{memo_id}
PUT /memos/{memo_id}
DELETE /memos/{memo_id}
```

이 실습은 Supabase 연결 전 단계입니다. 서버 메모리에 데이터를 저장하므로 서버를 재시작하면 데이터가 초기화됩니다.

### Mini API Server 확인

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-99_mini-memo-api-server
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

확인할 것:

```text
GET /health
GET /memos
GET /memos/search
GET /memos/{memo_id}
POST /memos
POST /ai/draft-response
```

이 실습은 FastAPI 단원의 마무리용 작은 API 서버입니다.

### Project Structure Refactor 확인

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-100_project-structure-refactor\solution
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

확인할 것:

```text
app/main.py에서 FastAPI 앱을 생성한다.
app/routers/memo_router.py에서 API 경로를 관리한다.
app/schemas/memo_schema.py에서 Pydantic 모델을 관리한다.
app/services/memo_service.py에서 메모 처리 로직을 관리한다.
tests/test_memo_api.py에서 TestClient 테스트를 실행한다.
```

테스트 실행:

```powershell
python -m pytest
```

이 실습은 `02_project-structure.md`에서 설명한 프로젝트 구조를 직접 만들어 보는 단계입니다.

## 실행 검증 체크리스트

- [ ] 가상환경이 활성화되어 있다.
- [ ] `pip install -r requirements.txt`를 실행했다.
- [ ] 서버 실행 위치가 `starter.py`, `solution.py`, `main.py`가 있는 폴더인지 확인했다.
- [ ] `uvicorn` 실행 시 오류가 없다.
- [ ] 브라우저에서 `/docs`가 열린다.
- [ ] `/health` 또는 실습 API가 정상 응답한다.
- [ ] Swagger UI에서 요청/응답을 확인했다.
- [ ] 잘못된 요청을 보냈을 때 422 또는 404 등 오류 응답을 확인했다.
- [ ] 서버 종료는 `Ctrl + C`로 한다는 것을 확인했다.

## API를 만들 때 확인할 기준

API를 구현한 뒤에는 [api-design-checklist.md](00_references/api-design-checklist.md)를 기준으로 확인합니다.

```text
1. URL이 명사 중심인가?
   예: /memos, /memos/{memo_id}

2. HTTP Method가 목적에 맞는가?
   조회는 GET, 생성은 POST, 수정은 PUT, 삭제는 DELETE를 사용합니다.

3. 요청 데이터 검증 모델이 있는가?
   Request Body를 받을 때는 Pydantic 모델을 사용합니다.

4. 응답 구조가 일관적인가?
   성공 응답과 오류 응답의 모양이 너무 제각각이면 프론트엔드에서 다루기 어렵습니다.

5. 민감정보가 응답에 포함되지 않는가?
   password, token, service role key 같은 값은 응답에 넣지 않습니다.
```

## Swagger UI 사용 순서

```text
1. 서버를 실행합니다.
2. 브라우저에서 http://127.0.0.1:8000/docs 로 접속합니다.
3. 테스트할 API를 클릭합니다.
4. Try it out 버튼을 누릅니다.
5. 필요한 Path, Query, Request Body 값을 입력합니다.
6. Execute 버튼을 누릅니다.
7. Status Code와 Response Body를 확인합니다.
```

Swagger UI에서 422가 나오면 요청 JSON이 Pydantic 모델과 맞지 않는 것입니다. 이때는 [common-errors.md](00_references/common-errors.md)를 함께 확인합니다.

## 자주 발생하는 문제

### `Error loading ASGI app`

실행한 파일명과 앱 변수명을 확인합니다.

```powershell
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

위 명령은 `solution.py` 파일 안에 `app = FastAPI()`가 있어야 동작합니다.

### 포트 8000이 이미 사용 중인 경우

기존 서버를 `Ctrl + C`로 종료하거나 다른 포트를 사용합니다.

```powershell
uvicorn solution:app --reload --port 8001
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload --port 8001
```

### 422 오류가 발생하는 경우

Pydantic 모델이 요구하는 JSON 형식과 실제 요청이 맞지 않는 상태입니다. Swagger UI의 Request body 예시와 모델 필드를 비교합니다.

### `ModuleNotFoundError: No module named 'fastapi'`

가상환경이 활성화되지 않았거나 패키지가 설치되지 않은 상태입니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 서버는 실행됐는데 브라우저가 열리지 않는 경우

서버 주소를 직접 입력합니다.

```text
http://127.0.0.1:8000/docs
```

포트를 바꿔 실행했다면 주소도 함께 바뀝니다.

```powershell
uvicorn solution:app --reload --port 8001
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload --port 8001
```

```text
http://127.0.0.1:8001/docs
```

## 이 단원에서 하지 않는 것

```text
Supabase 테이블 저장:
  이후 03_supabase-db-and-auth에서 진행합니다.

실제 LLM API 호출:
  이후 02_llm-api-integration에서 진행합니다.

Docker 실행:
  이 과정에서는 사용하지 않습니다. Docker 기반 운영은 C:\aidev\07_multi-agent-service-ops에서 다룹니다.

AWS 배포와 CI/CD:
  이 과정에서는 다루지 않고, 07_multi-agent-service-ops에서 진행합니다.
```

## 다음 단원 연결

이 단원 이후 `02_llm-api-integration`에서 FastAPI와 AI 모델 API 호출 구조를 연결합니다. 그 다음 `03_supabase-db-and-auth`에서 Supabase 테이블, Auth, RLS, 대화 이력, 서비스 로그 저장 구조를 FastAPI에 연결합니다.

Redis는 `03_supabase-db-and-auth`에서 Upstash Redis를 사용해 캐시와 TTL 개념을 먼저 다룹니다. Docker 기반 Redis 운영과 로컬 PostgreSQL 운영은 `C:\aidev\07_multi-agent-service-ops`에서 본격적으로 다룹니다.

