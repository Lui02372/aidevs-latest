# Assignment 01: Survey UI

## 목표

Streamlit의 입력 컴포넌트와 폼을 사용해 간단한 설문 화면을 만듭니다.

이 과제의 목적은 여러 입력값을 한 번에 제출하고, 제출된 내용을 결과 영역에서 확인하는 흐름을 만드는 것입니다.

## 요구사항

- 이름 또는 닉네임을 입력받습니다.
- 관심 주제를 선택받습니다.
- 체크박스 또는 슬라이더를 최소 1개 이상 사용합니다.
- `st.form`과 `st.form_submit_button`을 사용합니다.
- 제출 후 결과 영역에 입력 내용을 요약해서 보여 줍니다.
- 필수 입력값이 비어 있으면 안내 메시지를 표시합니다.

## 제출 파일 예시

```text
assignment-01-survey-ui.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\02_streamlit-ui-components\20_assignments\assignment-01-survey-ui.py
```

## 확인 기준

- 폼 제출 전에는 결과가 표시되지 않습니다.
- 제출 버튼을 누르면 입력값 요약이 표시됩니다.
- 최소 2개 이상의 입력 컴포넌트를 사용했습니다.
- 코드 주요 줄에 본인이 이해한 주석이 있습니다.
