# Assignment 02: Basic Dashboard App

## 목표

Streamlit의 sidebar, columns, tabs를 사용해 기본 대시보드 앱을 만듭니다.

이 과제의 목적은 입력 영역과 결과 영역을 구분하고, 여러 정보를 한 화면에서 읽기 쉽게 배치하는 것입니다. 이후 챗봇 UI, 로그 대시보드, 사용자별 대화 이력 화면을 만들 때 필요한 기본 레이아웃 감각을 연습합니다.

## 요구사항

- sidebar에서 사용자 이름과 설정값을 입력받습니다.
- columns를 사용해 최소 2개의 지표를 보여줍니다.
- tabs를 사용해 개요와 상세 내용을 나눕니다.
- 입력값에 따라 안내 메시지가 달라져야 합니다.
- 화면 제목과 각 영역의 설명 문구가 있어야 합니다.

## 제출 파일 예시

```text
assignment-02-basic-dashboard-app.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\01_streamlit-basic\20_assignments\assignment-02-basic-dashboard-app.py
```

## 구현 힌트

```text
st.set_page_config(layout="wide")
st.sidebar
st.columns
st.metric
st.tabs
st.progress
st.info / st.success / st.warning
```

sidebar는 설정 입력 영역으로 사용하고, 메인 화면은 결과를 보여 주는 영역으로 구성합니다.

## 확인 기준

- `streamlit run` 명령으로 실행됩니다.
- sidebar, columns, tabs가 모두 사용되었습니다.
- 사용자가 화면 흐름을 이해하기 쉽도록 제목과 안내 문구가 배치되었습니다.
- 입력값을 바꾸면 지표나 안내 메시지가 함께 바뀝니다.
