# 04_project-structure

이 단원에서는 작은 Python 프로그램을 여러 파일로 나누어 봅니다.

목표는 복잡한 설계가 아니라, 뒤 과정의 FastAPI 프로젝트를 보기 전에 아래 역할을 구분하는 것입니다.

```text
main.py       실행 시작점
models.py     데이터 모양
services.py   핵심 처리 로직
storage.py    JSON 저장/읽기, 02 예제에서 사용
tests         테스트
```

## 예제 프로젝트 흐름

처음부터 저장과 예외 처리까지 모두 보면 복잡할 수 있습니다. 그래서 같은 형태의 프로젝트를 두 단계로 봅니다.

| 예제 | 역할 | 포함 내용 |
| --- | --- | --- |
| `01_simple_chat_project` | 구조를 먼저 익히는 단순 버전 | `main.py`, `models.py`, `services.py`, `tests` |
| `02_simple_chat_project` | 검증과 저장을 추가한 확장 버전 | 01 구조 + `storage.py`, JSON 저장, 입력 검증, 예외 처리 |

## 01_simple_chat_project 구조

```text
01_simple_chat_project
├─ README.md
├─ main.py
├─ app
│  ├─ __init__.py
│  ├─ models.py
│  └─ services.py
└─ tests
   └─ test_basic_services.py
```

## 02_simple_chat_project 구조

```text
02_simple_chat_project
├─ README.md
├─ main.py
├─ app
│  ├─ __init__.py
│  ├─ models.py
│  ├─ services.py
│  └─ storage.py
└─ tests
   └─ test_validated_services.py
```

## 실행 방법

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\04_project-structure\01_simple_chat_project\main.py
python -m pytest .\02_python-advanced\04_project-structure\01_simple_chat_project

python .\02_python-advanced\04_project-structure\02_simple_chat_project\main.py
python -m pytest .\02_python-advanced\04_project-structure\02_simple_chat_project
```

## object는 여기서 얼마나 배우나요?

이 단원에서는 object를 깊게 배우지 않습니다.

딱 아래 정도만 이해하면 됩니다.

```text
dict:
  간단한 데이터를 key/value로 담습니다.
  JSON 저장에 바로 쓰기 쉽습니다.

dataclass object:
  관련 데이터를 하나의 object로 묶습니다.
  어떤 값이 들어가는지 코드에서 더 잘 보입니다.
  나중에 Pydantic BaseModel을 이해하는 데 도움이 됩니다.
```

상속, 캡슐화, 다형성은 다루지 않습니다.
