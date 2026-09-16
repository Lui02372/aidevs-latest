# 04. Auth JWT Profile API

Supabase Auth, JWT, Bearer token, RLS SQL을 하나의 작은 profile 예제로 확인합니다.

본문 04에서는 RLS SQL을 필수로 다루지 않았습니다. 이 예제는 나중에 참고하는 심화 구조 예제입니다.

## 1. Supabase 설정

Supabase SQL Editor에서 `schema.sql`을 실행합니다.

```text
C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\04_auth-jwt-profile-api\schema.sql
```

이 SQL은 `ex90_profiles` 테이블을 만들고, 로그인한 사용자가 자기 profile만 읽고 수정할 수 있도록 RLS 정책을 설정합니다.

## 2. 환경변수 준비

```text
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
```

이 예제는 `SUPABASE_ANON_KEY`와 `SUPABASE_SERVICE_ROLE_KEY`를 모두 사용합니다.

| key | 이 예제에서의 역할 |
|---|---|
| `SUPABASE_ANON_KEY` | 로그인한 사용자의 JWT/RLS 흐름으로 profile 조회/수정을 확인할 때 사용합니다. |
| `SUPABASE_SERVICE_ROLE_KEY` | 서버 측 Supabase client 생성과 Auth 처리에 사용합니다. |

`SUPABASE_SERVICE_ROLE_KEY`는 RLS를 우회할 수 있는 서버 전용 관리자 key입니다. GitHub, README, 제출 문서, 화면 캡처에 노출하지 않습니다.

## 3. 서버 실행

```powershell
cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\04_auth-jwt-profile-api
..\..\..\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8014
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8014
```

Swagger UI:

```text
http://127.0.0.1:8014/docs
```

## 테스트 순서

1. `POST /auth/signup`으로 가입합니다.
2. Confirm email이 켜져 있으면 이메일 인증을 완료합니다.
3. `POST /auth/signin`으로 로그인합니다.
4. 응답의 `access_token`을 복사합니다.
5. Swagger `Authorize`에 token을 넣습니다.
6. `GET /me`로 현재 사용자를 확인합니다.
7. `PUT /profile`로 display name을 저장합니다.
8. `GET /profile`로 자기 profile만 조회되는지 확인합니다.

## RLS 핵심 문장

```sql
auth.uid() = id
```

이 조건은 “현재 로그인한 사용자의 id와 profile 행의 id가 같을 때만 허용한다”는 뜻입니다.

## pytest 기본 테스트

```powershell
python -m pytest tests
```

기본 테스트는 `tests/test_app_routes.py`만 실행합니다. 실제 Supabase Auth와 RLS 테이블을 호출하지 않고 `/auth/signup`, `/auth/signin`, `/me`, `/profile` 흐름을 검증하는 테스트는 Codex와 함께 만들어 보는 선택 실습으로 둡니다.

참고 예시는 아래 파일에 있습니다.

```text
tests/reference_api_flow_example.py
```

이 파일 상단에는 Codex에게 보낼 수 있는 프롬프트 예시가 들어 있습니다. 실제로 실행하고 싶다면 아래처럼 복사합니다.

```powershell
Copy-Item .\tests\reference_api_flow_example.py .\tests\test_api_flow.py
python -m pytest tests
```
