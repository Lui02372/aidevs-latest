# Lab 03. 예외 처리와 디버깅

이 실습에서는 우리 과정에서 자주 사용하는 예외 처리만 연습합니다.

## 실습 목표

```text
1. ValueError를 처리할 수 있습니다.
2. 잘못된 입력을 다시 입력받을 수 있습니다.
3. 파일 없음 오류와 JSON 형식 오류를 처리할 수 있습니다.
4. 직접 raise로 검증 오류를 발생시킬 수 있습니다.
5. 오류 종류와 오류 메시지를 읽을 수 있습니다.
```

## 실습 1. 안전한 숫자 변환 함수

문자열을 숫자로 변환하되, 실패하면 0을 반환합니다.

```python
def convert_to_number(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


print(convert_to_number("10"))
print(convert_to_number("abc"))
print(convert_to_number(""))
```

## 실습 2. 다시 입력받는 반복문

숫자가 입력될 때까지 반복해서 입력받는 코드를 작성합니다.

조건:

```text
1. 숫자를 입력하면 해당 숫자를 출력하고 종료합니다.
2. q를 입력하면 프로그램을 종료합니다.
3. 숫자가 아닌 값을 입력하면 다시 입력받습니다.
```

## 실습 3. 파일과 JSON 오류 처리

없는 JSON 파일을 읽으려고 할 때 빈 dict를 반환하는 함수를 만듭니다.

요구사항:

```text
1. FileNotFoundError를 처리합니다.
2. json.JSONDecodeError를 처리합니다.
3. 오류가 발생하면 {}를 반환합니다.
4. 오류 상황을 사용자가 이해할 수 있는 문장으로 출력합니다.
```

## 실습 4. raise로 질문 검증하기

질문이 비어 있으면 `ValueError`를 직접 발생시키는 함수를 만듭니다.

```python
def validate_question(question: str) -> None:
    if question.strip() == "":
        raise ValueError("질문은 비워둘 수 없습니다.")
```

## 실습 5. 오류 메시지 읽기

아래 코드는 오류가 발생합니다.

```python
items = []
print(items[0])
```

확인할 내용:

```text
오류 종류는 무엇인가요?
오류 메시지는 무엇인가요?
오류가 발생한 줄은 어디인가요?
```

## 제출 기준

```text
1. ValueError 처리 예제가 있어야 합니다.
2. FileNotFoundError 또는 JSONDecodeError 처리 예제가 있어야 합니다.
3. raise를 사용한 검증 함수가 있어야 합니다.
4. 잘못된 입력을 다시 받는 반복문이 있어야 합니다.
5. 오류를 숨기지 않고 이해 가능한 메시지로 출력해야 합니다.
```
