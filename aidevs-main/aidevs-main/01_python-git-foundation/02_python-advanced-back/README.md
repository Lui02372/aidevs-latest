# 02_python-advanced

`01_python-basic`을 마친 뒤, 파이썬 코드를 더 구조적으로 작성하는 방법을 배우는 과정입니다.

이 과정의 목표는 단순 문법을 넘어서 **함수, 모듈, 예외 처리, 테스트, 프로젝트 구조**를 익히고 이후 FastAPI 백엔드 코드를 읽고 수정할 수 있게 되는 것입니다.

## 이 과정에서 배우는 것

```text
함수 심화
모듈과 패키지
상위 과정 `.venv`와 공통 패키지 관리
예외 처리와 디버깅
클래스와 객체지향 프로그래밍 맛보기
컴프리헨션을 이용한 list/dict 데이터 변환
JSON/날짜/경로 처리
테스트와 코드 품질
파이썬 프로젝트 구조
선택 종합 과제
```

위 목록을 모두 같은 깊이로 다루지는 않습니다. 다음 과정에서 바로 필요한 내용은 필수로 진행하고, 나머지는 선택/보충 자료로 둡니다.

## 전체 구조

```text
02_python-advanced
├─ README.md
├─ SETUP.md
├─ .gitignore
├─ 00_references
├─ 01_function-advanced
├─ 02_module-package-venv
├─ 03_exception-debugging
├─ 04_oop-basic
├─ 05_comprehension-iterator
├─ 06_data-processing-advanced
├─ 08_testing-code-quality
├─ 09_project-structure
├─ 10_labs
└─ 20_assignments
```

## 전체 자료 구성 순서

아래 순서는 전체 참고 자료의 배치 순서입니다. 모든 단원을 같은 깊이로 진행한다는 뜻은 아니며, 실제 수업에서는 `필수/선택 기준`을 먼저 따릅니다.

```text
00_references
-> 01_function-advanced
-> 02_module-package-venv
-> 03_exception-debugging
-> 04_oop-basic
-> 05_comprehension-iterator
-> 06_data-processing-advanced
-> 08_testing-code-quality
-> 09_project-structure
-> 10_labs
-> 20_assignments
```

## 필수/선택 기준

| 구분 | 단원 | 진행 기준 |
| --- | --- | --- |
| 필수 | `01_function-advanced` | `*args`, `**kwargs`, dict 언패킹, 검증 함수 전달을 이해합니다. |
| 필수 | `02_module-package-venv` | 직접 만든 모듈을 import하고, 공통 `.venv`를 확인합니다. |
| 필수 | `03_exception-debugging` | `try/except`, `raise`, traceback 읽기를 익힙니다. |
| 필수 | `08_testing-code-quality` | pytest로 작은 함수 테스트를 실행합니다. |
| 필수 | `09_project-structure` | `main.py`, `app`, `services`, `tests`처럼 역할별 구조를 이해합니다. |
| 축소 | `04_oop-basic` | 클래스 전체 설계보다 `class`, `self`, `dataclass` 모양만 확인합니다. |
| 축소 | `06_data-processing-advanced` | `pathlib`, JSON 저장, 날짜/시간 기록 중심으로 봅니다. |
| 선택 | `05_comprehension-iterator` | list/dict comprehension을 이용한 데이터 변환 복습용으로 봅니다. |
| 선택 | `20_assignments` | 시간이 충분할 때 구조화 연습으로 진행합니다. |

## 단원별 핵심 내용

| 단원 | 내용 |
| --- | --- |
| 00_references | 고급 과정 로드맵, 프로젝트 사고방식, 오류/디버깅 가이드 |
| 01_function-advanced | `*args`, `**kwargs`, 언패킹, 함수 전달, 데코레이터 맛보기, LLM 요청 데이터 구성 |
| 02_module-package-venv | 표준 라이브러리 `import`, `from import`, 별칭 import, 직접 만든 모듈, 패키지 구조, 공통 `.venv`와 외부 패키지 확인 |
| 03_exception-debugging | `try/except`, `ValueError`, 안전한 반복 입력, 파일/JSON 오류, `raise`, traceback 읽기 |
| 04_oop-basic | 클래스, 객체, `__init__`, `self`, `dataclass` 맛보기 |
| 05_comprehension-iterator | list/dict comprehension, API 응답 형태의 목록 변환, id 기반 조회 구조 |
| 06_data-processing-advanced | `pathlib` 파일 경로, JSON 설정/응답 저장, 날짜/시간 기록 |
| 08_testing-code-quality | `assert`, pytest 기초, 예외 테스트, API 응답 dict 구조 테스트, 리팩토링 확인 |
| 09_project-structure | `main.py`, package, config, README, Git 관리 |
| 20_assignments | AI 챗봇 요청/응답 관리 도구 선택 과제 |

## 처음 시작하는 방법

`02_python-advanced`는 `01_python-git-foundation`의 하위 단원이므로 별도의 `.venv`를 새로 만들지 않습니다. `01_python-git-foundation` 최상위에 이미 만든 `.venv`를 그대로 사용합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
pip install -r requirements.txt
python .\02_python-advanced\01_function-advanced\01_args_kwargs_api_options.py
```

`02_python-advanced`는 하위 단원이므로 별도의 `.venv`와 `requirements.txt`를 두지 않습니다. `pytest` 같은 고급 단원 패키지도 `01_python-git-foundation` 최상위 `requirements.txt`에서 함께 관리합니다.

## 01_python-basic과의 차이

```text
01_python-basic:
 문법을 배우고 작은 프로그램을 만들기

02_python-advanced:
 코드를 함수, 모듈, 클래스, 테스트, 프로젝트 구조로 정리하기
```

## 초보자에서 다음 단계로 넘어갈 때 중요한 생각

### 1. 코드를 나누는 이유를 이해합니다

작은 예제는 한 파일에 써도 됩니다. 하지만 프로그램이 커지면 역할별로 나누어야 합니다.

```text
입력 처리
데이터 처리
파일 저장
화면 출력
테스트
```

### 2. 오류를 미리 예상합니다

사용자가 잘못 입력할 수 있고, 파일이 없을 수 있고, JSON 파일이 깨져 있을 수 있습니다. 고급 과정에서는 이런 상황을 코드에 반영합니다.

### 3. 재사용 가능한 코드를 만듭니다

함수, 클래스, 모듈은 코드를 다시 쓰기 쉽게 만드는 도구입니다.

### 4. 실행뿐 아니라 검증까지 생각합니다

프로그램이 한 번 실행되는 것보다 중요한 것은, 여러 입력에서도 안정적으로 동작하는지 확인하는 것입니다.

## 추천 학습 방식

1. 각 단원 README를 읽습니다.
2. 예제 코드를 실행합니다.
3. 예제 값을 바꿔봅니다.
4. `10_labs` 실습을 풉니다.
5. 필수 단원을 먼저 마친 뒤, 시간이 충분하면 `20_assignments` 선택 과제로 확장합니다.
