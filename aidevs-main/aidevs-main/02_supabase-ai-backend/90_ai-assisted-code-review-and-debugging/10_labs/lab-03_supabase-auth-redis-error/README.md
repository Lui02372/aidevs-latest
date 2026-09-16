# Lab 03. Supabase, Auth, Redis 오류

## 목표

외부 서비스 오류를 한꺼번에 외우는 것이 아니라, 종류별로 나누어 질문하는 연습을 합니다.

이 lab은 다음 오류를 다룹니다.

- Supabase 테이블명 오류
- Authorization Bearer token 누락
- anon key/service role key 혼동
- Redis URL/token 누락
- Redis TTL 확인

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\90_ai-assisted-code-review-and-debugging\10_labs\lab-03_supabase-auth-redis-error
..\..\..\.venv\Scripts\Activate.ps1
python -m uvicorn broken_external_service_api:app --reload --host 127.0.0.1 --port 8093
```

Swagger:

```text
http://127.0.0.1:8093/docs
```

## 1차 프롬프트

```text
Supabase/Auth/Redis 연동 오류를 분석해주세요.
아직 코드는 수정하지 말고 아래 항목을 기준으로 가능한 원인을 나눠주세요.

1. Supabase 테이블명과 schema.sql 실행 여부
2. SUPABASE_ANON_KEY와 SUPABASE_SERVICE_ROLE_KEY 구분
3. Authorization: Bearer token 누락 여부
4. Upstash Redis URL/token 누락 여부
5. Redis TTL이 만료되었을 가능성
```

## 실습 팁

실제 key나 token은 Codex에게 보내지 않습니다.

```text
SUPABASE_SERVICE_ROLE_KEY=***
Authorization: Bearer ***
UPSTASH_REDIS_REST_TOKEN=***
```
