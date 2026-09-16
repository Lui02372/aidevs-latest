# Security Redaction Checklist

Codex에게 오류 메시지나 코드를 보낼 때 아래 항목은 반드시 가립니다.

## 가려야 하는 값

- [ ] `SUPABASE_SERVICE_ROLE_KEY`
- [ ] `SUPABASE_ANON_KEY`
- [ ] `GEMINI_API_KEY`
- [ ] `OPENAI_API_KEY`
- [ ] `UPSTASH_REDIS_REST_TOKEN`
- [ ] 실제 사용자 비밀번호
- [ ] 실제 access token 또는 refresh token

## 예시

나쁜 예:

```text
Authorization: Bearer eyJhbGciOi...
```

좋은 예:

```text
Authorization: Bearer ***
```

나쁜 예:

```text
SUPABASE_SERVICE_ROLE_KEY=실제값
```

좋은 예:

```text
SUPABASE_SERVICE_ROLE_KEY=***
```

## 프론트엔드 보안 기준

- [ ] Streamlit 프론트엔드에는 공개 가능한 설정만 둔다.
- [ ] 외부 LLM 호출은 가능한 백엔드 API를 통해 처리한다.
- [ ] service role key는 백엔드 `.env`에만 둔다.
- [ ] 오류 메시지에 token 원문이 표시되지 않게 한다.
