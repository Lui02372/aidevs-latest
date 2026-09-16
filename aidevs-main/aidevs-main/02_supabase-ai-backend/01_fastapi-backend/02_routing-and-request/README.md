# 02_routing-and-request

라우팅과 요청 데이터 처리 방식을 학습합니다.

`01_fastapi-project-setup`에서 서버 실행과 `/health` 확인을 배웠다면, 이번 단원에서는 **메모 관리 API 하나**를 기준으로 HTTP Method, Path Parameter, Query Parameter, Request Body를 연결해서 배웁니다.

## 이 단원에서 배우는 것

```text
HTTP Method:
  GET, POST, PUT, DELETE처럼 요청의 목적을 나타냅니다.

Route:
  /memos, /memos/{memo_id}, /memos/search 같은 API 주소입니다.

Path Parameter:
  URL 경로 안에 들어가는 값입니다. 예: /memos/1

Query Parameter:
  URL의 ? 뒤에 붙는 검색 조건입니다. 예: /memos/search?keyword=fastapi&limit=5

Request Body:
  POST나 PUT 요청에서 서버로 보내는 JSON 데이터입니다.
```

## 이 폴더의 파일

| 파일 | 역할 |
| --- | --- |
| `main.py` | 실제로 실행하는 메모 API 예제 |
| `01_http-methods.py` | GET/POST/PUT/DELETE 개념 학습용 |
| `02_path-parameters.py` | Path Parameter 개념 학습용 |
| `03_query-parameters.py` | Query Parameter 개념 학습용 |
| `04_request-body.py` | Request Body 개념 학습용 |

번호가 붙은 파일은 개념을 나누어 읽기 위한 파일입니다. 실제 서버 실행은 `main.py` 기준으로 진행합니다.

## 실행 전 준비

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 서버 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\02_routing-and-request
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

서버 종료:

```text
Ctrl + C
```

## 메모 API 구조

| Method | URL | 요청 데이터 | 의미 |
| --- | --- | --- | --- |
| GET | `/memos` | 없음 | 전체 메모 조회 |
| GET | `/memos/{memo_id}` | Path Parameter | 메모 한 건 조회 |
| GET | `/memos/search?keyword=fastapi&limit=5` | Query Parameter | 메모 검색 |
| POST | `/memos` | Request Body | 새 메모 생성 |
| PUT | `/memos/{memo_id}` | Path Parameter + Request Body | 기존 메모 수정 |
| DELETE | `/memos/{memo_id}` | Path Parameter | 기존 메모 삭제 |

## 1. 전체 메모 조회

```powershell
Invoke-RestMethod http://127.0.0.1:8000/memos
```

브라우저에서도 확인할 수 있습니다.

```text
http://127.0.0.1:8000/memos
```

## 2. Path Parameter로 메모 한 건 조회

```powershell
Invoke-RestMethod http://127.0.0.1:8000/memos/1
```

`/memos/{memo_id}`에서 `{memo_id}` 부분이 Path Parameter입니다. FastAPI는 URL의 `1`을 함수 인자 `memo_id`에 넣어 줍니다.

없는 메모를 요청하면 404 오류를 확인할 수 있습니다.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/memos/999
```

## 3. Query Parameter로 메모 검색

검색 조건을 URL 뒤에 붙입니다.

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/memos/search?keyword=FastAPI&limit=5"
```

`?keyword=FastAPI&limit=5` 부분이 Query Parameter입니다.

```text
keyword=FastAPI
limit=5
```

처럼 key=value 형태로 전달됩니다.

## 4. POST Request Body로 메모 생성

POST 요청은 Swagger UI에서 테스트하는 것이 가장 쉽습니다.

```text
http://127.0.0.1:8000/docs
-> POST /memos
-> Try it out
-> Request body 입력
-> Execute
```

입력 예시:

```json
{
  "title": "라우팅 실습",
  "content": "POST 요청으로 메모를 생성했습니다."
}
```

PowerShell로도 요청할 수 있습니다.

```powershell
$body = @{
  title = "라우팅 실습"
  content = "POST 요청으로 메모를 생성했습니다."
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/memos" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## 5. PUT으로 메모 수정

기존 메모를 수정합니다.

```powershell
$body = @{
  title = "수정된 메모"
  content = "PUT 요청으로 전체 내용을 수정했습니다."
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/memos/1" `
  -Method Put `
  -ContentType "application/json" `
  -Body $body
```

## 6. DELETE로 메모 삭제

기존 메모를 삭제합니다.

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/memos/1" `
  -Method Delete
```

## Path, Query, Body 차이

| 구분 | 위치 | 예시 | 주로 쓰는 상황 |
| --- | --- | --- | --- |
| Path Parameter | URL 경로 | `/memos/1` | 특정 데이터 하나를 지정 |
| Query Parameter | `?` 뒤 | `/memos/search?keyword=FastAPI` | 검색, 필터, 정렬, 페이지 |
| Request Body | JSON 본문 | `{ "title": "메모" }` | 생성, 수정할 데이터 전달 |

## 확인할 오류

```text
404:
  없는 메모를 요청할 때 발생합니다.

422:
  Request Body의 필수 필드가 빠지거나 타입이 맞지 않을 때 발생합니다.
```

Swagger UI에서 일부러 잘못된 JSON을 보내면 Pydantic 검증 오류를 확인할 수 있습니다.

## 이후 과정과 연결

```text
이번 단원:
  메모 데이터를 서버 메모리에 임시 저장합니다.

이후 Supabase 단원:
  같은 CRUD 흐름을 Supabase 테이블 저장으로 바꿉니다.

이후 LLM API 단원:
  Request Body로 받은 질문을 AI 모델 API 호출에 사용합니다.
```

## 확인 질문

```text
1. GET과 POST는 어떤 차이가 있나요?
2. /memos/1에서 1은 어떤 종류의 요청 데이터인가요?
3. /memos/search?keyword=FastAPI에서 keyword는 어떤 종류의 요청 데이터인가요?
4. Request Body는 주로 어떤 Method에서 사용하나요?
5. 404 오류와 422 오류는 각각 언제 발생하나요?
```
