# Lab 06 - Memo CRUD Review

## 목표

Supabase에 연결하기 전에 FastAPI만으로 메모 CRUD API 전체 흐름을 복습합니다.

이 실습에서는 서버 메모리에 데이터를 저장합니다. 서버를 재시작하면 데이터는 초기값으로 돌아갑니다. 실제 데이터 저장은 이후 `03_supabase-db-and-auth`에서 Supabase로 확장합니다.

## 요구사항

1. `GET /memos`로 전체 메모를 조회합니다.
2. `GET /memos/{memo_id}`로 메모 1개를 조회합니다.
3. `POST /memos`로 새 메모를 생성합니다.
4. `PUT /memos/{memo_id}`로 기존 메모를 수정합니다.
5. `DELETE /memos/{memo_id}`로 기존 메모를 삭제합니다.
6. 없는 메모 id는 404 오류를 반환합니다.

## POST 요청 예시

```json
{
  "title": "FastAPI CRUD",
  "content": "메모 생성과 조회를 연습합니다.",
  "tags": ["fastapi", "crud"]
}
```

## 확인 순서

```text
1. GET /memos
2. POST /memos
3. GET /memos/{memo_id}
4. PUT /memos/{memo_id}
5. DELETE /memos/{memo_id}
6. GET /memos/{memo_id}로 404 확인
```
