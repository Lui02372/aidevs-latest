# Security Redaction Checklist

AI에게 질문하기 전 아래 항목을 확인합니다.

## 절대 붙여 넣지 않는 값

- [ ] `OPENAI_API_KEY`
- [ ] `GEMINI_API_KEY`
- [ ] `SUPABASE_SERVICE_ROLE_KEY`
- [ ] `SUPABASE_ANON_KEY` 실제 값
- [ ] `UPSTASH_REDIS_REST_TOKEN`
- [ ] `Authorization: Bearer ...` 실제 token
- [ ] 비밀번호
- [ ] 개인 이메일, 전화번호, 주소

## 마스킹 예시

```text
OPENAI_API_KEY=***
GEMINI_API_KEY=***
SUPABASE_SERVICE_ROLE_KEY=***
Authorization: Bearer ***
UPSTASH_REDIS_REST_TOKEN=***
```

## 질문 전에 확인할 것

- [ ] Traceback 안에 key/token이 포함되어 있지 않다.
- [ ] `.env` 전체를 붙여 넣지 않았다.
- [ ] 스크린샷에 key/token이 보이지 않는다.
- [ ] 로그에 사용자 개인정보가 포함되어 있지 않다.
- [ ] 실제 값 대신 `your-...`, `***` 같은 예시값을 사용했다.
