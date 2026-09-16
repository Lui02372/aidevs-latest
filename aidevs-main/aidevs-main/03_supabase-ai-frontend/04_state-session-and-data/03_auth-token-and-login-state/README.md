# 03_auth-token-and-login-state

로그인 API 응답으로 받은 token을 Streamlit 상태에 저장하고, 로그인 여부에 따라 화면을 다르게 표시하는 방법을 학습합니다.

이 단원은 Supabase Auth를 프론트엔드에서 직접 호출하는 수업이 아닙니다. Supabase Auth는 `02_supabase-ai-backend`에서 처리하고, Streamlit은 백엔드 로그인 API를 호출한 뒤 응답으로 받은 token을 `st.session_state`에 저장합니다.

## 학습 목표

- 로그인 폼을 만들 수 있다.
- 회원가입 API를 호출하고 새 계정을 만들 수 있다.
- 로그인 API에 사용자 정보 또는 테스트 계정 정보를 POST 요청으로 보낼 수 있다.
- 로그인 성공 응답의 token을 `st.session_state`에 저장할 수 있다.
- 로그인 상태와 로그아웃 상태에 따라 화면을 다르게 표시할 수 있다.
- Authorization header를 사용해 보호된 API를 호출할 수 있다.

## 예제 파일

```text
01_login-token-state.py
02_authorization-header.py
03_logout-flow.py
04_signup-login-screen-change.py
```

권장 진행 순서는 다음과 같습니다.

| 순서 | 파일 | 학습 내용 |
| --- | --- | --- |
| 1 | `01_login-token-state.py` | 로그인 API 응답으로 받은 token을 `st.session_state`에 저장합니다. |
| 2 | `02_authorization-header.py` | 저장한 token을 `Authorization: Bearer ...` header로 보내 보호된 API를 호출합니다. |
| 3 | `03_logout-flow.py` | token을 지워 로그아웃 상태로 돌아가는 흐름을 확인합니다. |
| 4 | `04_signup-login-screen-change.py` | 회원가입, 로그인, 화면 전환, 로그아웃을 하나의 화면 흐름으로 통합합니다. |

## 백엔드 연결 기준

실제 수업에서는 다음 백엔드 단원과 연결합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\04_supabase-auth-and-rls
```

API 서버 실행 예시는 다음과 같습니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\03_fastapi-supabase-integration
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 보조 샘플 백엔드 실행

백엔드 인증 단원이 아직 준비되지 않았을 때는 아래 샘플로 token 저장 흐름만 확인할 수 있습니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\04_state-session-and-data\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

샘플 계정은 다음과 같습니다.

```text
student / 1234
```

## 프론트엔드 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\04_state-session-and-data\03_auth-token-and-login-state\01_login-token-state.py
```

회원가입부터 로그인 후 화면 전환까지 한 번에 확인하려면 마지막 통합 예제를 실행합니다.

```powershell
streamlit run .\04_state-session-and-data\03_auth-token-and-login-state\04_signup-login-screen-change.py
```

## 확인 내용

- 새 계정을 만들면 회원가입 성공 메시지가 표시되는가?
- 올바른 계정으로 로그인하면 token이 저장되는가?
- 로그인 후 화면이 로그인 전 화면과 다르게 표시되는가?
- 잘못된 계정으로 로그인하면 실패 메시지가 표시되는가?
- 로그아웃 버튼을 누르면 token이 제거되는가?
- `/api/me` 호출 시 `Authorization: Bearer ...` header가 포함되는가?
- 인증 실패 시 이해할 수 있는 오류 메시지가 표시되는가?

## 보안 메모

프론트엔드에는 Supabase service role key를 저장하지 않습니다. 서비스 권한 키는 백엔드에서만 사용해야 합니다.
