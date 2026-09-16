# Assignment 04 - Auth JWT Bearer Flow

Supabase Auth에서 로그인 후 발급되는 JWT와 Bearer token 흐름을 설명하는 과제입니다.

이번 과제에서는 RLS 정책 SQL을 작성하지 않습니다. RLS는 “나중에 사용자별 데이터 접근을 제한할 때 연결된다”는 수준까지만 설명합니다.

## 목표

- 회원가입과 로그인 API 흐름을 설명할 수 있습니다.
- JWT가 어떻게 생겼고 왜 사용하는지 설명할 수 있습니다.
- `Authorization: Bearer <access_token>` 헤더의 의미를 설명할 수 있습니다.
- `anon key`와 `service role key`의 사용 위치를 구분할 수 있습니다.

## 제출물

아래 내용을 포함해 작성합니다.

```text
1. /auth/signup 요청과 응답 흐름
2. /auth/signin 요청과 응답 흐름
3. access_token과 refresh_token의 차이
4. JWT의 Header, Payload, Signature 구조
5. Bearer token 헤더 예시
6. /me 보호 API가 동작하는 순서
7. Confirm email 설정이 켜져 있을 때 생길 수 있는 문제
8. anon key와 service role key의 사용 위치
9. token 전체 값을 제출하면 안 되는 이유
10. RLS SQL은 이후 프로젝트에서 다룬다는 정리
```

## 실행 참고

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\04_supabase-auth-and-rls
..\..\.venv\Scripts\Activate.ps1
python -m uvicorn 01_fastapi_supabase_auth:app --reload --host 127.0.0.1 --port 8002
```

Swagger UI:

```text
http://127.0.0.1:8002/docs
```

## 확인 기준

- 인증이 필요한 API와 공개 API를 구분했습니다.
- JWT의 구조를 3부분으로 설명했습니다.
- Bearer token이 HTTP Header에 들어간다는 점을 설명했습니다.
- service role key를 프론트엔드에 넣으면 안 되는 이유를 설명했습니다.
