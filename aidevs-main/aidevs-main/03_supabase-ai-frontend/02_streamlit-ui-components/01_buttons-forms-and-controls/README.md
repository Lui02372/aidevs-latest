# 01_buttons-forms-and-controls

버튼, 체크박스, 슬라이더, 폼처럼 사용자의 행동을 받는 UI 컴포넌트를 학습합니다.

이 폴더에서는 화면에 값을 보여 주는 단계에서 한 걸음 더 나아가, 사용자가 클릭하거나 선택하거나 제출하는 흐름을 만듭니다. 이후 챗봇 질문 입력, 설정값 변경, 서비스 로그 필터링 화면의 기초가 됩니다.

## 학습 목표

- 버튼을 클릭했을 때만 결과를 표시할 수 있습니다.
- 체크박스 값을 `True` 또는 `False`로 처리할 수 있습니다.
- 슬라이더 값을 조건문에 사용할 수 있습니다.
- 폼을 사용해 여러 입력값을 한 번에 제출할 수 있습니다.
- 업로드한 이미지와 일반 파일의 정보를 화면에 표시할 수 있습니다.

## 예제 파일

```text
01_button-click.py
02_checkbox-slider.py
03_form-input.py
04_simple-survey-form.py
05_image-upload.py
06_file-upload.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\02_streamlit-ui-components\01_buttons-forms-and-controls\01_button-click.py
streamlit run .\02_streamlit-ui-components\01_buttons-forms-and-controls\05_image-upload.py
streamlit run .\02_streamlit-ui-components\01_buttons-forms-and-controls\06_file-upload.py
```

## 확인할 내용

- 버튼 클릭 후 결과가 표시되는가?
- 체크박스 값이 `True` 또는 `False`로 처리되는가?
- 슬라이더 값으로 조건문을 만들 수 있는가?
- 폼 제출 전과 제출 후의 화면 흐름을 구분할 수 있는가?
- 입력 컴포넌트와 결과 출력 영역이 화면에서 분리되어 있는가?
- 이미지 업로드 후 미리보기가 표시되는가?
- 일반 파일 업로드 후 파일 정보와 텍스트 미리보기가 표시되는가?

## 이후 과정과 연결

```text
폼 입력
-> 사용자 질문 입력 UI
-> API 요청 payload 구성
-> 백엔드 응답 표시
```

지금은 설문 폼을 만들지만, 이후에는 같은 구조를 사용해 사용자 질문, 로그인 정보, API 요청 옵션을 입력받습니다.
