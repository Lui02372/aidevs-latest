# Lab 05 - Async External Context

## 목표

`async def`, `await`, `httpx.AsyncClient`를 사용해 외부 API 데이터를 가져오고 메모 데이터와 연결합니다.

## 요구사항

1. `fetch_external_post()` 비동기 함수를 만듭니다.
2. JSONPlaceholder 공개 API에서 게시글 데이터를 가져옵니다.
3. `GET /external/posts/{post_id}`에서 원본 데이터와 가공 데이터를 함께 반환합니다.
4. `GET /memos/{memo_id}/external-context`에서 메모와 외부 데이터를 함께 반환합니다.
5. 외부 API 오류는 `HTTPException`으로 바꿉니다.

## 실행 전 확인

이 실습은 인터넷 연결이 필요합니다.

사용하는 공개 API:

```text
https://jsonplaceholder.typicode.com/posts/1
```

## 확인 질문

```text
1. 외부 API 원본 데이터와 가공 데이터를 함께 보는 이유는 무엇인가요?
2. async 함수 안에서 외부 API를 호출할 때 await가 필요한 이유는 무엇인가요?
3. 외부 API 오류를 우리 API 오류로 바꾸는 이유는 무엇인가요?
```
