# Assignment 02: Table Chart Dashboard

## 목표

pandas DataFrame, 표, 차트, 필터를 사용해 기본 대시보드를 만듭니다.

이 과제의 목적은 데이터를 화면에서 읽기 좋은 형태로 표현하는 것입니다. 이후 API 응답, 대화 이력, 서비스 로그를 화면에 보여 주는 연습으로 이어집니다.

## 요구사항

- 리스트와 딕셔너리 또는 CSV 데이터를 DataFrame으로 만듭니다.
- `st.dataframe`으로 표를 표시합니다.
- `st.metric`으로 주요 지표를 최소 2개 이상 표시합니다.
- `st.line_chart` 또는 `st.bar_chart`를 사용합니다.
- sidebar 또는 selectbox로 필터 조건을 선택할 수 있어야 합니다.
- 필터 결과가 표와 차트에 반영되어야 합니다.

## 제출 파일 예시

```text
assignment-02-table-chart-dashboard.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\02_streamlit-ui-components\20_assignments\assignment-02-table-chart-dashboard.py
```

## 확인 기준

- 표와 차트가 같은 데이터를 기준으로 표시됩니다.
- 필터 값을 바꾸면 표나 차트가 함께 바뀝니다.
- 핵심 지표가 화면 위쪽에서 먼저 보입니다.
- 코드 주요 줄에 본인이 이해한 주석이 있습니다.
