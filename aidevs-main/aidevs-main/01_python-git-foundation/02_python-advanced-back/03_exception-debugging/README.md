# 03_exception-debugging

이 단원에서는 이후 과정에서 실제로 자주 만나는 오류만 중심으로 다룹니다.

입력값 변환, 반복 입력, 파일/JSON 읽기, 직접 검증 오류 발생, 오류 메시지 읽기를 익히면 FastAPI, Supabase, API 호출, 미니 프로젝트 디버깅으로 자연스럽게 이어질 수 있습니다.

## 이 단원에서 배우는 것

| 예제 | 핵심 내용 | 과정 연결 |
| --- | --- | --- |
| 01_try_except_value_error.py | `try/except`, `ValueError`, 기본값 반환 | 숫자 입력, API 파라미터 검증 |
| 02_safe_input_loop.py | 잘못 입력하면 다시 입력받기 | CLI 실습, 미니 프로젝트 |
| 03_file_json_error.py | `FileNotFoundError`, `json.JSONDecodeError` | 파일 저장, JSON 설정, 로그 저장 |
| 04_raise_validation.py | 직접 오류 발생시키기 | 서비스 로직 검증, Pydantic 전 단계 |
| 05_debugging_traceback_basic.py | 오류 종류, 메시지, 줄 번호 읽기 | Codex 리뷰, 디버깅, 테스트 실패 분석 |

## 실행 전 준비

이 폴더에서는 별도의 `.venv`를 만들지 않습니다. `01_python-git-foundation` 최상위에서 만든 공통 가상환경을 사용합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
```

## 실행 방법

```powershell
python .\02_python-advanced\03_exception-debugging\01_try_except_value_error.py
python .\02_python-advanced\03_exception-debugging\02_safe_input_loop.py
python .\02_python-advanced\03_exception-debugging\03_file_json_error.py
python .\02_python-advanced\03_exception-debugging\04_raise_validation.py
python .\02_python-advanced\03_exception-debugging\05_debugging_traceback_basic.py
```

## 핵심 구조

```python
try:
    # 오류가 날 수 있는 코드
    number = int("abc")
except ValueError:
    # 오류가 났을 때 실행할 코드
    print("숫자로 바꿀 수 없습니다.")
```

## else와 finally는 언제 쓰나요?

`else`와 `finally`도 예외 처리 문법에 포함됩니다. 다만 이번 과정에서는 자주 쓰는 `try/except`를 먼저 익히는 것이 더 중요합니다.

```text
else    : try 블록에서 오류가 없을 때만 실행합니다.
finally : 오류가 있든 없든 마지막에 항상 실행합니다.
```

파일 닫기, 네트워크 연결 정리처럼 “마지막에 반드시 정리해야 하는 일”이 있을 때 `finally`를 사용할 수 있습니다. 하지만 이번 과정의 대부분 예제에서는 `with`, `Path`, 라이브러리 기능이 정리를 대신해 주므로 깊게 다루지 않습니다.

## 이전 과정과의 연결

```text
01_python-basic/03_condition-basic
-> 입력값이 조건에 맞는지 확인합니다.

01_python-basic/04_loop-basic
-> 잘못 입력하면 다시 입력받는 흐름을 만듭니다.

01_python-basic/07_file-data-basic
-> 파일과 JSON을 읽을 때 생기는 오류를 처리합니다.

01_python-basic/20_assignments/assignment07_basic-python-final.md
-> 저장 파일이 없거나 데이터가 깨진 상황을 처리합니다.
```

## 주의할 점

모든 오류를 아래처럼 숨기는 방식은 좋지 않습니다.

```python
try:
    ...
except:
    pass
```

오류를 숨기면 프로그램이 왜 잘못되었는지 찾기 어렵습니다. 가능하면 `ValueError`, `FileNotFoundError`, `json.JSONDecodeError`처럼 구체적인 오류 타입을 사용합니다.
