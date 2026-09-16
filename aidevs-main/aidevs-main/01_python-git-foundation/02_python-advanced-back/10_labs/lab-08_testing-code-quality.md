# Lab 08. 테스트와 코드 품질

이 실습에서는 간단한 서비스 함수를 만들고 pytest로 검증합니다.

## 실습 목표

```text
1. print 확인과 assert 확인의 차이를 설명할 수 있습니다.
2. 테스트 대상 함수를 만들 수 있습니다.
3. pytest 테스트 파일을 작성할 수 있습니다.
4. assert로 예상 결과와 실제 결과를 비교할 수 있습니다.
5. pytest.raises로 오류 발생을 테스트할 수 있습니다.
6. 응답 dict에 필요한 key가 있는지 확인할 수 있습니다.
```

## 실습 1. print와 assert 차이 확인

먼저 아래 예제를 실행합니다.

```powershell
cd C:\aidev\01_python-git-foundation
python .\02_python-advanced\08_testing-code-quality\02_print_vs_assert.py
```

확인할 내용:

```text
print는 값을 보여 주기만 합니다.
assert는 값이 예상과 다르면 실패합니다.
```

## 실습 2. 질문 정리 함수 테스트

`normalize_question(question)` 함수를 만들고 앞뒤 공백이 제거되는지 테스트합니다.

```python
def normalize_question(question: str) -> str:
    return question.strip()
```

테스트 기준:

```text
"  FastAPI란?  " -> "FastAPI란?"
"   " -> ""
```

## 실습 3. 빈 질문 검증 테스트

`validate_question(question)` 함수를 만들고, 빈 질문이면 `ValueError`가 발생하도록 합니다.

```python
def validate_question(question: str) -> None:
    if question.strip() == "":
        raise ValueError("질문은 비워둘 수 없습니다.")
```

pytest에서는 아래처럼 오류 발생을 테스트합니다.

```python
import pytest


def test_validate_question_rejects_empty_text():
    with pytest.raises(ValueError):
        validate_question("   ")
```

## 실습 4. API 응답 dict 구조 테스트

`build_chat_response(question)` 함수가 아래 key를 가진 dict를 반환하는지 확인합니다.

```text
question
answer
```

테스트 기준:

```text
response["question"] 값이 질문과 일치해야 합니다.
"answer" key가 있어야 합니다.
answer 값은 빈 문자열이면 안 됩니다.
빈 질문을 넣으면 ValueError가 발생해야 합니다.
```

## 실행 방법

```powershell
cd C:\aidev\01_python-git-foundation
python -m pytest .\02_python-advanced\08_testing-code-quality
```

자세한 테스트 이름을 보고 싶으면 아래처럼 실행합니다.

```powershell
python -m pytest .\02_python-advanced\08_testing-code-quality -v
```

## 제출 기준

```text
1. 테스트 대상 함수 파일이 있어야 합니다.
2. test_로 시작하는 테스트 파일이 있어야 합니다.
3. 정상 입력 테스트가 있어야 합니다.
4. 오류 발생 테스트가 있어야 합니다.
5. 응답 dict 구조 테스트가 있어야 합니다.
6. print와 assert의 차이를 README나 메모에 한 줄로 정리해야 합니다.
```
