# 04_oop-basic

이 단원에서는 객체지향 프로그래밍 전체를 깊게 다루지 않습니다. 이후 FastAPI, Pydantic, Supabase, 미니 프로젝트 코드에서 자주 만나는 부분만 학습합니다.

핵심은 “데이터와 동작을 하나로 묶는 방법”입니다.

## 이 단원에서 배우는 것

| 예제 | 핵심 내용 | 이후 연결되는 내용 |
| --- | --- | --- |
| 01_class_object_init_self.py | 클래스, 객체, `__init__`, `self`, 인스턴스 변수 | Pydantic 모델, 데이터 객체 이해 |
| 02_method_and_state.py | 메서드로 객체 상태 변경 | 사용자 상태, 작업 상태, 대화 상태 관리 |
| 03_dataclass_and_dict.py | `dataclass`, `dict` 변환 | JSON 저장, API 응답, 데이터 모델 |

## 실행 전 준비

이 폴더에서는 별도의 `.venv`를 만들지 않습니다. `01_python-git-foundation` 최상위에서 만든 공통 가상환경을 사용합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
```

## 실행 방법

```powershell
python .\02_python-advanced\04_oop-basic\01_class_object_init_self.py
python .\02_python-advanced\04_oop-basic\02_method_and_state.py
python .\02_python-advanced\04_oop-basic\03_dataclass_and_dict.py
```

## 상속은 이번 단원에서 깊게 다루지 않습니다

Pydantic의 `BaseModel`처럼 아래와 같은 문법을 만날 수 있습니다.

```python
class UserCreate(BaseModel):
    ...
```

이 문법은 “기존 클래스의 기능을 물려받아 새 클래스를 만든다”는 의미입니다. 하지만 이번 과정에서는 상속 설계를 깊게 다루지 않습니다. FastAPI와 Pydantic을 사용할 때 필요한 만큼만 짧게 설명하고, 실제 실습은 데이터 객체 중심으로 진행합니다.

## 핵심 확인

```text
클래스는 설계도입니다.
객체는 클래스로 만든 실제 데이터입니다.
self는 객체 자기 자신을 가리킵니다.
인스턴스 변수는 객체마다 따로 가지는 값입니다.
메서드는 클래스 안에 있는 함수입니다.
dataclass는 데이터를 담는 클래스를 짧게 만들 때 사용합니다.
```
