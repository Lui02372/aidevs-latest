# Solution Tabs

`solution_tabs`는 `99_final-frontend-project`의 탭 기반 Streamlit 완성 예제입니다.

하나의 `app.py` 안에서 `st.tabs()`로 화면을 전환합니다. 빠르게 전체 기능을 확인하거나, 작은 규모의 대시보드 UI를 만들 때 적합합니다.

## 실행 방법

PowerShell 1: backend 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_mock
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

PowerShell 2: frontend 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\solution_tabs
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

## 화면 구성

- 사이드바: API 주소, 회원가입, 로그인, 로그아웃, 현재 사용자
- 탭 1: 챗봇
- 탭 2: 대화 기록
- 탭 3: 서비스 로그
- 탭 4: 배포 전 점검

## 확인할 점

- 기본 샘플 계정은 `student@example.com / pass1234`입니다.
- 로그인 성공 시 `st.session_state["access_token"]`에 token을 저장합니다.
- 보호 API 호출 시 `Authorization: Bearer ...` header를 보냅니다.
- 챗봇 탭에서는 질문 입력 영역을 위쪽에 두고, 대화 내용은 아래에 누적 표시합니다.
- 이 예제는 프론트엔드에 Supabase key, Gemini key, Redis token을 직접 저장하지 않습니다.
