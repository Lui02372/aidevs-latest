# Lab 02 - Memo Routing And Search

## 목표

Path Parameter와 Query Parameter를 사용해 메모 조회 API를 구현합니다.

## 요구사항

1. 기본 메모 데이터를 dict로 준비합니다.
2. `GET /memos`에서 전체 메모 목록을 반환합니다.
3. `GET /memos/{memo_id}`에서 메모 1개를 반환합니다.
4. `GET /memos/search?keyword=...&limit=...`에서 제목 또는 본문 검색을 구현합니다.
5. 없는 메모 id를 요청하면 404 오류를 반환합니다.

## 주의할 점

`/memos/search`는 `/memos/{memo_id}`보다 먼저 정의합니다.

```text
좋은 순서:
  /memos/search
  /memos/{memo_id}

이유:
  /memos/{memo_id}를 먼저 쓰면 search가 memo_id처럼 해석될 수 있습니다.
```

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-02_memo-routing-and-search
uvicorn starter:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn starter:app --reload
```

## 확인 질문

```text
1. Path Parameter와 Query Parameter의 차이는 무엇인가요?
2. /memos/search를 /memos/{memo_id}보다 먼저 쓰는 이유는 무엇인가요?
3. limit 값에 ge, le 조건을 거는 이유는 무엇인가요?
```
