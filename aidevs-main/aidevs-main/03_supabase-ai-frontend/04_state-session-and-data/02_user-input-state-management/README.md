# 02_user-input-state-management

사용자 입력값과 화면 선택값을 상태로 관리하는 방법을 학습합니다.

이 단원에서는 단순 입력을 넘어서 프로필 정보, 필터 조건, 단계 이동, 단계형 입력처럼 화면 흐름에 따라 유지되어야 하는 값을 관리합니다. 먼저 `03_simple-step-progress.py`에서 `step` 값만으로 화면이 바뀌는 흐름을 익힙니다. 이후 `04_simple-multi-step-form.py`에서 간단한 단계형 입력을 만들고, `05_multi-step-form.py`에서 입력 중 값과 확정 값을 분리한 안정적인 구조로 확장합니다.

## 학습 목표

- 여러 입력값을 하나의 딕셔너리 상태로 저장할 수 있다.
- 필터 조건을 상태에 저장하고 다시 사용할 수 있다.
- `step` 상태로 화면 단계를 바꿀 수 있다.
- 간단한 단계형 입력 화면에서 이전 단계 입력값을 유지할 수 있다.
- 입력 중 값과 확정 값을 분리한 단계형 입력 구조를 설명할 수 있다.
- 이후 로그인 화면과 대화 이력 화면에서 필요한 상태 관리 방식을 설명할 수 있다.

## 예제 파일

```text
01_profile-state.py
02_filter-state.py
03_simple-step-progress.py
04_simple-multi-step-form.py
05_multi-step-form.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\04_state-session-and-data\02_user-input-state-management\03_simple-step-progress.py
```

## 확인 내용

- 저장 버튼을 누른 뒤 입력값이 상태에 반영되는가?
- 필터 적용 전과 후의 상태가 구분되는가?
- `step` 값만으로 화면이 1단계, 2단계, 3단계로 바뀌는가?
- 단계형 입력에서 이전 단계 값이 유지되는가?
- 입력 중 값과 확정 저장된 값의 차이를 설명할 수 있는가?

## 다음 단원 연결

다음 단원에서는 이 상태 관리 개념을 로그인 token과 로그인 여부 관리로 확장합니다.
