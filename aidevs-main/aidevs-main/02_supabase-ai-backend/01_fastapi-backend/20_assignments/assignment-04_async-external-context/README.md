# Assignment 04 - Async External Context

## 목표

`async def`, `await`, `httpx.AsyncClient`를 사용해 외부 API 데이터를 가져오고 메모 데이터와 연결합니다.

## 필수 요구사항

1. `GET /external/posts/{post_id}`를 구현합니다.
2. 외부 API 원본 데이터 `raw`와 가공 데이터 `parsed`를 함께 반환합니다.
3. `GET /memos/{memo_id}/external-context`를 구현합니다.
4. 메모 데이터와 외부 API 데이터를 하나의 응답으로 묶습니다.
5. 외부 API의 4xx/5xx 오류를 `HTTPException`으로 처리합니다.
6. 네트워크 오류나 타임아웃을 503 오류로 처리합니다.

## 사용하는 공개 API

```text
https://jsonplaceholder.typicode.com/posts/1
```

## README에 포함할 내용

```text
1. 실행 명령
2. 외부 API URL
3. raw와 parsed의 차이
4. /memos/{memo_id}/external-context 응답 예시
5. 외부 API 오류 처리 방식
```
