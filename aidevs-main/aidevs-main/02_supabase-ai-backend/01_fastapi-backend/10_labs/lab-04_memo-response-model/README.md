# Lab 04 - Memo Response Model

## 목표

Response Model을 사용해 응답으로 내보낼 메모 필드를 제한합니다.

## 요구사항

1. 내부 메모 데이터에 `internal_note` 값을 포함합니다.
2. `MemoPublic` 응답 모델을 만듭니다.
3. `GET /memos/{memo_id}`에 `response_model=MemoPublic`을 적용합니다.
4. API 응답에서 `internal_note`가 제외되는지 확인합니다.

## 확인 질문

```text
1. response_model은 어떤 역할을 하나요?
2. 내부 데이터와 외부 응답 데이터를 분리하는 이유는 무엇인가요?
3. password, token, internal_note 같은 값은 왜 응답에서 제외해야 하나요?
```
