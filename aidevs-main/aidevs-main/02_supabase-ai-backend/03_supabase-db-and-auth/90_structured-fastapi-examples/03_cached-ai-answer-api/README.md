# 03. Cached AI Answer API

Gemini AI 답변을 Upstash Redis에 TTL로 캐시하는 구조화 예제입니다.

이 예제는 Supabase 테이블을 사용하지 않습니다. 따라서 `schema.sql`이 없습니다.

## 실행 전 준비

`.env.example`을 참고해 같은 폴더에 `.env`를 만듭니다.

이 예제는 Supabase를 사용하지 않습니다. 따라서 아래 값은 필요 없습니다.

```text
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
```

필요한 값은 Upstash Redis 설정입니다.

```text
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash-lite
```

`UPSTASH_REDIS_REST_TOKEN`, `GEMINI_API_KEY`는 외부에 노출하지 않습니다.

## 서버 실행

```powershell
cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\03_cached-ai-answer-api
..\..\..\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8013
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8013
```

Swagger UI:

```text
http://127.0.0.1:8013/docs
```

## 확인할 endpoint

| Method | URL | 설명 |
|---|---|---|
| GET | `/health` | 서버와 Redis 환경변수 상태 확인 |
| GET | `/ai/answer` | Gemini 질문 답변을 Redis에 캐시 |
| DELETE | `/ai/answer-cache` | 질문 캐시 삭제 |

## 테스트 흐름

1. 같은 질문으로 `/ai/answer`를 두 번 호출합니다.
2. 첫 번째는 `cached: false`입니다.
3. 두 번째는 `cached: true`입니다.
4. `/ai/answer-cache`로 삭제 후 다시 호출하면 `cached: false`입니다.

## pytest 기본 테스트

```powershell
python -m pytest tests
```

기본 테스트는 `tests/test_app_routes.py`만 실행합니다. 실제 Redis를 호출하지 않고 endpoint 흐름을 검증하는 테스트는 Codex와 함께 만들어 보는 선택 실습으로 둡니다.

참고 예시는 아래 파일에 있습니다.

```text
tests/reference_api_flow_example.py
```

이 파일 상단에는 Codex에게 보낼 수 있는 프롬프트 예시가 들어 있습니다. 실제로 실행하고 싶다면 아래처럼 복사합니다.

```powershell
Copy-Item .\tests\reference_api_flow_example.py .\tests\test_api_flow.py
python -m pytest tests
```
