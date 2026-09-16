# 01_streamlit-session-state

Streamlit의 `st.session_state` 기본 사용법을 학습합니다.

Streamlit은 버튼을 클릭하거나 입력값이 바뀔 때마다 Python 파일을 처음부터 다시 실행합니다. 일반 변수에만 값을 저장하면 다음 실행 때 값이 사라질 수 있습니다. 화면에서 계속 유지해야 하는 값은 `st.session_state`에 저장합니다.

## 학습 목표

- `st.session_state`에 값을 저장할 수 있다.
- 상태값이 없을 때만 초기값을 만들 수 있다.
- 버튼 클릭 결과를 상태로 유지할 수 있다.
- 상태 초기화 버튼을 만들 수 있다.
- 04 단원의 간단한 대화 이력 미리보기가 왜 `session_state`를 사용하는지 설명할 수 있다.

## 예제 파일

```text
01_counter-state.py
02_initialize-state.py
03_button-state.py
04_state-reset.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\04_state-session-and-data\01_streamlit-session-state\01_counter-state.py
```

## 확인 내용

- 버튼을 누를 때마다 count 값이 증가하는가?
- 입력값이 화면 재실행 후에도 유지되는가?
- 초기화 버튼을 누르면 상태값이 비워지는가?
- 상태 초기화 코드가 사용 전에 실행되는가?

## 자주 만나는 오류

- `st.session_state.count`를 초기화하기 전에 사용하면 오류가 발생할 수 있습니다.
- 버튼 클릭 결과를 일반 변수에만 저장하면 다음 실행 때 값이 사라질 수 있습니다.
