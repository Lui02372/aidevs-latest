# Assignment 01 - Memo Health And Routing

## 목표

FastAPI 서버의 기본 상태 확인 API와 메모 조회/검색 API를 직접 구현합니다.

## 필수 요구사항

1. `GET /health`에서 `{"status": "ok"}`를 반환합니다.
2. `GET /memos`에서 전체 메모 목록과 개수를 반환합니다.
3. `GET /memos/search?keyword=...&limit=...`에서 제목 또는 본문 검색을 구현합니다.
4. `GET /memos/{memo_id}`에서 메모 1개를 반환합니다.
5. 없는 메모 id를 요청하면 404 오류를 반환합니다.
6. `/memos/search`는 `/memos/{memo_id}`보다 먼저 정의합니다.

## 제출 파일

```text
main.py
README.md
```

## README에 포함할 내용

```text
1. 실행 명령
2. API 목록
3. /memos/search 요청 예시
4. 없는 memo_id 요청 시 404 응답 예시
5. Path Parameter와 Query Parameter 차이 설명
```

## 확인 기준

```text
GET /health
GET /memos
GET /memos/search?keyword=fastapi&limit=2
GET /memos/1
GET /memos/999
```
