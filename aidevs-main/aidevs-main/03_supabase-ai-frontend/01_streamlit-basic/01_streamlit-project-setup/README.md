# 01_streamlit-project-setup

Streamlit 앱의 가장 기본적인 실행 방법과 화면 출력 방법을 익히는 챕터입니다.

이 폴더에서는 “Python 파일 하나를 웹 화면으로 실행한다”는 감각을 먼저 익힙니다. 아직 버튼, 입력창, API 호출은 중요하지 않습니다. `streamlit run` 명령을 실행하면 Python 코드가 브라우저 화면으로 바뀐다는 점을 확인하는 것이 핵심입니다.

## 학습 목표

- Streamlit 앱 파일을 만들 수 있다.
- `streamlit run` 명령으로 앱을 실행할 수 있다.
- 제목, 본문, 코드, 상태 메시지를 출력할 수 있다.
- Streamlit 앱의 기본 파일 구조를 이해한다.
- 화면을 함수 단위로 나누면 코드가 읽기 쉬워진다는 점을 이해한다.

## 예제 파일

```text
01_hello-streamlit.py
02_page-title-and-text.py
03_basic-app-structure.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\01_streamlit-basic\01_streamlit-project-setup\01_hello-streamlit.py
```

## 확인할 내용

- 브라우저에 앱 화면이 표시되는가?
- 코드를 수정한 뒤 화면이 자동으로 갱신되는가?
- `st.title`, `st.write`, `st.code`, `st.success`의 차이를 설명할 수 있는가?
- `render_header`, `render_content`, `render_footer`처럼 화면 영역을 함수로 나누면 어떤 장점이 있는가?

## 코드 읽는 순서

Streamlit 코드는 위에서 아래로 실행됩니다. 일반 Python 파일과 같지만, 출력 결과가 터미널이 아니라 브라우저 화면에 표시됩니다.

```text
1. import streamlit as st
2. 페이지 설정 또는 제목 출력
3. 본문 텍스트와 안내 메시지 출력
4. 필요한 경우 함수를 호출해 화면 영역 구성
```

화면이 이상하게 보이면 먼저 터미널의 오류 메시지를 보고, 그다음 브라우저를 새로고침하거나 Streamlit의 Rerun을 실행합니다.

