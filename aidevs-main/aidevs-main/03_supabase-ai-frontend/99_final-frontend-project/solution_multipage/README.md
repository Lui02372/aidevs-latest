# Solution Multipage

`solution_multipage`는 `99_final-frontend-project`의 멀티페이지 Streamlit 완성 예제입니다.

`app.py`, `frontend_common.py`, `pages/`로 화면을 나누어 개발합니다. `app.py`에서는 `st.Page`와 `st.navigation()`으로 왼쪽 메뉴에 표시할 화면 이름과 순서를 명확하게 정의합니다.

## 폴더 구조

```text
solution_multipage
├─ README.md
├─ app.py
├─ frontend_common.py
└─ pages
   ├─ 01_chatbot.py
   ├─ 02_conversation_history.py
   ├─ 03_service_logs.py
   └─ 04_deployment_checklist.py
```

| 파일 | 역할 |
| --- | --- |
| `app.py` | `st.Page`, `st.navigation()`으로 왼쪽 메뉴 구성 |
| `frontend_common.py` | API 호출, 로그인 상태, Authorization header, sidebar 공통 함수 |
| `pages/01_chatbot.py` | 챗봇 질문/응답 화면 |
| `pages/02_conversation_history.py` | 이전 대화 기록 조회 화면 |
| `pages/03_service_logs.py` | 서비스 로그 조회 화면 |
| `pages/04_deployment_checklist.py` | 배포 전 점검 화면 |

## 실행 방법

PowerShell 1: backend 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_mock
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

PowerShell 2: frontend 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\solution_multipage
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

실행 후 브라우저 왼쪽 메뉴에서 각 화면을 선택합니다.

## navigation 구조로 개발하는 방법

Streamlit 앱은 항상 진입점인 `app.py`로 실행합니다.

```powershell
streamlit run .\app.py
```

`app.py`는 왼쪽 메뉴에 표시할 화면 목록을 관리합니다.

```python
pages = [
    st.Page("pages/01_chatbot.py", title="1. 챗봇"),
    st.Page("pages/02_conversation_history.py", title="2. 대화 기록"),
    st.Page("pages/03_service_logs.py", title="3. 서비스 로그"),
    st.Page("pages/04_deployment_checklist.py", title="4. 배포 전 점검"),
]

navigation = st.navigation(pages)
navigation.run()
```

화면 이름이나 순서를 바꾸고 싶으면 `app.py`의 `pages` 목록을 수정합니다. 각 화면의 실제 기능은 `pages/*.py`에서 구현합니다.

예를 들어 챗봇 화면을 수정하고 싶다면:

```text
수정 파일:
  C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\solution_multipage\pages\01_chatbot.py

실행 명령:
  streamlit run .\app.py

확인 방법:
  브라우저 왼쪽 메뉴에서 "1. 챗봇" 선택
```

보통 아래처럼 page 파일을 직접 실행하지 않습니다.

```powershell
streamlit run .\pages\01_chatbot.py
```

직접 실행하면 전체 앱의 진입점, navigation 메뉴, 공통 sidebar 구조를 함께 확인하기 어렵습니다.

## 공통 코드 위치

여러 page에서 반복해서 쓰는 코드는 `frontend_common.py`에 둡니다.

예:

```text
API_BASE_URL 읽기
backend API 호출
Authorization header 만들기
로그인 상태 초기화
회원가입/로그인/로그아웃
공통 sidebar
```

모든 page 파일 시작 부분에서는 `init_state()`를 호출해야 합니다.

```python
from frontend_common import init_state

init_state()
```

이 호출이 빠지면 특정 page를 먼저 열었을 때 `access_token`, `current_user`, `messages` 같은 값이 없어 오류가 날 수 있습니다.
