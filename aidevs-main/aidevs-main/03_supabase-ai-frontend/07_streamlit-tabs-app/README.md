# 07. Streamlit Tabs App

이 단원은 Streamlit `st.tabs()`로 한 화면 안에서 여러 영역을 전환하는 구조를 연습합니다.

`06_streamlit-multipage-app`이 왼쪽 메뉴로 화면을 이동하는 구조라면, 이 단원은 상단 탭으로 화면을 바꾸는 구조입니다. 최종 프로젝트나 미니 프로젝트에서 `frontend_tabs` 구조를 선택할 때 참고합니다.

이 예제는 실제 backend API를 호출하지 않는 mock 앱입니다. 화면 구조와 파일 분리 방식을 익히는 데 집중합니다.

## 학습 목표

- `st.tabs()`로 탭 기반 화면을 구성합니다.
- 탭별 화면 코드를 `tab_pages/*.py` 파일로 분리합니다.
- `app.py`는 탭을 만들고, 실제 화면 구현은 각 `render_*_tab()` 함수에 맡깁니다.
- 한 화면 안에서 로그, Chat, 데이터베이스, 설정 정보를 빠르게 전환하는 UI를 연습합니다.

## 폴더 구조

```text
07_streamlit-tabs-app
├─ README.md
├─ app.py
├─ frontend_common.py
└─ tab_pages
   ├─ __init__.py
   ├─ overview_tab.py
   ├─ signup_tab.py
   ├─ log_view_tab.py
   ├─ chat_tab.py
   └─ database_view_tab.py
```

| 파일 | 역할 |
| --- | --- |
| `app.py` | `st.tabs()`로 탭 목록을 만들고 각 탭 함수를 호출합니다. |
| `frontend_common.py` | 로그인 상태, mock 데이터, 공통 함수를 관리합니다. |
| `tab_pages/overview_tab.py` | 탭 구조 설명 화면입니다. |
| `tab_pages/signup_tab.py` | 회원가입 mock 화면입니다. |
| `tab_pages/log_view_tab.py` | 로그조회 mock 화면입니다. |
| `tab_pages/chat_tab.py` | Chat mock 화면입니다. |
| `tab_pages/database_view_tab.py` | 데이터베이스조회 mock 화면입니다. |

## 실행 방법

```powershell
cd C:\aidev\03_supabase-ai-frontend\07_streamlit-tabs-app
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

## 06과 07의 차이

| 구분 | 06 multipage | 07 tabs |
| --- | --- | --- |
| 화면 이동 | 왼쪽 메뉴 | 상단 탭 |
| Streamlit 기능 | `st.Page`, `st.navigation()` | `st.tabs()` |
| 코드 분리 | `pages/*.py` | `tab_pages/*.py` |
| 적합한 경우 | 화면이 독립적이고 많을 때 | 한 화면 안에서 정보를 빠르게 전환할 때 |

## 개발 방법

탭 화면을 수정할 때도 항상 `app.py`를 실행합니다.

```powershell
streamlit run .\app.py
```

예를 들어 Chat 탭을 수정하고 싶다면:

```text
수정 파일:
  C:\aidev\03_supabase-ai-frontend\07_streamlit-tabs-app\tab_pages\chat_tab.py

실행 명령:
  streamlit run .\app.py

확인 방법:
  브라우저 상단 탭에서 "Chat" 선택
```

## 최종 프로젝트와 연결

이 단원은 `99_final-frontend-project/solution_tabs`와 연결됩니다.

```text
07_streamlit-tabs-app
-> backend 없는 mock 탭 화면 흐름 연습

99_final-frontend-project/solution_tabs
-> backend_mock 또는 backend_service와 연결한 최종 탭 기반 예제
```

04 미니 프로젝트의 `03_project_structure/frontend_tabs`도 이 단원과 같은 방향으로 이해하면 됩니다.
