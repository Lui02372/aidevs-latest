# Assignment 99 - FastAPI Memo Mini Project

## 목표

`01_fastapi-backend` 단원의 마무리로 작은 메모 API 서버를 완성합니다.

이 과제는 이후 `02_llm-api-integration`, `03_supabase-db-and-auth`, `03_supabase-ai-frontend`, `04_supabase-ai-mini-project`로 이어지는 기반입니다. 여기서는 Supabase에 저장하지 않고 서버 메모리 dict에 저장합니다.

## 필수 요구사항

1. `GET /health`를 구현합니다.
2. `GET /memos`로 전체 메모를 조회합니다.
3. `GET /memos/search`로 제목/본문 검색을 구현합니다.
4. `GET /memos/{memo_id}`로 메모 1개를 조회합니다.
5. `POST /memos`로 새 메모를 생성합니다.
6. `PUT /memos/{memo_id}`로 메모를 수정합니다.
7. `DELETE /memos/{memo_id}`로 메모를 삭제합니다.
8. `POST /ai/draft-response`로 가짜 AI 응답을 비동기로 반환합니다.
9. `MemoCreate`, `MemoUpdate`, `MemoPublic`, `ApiResponse` 모델을 사용합니다.
10. 없는 메모 id는 404 오류를 반환합니다.
11. 잘못된 요청은 422 오류가 발생해야 합니다.
12. 내부 관리 값 `internal_note`는 API 응답에 포함되지 않아야 합니다.

## 제출 파일

```text
main.py
README.md
```

## README에 포함할 내용

```text
1. 프로젝트 목표
2. 실행 방법
3. API 목록
4. 메모 생성 요청/응답 예시
5. 메모 검색 요청/응답 예시
6. 404 오류 예시
7. 422 오류 예시
8. internal_note가 응답에서 제외되는 결과
9. 다음 단원에서 Supabase/LLM/Streamlit로 확장할 부분
```

## 실행 기준

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\20_assignments\assignment-99_fastapi-memo-mini-project
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 평가 기준

```text
기본 실행:
  서버가 실행되고 /health가 정상 응답합니다.

API 설계:
  메모 리소스를 기준으로 URL과 HTTP Method가 자연스럽게 설계되었습니다.

요청 검증:
  Pydantic Field 조건으로 잘못된 요청을 막습니다.

응답 보호:
  response_model 또는 별도 변환을 통해 internal_note가 응답에서 제외됩니다.

비동기 흐름:
  AI placeholder API가 async def와 await를 사용합니다.

문서:
  README만 보고 실행과 테스트를 진행할 수 있습니다.
```
