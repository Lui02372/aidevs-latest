# 03_layout-and-pages

Streamlit의 기본 레이아웃 기능을 사용해 화면을 나누는 챕터입니다.

좋은 화면은 기능이 많기만 한 화면이 아니라, 사용자가 어디에 입력하고 어디에서 결과를 확인해야 하는지 바로 알 수 있는 화면입니다. 이 폴더에서는 `columns`, `tabs`, `sidebar`를 사용해 입력 영역, 결과 영역, 보조 설명 영역을 나누는 방법을 연습합니다.

## 학습 목표

- `st.columns`로 화면을 열 단위로 나눌 수 있다.
- `st.tabs`로 관련 내용을 탭으로 구분할 수 있다.
- `st.sidebar`로 설정 입력 영역을 분리할 수 있다.
- 여러 레이아웃 기능을 조합해 기본 대시보드 페이지를 만들 수 있다.
- 이후 챗봇 UI에서 입력 영역, 응답 영역, 대화 이력 영역을 어떻게 나눌지 생각할 수 있다.

## 예제 파일

```text
01_columns.py
02_tabs.py
03_sidebar.py
04_basic-dashboard-page.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\01_streamlit-basic\03_layout-and-pages\04_basic-dashboard-page.py
```

## 확인할 내용

- 화면이 의도한 열과 탭으로 나뉘는가?
- 설정 영역과 결과 영역이 구분되는가?
- 사용자가 봤을 때 입력 흐름이 자연스러운가?
- 너무 많은 정보가 한 화면에 몰려 있지는 않은가?

## 레이아웃 선택 기준

```text
columns
-> 같은 화면에서 여러 정보를 나란히 비교할 때 사용합니다.

tabs
-> 관련은 있지만 동시에 볼 필요는 없는 내용을 구분할 때 사용합니다.

sidebar
-> 필터, 설정, 로그인 정보처럼 보조 입력을 화면 왼쪽에 분리할 때 사용합니다.
```

이 기준은 나중에 사용자별 대화 기록, API 응답 상태, 서비스 로그를 화면에 배치할 때도 그대로 사용됩니다.

