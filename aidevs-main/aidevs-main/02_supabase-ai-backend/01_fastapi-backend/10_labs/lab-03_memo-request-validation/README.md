# Lab 03 - Memo Request Validation

## 목표

Pydantic 모델을 사용해 메모 생성 요청 Body를 검증합니다.

## 요구사항

1. `MemoCreate` 모델을 만듭니다.
2. `title`은 1~50자로 제한합니다.
3. `content`는 1~500자로 제한합니다.
4. `tags`는 문자열 목록이며 최대 5개로 제한합니다.
5. `POST /memos`에서 검증된 요청 데이터를 반환합니다.
6. 잘못된 요청을 보내 422 오류를 확인합니다.

## 잘못된 요청 예시

```json
{
  "title": "",
  "content": "",
  "tags": ["a", "b", "c", "d", "e", "f"]
}
```

## 확인 질문

```text
1. Pydantic 모델은 요청의 어떤 부분을 검사하나요?
2. 422 오류는 언제 발생하나요?
3. Field의 min_length, max_length는 어떤 역할을 하나요?
```
