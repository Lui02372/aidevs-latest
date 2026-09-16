# Lab 03. session_state와 token 오류 분석

이 실습은 로그인 token을 `st.session_state`에 저장하고 보호된 API에 보내는 과정에서 생기는 문제를 다룹니다.

## 실행

먼저 샘플 백엔드를 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\04_state-session-and-data\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

새 터미널에서 문제 예제를 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-03_session-state-token-error\broken_login_state.py
```

## 해야 할 일

1. 로그인 전 `session_state` key를 읽을 때 어떤 문제가 생기는지 확인합니다.
2. 로그인 성공 후 token이 저장되는지 확인합니다.
3. `/api/me` 호출 시 header 이름과 형식이 맞는지 확인합니다.
4. 수정 후 로그인, 내 정보 조회, 로그아웃 흐름을 테스트합니다.

## Codex 요청 예시

```text
이 Streamlit 로그인 예제의 session_state와 Authorization header 문제를 찾아주세요.

리뷰 관점:
1. session_state key를 사용하기 전에 초기화했는가?
2. 로그인 성공 후 access_token을 저장하는가?
3. 보호된 API 호출 시 Authorization: Bearer token 형식인가?
4. 로그아웃 시 상태를 정리하는가?

아직 코드는 수정하지 말고 문제점과 수정 순서를 알려주세요.
```
