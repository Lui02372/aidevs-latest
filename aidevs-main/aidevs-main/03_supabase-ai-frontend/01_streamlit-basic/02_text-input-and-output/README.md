# 02_text-input-and-output

사용자 입력을 받고 입력값에 따라 화면 출력을 바꾸는 챕터입니다.

Streamlit 화면에서 사용자가 입력한 값은 Python 변수에 저장됩니다. 이 폴더의 핵심은 “입력 컴포넌트가 값을 돌려주고, 그 값을 조건문과 문자열 출력에 사용할 수 있다”는 흐름을 익히는 것입니다.

## 학습 목표

- 텍스트 입력값을 받을 수 있다.
- 숫자 입력값을 받을 수 있다.
- 선택 입력값을 받을 수 있다.
- 로컬 이미지 파일을 Streamlit 화면에 출력할 수 있다.
- 입력값을 조합해 간단한 피드백 앱을 만들 수 있다.
- 빈 입력값, 기본값, 선택값을 화면에서 어떻게 안내할지 결정할 수 있다.

## 예제 파일

```text
01_text-input.py
02_number-input.py
03_selectbox-radio.py
04_simple-feedback-app.py
05_image-output.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\01_streamlit-basic\02_text-input-and-output\01_text-input.py
```

이미지 출력 예제는 다음과 같이 실행합니다.

```powershell
streamlit run .\01_streamlit-basic\02_text-input-and-output\05_image-output.py
```

## 확인할 내용

- 입력값을 바꾸면 출력 문장이 바뀌는가?
- 빈 입력값을 어떻게 처리하는지 설명할 수 있는가?
- 선택 입력과 숫자 입력의 반환값 타입을 구분할 수 있는가?
- `imgs` 폴더의 이미지가 Streamlit 화면에 정상적으로 출력되는가?
- 입력 영역과 결과 영역이 화면에서 자연스럽게 구분되는가?

## 이후 과정과 연결

지금은 입력값으로 간단한 문장을 만들지만, 이후에는 같은 입력값을 FastAPI 백엔드로 전송합니다.

```text
사용자 입력
-> Streamlit 변수에 저장
-> FastAPI API 요청 데이터로 변환
-> 백엔드 응답을 화면에 표시
```

따라서 이 단원에서는 입력 컴포넌트를 많이 외우기보다, 입력값이 변수에 저장되고 그 변수로 화면이 바뀌는 흐름을 정확히 이해하는 것이 중요합니다.

