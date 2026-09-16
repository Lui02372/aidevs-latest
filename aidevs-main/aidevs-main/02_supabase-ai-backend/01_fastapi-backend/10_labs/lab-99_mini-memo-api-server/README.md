# Lab 99 - Mini Memo API Server

## 목표

FastAPI 백엔드 기초 단원의 마무리로 작은 메모 API 서버를 완성합니다.

이 실습은 이후 `02_llm-api-integration`, `03_supabase-db-and-auth`, `03_supabase-ai-frontend`와 연결됩니다. 여기서는 Supabase에 저장하지 않고 메모리 dict에 저장합니다.

기능 구현은 이 실습에서 마무리하고, 다음 `lab-100_project-structure-refactor`에서 같은 API를 `app/main.py`, `routers`, `schemas`, `services`, `tests` 구조로 분리합니다.

## 요구사항

1. `GET /health`를 구현합니다.
2. `GET /memos`에서 전체 메모를 조회합니다.
3. `GET /memos/search`에서 키워드 검색을 구현합니다.
4. `GET /memos/{memo_id}`에서 메모 1개를 조회합니다.
5. `POST /memos`에서 Pydantic 요청 검증을 적용합니다.
6. `response_model`을 사용해 내부 관리 값을 응답에서 제외합니다.
7. `POST /ai/draft-response`에서 가짜 AI 응답을 비동기로 반환합니다.

## 산출물 기준

```text
API 실행:
  uvicorn solution:app --reload로 실행됩니다.
  # 위 명령에서 오류가 나면 아래처럼 실행합니다.
  python -m uvicorn solution:app --reload로 실행됩니다.

Swagger 확인:
  /docs에서 모든 API를 테스트할 수 있습니다.

요청 검증:
  잘못된 메모 생성 요청은 422 오류를 반환합니다.

응답 보호:
  internal_note는 API 응답에 포함되지 않습니다.

비동기 흐름:
  AI placeholder 응답은 async 함수로 처리됩니다.
```

## 확인 질문

```text
1. 이 미니 서버에서 Supabase로 옮기면 어떤 부분이 바뀔까요?
2. 실제 LLM API를 연결하면 어떤 함수가 바뀔까요?
3. Streamlit 화면에서는 어떤 API를 먼저 호출하면 좋을까요?
```
