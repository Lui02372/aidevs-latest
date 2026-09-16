# 02_streamlit-ui-components

Streamlit에서 자주 사용하는 UI 컴포넌트를 직접 다루는 단원입니다.

`01_streamlit-basic`에서 화면 출력, 입력, 기본 레이아웃을 배웠다면, 이 단원에서는 버튼, 폼, 표, 차트, 파일 업로드, 대시보드 구성을 학습합니다.

이 단원은 단순히 컴포넌트 이름을 외우는 과정이 아닙니다. 이후 `03_api-integration`에서 FastAPI 응답을 표로 보여 주고, `05_ai-chatbot-interface`에서 질문 입력 UI를 만들고, `04_state-session-and-data`에서 대화 이력과 서비스 로그를 화면에 표시하기 위한 준비 단계입니다.

pandas는 데이터 분석 전체를 깊게 다루기보다, Streamlit에서 표와 차트를 만들기 위해 필요한 만큼만 사용합니다.

## 학습 목표

- 버튼, 체크박스, 슬라이더, 폼의 역할을 구분할 수 있습니다.
- 사용자의 입력을 모아 한 번에 제출하는 폼 흐름을 만들 수 있습니다.
- 리스트와 딕셔너리 데이터를 pandas DataFrame으로 바꿀 수 있습니다.
- `st.dataframe`, `st.table`로 표를 출력하고 차이를 설명할 수 있습니다.
- 간단한 필터링과 요약 값을 만들어 화면에 표시할 수 있습니다.
- Streamlit 기본 차트를 출력할 수 있습니다.
- CSV 파일을 업로드하고 화면에 표시할 수 있습니다.
- 여러 UI 요소를 조합해 기본 대시보드를 만들 수 있습니다.

## 학습 순서

```text
01_buttons-forms-and-controls
-> 02_dataframe-table-basics
-> 03_charts-and-files
-> 04_dashboard-layout
-> 10_labs
-> 20_assignments
```

## 폴더 구성

```text
02_streamlit-ui-components
├─ README.md
├─ 00_references
├─ 01_buttons-forms-and-controls
├─ 02_dataframe-table-basics
├─ 03_charts-and-files
├─ 04_dashboard-layout
├─ 10_labs
└─ 20_assignments
```

## 실행 방법

`03_supabase-ai-frontend` 최상위 폴더에서 가상환경을 활성화한 뒤 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\02_streamlit-ui-components\01_buttons-forms-and-controls\01_button-click.py
```

패키지 설치가 필요하면 최상위 `requirements.txt`를 기준으로 설치합니다.

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 실행 확인 기준

- 버튼 클릭 여부에 따라 화면 결과가 바뀝니다.
- 폼 입력 후 제출 버튼을 눌렀을 때 결과가 표시됩니다.
- DataFrame 표가 화면에 표시됩니다.
- CSV 업로드 후 데이터가 표시됩니다.
- 차트와 필터가 같은 데이터를 기준으로 함께 동작합니다.

## 필수와 선택 기준

| 구분 | 내용 |
| --- | --- |
| 필수 | 버튼, 폼, 표, 기본 차트, CSV 업로드, 간단한 대시보드 배치 |
| 선택 | 복잡한 차트 라이브러리, 고급 pandas 분석, 세부 디자인 조정 |
| 제외 | React UI, Supabase 직접 조회, LLM API 직접 호출 |

## 학습할 때 보는 기준

이 단원에서 보는 핵심 질문은 다음과 같습니다.

```text
사용자가 어떤 행동을 할 수 있어야 하는가?
입력값은 언제 화면에 반영되는가?
데이터는 표로 보는 것이 좋은가, 차트로 보는 것이 좋은가?
필터 조건과 결과 화면이 서로 연결되어 있는가?
나중에 백엔드 응답이나 Gemini 응답을 어디에 표시할 수 있는가?
```

## 다음 단원 연결

이 단원을 마치면 `03_api-integration`에서 Streamlit 화면과 FastAPI 백엔드를 HTTP 요청으로 연결합니다. 이때 API 응답을 표, 상태 메시지, 대시보드 카드로 표현하는 데 이 단원의 컴포넌트가 사용됩니다.
