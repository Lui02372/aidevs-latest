# Assignment 02 - Memo CRUD API

## 목표

서버 메모리 dict를 사용해 메모 생성, 조회, 수정, 삭제 API를 구현합니다.

## 필수 요구사항

1. `GET /memos`로 전체 메모를 조회합니다.
2. `GET /memos/{memo_id}`로 메모 1개를 조회합니다.
3. `POST /memos`로 새 메모를 생성합니다.
4. `PUT /memos/{memo_id}`로 기존 메모를 수정합니다.
5. `DELETE /memos/{memo_id}`로 기존 메모를 삭제합니다.
6. 생성/수정 요청에는 Pydantic 모델을 사용합니다.
7. 없는 메모 id는 404 오류를 반환합니다.

## 요청 예시

```json
{
  "title": "FastAPI CRUD",
  "content": "메모 생성과 수정을 구현합니다.",
  "tags": ["fastapi", "crud"]
}
```

## README에 포함할 내용

```text
1. 실행 명령
2. CRUD API 목록
3. POST 요청/응답 예시
4. PUT 요청/응답 예시
5. DELETE 요청/응답 예시
6. 서버를 재시작하면 데이터가 초기화되는 이유
```
