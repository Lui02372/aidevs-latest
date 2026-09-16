# Assignment 01. Python 고급 종합 과제

## 과제 주제

간단한 **AI 챗봇 요청/응답 관리 도구**를 만듭니다.

실제 LLM API를 호출하지 않아도 됩니다. 이번 과제의 핵심은 AI 모델 API를 호출하기 전 단계에서 필요한 Python 구조를 연습하는 것입니다.

```text
사용자 질문 입력
-> 질문 정리 및 검증
-> 임시 답변 생성
-> 응답 dict 생성
-> JSON 저장
-> pytest로 핵심 함수 검증
```

## 해야 할 일

| 순서 | 해야 할 일 | 설명 |
| --- | --- | --- |
| 1 | 질문 입력 흐름 만들기 | 사용자가 질문을 입력하면 앞뒤 공백을 정리합니다. |
| 2 | 질문 검증 | 빈 질문이면 `ValueError`를 발생시키고 사용자에게 안내합니다. |
| 3 | 임시 답변 생성 | 실제 LLM 대신 고정된 규칙으로 연습용 답변을 만듭니다. |
| 4 | 응답 dict 생성 | `question`, `answer`, `model`, `created_at` 값을 가진 dict를 만듭니다. |
| 5 | JSON 저장/읽기 | 응답 기록을 JSON 파일로 저장하고 다시 읽습니다. |
| 6 | 테스트 작성 | 질문 정리, 빈 질문 검증, 응답 dict 구조를 pytest로 확인합니다. |
| 7 | 프로젝트 구조 분리 | `main.py`, `app/services.py`, `app/storage.py`, `tests`처럼 역할을 나눕니다. |

## 과제 목표

```text
1. 함수, 모듈, 클래스, 예외 처리, 데이터 저장, 테스트를 하나의 흐름으로 연결합니다.
2. 이후 FastAPI 백엔드와 Supabase 저장 구조로 확장하기 쉬운 형태를 만듭니다.
3. main.py에 모든 코드를 몰아넣지 않고 파일 역할을 분리합니다.
4. 실행 방법과 파일 역할을 README에 정리합니다.
```

## 권장 프로젝트 구조

```text
advanced_chat_manager
├─ README.md
├─ main.py
├─ app
│  ├─ __init__.py
│  ├─ config.py
│  ├─ models.py
│  ├─ services.py
│  └─ storage.py
└─ tests
   └─ test_services.py
```

각 파일의 역할은 다음과 같습니다.

```text
main.py:
  프로그램을 실행하는 시작점입니다.

app/config.py:
  기본 모델명, 저장 파일 경로 같은 설정값을 관리합니다.

app/models.py:
  질문과 응답 데이터를 dict 형태로 만드는 함수를 둡니다.

app/services.py:
  질문 정리, 질문 검증, 임시 답변 생성 같은 핵심 로직을 둡니다.

app/storage.py:
  JSON 파일 저장과 읽기 함수를 둡니다.

tests/test_services.py:
  pytest로 핵심 서비스 함수를 검증합니다.
```

## 필수 기능

### 1. 질문 정리

사용자 질문 앞뒤 공백을 제거하는 함수를 만듭니다.

```python
def normalize_question(question: str) -> str:
    return question.strip()
```

### 2. 질문 검증

질문이 비어 있으면 `ValueError`를 발생시킵니다.

```python
def validate_question(question: str) -> None:
    if question.strip() == "":
        raise ValueError("질문은 비워둘 수 없습니다.")
```

### 3. 응답 dict 생성

아래 key를 가진 dict를 생성합니다.

```text
question
answer
model
created_at
```

예시:

```python
{
    "question": "FastAPI란?",
    "answer": "FastAPI는 Python 웹 API 프레임워크입니다.",
    "model": "practice-chat-model",
    "created_at": "2026-06-22T10:30:00+00:00",
}
```

### 4. 데이터 저장

응답 dict를 JSON 파일로 저장합니다.

기준:

```text
1. data 폴더가 없으면 코드에서 생성합니다.
2. ensure_ascii=False를 사용해 한글이 깨지지 않게 저장합니다.
3. indent=2를 사용해 사람이 읽기 좋은 형태로 저장합니다.
4. 저장한 파일을 다시 읽어 내용이 유지되는지 확인합니다.
```

### 5. 테스트 작성

pytest 테스트를 최소 3개 작성합니다.

필수 테스트:

```text
1. normalize_question이 앞뒤 공백을 제거하는지 테스트합니다.
2. validate_question이 빈 질문에서 ValueError를 발생시키는지 테스트합니다.
3. 응답 dict에 question, answer, model, created_at key가 있는지 테스트합니다.
```

## 선택 기능

시간이 충분하면 아래 기능 중 하나를 추가합니다.

```text
1. 질문 목록을 여러 개 처리하는 기능
2. list comprehension으로 빈 질문을 제외하는 기능
3. dict comprehension으로 질문 id 기반 조회 구조를 만드는 기능
4. dataclass를 사용해 응답 데이터를 표현하는 기능
```

## 실행 방법 작성 기준

README에는 아래 내용을 포함합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
python .\02_python-advanced\20_assignments\advanced_chat_manager\main.py
python -m pytest .\02_python-advanced\20_assignments\advanced_chat_manager
```

프로젝트 위치를 다르게 만들었다면 실제 폴더 위치에 맞게 명령을 수정합니다.

## 제출 기준

```text
1. 권장 프로젝트 구조와 비슷하게 파일이 나누어져 있어야 합니다.
2. 함수가 최소 3개 이상 있어야 합니다.
3. 클래스 또는 dataclass는 선택 사항입니다. 시간이 부족하면 함수와 dict 중심으로 작성해도 됩니다.
4. ValueError 처리 또는 raise 예제가 있어야 합니다.
5. JSON 저장 기능이 있어야 합니다.
6. pytest 테스트가 최소 3개 이상 있어야 합니다.
7. README에 실행 방법과 파일 역할이 정리되어 있어야 합니다.
```

## 점검 체크리스트

```text
[ ] main.py가 실행 시작점 역할만 담당하나요?
[ ] config.py에 기본 설정값이 분리되어 있나요?
[ ] services.py에 핵심 로직이 분리되어 있나요?
[ ] storage.py에 저장 로직이 분리되어 있나요?
[ ] 빈 질문이 들어왔을 때 프로그램이 갑자기 종료되지 않나요?
[ ] 저장된 JSON 파일을 열었을 때 한글이 깨지지 않나요?
[ ] pytest 실행 결과가 모두 통과하나요?
[ ] README만 보고 실행할 수 있나요?
```

## 이후 과정과의 연결

```text
이 과제의 main.py 흐름은 이후 FastAPI 엔드포인트 흐름으로 연결됩니다.
이 과제의 response dict는 이후 Pydantic Response Model로 연결됩니다.
이 과제의 JSON 저장은 이후 Supabase 테이블 저장으로 연결됩니다.
이 과제의 pytest 테스트는 이후 API 테스트와 리팩토링 검증으로 연결됩니다.
```
