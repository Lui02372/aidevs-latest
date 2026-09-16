# Lab 09. 프로젝트 구조 만들기

이 실습에서는 하나의 Python 프로그램을 여러 파일로 나누어 구성합니다.

목표는 큰 프로젝트를 만드는 것이 아니라, 이후 FastAPI, Supabase, LLM API 예제를 볼 때 파일 역할을 구분할 수 있도록 연습하는 것입니다.

## 실습 목표

```text
1. main.py의 역할을 설명할 수 있습니다.
2. config.py에 설정값을 분리할 수 있습니다.
3. models.py에 데이터 모양을 만드는 함수를 둘 수 있습니다.
4. services.py에 핵심 처리 로직을 둘 수 있습니다.
5. storage.py에 저장 역할을 분리할 수 있습니다.
```

## 실습 1. 기본 폴더 구조 만들기

아래 구조를 만듭니다.

```text
my_chat_project
├─ main.py
└─ app
   ├─ __init__.py
   ├─ config.py
   ├─ models.py
   ├─ services.py
   └─ storage.py
```

각 파일의 역할은 다음과 같습니다.

```text
main.py:
  프로그램을 실행하는 시작점입니다.

config.py:
  모델명, 기본 사용자명 같은 설정값을 관리합니다.

models.py:
  응답 데이터를 dict 형태로 만드는 함수를 둡니다.

services.py:
  질문 검증, 답변 생성 같은 핵심 로직을 둡니다.

storage.py:
  응답 데이터를 저장하는 함수를 둡니다.
```

## 실습 2. 설정값 분리하기

`app/config.py`에 아래 값을 작성합니다.

```python
DEFAULT_LLM_MODEL = "practice-chat-model"
DEFAULT_USER_NAME = "학습자"
```

## 실습 3. 데이터 모양 만들기

`app/models.py`에 챗봇 응답 dict를 만드는 함수를 작성합니다.

```python
def create_chat_reply(user_name: str, question: str, answer: str, model: str) -> dict:
    return {
        "user_name": user_name,
        "question": question,
        "answer": answer,
        "model": model,
    }
```

## 실습 4. 서비스 로직 분리하기

`app/services.py`에 질문을 정리하고 응답을 만드는 함수를 작성합니다.

```python
from app.config import DEFAULT_LLM_MODEL
from app.models import create_chat_reply


def build_chat_reply(user_name: str, question: str) -> dict:
    clean_question = question.strip()

    if clean_question == "":
        raise ValueError("질문은 비워둘 수 없습니다.")

    answer = "프로젝트 구조를 나누면 코드를 이해하고 수정하기 쉬워집니다."

    return create_chat_reply(
        user_name=user_name,
        question=clean_question,
        answer=answer,
        model=DEFAULT_LLM_MODEL,
    )
```

## 실습 5. 저장 함수 분리하기

`app/storage.py`에 임시 저장소와 저장 함수를 작성합니다.

```python
CHAT_LOGS: list[dict] = []


def save_chat_log(reply: dict) -> dict:
    CHAT_LOGS.append(reply)

    return {
        "status": "saved",
        "total_logs": len(CHAT_LOGS),
        "question": reply["question"],
    }
```

## 실습 6. main.py에서 연결하기

`main.py`에서 각 파일의 함수를 import해 실행합니다.

```python
from app.config import DEFAULT_USER_NAME
from app.services import build_chat_reply
from app.storage import save_chat_log


def main() -> None:
    reply = build_chat_reply(
        user_name=DEFAULT_USER_NAME,
        question="프로젝트 구조는 왜 필요한가요?",
    )

    saved_log = save_chat_log(reply)

    print(reply)
    print(saved_log)


if __name__ == "__main__":
    main()
```

## 실행 방법

프로젝트 폴더의 상위 폴더에서 실행합니다.

```powershell
python .\my_chat_project\main.py
```

## 제출 기준

```text
1. app 폴더 안에 __init__.py가 있어야 합니다.
2. config.py, models.py, services.py, storage.py가 역할별로 나누어져 있어야 합니다.
3. main.py는 세부 로직을 직접 많이 작성하지 않고 함수를 import해서 사용해야 합니다.
4. 실행 결과에 질문, 답변, 저장 상태가 출력되어야 합니다.
5. README 또는 메모 파일에 각 파일의 역할을 한 줄씩 정리해야 합니다.
```

## 확인 질문

```text
1. main.py에 모든 코드를 몰아넣으면 어떤 문제가 생길까요?
2. config.py에는 어떤 값을 넣는 것이 좋을까요?
3. services.py와 storage.py는 왜 분리하나요?
4. 지금 만든 storage.py는 이후 어떤 기술과 연결될까요?
5. FastAPI 프로젝트로 바꾸면 어떤 파일이 추가될까요?
```
