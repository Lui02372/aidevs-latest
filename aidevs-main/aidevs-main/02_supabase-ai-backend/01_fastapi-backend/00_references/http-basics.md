# HTTP 기초

## 주요 Method

```text
GET 데이터 조회
POST 데이터 생성
PUT 전체 수정
PATCH 일부 수정
DELETE 삭제
```

## URL 구성

```text
http://127.0.0.1:8000/users/1?active=true
```

- `/users/1`: 경로
- `1`: Path Parameter
- `active=true`: Query Parameter

## 상태 코드

```text
200 OK
201 Created
400 Bad Request
404 Not Found
500 Internal Server Error
```

