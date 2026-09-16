# Lab 02. 모듈, 패키지, 가상환경

이 실습에서는 직접 만든 모듈과 패키지를 `import`해서 사용하는 방법을 연습합니다.

## 실습 목표

```text
1. 표준 라이브러리와 직접 만든 모듈의 차이를 설명할 수 있습니다.
2. import module 방식과 from module import name 방식을 구분할 수 있습니다.
3. 패키지 폴더 안의 모듈을 가져와 사용할 수 있습니다.
4. 공통 .venv에 설치된 외부 패키지를 확인할 수 있습니다.
```

## 실습 1. 표준 라이브러리 사용하기

`datetime`과 `pathlib`를 사용해 오늘 날짜와 현재 폴더 경로를 출력합니다.

```python
from pathlib import Path
import datetime as dt

print("현재 폴더:", Path.cwd())
print("오늘 날짜:", dt.date.today())
```

## 실습 2. 직접 만든 모듈 사용하기

`my_text_tools.py` 파일을 만들고 문자열 처리 함수를 작성합니다.

```python
def make_title(text: str) -> str:
    return text.strip().title()
```

그 다음 `use_text_tools.py`에서 가져와 실행합니다.

```python
import my_text_tools

result = my_text_tools.make_title("  hello python  ")
print(result)
```

## 실습 3. 패키지 만들기

`api_helpers` 폴더를 만들고 아래 구조를 구성합니다.

```text
api_helpers
├─ __init__.py
├─ formatter.py
└─ validators.py
```

`validators.py`에는 질문 검증 함수를 작성합니다.

```python
def is_valid_question(question: str) -> bool:
    return question.strip() != ""
```

`formatter.py`에는 API 응답 모양을 만드는 함수를 작성합니다.

```python
def make_response(question: str, answer: str) -> dict:
    return {
        "question": question.strip(),
        "answer": answer,
    }
```

## 실습 4. 외부 패키지 확인하기

공통 `.venv`가 활성화된 상태에서 아래 명령을 실행합니다.

```powershell
python -c "import pytest; print(pytest.__version__)"
```

확인할 내용:

```text
pytest는 표준 라이브러리인가요, 외부 패키지인가요?
이 패키지는 어느 requirements.txt에서 관리하나요?
```

## 제출 기준

```text
1. 직접 만든 모듈을 import한 예제가 있어야 합니다.
2. from import를 사용한 예제가 있어야 합니다.
3. 패키지 폴더 구조가 있어야 합니다.
4. 공통 .venv와 requirements.txt의 역할을 README에 짧게 정리합니다.
```
