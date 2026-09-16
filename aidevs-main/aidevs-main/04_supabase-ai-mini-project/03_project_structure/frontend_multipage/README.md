# Frontend Multipage Template

이 폴더는 Streamlit 왼쪽 메뉴로 화면을 이동하는 frontend starter입니다.

최종 프로젝트에서 화면이 여러 개로 나뉘고, 팀원이 화면별로 파일을 나누어 개발해야 한다면 이 구조를 권장합니다.

## 화면 구성

```text
frontend_multipage
├─ README.md
├─ requirements.txt
├─ app.py
├─ frontend_common.py
└─ pages
   ├─ 00_overview.py
   ├─ 01_log_dashboard.py
   ├─ 02_realtime_stream.py
   ├─ 03_feedback_analysis.py
   └─ 04_settings.py
```

## 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\frontend_multipage
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

## 언제 사용하나요?

| 상황 | 추천 이유 |
| --- | --- |
| 메뉴가 여러 개로 나뉘는 서비스 | 왼쪽 메뉴에서 화면을 명확하게 이동할 수 있습니다. |
| 팀원별로 화면을 나누어 개발 | `pages` 폴더 아래 파일 단위로 작업을 나눌 수 있습니다. |
| 최종 프로젝트 제출용 화면 | 화면 구조가 커져도 관리하기 쉽습니다. |

## 학생 구현 위치

- `pages/01_log_dashboard.py`: 로그 입력, 로그 조회, 표와 그래프
- `pages/02_realtime_stream.py`: SSE 실시간 로그 수신
- `pages/03_feedback_analysis.py`: 사용자 피드백 조회와 분석
- `pages/04_settings.py`: API 주소, 배포 URL, 환경 설정 확인

완성 예시는 `01_realtime-log-dashboard-practice/frontend`를 참고합니다.
