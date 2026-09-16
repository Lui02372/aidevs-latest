# 90. Structured FastAPI Examples

이 폴더는 `03_supabase-db-and-auth`의 `00`~`06`을 마친 뒤 참고하는 구조화 예제 모음입니다.

본문에서는 개념과 최소 실행 흐름을 작게 배웠습니다. 이 폴더에서는 같은 내용을 실제 프로젝트에 가까운 FastAPI 구조로 나누어 봅니다.

처음 학습할 때 반드시 모두 실행해야 하는 필수 실습은 아닙니다. 나중에 프로젝트를 만들 때 “폴더를 어떻게 나누면 좋을까?”를 다시 확인하는 참고 자료로 사용합니다.

## 예제 목록

| 순서 | 예제 | 연결 내용 |
|---|---|---|
| 1 | `01_notes-api-with-supabase` | Supabase 테이블 CRUD를 FastAPI 구조로 분리 |
| 2 | `02_simple-chat-log-api` | 질문/답변 로그를 Supabase에 저장 |
| 3 | `03_cached-ai-answer-api` | Upstash Redis TTL 캐시 |
| 4 | `04_auth-jwt-profile-api` | Supabase Auth, JWT, Bearer token, RLS SQL |
| 5 | `05_integrated-ai-backend-api` | Auth, DB 저장, Redis 캐시, Gemini 선택 호출을 하나로 연결 |

## 공통 구조

각 예제는 최대한 같은 구조를 사용합니다.

```text
example-name
├─ README.md
├─ .env.example
├─ schema.sql
├─ app
│  ├─ main.py
│  ├─ core
│  ├─ routers
│  ├─ schemas
│  └─ services
└─ tests
```

`schema.sql`이 없는 예제는 Supabase 테이블 없이 Redis만 사용합니다.

## 테스트 기준

각 예제의 기본 테스트는 `tests/test_app_routes.py`입니다.

```powershell
python -m pytest tests
```

기본 테스트는 아래 내용을 확인합니다.

- FastAPI 앱이 정상 import되는가?
- `/health`가 응답하는가?
- Swagger/OpenAPI 문서에 핵심 endpoint가 등록되어 있는가?

`tests/reference_api_flow_example.py`는 필수 실행 테스트가 아니라 **바이브 코딩 참고 예시**입니다. 수강생이 Codex에게 endpoint 흐름 테스트 생성을 요청할 때 어떤 프롬프트를 던지면 좋은지, 생성된 테스트가 어떤 모양이면 좋은지 보여 주는 파일입니다.

실제로 실행해 보고 싶다면 해당 파일을 `tests/test_api_flow.py`로 복사한 뒤 실행합니다.

```powershell
Copy-Item .\tests\reference_api_flow_example.py .\tests\test_api_flow.py
python -m pytest tests
```

수업 중에는 `test_app_routes.py`만 이해해도 충분합니다. `reference_api_flow_example.py`는 빠른 수강생이나 최종 프로젝트 테스트를 강화하고 싶은 수강생을 위한 참고 자료입니다.

## 테이블 이름 기준

90번 예제는 본문 실습 데이터와 섞이지 않도록 `ex90_` prefix를 사용합니다.

```text
ex90_notes
ex90_simple_chat_logs
ex90_profiles
ex90_user_chat_logs
```

## 실행 전 공통 준비

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

각 예제 폴더의 `.env.example`을 참고해 `.env`를 만듭니다. 실제 key 값은 GitHub, README, 제출 문서에 올리지 않습니다.

## Supabase key 사용 기준

| key | 사용하는 경우 | 주의 |
|---|---|---|
| `SUPABASE_ANON_KEY` | 로그인한 사용자 JWT/RLS 흐름을 확인할 때 사용합니다. | 브라우저에서 사용할 수 있는 공개용 key지만, 그래도 문서와 화면 캡처에는 실제 값을 쓰지 않습니다. |
| `SUPABASE_SERVICE_ROLE_KEY` | FastAPI 백엔드가 서버 권한으로 DB에 저장/조회할 때 사용합니다. | RLS를 우회할 수 있는 서버 전용 관리자 key입니다. 절대 GitHub, README, 캡처 화면에 노출하지 않습니다. |

예제별 기준:

| 예제 | 필요한 key |
|---|---|
| `01_notes-api-with-supabase` | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` |
| `02_simple-chat-log-api` | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` |
| `03_cached-ai-answer-api` | Supabase key 필요 없음 |
| `04_auth-jwt-profile-api` | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` |
| `05_integrated-ai-backend-api` | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, Redis/Gemini 설정 |

## 학습 기준

이 폴더에서 가장 중요한 것은 기능의 양이 아니라 코드의 위치입니다.

```text
main.py:
  FastAPI 앱 생성과 router 연결

routers:
  URL, HTTP Method, status code

schemas:
  요청/응답 Pydantic 모델

services:
  Supabase, Redis, Auth 같은 외부 서비스 호출

core:
  환경변수와 공통 설정
```

처음에는 `01`부터 순서대로 보는 것을 권장합니다.

`05_integrated-ai-backend-api`는 Redis 캐시가 없을 때 Gemini SDK를 호출합니다. `.env`에 `GEMINI_API_KEY`를 설정하면 실제 Gemini 답변 생성 흐름을 확인할 수 있습니다.
