# Frontend Tabs Template

이 폴더는 Streamlit `st.tabs()`로 한 화면 안에서 탭을 전환하는 frontend starter입니다.

대시보드 화면을 한 페이지 안에서 빠르게 구성하고 싶다면 이 구조를 사용할 수 있습니다.

## 화면 구성

```text
frontend_tabs
├─ README.md
├─ requirements.txt
├─ app.py
├─ frontend_common.py
└─ tab_pages
   ├─ __init__.py
   ├─ overview_tab.py
   ├─ log_dashboard_tab.py
   ├─ realtime_stream_tab.py
   ├─ feedback_analysis_tab.py
   └─ settings_tab.py
```

## 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\frontend_tabs
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

## 언제 사용하나요?

| 상황 | 추천 이유 |
| --- | --- |
| 한 화면 안에서 빠르게 정보를 전환 | 탭을 누르며 요약, 표, 그래프를 한 번에 볼 수 있습니다. |
| 빠른 프로토타입 | 파일 구조가 비교적 단순합니다. |
| 작은 규모의 대시보드 | 메뉴 이동 없이 한 페이지에서 확인할 수 있습니다. |

## 학생 구현 위치

`app.py`는 탭을 만드는 역할만 합니다. 실제 내용은 `tab_pages` 폴더의 각 파일에 구현합니다.

- `tab_pages/log_dashboard_tab.py`: 로그 입력, 조회, 표와 그래프
- `tab_pages/realtime_stream_tab.py`: SSE 실시간 로그 수신
- `tab_pages/feedback_analysis_tab.py`: 사용자 피드백 조회와 분석
- `tab_pages/settings_tab.py`: API 주소, 배포 URL, 환경 설정 확인
