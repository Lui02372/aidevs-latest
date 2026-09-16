# 05. Integrated AI Backend API

Auth, Supabase DB 저장, Upstash Redis TTL 캐시, Gemini 호출을 하나로 연결한 통합 참고 예제입니다.

이 예제는 완성 서비스가 아니라, `01`~`04`에서 배운 구조가 한 요청 흐름 안에서 어떻게 연결되는지 보여주는 작은 예제입니다.

Redis 캐시가 없을 때 Gemini SDK로 실제 답변을 생성합니다.

## 1. Supabase 테이블 만들기

Supabase SQL Editor에서 `schema.sql`을 실행합니다.

```text
C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\05_integrated-ai-backend-api\schema.sql
```

## 2. 환경변수 준비

`.env.example`을 참고해 같은 폴더에 `.env`를 만듭니다.

```text
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash-lite
```

이 예제는 `SUPABASE_ANON_KEY`와 `SUPABASE_SERVICE_ROLE_KEY`를 모두 사용합니다.

| key | 이 예제에서의 역할 |
|---|---|
| `SUPABASE_ANON_KEY` | 로그인한 사용자의 JWT/RLS 흐름으로 `/logs` 같은 사용자별 조회를 확인할 때 사용합니다. |
| `SUPABASE_SERVICE_ROLE_KEY` | 서버가 채팅 로그를 저장하는 흐름에 사용합니다. |
| `UPSTASH_REDIS_REST_TOKEN` | 같은 질문의 답변을 Redis에 TTL 캐시할 때 사용합니다. |
| `GEMINI_API_KEY` | Gemini SDK 호출에 사용합니다. |

`SUPABASE_SERVICE_ROLE_KEY`, Redis token, Gemini API key는 외부에 노출하지 않습니다.

## 3. 서버 실행

```powershell
cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\05_integrated-ai-backend-api
..\..\..\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8015
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8015
```

Swagger UI:

```text
http://127.0.0.1:8015/docs
```

## 테스트 순서

1. `POST /auth/signup`
2. `POST /auth/signin`
3. 응답의 `access_token`을 복사
4. Swagger 오른쪽 위 `Authorize` 클릭
5. `Value`에 access token만 붙여 넣고 Authorize 클릭
   - `Bearer `를 직접 붙이지 않아도 됩니다.
   - Swagger가 이후 요청에 `Authorization: Bearer <access_token>` 헤더를 자동으로 붙입니다.
6. `GET /me`
7. `POST /chat`
8. 같은 질문으로 `POST /chat` 다시 실행
9. `GET /logs`

`/me`, `/chat`, `/logs`에서 token을 매번 입력하는 칸이 보인다면 인증 구현이 `Header` 직접 입력 방식으로 되어 있는 것입니다.
이 예제는 `HTTPBearer`를 사용하므로 Swagger `Authorize`에 한 번만 입력하면 됩니다.

이전 단계 요약:

```text
POST /auth/signin
-> access_token 복사
-> Swagger Authorize에 token 입력
-> /me, /chat, /logs 호출
```

두 번째 `POST /chat`에서는 Redis 캐시가 있으면 `cached: true`가 됩니다.

## token과 RLS 흐름 자세히 보기

이 예제에서 가장 중요한 흐름은 다음 3가지입니다.

1. Supabase Auth가 로그인 token을 발급합니다.
2. FastAPI는 token을 받아 현재 사용자를 확인합니다.
3. Supabase RLS는 사용자 token으로 DB를 조회할 때 사용자별 접근을 제한합니다.

초보 단계에서는 "token을 어디서 받고, 어디에 넣고, DB 권한은 언제 확인되는가"가 가장 헷갈립니다.
아래 순서대로 보면 됩니다.

### 1. 회원가입: 아직 token 흐름의 시작은 아닙니다

Swagger에서 `POST /auth/signup`을 호출하면 FastAPI는 Supabase Auth에 회원가입 요청을 보냅니다.

```text
Swagger
-> FastAPI POST /auth/signup
-> Supabase Auth sign_up
-> auth.users에 사용자 생성
-> 사용자 id/email 반환
```

이 단계의 목적은 Supabase Auth에 사용자를 만드는 것입니다.
Supabase 프로젝트 설정에서 Confirm email이 켜져 있으면 이메일 인증을 완료해야 로그인할 수 있습니다.

회원가입 응답에 사용자 정보가 보일 수 있지만, 이후 보호 API를 호출할 때 사용할 핵심 값은 보통 로그인 단계에서 받는 `access_token`입니다.

### 2. 로그인: Supabase가 access_token을 발급합니다

Swagger에서 `POST /auth/signin`을 호출하면 FastAPI는 Supabase Auth에 이메일/비밀번호 로그인을 요청합니다.

```text
Swagger
-> FastAPI POST /auth/signin
-> Supabase Auth sign_in_with_password
-> 이메일/비밀번호 확인
-> access_token 발급
-> FastAPI가 access_token을 응답으로 반환
```

응답 예시는 이런 형태입니다.

```json
{
  "user": {
    "id": "사용자 uuid",
    "email": "student@example.com",
    "access_token": "eyJ..."
  },
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

여기서 `access_token`은 Supabase가 발급한 JWT입니다.
JWT 안에는 대략 다음과 같은 정보가 들어 있습니다.

| 항목 | 의미 |
|---|---|
| `sub` | 현재 로그인한 사용자 id입니다. Supabase에서는 보통 `auth.users.id`와 연결됩니다. |
| `role` | 보통 로그인 사용자는 `authenticated` 역할을 가집니다. |
| `exp` | token 만료 시간입니다. 만료되면 다시 로그인하거나 refresh가 필요합니다. |
| `aud`, `iss` | token을 발급한 대상과 발급자를 나타냅니다. |

수업에서는 JWT를 직접 해석하기보다, "이 token이 현재 사용자를 증명한다"는 점을 먼저 이해하면 됩니다.

### 3. Swagger Authorize: token을 클라이언트가 보관합니다

로그인 응답에서 받은 `access_token`을 Swagger 오른쪽 위 `Authorize`에 넣습니다.

```text
access_token 복사
-> Swagger Authorize 클릭
-> token 값 붙여 넣기
-> Authorize
```

이후 Swagger는 보호 API를 호출할 때 자동으로 아래 헤더를 붙입니다.

```http
Authorization: Bearer eyJ...
```

여기서 중요한 점은 token을 FastAPI 서버가 세션처럼 저장하는 것이 아니라는 점입니다.

```text
token 저장 위치: Swagger UI 또는 프론트엔드
token 사용 방식: 매 요청마다 Authorization 헤더로 전송
FastAPI 역할: 받은 token이 유효한지 Supabase에 확인
```

나중에 Streamlit이나 React 화면을 만들면 Swagger 대신 프론트엔드가 이 역할을 합니다.
예를 들어 Streamlit에서는 `st.session_state["access_token"]`에 token을 저장한 뒤 API를 호출할 때 Authorization 헤더로 붙입니다.

### 4. 보호 API 호출: FastAPI가 token으로 현재 사용자를 확인합니다

`GET /me`, `POST /chat`, `GET /logs`는 로그인한 사용자만 호출해야 하는 보호 API입니다.

이 예제는 `HTTPBearer`를 사용합니다.

```text
Swagger Authorize에 저장된 token
-> Authorization: Bearer <access_token>
-> FastAPI get_current_user 실행
-> Supabase Auth get_user(token)
-> token이 유효하면 사용자 id/email 확인
```

코드 흐름은 `app/services/auth_service.py`의 `get_current_user()`에서 확인할 수 있습니다.

```text
get_current_user()
-> Authorization 헤더에서 Bearer token 추출
-> Supabase Auth에 token 확인 요청
-> user.id, user.email, access_token을 UserPublic으로 반환
```

이렇게 반환된 `UserPublic`은 `/chat`, `/logs`에서 현재 사용자 정보로 사용됩니다.

### 5. `/chat`: token 확인 후 채팅 로그를 저장합니다

`POST /chat` 호출 흐름은 다음과 같습니다.

```text
Swagger POST /chat
-> Authorization: Bearer <access_token>
-> FastAPI가 token으로 현재 사용자 확인
-> user.id 확보
-> Redis 캐시 확인
-> Gemini 답변 생성
-> ex90_user_chat_logs에 user_id와 함께 로그 저장
-> Redis에 답변 캐시 저장
-> 응답 반환
```

이때 DB에 저장되는 행에는 `user_id`가 들어갑니다.

```json
{
  "user_id": "현재 로그인한 사용자 id",
  "user_message": "사용자 질문",
  "assistant_message": "AI 답변",
  "provider": "gemini 또는 redis-cache",
  "status": "success"
}
```

현재 예제의 저장 코드는 서버가 신뢰할 수 있는 백엔드라는 전제로 `SUPABASE_SERVICE_ROLE_KEY`를 사용합니다.
즉, `/chat` 저장 단계에서는 FastAPI가 먼저 token을 검증하고, 검증된 `user.id`를 넣어 서버 권한으로 저장합니다.

이 방식에서는 저장 요청 자체는 RLS를 통과하지 않고 service role 권한으로 처리됩니다.
대신 "누가 저장할 수 있는가"는 FastAPI의 `get_current_user()`가 먼저 막고, "어느 사용자 데이터인가"는 저장할 때 `user_id`로 남깁니다.

### 6. `/logs`: 사용자 token으로 조회하므로 RLS가 실제로 작동합니다

`GET /logs`는 RLS 흐름을 확인하기 가장 좋은 endpoint입니다.

```text
Swagger GET /logs
-> Authorization: Bearer <access_token>
-> FastAPI가 token으로 현재 사용자 확인
-> Supabase REST API 호출
   apikey: SUPABASE_ANON_KEY
   Authorization: Bearer <access_token>
-> Supabase가 JWT의 auth.uid() 확인
-> RLS 정책에 맞는 행만 반환
```

`app/services/chat_service.py`의 `list_logs()`는 조회할 때 `user_headers(access_token)`을 사용합니다.

```text
apikey = SUPABASE_ANON_KEY
Authorization = Bearer <사용자 access_token>
```

이 조합이 중요합니다.

| header | 의미 |
|---|---|
| `apikey: SUPABASE_ANON_KEY` | Supabase REST API를 일반 클라이언트 권한으로 호출합니다. |
| `Authorization: Bearer <access_token>` | 현재 로그인한 사용자가 누구인지 Supabase에 알려 줍니다. |

Supabase는 이 JWT를 보고 `auth.uid()` 값을 계산합니다.
그리고 `schema.sql`의 RLS 정책을 적용합니다.

```sql
create policy "ex90 chat logs select own"
on ex90_user_chat_logs
for select
using (auth.uid() = user_id);
```

이 정책의 의미는 다음과 같습니다.

```text
현재 token의 사용자 id(auth.uid())
와
테이블 행의 user_id
가 같은 행만 조회할 수 있다.
```

따라서 A 사용자의 token으로 `/logs`를 호출하면 A의 로그만 조회됩니다.
B 사용자의 로그는 같은 테이블에 있어도 RLS 때문에 응답에 포함되지 않습니다.

### 7. RLS insert 정책은 왜 들어 있나요?

`schema.sql`에는 insert 정책도 있습니다.

```sql
create policy "ex90 chat logs insert own"
on ex90_user_chat_logs
for insert
with check (auth.uid() = user_id);
```

이 정책의 의미는 다음과 같습니다.

```text
사용자 token으로 insert할 경우,
삽입하려는 user_id가 현재 token의 사용자 id와 같아야 한다.
```

다만 현재 예제의 `/chat` 저장은 서버가 `SUPABASE_SERVICE_ROLE_KEY`를 사용하므로 이 insert RLS 정책을 직접 통과하지는 않습니다.
정책을 넣어 둔 이유는 다음 확장 방향을 보여 주기 위해서입니다.

| 방식 | 설명 |
|---|---|
| 현재 예제 | FastAPI가 token을 검증하고 service role로 로그를 저장합니다. 서버 중심 구조라 구현이 단순합니다. |
| RLS insert 확장 | `SUPABASE_ANON_KEY`와 사용자 `access_token`으로 insert하면 `insert own` 정책이 실제로 적용됩니다. |

수업에서는 먼저 현재 구조로 전체 흐름을 이해하고, RLS를 체감하는 지점은 `/logs` 조회에서 확인하면 됩니다.
시간이 충분하면 저장도 사용자 token 기반으로 바꾸어 insert RLS까지 확인할 수 있습니다.

### 8. 전체 흐름 한눈에 보기

```text
[회원가입]
Swagger -> FastAPI /auth/signup -> Supabase Auth -> auth.users 생성

[로그인]
Swagger -> FastAPI /auth/signin -> Supabase Auth -> access_token 발급

[token 보관]
access_token -> Swagger Authorize 또는 프론트엔드 session state에 저장

[/me]
Swagger -> Authorization: Bearer token -> FastAPI -> Supabase Auth get_user(token)

[/chat]
Swagger -> Authorization: Bearer token
-> FastAPI가 현재 사용자 확인
-> Redis 캐시 확인
-> Gemini 답변 생성
-> service role로 ex90_user_chat_logs에 user_id 포함 저장

[/logs]
Swagger -> Authorization: Bearer token
-> FastAPI가 현재 사용자 확인
-> Supabase REST API를 anon key + user token으로 호출
-> RLS using (auth.uid() = user_id) 적용
-> 현재 사용자 로그만 반환
```

### 9. key와 token을 헷갈리지 않기

| 이름 | 누가 발급/관리하나요? | 어디에 쓰나요? | 노출 가능 여부 |
|---|---|---|---|
| `SUPABASE_ANON_KEY` | Supabase 프로젝트 설정 | 사용자 token과 함께 REST/RLS 흐름 호출 | 프론트에 둘 수 있지만 도메인/RLS 정책이 중요합니다. |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase 프로젝트 설정 | 서버가 강한 권한으로 DB 작업 | 절대 프론트/GitHub에 노출하면 안 됩니다. |
| `access_token` | 로그인 성공 시 Supabase Auth가 발급 | 현재 사용자를 증명하는 Bearer token | 화면/브라우저에 임시 저장되지만 공유하면 안 됩니다. |
| `GEMINI_API_KEY` | Google AI Studio | Gemini SDK 호출 | 서버 `.env`에만 둡니다. |
| `UPSTASH_REDIS_REST_TOKEN` | Upstash Console | Redis REST API 호출 | 서버 `.env`에만 둡니다. |

가장 중요한 구분은 이것입니다.

```text
project key: 서비스가 Supabase에 접속하기 위한 key
access token: 로그인한 사용자가 누구인지 증명하는 token
RLS: access token 안의 사용자 id를 기준으로 행 접근을 제한하는 DB 정책
```

## 요청 흐름

```text
Bearer token 확인
-> Redis에서 같은 질문 캐시 확인
-> 캐시가 있으면 Redis 답변 반환
-> 캐시가 없으면 Gemini SDK 호출
-> Supabase ex90_user_chat_logs에 저장
-> Redis에 TTL과 함께 답변 저장
-> 응답 반환
```

## Gemini 호출 기준

`GEMINI_API_KEY`가 없거나 Gemini 호출이 실패하면 `/chat`은 오류를 반환합니다.

## pytest 기본 테스트

```powershell
python -m pytest tests
```

기본 테스트는 `tests/test_app_routes.py`만 실행합니다. 실제 Supabase, Redis, Gemini를 호출하지 않고 인증, 채팅, 로그 endpoint 흐름을 검증하는 테스트는 Codex와 함께 만들어 보는 선택 실습으로 둡니다.

참고 예시는 아래 파일에 있습니다.

```text
tests/reference_api_flow_example.py
```

이 파일 상단에는 Codex에게 보낼 수 있는 프롬프트 예시가 들어 있습니다. 실제로 실행하고 싶다면 아래처럼 복사합니다.

```powershell
Copy-Item .\tests\reference_api_flow_example.py .\tests\test_api_flow.py
python -m pytest tests
```
