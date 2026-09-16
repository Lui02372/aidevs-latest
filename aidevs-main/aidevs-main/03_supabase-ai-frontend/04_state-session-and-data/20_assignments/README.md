# 20_assignments

`04_state-session-and-data` 과제 안내입니다.

과제의 핵심은 04 단원에서 만든 챗봇 UI 흐름을 실제 서비스 상태 관리 구조로 확장하는 것입니다.

## 제출 과제

```text
assignment-01-login-state-app.md
assignment-02-auth-user-data-page.md
assignment-03-cache-report.md
```

## 제출 기준

- `st.session_state`를 사용해 상태를 유지합니다.
- 로그인 성공 후 access token을 저장합니다.
- 로그인 여부에 따라 화면을 다르게 표시합니다.
- Authorization header를 사용해 보호된 API를 호출합니다.
- 사용자별 데이터 또는 대화 이력을 화면에 표시합니다.
- 캐시 적용 위치와 이유를 설명합니다.
- Supabase service role key 또는 Gemini API key를 프론트엔드에 직접 두지 않는 이유를 설명합니다.
