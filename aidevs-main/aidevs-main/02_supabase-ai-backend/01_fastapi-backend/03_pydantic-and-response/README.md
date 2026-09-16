# 03_pydantic-and-response

이 단원에서는 FastAPI에서 **요청 데이터 검증**과 **응답 데이터 설계**를 다룹니다.

앞 단원인 `02_routing-and-request`에서는 URL, HTTP Method, Path Parameter, Query Parameter, Request Body의 위치를 배웠습니다. 이번 단원에서는 같은 메모 API를 이어서 사용하되, “클라이언트가 어떤 JSON을 보내야 하는지”, “서버가 어떤 JSON을 돌려주어야 하는지”를 더 명확하게 정합니다.

## 핵심 요약

```text
Pydantic Model
  API가 주고받는 데이터의 필드, 타입, 검증 조건을 정의합니다.

Request Validation
  잘못된 요청이 들어오면 FastAPI가 자동으로 422 오류를 반환합니다.

Response Model
  API가 외부로 내보낼 응답 데이터의 모양을 제한합니다.

Standard Response
  여러 API의 응답 모양을 success, message, data 같은 구조로 통일합니다.
```

## 폴더 파일

| 파일 | 역할 |
| --- | --- |
| `main.py` | 실제로 실행하는 통합 FastAPI 예제 |
| `01_pydantic-models.py` | Pydantic 모델 기본 개념 예제 |
| `02_request-validation.py` | 요청 데이터 검증 예제 |
| `03_response-model.py` | 응답 모델과 내부 값 숨김 예제 |
| `04_standard-response.py` | 표준 응답 구조 예제 |

번호가 붙은 파일은 개념을 나누어 읽기 위한 학습용 파일입니다. 실제 서버 실행은 `main.py` 기준으로 진행합니다.

## 실행 준비

가상환경은 `02_supabase-ai-backend` 폴더 아래의 `.venv`를 사용합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

서버를 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\03_pydantic-and-response
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

브라우저에서 Swagger UI를 엽니다.

```text
http://127.0.0.1:8000/docs
```

서버를 종료할 때는 터미널에서 `Ctrl + C`를 누릅니다.

## 1. 서버 상태 확인

Swagger UI에서 `GET /health`를 실행합니다.

예상 응답:

```json
{
  "status": "ok"
}
```

이 응답이 나오면 FastAPI 서버가 정상적으로 실행 중입니다.

## 2. Pydantic 요청 모델 확인

`POST /memos`는 새 메모를 만드는 API입니다.

요청 Body 예시:

```json
{
  "title": "FastAPI 복습",
  "content": "오늘 배운 Path Parameter와 Query Parameter를 정리합니다.",
  "tags": ["fastapi", "backend"]
}
```

이 요청은 `main.py`의 `MemoCreate` 모델을 기준으로 검증됩니다.

```python
class MemoCreate(BaseModel):
    title: str
    content: str
    tags: list[str]
```

실제 코드에는 `Field()`를 사용해서 제목 길이, 본문 길이, 태그 개수 조건을 더 자세히 걸어 두었습니다.

## 3. 422 Validation Error 확인

이번에는 일부러 잘못된 요청을 보내 봅니다.

```json
{
  "title": "",
  "content": "",
  "tags": ["a", "b", "c", "d", "e", "f"]
}
```

확인할 점:

```text
title:
  빈 문자열이면 안 됩니다.

content:
  빈 문자열이면 안 됩니다.

tags:
  최대 5개까지만 허용합니다.
```

FastAPI는 Pydantic 모델의 조건을 보고 엔드포인트 함수가 실행되기 전에 요청을 검사합니다. 조건을 만족하지 않으면 자동으로 `422 Unprocessable Entity` 응답을 반환합니다.

## 4. Response Model 확인

`GET /memos/1`을 실행합니다.

예상 응답:

```json
{
  "id": 1,
  "title": "FastAPI 시작",
  "content": "GET, POST, PUT, DELETE의 차이를 정리합니다.",
  "tags": ["fastapi", "api"]
}
```

서버 내부 데이터에는 `internal_note`라는 관리용 값이 들어 있습니다. 하지만 API 응답에는 보이지 않습니다.

이유는 엔드포인트에 `response_model=MemoPublic`이 지정되어 있기 때문입니다.

```python
@app.get("/memos/{memo_id}", response_model=MemoPublic)
def get_memo(memo_id: int):
    ...
```

`MemoPublic`에 정의된 필드만 응답으로 나가므로 내부 관리 값, 비밀번호, 토큰 같은 민감한 값을 실수로 노출하는 위험을 줄일 수 있습니다.

## 5. 표준 응답 구조 확인

`GET /memos`를 실행합니다.

예상 응답:

```json
{
  "success": true,
  "message": "memos loaded",
  "data": [
    {
      "id": 1,
      "title": "FastAPI 시작",
      "content": "GET, POST, PUT, DELETE의 차이를 정리합니다.",
      "tags": ["fastapi", "api"]
    }
  ]
}
```

이 구조를 사용하면 프론트엔드에서 응답을 처리하기 쉬워집니다.

```text
success:
  요청 성공 여부를 판단합니다.

message:
  화면에 보여줄 안내 문구나 개발자가 확인할 메시지를 담습니다.

data:
  실제 화면에 표시하거나 저장할 데이터를 담습니다.
```

데이터가 없는 경우에도 같은 구조를 유지합니다.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/empty
```

예상 응답:

```json
{
  "success": true,
  "message": "no data yet",
  "data": null
}
```

## 6. PowerShell로 직접 호출하기

Swagger UI 외에도 PowerShell에서 API를 호출할 수 있습니다.

메모 목록 조회:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/memos
```

메모 1개 조회:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/memos/1
```

새 메모 생성:

```powershell
$body = @{
    title = "Pydantic 정리"
    content = "요청 모델과 응답 모델을 분리해서 API를 안전하게 설계합니다."
    tags = @("pydantic", "response")
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:8000/memos `
    -ContentType "application/json" `
    -Body $body
```

## Pydantic Field 조건 정리

| 조건 | 의미 | 예시 |
| --- | --- | --- |
| `min_length` | 문자열 또는 목록의 최소 길이 | `Field(min_length=1)` |
| `max_length` | 문자열 또는 목록의 최대 길이 | `Field(max_length=50)` |
| `examples` | Swagger UI에 보여줄 예시 값 | `examples=["FastAPI 복습"]` |
| `description` | Swagger UI에 표시되는 필드 설명 | `description="메모 제목입니다."` |

## 요청 모델과 응답 모델을 나누는 이유

```text
요청 모델:
  클라이언트가 서버로 보내는 데이터의 모양을 검증합니다.

응답 모델:
  서버가 클라이언트에게 돌려주는 데이터의 모양을 제한합니다.

분리하는 이유:
  요청에는 필요하지만 응답에는 숨겨야 하는 값이 있을 수 있습니다.
  예를 들어 password, token, internal_note, service_role_key 같은 값은 응답에 포함되면 안 됩니다.
```

## 이후 과정과의 연결

```text
02_llm-api-integration:
  사용자 질문 Request Body를 검증하고 AI 응답 구조를 표준화합니다.

03_supabase-db-and-auth:
  Supabase 테이블에 저장할 데이터와 API 응답 데이터를 구분합니다.

03_supabase-ai-frontend:
  Streamlit 화면에서 success, message, data 구조를 기준으로 응답을 처리합니다.

04_supabase-ai-mini-project:
  백엔드, DB, UI를 연결할 때 API 설계 문서와 응답 구조를 산출물로 정리합니다.
```

## 확인 질문

```text
1. Pydantic 모델은 왜 필요한가요?
2. 422 오류는 언제 발생하나요?
3. response_model은 어떤 값을 보호하는 데 도움이 되나요?
4. 요청 모델과 응답 모델을 나누는 이유는 무엇인가요?
5. success, message, data 구조를 쓰면 프론트엔드에서 어떤 점이 좋아지나요?
```
