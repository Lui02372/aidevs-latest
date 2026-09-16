# Assignment 01: Self Introduction App

## 목표

Streamlit을 사용해 자기소개 앱을 만듭니다.

이 과제의 목적은 입력값을 받고, 그 입력값을 결과 화면에 보기 좋게 출력하는 기본 흐름을 익히는 것입니다. 화려한 디자인보다 입력과 출력이 명확하게 연결되는지가 중요합니다.

## 요구사항

- 이름을 입력받습니다.
- 관심 분야를 선택받습니다.
- 자기소개 문장을 입력받습니다.
- 입력값을 바탕으로 결과 영역에 자기소개 카드를 출력합니다.
- 빈 입력값이 있을 때 안내 메시지를 표시합니다.
- 결과 영역에는 이름, 관심 분야, 자기소개 문장이 모두 보여야 합니다.

## 제출 파일 예시

```text
assignment-01-self-introduction-app.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\01_streamlit-basic\20_assignments\assignment-01-self-introduction-app.py
```

## 구현 힌트

```text
st.title
st.text_input
st.selectbox
st.text_area
st.divider
st.success 또는 st.info
st.warning
```

입력값이 모두 있을 때만 결과 카드를 보여 주고, 하나라도 비어 있으면 안내 메시지를 보여 주는 구조로 작성합니다.

## 확인 기준

- `streamlit run` 명령으로 실행됩니다.
- 입력값을 변경하면 결과가 함께 변경됩니다.
- 빈 입력값이 있을 때 안내 메시지가 표시됩니다.
- 코드 주요 줄에 본인이 이해한 주석이 있습니다.
