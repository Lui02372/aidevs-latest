# Lab 01. 함수 심화 핵심

이 실습에서는 이후 FastAPI, Supabase, LLM API 예제에서 자주 쓰는 함수 사용법만 연습합니다.

## 실습 목표

```text
1. *args와 **kwargs로 값을 유연하게 전달할 수 있습니다.
2. 리스트와 딕셔너리를 함수 인자로 풀어 전달할 수 있습니다.
3. 함수를 인자로 전달해 검증 방식을 바꿀 수 있습니다.
4. 데코레이터가 FastAPI 라우터 문법과 연결된다는 것을 이해할 수 있습니다.
5. LLM 질문 요청 데이터를 함수로 나누어 만들 수 있습니다.
```

## 실습 1. 검색 조건 만들기

`*tags`, `**options`를 사용해 검색 조건을 dict로 만듭니다.

```python
def build_search_query(keyword: str, *tags: str, **options: str) -> dict[str, object]:
    return {
        "keyword": keyword,
        "tags": list(tags),
        "options": options,
    }
```

확인할 내용:

```text
태그는 list로 정리되나요?
sort, limit 같은 옵션은 dict로 들어가나요?
```

## 실습 2. 요청 데이터 언패킹

딕셔너리를 함수 인자로 풀어서 전달합니다.

```python
def create_user_request(name: str, email: str, role: str) -> dict[str, str]:
    return {
        "name": name,
        "email": email,
        "role": role,
    }


data = {
    "name": "Mina",
    "email": "mina@example.com",
    "role": "student",
}

print(create_user_request(**data))
```

## 실습 3. 검증 함수 전달

질문을 검증하는 함수를 따로 만들고, 처리 함수에 전달합니다.

```python
def validate_not_empty(text: str) -> bool:
    return text.strip() != ""


def process_question(question: str, validator) -> dict[str, str]:
    if not validator(question):
        return {"status": "error"}

    return {"status": "ok", "message": question.strip()}
```

## 실습 4. 데코레이터 모양 이해

FastAPI의 `@app.get("/health")`와 비슷한 모양의 데코레이터를 간단히 만들어 봅니다.

```python
def route(path: str):
    def decorator(original_function):
        def wrapper():
            print(path)
            return original_function()

        return wrapper

    return decorator
```

## 실습 5. LLM 질문 요청 데이터 만들기

질문을 정리하고 검증한 뒤 요청 dict를 만듭니다.

요구사항:

```text
1. normalize_question(question) 함수를 만듭니다.
2. validate_question(question) 함수를 만듭니다.
3. build_chat_request(question, **options) 함수를 만듭니다.
4. 질문이 비어 있으면 ok: False를 반환합니다.
5. 질문이 정상이라면 ok: True, message, options를 반환합니다.
```

## 제출 기준

```text
1. *args 또는 **kwargs 사용 예제가 있어야 합니다.
2. **dict 언패킹 예제가 있어야 합니다.
3. 함수를 인자로 전달하는 예제가 있어야 합니다.
4. 데코레이터 모양을 이해하는 예제가 있어야 합니다.
5. LLM 요청 데이터 구성 예제가 있어야 합니다.
```
