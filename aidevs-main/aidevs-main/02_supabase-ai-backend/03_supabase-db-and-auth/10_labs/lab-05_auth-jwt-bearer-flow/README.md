# Lab 05 - Auth JWT Bearer Flow

이 lab은 `04_supabase-auth-and-rls`의 실제 FastAPI 예제를 실행해서 Supabase Auth, JWT, Bearer token 흐름을 확인합니다.

이번 단계에서는 RLS 정책 SQL을 작성하지 않습니다. 목표는 로그인 후 발급된 `access_token`을 Swagger의 `Authorize`에 넣고, `/me` 보호 API를 호출하는 흐름을 이해하는 것입니다.

## 학습 목표

- 회원가입과 로그인 흐름을 Swagger에서 확인합니다.
- 로그인 응답의 `access_token`이 JWT라는 것을 이해합니다.
- `Authorization: Bearer <access_token>` 헤더가 보호 API 호출에 사용된다는 것을 확인합니다.
- `Confirm email` 설정 때문에 로그인이 실패할 수 있음을 이해합니다.

## 실행 방법

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\04_supabase-auth-and-rls
..\..\.venv\Scripts\Activate.ps1
python -m uvicorn 01_fastapi_supabase_auth:app --reload --host 127.0.0.1 --port 8002
```

Swagger UI:

```text
http://127.0.0.1:8002/docs
```

## 테스트 순서

```text
1. GET /health를 실행합니다.
2. POST /auth/signup으로 테스트 계정을 만듭니다.
3. Supabase Confirm email 설정이 켜져 있다면 이메일 인증을 완료합니다.
4. POST /auth/signin으로 로그인합니다.
5. 응답의 access_token을 복사합니다.
6. Swagger 오른쪽 위 Authorize 버튼을 누릅니다.
7. access_token을 입력하고 Authorize를 누릅니다.
8. GET /me를 실행합니다.
```

## 확인 기준

- `/auth/signin` 응답에 `access_token`이 포함됩니다.
- `/me` 호출 결과에 현재 로그인한 사용자의 `id`, `email`이 표시됩니다.
- access token 전체 값을 문서나 GitHub에 남기지 않습니다.

## 정리 질문

- JWT는 왜 이메일/비밀번호를 매번 보내는 방식보다 안전한가요?
- Bearer token은 HTTP 요청의 어느 위치에 들어가나요?
- RLS SQL은 왜 이번 lab에서 바로 작성하지 않나요?
