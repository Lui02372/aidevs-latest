# 04. Supabase Auth와 RLS

이 챕터에서는 Supabase Auth, JWT, Bearer token 흐름을 이해합니다.

이번 단계에서는 RLS 정책 SQL을 직접 작성하지 않습니다. 초보자에게는 Auth/JWT 흐름과 RLS SQL을 한 번에 다루는 것이 부담이 크기 때문입니다. RLS는 “로그인한 사용자별 데이터 접근을 제한하는 기능”이라는 개념까지만 연결하고, 실제 정책 SQL 작성은 이후 사용자별 데이터 접근이 필요한 프로젝트에서 다룹니다.

## 학습 목표

- Supabase Auth가 어떤 역할을 하는지 이해합니다.
- 로그인 결과로 발급되는 JWT의 의미를 이해합니다.
- `Authorization: Bearer <access_token>` 헤더 구조를 이해합니다.
- anon key와 service role key의 차이를 설명할 수 있습니다.
- FastAPI와 Swagger에서 signup, signin, me 흐름을 확인합니다.
- RLS는 나중에 사용자별 데이터 접근을 제한할 때 사용하는 기능임을 이해합니다.

## 핵심 개념

| 개념 | 의미 |
| --- | --- |
| Auth | 사용자가 누구인지 확인하는 기능입니다. |
| JWT | 로그인 성공 후 발급되는 토큰입니다. 서버가 “이 사용자는 로그인한 사용자다”라고 확인할 때 사용합니다. |
| Bearer token | API 요청 헤더에 JWT access token을 담아 보내는 인증 방식입니다. |
| RLS | 테이블의 행(row) 단위로 읽기/쓰기 권한을 제한하는 기능입니다. |
| anon key | 클라이언트에서 사용할 수 있는 공개용 key입니다. RLS 정책과 함께 사용해야 안전합니다. |
| service role key | RLS를 우회할 수 있는 서버 전용 key입니다. 프론트엔드에 노출하면 안 됩니다. |

### Auth는 무엇을 확인하나요?

Auth는 “이 요청을 보낸 사람이 누구인가?”를 확인합니다.

예를 들어 사용자가 이메일과 비밀번호로 로그인하면 Supabase Auth는 아래 정보를 확인합니다.

```text
1. 이 이메일로 가입한 사용자가 있는가?
2. 비밀번호가 맞는가?
3. 로그인할 수 있는 상태인가?
4. 맞다면 이 사용자를 증명할 token을 발급한다.
```

로그인에 성공하면 Supabase는 `access_token`을 발급합니다. 이 `access_token`이 보통 JWT 형식입니다.

### JWT는 어떻게 생겼나요?

JWT는 JSON Web Token의 줄임말입니다. 이름 그대로 JSON 정보를 담은 token입니다.

실제 JWT는 보통 아래처럼 점(`.`)으로 나뉜 긴 문자열입니다.

```text
xxxxx.yyyyy.zzzzz
```

구조는 3부분입니다.

| 부분 | 역할 | 담기는 내용 예시 |
|---|---|---|
| Header | 토큰의 종류와 서명 방식을 나타냅니다. | `typ`, `alg` |
| Payload | 사용자와 만료 시간 같은 정보를 담습니다. | `sub`, `email`, `role`, `exp` |
| Signature | 토큰이 위조되지 않았는지 확인하는 서명입니다. | 서버가 검증하는 값 |

예시로 보면 아래와 같은 느낌입니다.

```text
Header.Payload.Signature
```

Payload에는 보통 이런 정보가 들어갑니다.

```json
{
  "sub": "사용자 id",
  "email": "user@example.com",
  "role": "authenticated",
  "exp": 1730000000
}
```

여기서 `sub`는 subject의 줄임말로, “이 token이 가리키는 사용자 id”라고 보면 됩니다. `exp`는 token 만료 시간입니다.

중요한 점은 JWT가 “암호화된 비밀 문서”가 아니라는 것입니다. JWT의 Header와 Payload는 도구로 열어 보면 내용을 읽을 수 있습니다. 그래서 JWT 안에는 비밀번호, API key, 주민번호 같은 민감 정보를 넣으면 안 됩니다.

### JWT는 왜 사용하나요?

로그인한 사용자가 API를 호출할 때마다 이메일과 비밀번호를 다시 보내는 방식은 위험하고 불편합니다.

대신 로그인할 때 한 번 확인한 뒤, 서버는 사용자에게 짧은 수명의 token을 발급합니다. 이후 사용자는 API 요청마다 그 token을 함께 보냅니다.

```text
1. 사용자가 로그인한다.
2. Supabase Auth가 access token을 발급한다.
3. 사용자가 API를 호출할 때 access token을 함께 보낸다.
4. 서버는 token을 확인하고 사용자를 식별한다.
```

이렇게 하면 FastAPI 서버는 요청을 받을 때마다 “이 사용자가 누구인지”를 token으로 확인할 수 있습니다.

### Bearer Token은 무엇인가요?

Bearer는 “소지자”라는 뜻입니다.

`Bearer token` 방식은 간단히 말해 “이 token을 가지고 온 사람을 로그인한 사용자로 보고 처리하겠다”는 방식입니다.

API 요청에서는 보통 아래처럼 HTTP Header에 담아 보냅니다.

```text
Authorization: Bearer <access_token>
```

여기서 각 부분의 의미는 다음과 같습니다.

| 부분 | 의미 |
|---|---|
| `Authorization` | 인증 정보를 담는 HTTP Header 이름입니다. |
| `Bearer` | 뒤에 오는 token을 소지자 token으로 해석하라는 표시입니다. |
| `<access_token>` | Supabase Auth가 로그인 성공 후 발급한 JWT입니다. |

예시:

```text
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Bearer token은 편리하지만, token을 가진 사람이 곧 권한을 가진 사람처럼 동작할 수 있습니다. 그래서 access token은 비밀번호처럼 조심해서 다뤄야 합니다.

```text
주의:
1. access token 전체 값을 GitHub에 올리지 않습니다.
2. token이 보이는 화면을 그대로 캡처해 공유하지 않습니다.
3. 브라우저 개발자 도구나 터미널에 출력할 때도 전체 값을 노출하지 않습니다.
4. token은 만료될 수 있으므로, 만료되면 다시 로그인하거나 refresh token으로 갱신해야 합니다.
```

### JWT와 RLS는 어떻게 연결되나요?

Auth는 사용자를 확인하고, JWT는 확인된 사용자 정보를 API 요청에 실어 보냅니다.

RLS는 나중에 데이터베이스가 그 사용자 정보를 기준으로 “이 사용자가 이 행(row)을 읽거나 쓸 수 있는가?”를 판단할 때 사용합니다.

이번 챕터에서는 RLS SQL을 직접 작성하지 않고, 아래 흐름까지만 이해합니다.

```text
로그인 성공
-> JWT access token 발급
-> API 요청에 Bearer token으로 전달
-> 서버 또는 Supabase가 token으로 사용자 확인
-> 이후 RLS 정책에서 사용자별 데이터 접근 제어 가능
```

## Auth와 RLS의 차이

```text
Auth:
  이 사용자가 누구인지 확인합니다.

RLS:
  이 사용자가 어떤 데이터 행을 읽거나 쓸 수 있는지 제한합니다.
```

이번 챕터에서는 Auth와 JWT 흐름을 FastAPI/Swagger로 확인합니다. RLS 정책 SQL 작성은 아직 하지 않습니다.

## JWT를 조금 더 자세히 보기

Supabase Auth에서 이메일/비밀번호 로그인이 성공하면 Supabase는 사용자를 식별할 수 있는 token을 발급합니다.

로그인 결과에서 중요하게 보는 값은 아래와 같습니다.

| 값 | 의미 |
| --- | --- |
| `user.id` | Supabase Auth가 발급한 사용자 고유 id입니다. |
| `user.email` | 로그인한 사용자의 이메일입니다. |
| `session.access_token` | API 요청에 사용할 JWT입니다. |
| `session.refresh_token` | access token을 다시 발급받을 때 사용하는 토큰입니다. |

JWT는 보통 아래처럼 API 요청 헤더에 들어갑니다.

```text
Authorization: Bearer <access_token>
```

주의할 점:

```text
1. access token은 비밀번호처럼 다룹니다.
2. token 전체 값을 터미널, README, GitHub, 화면 공유에 노출하지 않습니다.
3. access token은 만료될 수 있습니다.
4. refresh token도 노출되면 안 됩니다.
5. 나중에 RLS를 적용할 때는 이 token으로 확인된 사용자 id가 데이터 접근 기준이 됩니다.
```

## Supabase Dashboard에서 확인할 위치

### Auth 설정

```text
Supabase Dashboard
-> Authentication
-> Providers
-> Email
```

이곳에서 이메일 로그인, 소셜 로그인 같은 인증 방식을 설정합니다.

수업 중 반드시 확인할 항목:

| 설정 | 의미 |
| --- | --- |
| `Enable Email provider` | 이메일/비밀번호 회원가입과 로그인을 사용할지 결정합니다. |
| `Confirm email` | 사용자가 처음 로그인하기 전에 이메일 주소를 확인해야 하는지 결정합니다. |

Supabase Dashboard에는 `Confirm email` 항목이 아래 설명으로 표시됩니다.

```text
Users will need to confirm their email address before signing in for the first time
```

이 설정이 켜져 있으면 `/auth/signup`이 성공해도, 사용자가 인증 메일을 확인하기 전에는 `/auth/signin`이 실패할 수 있습니다. 수업 시간을 줄이려면 실습용 프로젝트에서는 잠시 끄고 진행할 수 있습니다. 실제 서비스에서는 보안을 위해 켜 두는 것이 일반적입니다.

### RLS 설정 위치만 확인

```text
Supabase Dashboard
-> Table Editor
-> 테이블 선택
-> RLS 설정 확인
```

이번 챕터에서는 위치만 확인합니다. 실제 RLS 정책 SQL은 작성하지 않습니다.

## 서버 코드에서 key 선택 기준

| 위치 | 사용할 key | 기준 |
| --- | --- | --- |
| 브라우저/Streamlit 화면 | `SUPABASE_ANON_KEY` | 공개 가능한 key입니다. 반드시 RLS 정책과 함께 사용합니다. |
| FastAPI 서버 | `SUPABASE_SERVICE_ROLE_KEY` | 서버에서만 사용하는 강한 권한의 key입니다. |
| GitHub 저장소 | key 저장 금지 | `.env`는 올리지 않고 `.env.example`만 공유합니다. |

## 예제 실행

### FastAPI/Swagger로 Auth 흐름 확인

이 챕터의 Python 예제는 실제 Supabase Auth API를 FastAPI endpoint에서 호출합니다.

실행 전 `.env`에 아래 값을 준비합니다.

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
```

이 예제는 사용자를 대신해 Auth API를 호출하는 흐름이므로 `SUPABASE_SERVICE_ROLE_KEY`가 아니라 `SUPABASE_ANON_KEY`를 사용합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\04_supabase-auth-and-rls
..\..\.venv\Scripts\Activate.ps1
python -m uvicorn 01_fastapi_supabase_auth:app --reload --host 127.0.0.1 --port 8002
```

Swagger 주소:

```text
http://127.0.0.1:8002/docs
```

Swagger에서 확인할 endpoint:

| Endpoint | Method | 역할 |
| --- | --- | --- |
| `/health` | GET | FastAPI 서버 실행 확인 |
| `/auth/signup` | POST | Supabase Auth 회원가입 요청 |
| `/auth/signin` | POST | 로그인 후 access token 발급 확인 |
| `/me` | GET | `Authorization: Bearer <access_token>`으로 현재 사용자 확인 |

Swagger 실습 순서:

```text
1. /health를 실행해 서버가 켜져 있는지 확인합니다.
2. /auth/signup에서 테스트 이메일과 비밀번호로 가입합니다.
3. Confirm email이 켜져 있다면 받은 메일에서 이메일 인증을 완료합니다.
4. /auth/signin에서 같은 이메일과 비밀번호로 로그인합니다.
5. 응답의 access_token 값을 복사합니다.
6. Swagger 오른쪽 위 Authorize 버튼을 누릅니다.
7. Value에 access_token을 붙여 넣습니다.
   Swagger UI가 Bearer 형식으로 전송합니다.
8. /me를 실행해 현재 로그인한 user id와 email이 나오는지 확인합니다.
```

`/me`는 FastAPI가 직접 비밀번호를 확인하는 예제가 아닙니다. 클라이언트가 보낸 Bearer token을 Supabase Auth에 확인시키고, Supabase가 알려 준 현재 사용자 정보를 반환하는 예제입니다.

## RLS는 언제 다시 다루나요?

이번 챕터에서는 `/me`에서 확인한 `user.id`가 “현재 로그인한 사용자”라는 점까지만 이해합니다.

나중에 사용자별 데이터 접근이 필요한 프로젝트에서 아래 흐름으로 다시 다룹니다.

```text
Authorization: Bearer <access_token>
-> 현재 사용자 확인
-> user_id와 데이터 행 연결
-> RLS 정책으로 자기 데이터만 접근 허용
```

즉, 지금은 Auth/JWT/Bearer token 흐름을 익히고, RLS SQL은 이후 프로젝트에서 실제 데이터 예제와 함께 다룹니다.

## 수업 진행 순서

1. Auth와 RLS의 차이를 먼저 설명합니다.
2. Supabase Dashboard에서 Authentication 메뉴를 확인합니다.
3. anon key와 service role key의 차이를 다시 확인합니다.
4. FastAPI/Swagger 예제로 sign up/sign in 흐름을 확인합니다.
5. access token을 `/me` 같은 보호 API에 전달하는 흐름을 확인합니다.
6. `/me` 결과의 user id가 나중에 사용자별 데이터 접근 기준이 된다는 점만 연결합니다.

## 자주 만나는 문제

### service role key로는 다 보이는 경우

service role key는 RLS를 우회할 수 있습니다. 그래서 FastAPI 서버에서만 사용해야 합니다. 사용자 화면에서 service role key를 사용하면 보안상 매우 위험합니다.

### /me 호출에서 Authorization 오류가 나는 경우

Swagger 오른쪽 위 `Authorize` 버튼에 `/auth/signin` 응답의 access token을 넣었는지 확인합니다. token 앞뒤에 공백이 들어가도 실패할 수 있습니다.

### sign_up 후 sign_in이 바로 실패하는 경우

Supabase Auth의 `Confirm email` 설정이 켜져 있으면 가입 직후 바로 로그인되지 않을 수 있습니다.

```text
Supabase Dashboard
-> Authentication
-> Providers
-> Email
-> Confirm email
```

`Confirm email`은 “처음 로그인하기 전에 이메일 주소를 확인해야 한다”는 설정입니다. Supabase가 보낸 인증 메일을 확인한 뒤 다시 `/auth/signin`을 실행합니다. 수업용 프로젝트에서 빠르게 흐름만 확인해야 한다면 `Confirm email`을 잠시 끄고 진행할 수 있습니다.

### email rate limit exceeded가 나오는 경우

짧은 시간에 `/auth/signup` 또는 인증 메일 발송을 여러 번 요청하면 Supabase가 이메일 발송을 잠시 제한할 수 있습니다. 이때는 signup을 반복하지 말고, 이미 만든 테스트 계정으로 `/auth/signin`을 시도하거나 잠시 기다립니다. 수업 중에는 `Confirm email`을 끄고 진행하면 이 문제를 줄일 수 있습니다.

### access token을 그대로 출력한 경우

토큰은 사용자를 대신해 API를 호출할 수 있는 값입니다. 실습 중 실수로 전체 토큰을 화면에 노출했다면 해당 사용자를 로그아웃시키거나 테스트 계정을 다시 만드는 것이 좋습니다.

## 완료 체크리스트

```text
[ ] Auth와 RLS의 차이를 설명할 수 있습니다.
[ ] anon key와 service role key의 차이를 설명할 수 있습니다.
[ ] service role key를 프론트엔드에 노출하면 안 되는 이유를 설명할 수 있습니다.
[ ] FastAPI/Swagger에서 /auth/signup, /auth/signin, /me 흐름을 확인했습니다.
[ ] access token과 refresh token을 전체 출력하면 안 되는 이유를 이해했습니다.
[ ] Authorization: Bearer <access_token> 헤더의 의미를 설명할 수 있습니다.
[ ] RLS SQL은 이후 프로젝트에서 실제 데이터 예제와 함께 다룬다는 것을 이해했습니다.
```
