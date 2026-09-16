# Assignment 03 - Memo Validation And Response

## 목표

Pydantic 요청 검증, Response Model, 표준 응답 구조를 적용한 메모 API를 구현합니다.

## 필수 요구사항

1. `MemoCreate` 요청 모델을 만듭니다.
2. `MemoPublic` 응답 모델을 만듭니다.
3. `ApiResponse` 표준 응답 모델을 만듭니다.
4. `POST /memos`에서 요청 데이터를 검증합니다.
5. `GET /memos/{memo_id}`에서 `response_model=MemoPublic`을 적용합니다.
6. 내부 데이터에 `internal_note`를 넣고 응답에서는 제외합니다.
7. 잘못된 요청을 보내 422 오류를 확인합니다.

## 잘못된 요청 예시

```json
{
  "title": "",
  "content": "",
  "tags": ["a", "b", "c", "d", "e", "f"]
}
```

## README에 포함할 내용

```text
1. 실행 명령
2. 요청 모델과 응답 모델을 나눈 이유
3. 422 오류가 발생하는 요청 예시
4. internal_note가 응답에서 제외되는 결과
5. success, message, data 구조 설명
```
