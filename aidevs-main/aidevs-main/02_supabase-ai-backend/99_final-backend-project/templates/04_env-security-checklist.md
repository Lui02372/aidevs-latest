# 04. Env Security Checklist

- [ ] `.env` 파일은 Git에 올리지 않습니다.
- [ ] `.env.example`에는 예시 값만 적습니다.
- [ ] `GEMINI_API_KEY`를 코드에 직접 적지 않았습니다.
- [ ] `SUPABASE_SERVICE_ROLE_KEY`를 README나 화면에 노출하지 않았습니다.
- [ ] JWT 또는 Bearer token을 제출 문서에 그대로 붙여 넣지 않았습니다.
- [ ] 로그에 API key, 비밀번호, 개인정보가 들어가지 않습니다.

## `.env.example` 예시

```text
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
```
