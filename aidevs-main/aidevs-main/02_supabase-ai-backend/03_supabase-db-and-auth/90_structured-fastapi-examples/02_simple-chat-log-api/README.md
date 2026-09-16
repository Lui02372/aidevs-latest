# 02. Simple Chat Log API

사용자 질문과 AI 답변을 `ex90_simple_chat_logs` 테이블에 저장하는 구조화 예제입니다.

본문의 `05_conversation-history-and-service-logs`를 FastAPI 프로젝트 구조로 나누어 봅니다.

## 실행 전 준비

1. Supabase SQL Editor에서 `schema.sql`을 실행합니다.
2. `.env.example`을 참고해 `.env`를 만듭니다.

```text
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash-lite
```

`SUPABASE_SERVICE_ROLE_KEY`는 실제 `/chat`, `/logs` API가 Supabase의 `ex90_simple_chat_logs` 테이블에 데이터를 저장하고 조회할 때 필요합니다. `GEMINI_API_KEY`는 `/chat`에서 답변을 생성할 때 필요합니다.

이 예제에는 `SUPABASE_ANON_KEY`를 사용하지 않습니다. 로그인한 사용자 권한으로 RLS를 확인하는 예제가 아니라, FastAPI 서버가 서버 권한으로 로그를 저장하는 구조이기 때문입니다. `SUPABASE_ANON_KEY`는 `04_auth-jwt-profile-api`, `05_integrated-ai-backend-api`처럼 사용자 JWT와 RLS 흐름을 확인할 때 사용합니다.

다만 아래의 기본 pytest는 Supabase를 실제로 호출하지 않고, FastAPI 앱과 라우트가 준비되었는지만 확인합니다.

```powershell
python -m pytest tests
```

그래서 `python -m pytest tests`만 실행할 때는 `SUPABASE_SERVICE_ROLE_KEY`가 없어도 통과할 수 있습니다. 반대로 Swagger에서 `POST /chat`, `GET /logs`를 실제로 호출하려면 `.env`에 `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`가 모두 있어야 합니다.

주의: `SUPABASE_SERVICE_ROLE_KEY`는 서버 전용 관리자 키입니다. README, GitHub, 제출 문서, 화면 캡처에 노출하지 않습니다. 노출된 경우 Supabase Dashboard에서 즉시 key를 재발급합니다.

## 서버 실행

```powershell
cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\02_simple-chat-log-api
..\..\..\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8012
```

Swagger UI:

```text
http://127.0.0.1:8012/docs
```

## 확인할 endpoint

| Method | URL | 설명 |
|---|---|---|
| GET | `/health` | 서버 상태 확인 |
| POST | `/chat` | Gemini AI 답변 생성 후 로그 저장 |
| GET | `/logs` | 최근 로그 조회 |

## 테스트

```powershell
python -m pytest tests
```

기본 테스트는 `tests/test_app_routes.py`만 실행합니다. `/chat`, `/logs`의 endpoint 흐름 테스트는 Codex와 함께 만들어 보는 선택 실습으로 둡니다.

참고 예시는 아래 파일에 있습니다.

```text
tests/reference_api_flow_example.py
```

이 파일 상단에는 Codex에게 보낼 수 있는 프롬프트 예시가 들어 있습니다. 실제로 실행하고 싶다면 아래처럼 복사합니다.

```powershell
Copy-Item .\tests\reference_api_flow_example.py .\tests\test_api_flow.py
python -m pytest tests
```
