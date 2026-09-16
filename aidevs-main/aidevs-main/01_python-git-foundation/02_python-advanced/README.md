# 02_python-advanced

이 단원은 Python 고급 문법 전체를 배우는 과정이 아닙니다.

목표는 `02_supabase-ai-backend`의 FastAPI 코드로 넘어가기 전에 꼭 필요한 **함수 분리, import, 오류 처리, 테스트, 작은 프로젝트 구조**를 익히는 것입니다.

2일 안에 진행할 수 있도록 내용을 줄였고, 뒤 과정에서 바로 쓰지 않는 고급 문법은 제외했습니다.

## 이 단원에서 배우는 것

```text
함수로 코드 나누기
dict 데이터를 함수에 전달하기
직접 만든 파일을 import하기
try/except로 오류 처리하기
raise로 직접 검증 오류 만들기
JSON 파일을 안전하게 읽기
assert와 pytest로 함수 결과 확인하기
main.py, app/models.py, app/services.py, app/storage.py 구조 이해하기
dict와 dataclass object의 차이 맛보기
```

## 전체 구조

```text
02_python-advanced
├─ README.md
├─ SETUP.md
├─ .gitignore
├─ 00_references
├─ 01_function-and-import
├─ 02_exception-debugging
├─ 03_testing-basic
├─ 04_project-structure
├─ 10_labs
└─ 20_assignments
```

## 2일 기준 진행 흐름

| 구분 | 진행 내용 | 목표 |
| --- | --- | --- |
| 1일차 | 함수, dict 전달, import, 예외 처리, JSON 안전 읽기 | 한 파일 코드를 여러 함수와 파일로 나누고 오류를 읽을 수 있습니다. |
| 2일차 | assert, pytest, 작은 프로젝트 구조, JSON 저장, dataclass 맛보기 | 뒤 과정의 FastAPI 프로젝트 구조를 이해할 준비를 합니다. |

## 단원별 역할

| 단원 | 역할 |
| --- | --- |
| `00_references` | 2일 진행 흐름, 디버깅 체크리스트, 뒤 과정 연결을 정리합니다. |
| `01_function-and-import` | 함수와 import를 이용해 코드를 작게 나누는 방법을 배웁니다. |
| `02_exception-debugging` | 오류 메시지를 읽고 `try/except`, `raise`, JSON 오류 처리를 연습합니다. |
| `03_testing-basic` | `print` 확인에서 `assert`, `pytest` 확인으로 넘어갑니다. |
| `04_project-structure` | 같은 구조의 쉬운 예제와 확장 예제를 통해 `main.py`, `app`, `tests` 구조를 봅니다. |
| `10_labs` | 4개 단원에 맞춘 짧은 실습입니다. |
| `20_assignments` | 선택 과제입니다. 시간이 부족하면 생략해도 됩니다. |

## 제외한 내용

아래 내용은 뒤 과정에서 꼭 필요한 순간에 다시 설명합니다.

```text
복잡한 *args, **kwargs
callback 함수
decorator 직접 구현
상속, 캡슐화, 다형성 같은 OOP 설계
복잡한 package 구조
컴프리헨션 심화
datetime 심화
큰 종합 과제
```

FastAPI에서 `@app.get()` 같은 데코레이터를 만나지만, 이 단원에서는 직접 구현하지 않습니다. 지금은 “함수 위에 붙어 있는 표시가 FastAPI에게 endpoint 정보를 알려준다” 정도로만 이해하면 됩니다.

## 시작 방법

`02_python-advanced`는 `01_python-git-foundation`의 하위 단원입니다. 별도 `.venv`를 새로 만들지 않고 상위 과정의 `.venv`를 그대로 사용합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 예제 실행

```powershell
python .\02_python-advanced\01_function-and-import\01_function_basic_review.py
python .\02_python-advanced\02_exception-debugging\03_read_json_safely.py
python -m pytest .\02_python-advanced\03_testing-basic
python .\02_python-advanced\04_project-structure\01_simple_chat_project\main.py
python .\02_python-advanced\04_project-structure\02_simple_chat_project\main.py
```

## 다음 과정과의 연결

이 단원을 마치면 `02_supabase-ai-backend`에서 아래 구조를 볼 때 덜 낯설어집니다.

```text
FastAPI endpoint 함수
Pydantic 모델
service 함수
storage 또는 database 함수
pytest 테스트
.env와 설정 파일
JSON 응답 구조
```

완벽히 외우는 것이 목표가 아닙니다. 코드를 봤을 때 “어느 파일이 어떤 역할인지”를 구분할 수 있으면 충분합니다.
