# 04_dashboard-layout

버튼, 폼, 표, 차트, sidebar, columns, tabs를 조합해 기본 대시보드를 만드는 챕터입니다.

이 폴더는 앞에서 배운 UI 컴포넌트를 하나의 화면으로 묶어 보는 단계입니다. 이후 사용자별 대화 이력, 서비스 로그, API 호출 상태를 보여 주는 화면의 기초가 됩니다.

## 학습 목표

- `st.metric`으로 핵심 지표를 표시할 수 있습니다.
- sidebar 필터와 메인 결과 영역을 구분할 수 있습니다.
- 표와 차트를 같은 데이터 기준으로 연결할 수 있습니다.
- tabs를 사용해 개요와 상세 정보를 분리할 수 있습니다.

## 예제 파일

```text
01_metric-cards.py
02_filter-dashboard.py
03_tabs-dashboard.py
04_student-progress-dashboard.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\02_streamlit-ui-components\04_dashboard-layout\04_student-progress-dashboard.py
```

## 확인할 내용

- 필터와 결과 영역이 구분되어 있는가?
- 주요 지표가 `st.metric`으로 표시되는가?
- 표와 차트가 같은 데이터를 기준으로 연결되어 있는가?
- 사용자가 먼저 봐야 하는 정보가 화면 위쪽에 배치되어 있는가?

## 이후 과정과 연결

```text
API 상태
대화 이력
서비스 로그
사용자 피드백
```

이 데이터들은 이후 단원에서 모두 대시보드 형태로 확인할 수 있습니다. 이 폴더에서는 그 화면 구조를 미리 연습합니다.
