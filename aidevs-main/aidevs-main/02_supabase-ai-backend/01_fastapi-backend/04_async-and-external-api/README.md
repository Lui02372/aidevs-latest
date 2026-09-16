# 04_async-and-external-api

이 단원에서는 FastAPI에서 **비동기 처리(async/await)** 와 **외부 API 연동**을 학습합니다.

앞 단원까지는 메모 API의 라우팅, 요청 데이터 검증, 응답 모델을 만들었습니다. 이번 단원에서는 서버가 오래 걸리는 작업을 기다리는 방법과, 우리 서버 밖에 있는 공개 API 데이터를 가져와 메모 API 흐름에 연결하는 방법을 연습합니다.

## 핵심 요약

```text
async def
  오래 걸릴 수 있는 작업을 기다리는 동안 서버가 다른 일을 처리할 수 있게 하는 함수 형태입니다.

await
  비동기 작업이 끝날 때까지 기다리되, 서버 전체를 멈추지 않도록 해 줍니다.

External API
  우리가 만든 서버 밖에 있는 다른 서비스의 API입니다.

httpx.AsyncClient
  FastAPI의 async 함수 안에서 외부 API를 비동기로 호출할 때 자주 사용하는 도구입니다.

StreamingResponse
  응답을 한 번에 보내지 않고 조금씩 나누어 보내는 방식입니다.
```

## 폴더 파일

| 파일 | 역할 |
| --- | --- |
| `main.py` | 실제로 실행하는 통합 FastAPI 예제 |
| `01_async-endpoint.py` | `async def`, `await`, `asyncio.gather` 개념 예제 |
| `02_external-api-structure.py` | 외부 API 호출과 오류 처리 구조 예제 |
| `03_ai-api-call-placeholder.py` | 실제 LLM API 전 placeholder 호출 흐름 예제 |
| `04_streaming-response.py` | `StreamingResponse` 기초 예제 |

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
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\04_async-and-external-api
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

## 2. async/await 흐름 확인

`GET /async/wait`를 실행합니다.

쿼리 파라미터 예시:

```text
seconds = 2
```

예상 응답:

```json
{
  "success": true,
  "message": "async wait finished",
  "data": {
    "waited_seconds": 2
  }
}
```

중요한 점은 “기다리는 작업이 있다”는 것입니다. 실제 서비스에서는 외부 API 호출, 데이터베이스 조회, 파일 업로드, AI 모델 호출처럼 시간이 걸리는 작업이 자주 생깁니다.

FastAPI의 async 함수 안에서는 아래처럼 `await`를 사용합니다.

```python
await asyncio.sleep(seconds)
```

`time.sleep()`은 서버의 이벤트 루프를 막을 수 있으므로, async 함수 안에서는 `asyncio.sleep()`처럼 await 가능한 함수를 사용합니다.

## 3. 여러 비동기 작업을 동시에 기다리기

`GET /async/parallel`을 실행합니다.

이 API는 아래 세 작업을 동시에 기다립니다.

```text
memo          1초
external_post 2초
usage_log     1초
```

순서대로 기다리면 약 4초가 걸리지만, `asyncio.gather()`로 동시에 기다리면 가장 오래 걸리는 작업 기준인 약 2초에 끝납니다.

```python
results = await asyncio.gather(
    fetch_mock_data("memo", 1),
    fetch_mock_data("external_post", 2),
    fetch_mock_data("usage_log", 1),
)
```

이 구조는 이후 외부 API, Supabase, LLM 호출을 함께 처리할 때 중요합니다.

## 4. 외부 API 호출 확인

`GET /external/posts/{post_id}`를 실행합니다.

예시:

```text
post_id = 1
```

이 API는 로그인이 필요 없는 공개 테스트 API인 JSONPlaceholder에서 게시글 데이터를 가져옵니다.

응답에는 두 가지 데이터가 들어 있습니다.

```text
raw:
  외부 API가 보내준 원본 데이터입니다.

parsed:
  우리 서비스에서 필요한 형태로 일부만 가공한 데이터입니다.
```

예상 응답 구조:

```json
{
  "success": true,
  "message": "external post loaded",
  "data": {
    "raw": {
      "userId": 1,
      "id": 1,
      "title": "...",
      "body": "..."
    },
    "parsed": {
      "id": 1,
      "title": "...",
      "body_preview": "..."
    }
  }
}
```

초보 단계에서는 원본 데이터를 함께 보는 것이 좋습니다. 그래야 외부 API가 실제로 어떤 JSON을 보내는지 확인하고, 그중 필요한 값을 어떻게 골라 쓰는지 이해할 수 있습니다.

## 5. 메모와 외부 데이터 연결

`GET /memos/{memo_id}/external-context`를 실행합니다.

예시:

```text
memo_id = 1
post_id = 1
```

이 API는 내부 메모 데이터와 외부 API 데이터를 하나의 응답으로 묶습니다.

```json
{
  "success": true,
  "message": "memo enriched with external context",
  "data": {
    "memo": {
      "id": 1,
      "title": "비동기 처리 복습",
      "content": "...",
      "tags": ["async", "external-api"]
    },
    "external_context": {
      "source": "jsonplaceholder",
      "post_id": 1,
      "title": "...",
      "body_preview": "..."
    }
  }
}
```

이 구조는 이후 과정과 직접 연결됩니다.

```text
02_llm-api-integration:
  사용자 질문과 외부 데이터를 함께 LLM에 전달합니다.

03_supabase-db-and-auth:
  외부 API에서 가져온 결과나 사용자 요청 기록을 Supabase에 저장합니다.

04_supabase-ai-mini-project:
  로그, 대화 이력, 사용자 피드백을 연결한 통합 서비스를 만듭니다.
```

## 6. AI API placeholder 흐름 확인

`POST /ai/draft-response`를 실행합니다.

요청 Body:

```json
{
  "question": "FastAPI에서 async def를 언제 사용하나요?",
  "tone": "friendly"
}
```

이 API는 실제 Gemini 또는 OpenAI API를 호출하지 않습니다. 다음 단원에서 실제 LLM API를 배우기 전에, 요청 검증과 비동기 호출 흐름을 먼저 익히기 위한 예제입니다.

예상 응답:

```json
{
  "success": true,
  "message": "draft response generated",
  "data": {
    "question": "FastAPI에서 async def를 언제 사용하나요?",
    "answer": "[friendly] 'FastAPI에서 async def를 언제 사용하나요?'에 대한 샘플 답변입니다. 실제 LLM API 호출은 다음 단원에서 연결합니다."
  }
}
```

## 7. 기본 스트리밍 확인

`GET /stream`을 실행합니다.

이 API는 텍스트를 한 번에 보내지 않고 단어 단위로 조금씩 보냅니다.

```text
FastAPI async external API streaming
```

이번 단원에서는 스트리밍의 개념만 확인합니다. **Server-Sent Events(SSE) 기반 AI 응답 스트리밍**은 `04_supabase-ai-mini-project`에서 백엔드, 프론트엔드, Supabase 저장 흐름과 함께 통합 실습으로 다룹니다.

## 외부 API 오류 처리 흐름

외부 API는 항상 성공하지 않습니다.

```text
1. 네트워크가 끊길 수 있습니다.
2. 외부 서비스가 느릴 수 있습니다.
3. 존재하지 않는 데이터 ID를 요청할 수 있습니다.
4. 외부 서비스가 4xx 또는 5xx 오류를 줄 수 있습니다.
```

그래서 `main.py`의 `fetch_jsonplaceholder_post()` 함수에서는 아래 두 오류를 구분합니다.

```text
httpx.HTTPStatusError:
  외부 API가 404, 500 같은 HTTP 오류 응답을 준 경우입니다.

httpx.RequestError:
  네트워크 연결 실패, 타임아웃처럼 요청 자체가 실패한 경우입니다.
```

이렇게 외부 오류를 우리 API의 `HTTPException`으로 바꾸면, 프론트엔드는 더 일관된 방식으로 오류를 처리할 수 있습니다.

## PowerShell로 직접 호출하기

비동기 대기:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/async/wait?seconds=1"
```

외부 API 조회:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/external/posts/1
```

메모와 외부 데이터 연결:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/memos/1/external-context?post_id=1"
```

AI placeholder 호출:

```powershell
$body = @{
    question = "FastAPI에서 async def를 언제 사용하나요?"
    tone = "friendly"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:8000/ai/draft-response `
    -ContentType "application/json" `
    -Body $body
```

## 이번 단원에서 하지 않는 것

```text
실제 Gemini API 호출:
  02_llm-api-integration에서 진행합니다.

Supabase 저장:
  03_supabase-db-and-auth에서 진행합니다.

SSE 기반 AI 응답 스트리밍 통합:
  04_supabase-ai-mini-project에서 진행합니다.

Docker 실행:
  05_llm-agent-orchestration부터 Docker Desktop 기반으로 시작하고,
  Docker Compose와 AWS 배포는 07_multi-agent-service-ops에서 다룹니다.
```

## 확인 질문

```text
1. async def와 일반 def의 차이는 무엇인가요?
2. await는 어떤 작업 앞에 붙이나요?
3. 외부 API 원본 데이터(raw)와 가공 데이터(parsed)를 함께 보면 어떤 점이 좋나요?
4. 외부 API 호출 실패를 HTTPException으로 바꾸는 이유는 무엇인가요?
5. 기본 스트리밍과 SSE 기반 AI 응답 스트리밍은 왜 다른 단계에서 다루나요?
```
