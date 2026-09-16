# 01_python-basic

파이썬을 처음 배우는 사람을 위한 기초 과정입니다.

이 과정의 목표는 문법을 많이 외우는 것이 아니라, **코드를 직접 실행하고, 오류를 읽고, 작은 프로그램을 만들 수 있는 감각**을 익히는 것입니다.

## 이 과정에서 배우는 것

```text
Python 실행 환경
변수와 자료형
문자열
입력과 출력
조건문
반복문
리스트와 딕셔너리
함수 기초
파일 저장과 읽기
기초 종합 과제
```

## 전체 구조

```text
01_python-basic
├─ README.md
├─ SETUP.md
├─.gitignore
├─ 00_references
├─ 01_python-start
├─ 02_variables-and-data-types
├─ 03_condition-basic
├─ 04_loop-basic
├─ 05_data-structures-basic
├─ 06_function-basic
├─ 07_file-data-basic
├─ 10_labs
└─ 20_assignments
```

## 전체 자료 구성 순서

아래 순서는 폴더가 배치된 전체 자료 순서입니다. 실제 수업에서는 바로 아래의 `필수/선택 기준`에 따라 필요한 부분을 먼저 진행합니다.

```text
00_references
-> 01_python-start
-> 02_variables-and-data-types
-> 03_condition-basic
-> 04_loop-basic
-> 05_data-structures-basic
-> 06_function-basic
-> 07_file-data-basic
-> 10_labs
-> 20_assignments
```

## 필수/선택 기준

`01_python-basic`에서는 기초 문법을 빠르게 훑는 것보다, 직접 실행하고 작은 프로그램으로 연결하는 경험이 더 중요합니다.

| 구분 | 단원 | 기준 |
| --- | --- | --- |
| 필수 | `01_python-start` ~ `07_file-data-basic` | 핵심 예제를 실행하고 값과 조건을 바꿔 봅니다. |
| 필수 | `10_labs` 일부 | 수업 중 핵심 문법을 직접 입력해 봅니다. |
| 필수 | `20_assignments`의 종합 과제 | 주제와 요구 기능이 있는 작은 프로그램 1개를 완성합니다. |
| 선택 | `20_assignments`의 단원별 과제 | 부족한 문법을 보충할 때 선택해서 풉니다. |

## 단원별 핵심 내용

| 단원 | 내용 |
| --- | --- |
| 00_references | 학습 로드맵, 파이썬 용어, 초보자 오류 가이드 |
| 01_python-start | Python 실행, `print`, 주석, 입력과 출력 |
| 02_variables-and-data-types | 변수, 숫자, 문자열, 불 자료형, 형 변환, 타입 힌트 기초 |
| 03_condition-basic | `if`, `elif`, `else`, `match-case`, 비교 연산자, 논리 연산자 |
| 04_loop-basic | `for`, `while`, `while True`, `range`, `break`, `continue` |
| 05_data-structures-basic | 리스트, 튜플, 딕셔너리, 세트, 반복문과 자료구조, 중첩 API 응답 형태 |
| 06_function-basic | 함수 정의, 매개변수, 반환값, 기본값, 키워드 인자, 자료구조 처리, 코드 정리 |
| 07_file-data-basic | 파일 경로, JSON dict/list 저장과 읽기, 텍스트/CSV 보충 예제 |
| 10_labs | 단원별 실습 문제 |
| 20_assignments | 기초 과제 |

## 처음 시작하는 방법

`01_python-basic`은 `01_python-git-foundation`의 하위 단원이므로 별도의 `.venv`를 새로 만들지 않습니다. `01_python-git-foundation` 최상위에 이미 만든 `.venv`를 그대로 사용합니다.

PowerShell에서 아래 순서로 실행합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
pip install -r requirements.txt
```

프롬프트 앞에 `(.venv)`가 보이면 가상환경이 활성화된 것입니다.

`01_python-basic`은 Python 표준 라이브러리만 사용하므로 이 하위 폴더에는 별도의 `requirements.txt`를 두지 않습니다. 위 명령의 `requirements.txt`는 `01_python-git-foundation` 최상위의 공통 패키지 설치 파일입니다.

## 첫 예제 실행

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
python .\01_python-basic\01_python-start\01_hello_python.py
```

정상 실행되면 화면에 인사말과 간단한 계산 결과가 출력됩니다.

## 초보자가 꼭 기억할 것

### 1. 코드는 위에서 아래로 실행됩니다

파이썬은 파일의 첫 줄부터 마지막 줄까지 순서대로 실행합니다.

```python
print("첫 번째")
print("두 번째")
print("세 번째")
```

### 2. 들여쓰기는 문법입니다

파이썬에서 들여쓰기는 보기 좋게 만드는 장식이 아니라 문법입니다.

```python
if True:
 print("조건문 안쪽입니다.")
```

### 3. 오류 메시지는 힌트입니다

오류가 나면 당황하지 말고 아래 순서로 봅니다.

```text
1. 어떤 파일에서 오류가 났는가?
2. 몇 번째 줄에서 오류가 났는가?
3. 오류 이름이 무엇인가?
4. 오류 메시지가 무엇을 말하는가?
```

예를 들어 `NameError`는 이름을 찾을 수 없다는 뜻이고, `SyntaxError`는 문법이 틀렸다는 뜻입니다.

### 4. 외우기보다 많이 실행합니다

처음에는 모든 문법을 외우려고 하지 않아도 됩니다.

```text
코드 입력
-> 실행
-> 결과 확인
-> 값 바꿔보기
-> 오류가 나면 이유 찾기
```

이 과정을 반복하면 자연스럽게 익숙해집니다.

## 02_python-advanced와의 차이

```text
01_python-basic:
 파이썬 문법과 작은 프로그램 작성

02_python-advanced:
 함수 심화, 모듈, 예외 처리, 클래스, API, 테스트, 프로젝트 구조
```

따라서 이 과정에서는 어렵고 복잡한 설계보다 **기초 문법을 정확히 이해하고 작은 프로그램을 완성하는 경험**에 집중합니다.

## 추천 학습 방식

1. 각 단원 README를 먼저 읽습니다.
2. 예제 `.py` 파일을 실행합니다.
3. 예제 안의 값을 바꿔봅니다.
4. `10_labs`의 실습을 풉니다.
5. 필수 과제를 먼저 완성하고, 시간이 충분하면 선택 과제로 확장합니다.

## 참고 방향

이 과정은 파이썬 입문서에서 자주 다루는 기초 흐름을 참고하되, 교재 본문이나 문제를 그대로 복제하지 않고 수업용 예제와 과제로 새롭게 구성했습니다.
