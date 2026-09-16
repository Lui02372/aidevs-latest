# 09_project-structure

이 단원에서는 작은 Python 프로그램을 여러 파일로 나누어 관리하는 방법을 배웁니다.

앞 단원까지는 하나의 파일 안에서 함수, 클래스, 예외 처리, API 호출, 테스트를 연습했습니다. 이제부터는 FastAPI, Supabase, LLM API 예제처럼 파일이 많아지는 프로젝트를 다루게 됩니다. 그래서 코드 역할을 나누는 기준을 먼저 익히는 것이 중요합니다.

## 이 단원에서 배우는 것

| 파일 또는 폴더 | 역할 | 이후 과정 연결 |
| --- | --- | --- |
| `main.py` | 프로그램 시작점 | FastAPI의 `main.py`, Streamlit의 `app.py` 이해 |
| `app/config.py` | 설정값 관리 | API URL, 모델명, 환경변수 관리 |
| `app/models.py` | 데이터 모양 정의 | Pydantic 모델, API Request/Response 구조 |
| `app/services.py` | 핵심 처리 로직 | LLM 호출, 질문 처리, 서비스 함수 분리 |
| `app/storage.py` | 저장소 역할 | Supabase 저장, 로그 저장 구조 이해 |
| `app/__init__.py` | 패키지 표시 | 폴더를 import 가능한 Python 패키지로 인식 |

## 권장 구조

```text
sample_project
├─ main.py
└─ app
   ├─ __init__.py
   ├─ config.py
   ├─ models.py
   ├─ services.py
   └─ storage.py
```

이 구조는 작은 예제이지만 실제 백엔드 프로젝트와 연결됩니다.

```text
설정값(config)
   ↓
데이터 구조(models)
   ↓
서비스 로직(services)
   ↓
저장 처리(storage)
   ↓
실행 시작점(main)
```

## 실행 전 준비

이 폴더에서는 별도의 `.venv`를 만들지 않습니다. `01_python-git-foundation` 최상위에서 만든 공통 가상환경을 사용합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
```

## 실행 방법

```powershell
python .\02_python-advanced\09_project-structure\sample_project\main.py
```

## 핵심 정리

```text
main.py:
  프로그램을 시작하는 파일입니다. 여러 함수를 직접 모두 작성하기보다 필요한 함수를 import해서 실행합니다.

config.py:
  모델명, API 주소, 기본 사용자명처럼 설정에 가까운 값을 모아둡니다.

models.py:
  데이터가 어떤 key를 가져야 하는지 정리합니다. 이후 Pydantic 모델을 배우면 이 역할이 더 명확해집니다.

services.py:
  실제 업무 로직을 작성합니다. 질문을 검증하거나 답변을 만드는 함수가 여기에 들어갑니다.

storage.py:
  데이터를 저장하는 함수를 둡니다. 지금은 리스트에 저장하지만, 이후에는 Supabase 테이블 저장으로 연결됩니다.
```

## 프로젝트 구조를 나누는 이유

```text
1. 파일이 길어지는 것을 막을 수 있습니다.
2. 설정, 데이터 구조, 처리 로직, 저장 로직을 따로 볼 수 있습니다.
3. 테스트할 함수를 찾기 쉬워집니다.
4. FastAPI 프로젝트로 넘어갈 때 구조를 이해하기 쉽습니다.
5. 여러 기능을 추가해도 기존 코드를 덜 건드리게 됩니다.
```

## 확인 질문

```text
1. main.py는 어떤 역할을 하나요?
2. services.py와 storage.py를 나누는 이유는 무엇인가요?
3. config.py에 API Key를 직접 적어도 될까요?
4. app 폴더 안에 __init__.py가 있으면 무엇이 좋아지나요?
5. 이 구조를 FastAPI 프로젝트에 적용하면 어떤 파일이 추가될까요?
```
