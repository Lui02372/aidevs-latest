# assignment-100_llm-api-structure-refactor

`assignment-99_fastapi-llm-mini-service`에서 단일 파일로 만든 mock-first LLM API를 `routers`, `schemas`, `services` 구조로 분리하는 과제입니다.

이 과제는 `01_fastapi-backend`의 `assignment-100_product-api-structure-refactor`와 같은 방식으로 진행하되, 주제는 상품 API가 아니라 **LLM Chat API**입니다.

## 목표

```text
starter/app/main.py:
  FastAPI 앱 생성과 router 연결

starter/app/routers/chat_router.py:
  /health, /ai/chat, /ai/chat-with-history 경로 정의

starter/app/schemas/chat_schema.py:
  요청/응답 Pydantic 모델 정의

starter/app/services/llm_service.py:
  prompt 구성, mock 응답 생성, 저장용 메시지 구성

starter/tests/test_llm_api.py:
  TestClient로 API 동작 검증
```

## 폴더 구조

```text
assignment-100_llm-api-structure-refactor
├─ README.md
├─ starter
│  ├─ app
│  └─ tests
└─ solution
   ├─ app
   └─ tests
```

먼저 `starter` 폴더의 TODO를 완성합니다. 수업 후 또는 복습할 때 `solution` 폴더와 비교합니다.

## 실행 방법

과정 가상환경을 활성화합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

starter 폴더로 이동해 서버를 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\20_assignments\assignment-100_llm-api-structure-refactor\starter
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 테스트 실행

```powershell
python -m pytest -s
```

처음에는 TODO가 남아 있어 테스트가 실패할 수 있습니다. 실패 메시지를 보고 `app/services`, `app/routers`, `app/schemas`를 하나씩 완성합니다.

solution을 확인하려면 아래처럼 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\20_assignments\assignment-100_llm-api-structure-refactor\solution
python -m pytest -s
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

## 구현 요구사항

1. `GET /health`는 `{"status": "ok"}`를 반환합니다.
2. `POST /ai/chat`은 single-turn mock 응답을 반환합니다.
3. `POST /ai/chat-with-history`는 이전 대화 이력을 포함한 mock 응답을 반환합니다.
4. 모든 응답에는 `provider`, `model`, `actual_api_called`, `answer`, `messages_for_storage`가 포함됩니다.
5. 실제 API를 호출하지 않으므로 `actual_api_called`는 `false`입니다.
6. `messages_for_storage`에는 user 메시지와 assistant 메시지가 저장 가능한 구조로 들어갑니다.
7. endpoint 함수 안에 모든 로직을 넣지 않고, prompt 구성과 mock 응답 생성은 `llm_service.py`로 분리합니다.

## 제출 기준

아래 항목을 README에 정리합니다.

```text
1. 실행 명령
2. 구현한 API 목록
3. 요청/응답 예시
4. 테스트 실행 결과
5. 구조를 나누면서 이해한 점
6. Gemini SDK 실제 호출로 바꿀 위치
7. Supabase 대화 이력 저장으로 이어질 데이터 구조
```

## 점검 질문

```text
구조:
  app/main.py는 router 연결만 담당하는가?

Router:
  API 경로와 HTTP Method가 chat_router.py에 모여 있는가?

Schema:
  요청 모델과 응답 모델이 chat_schema.py에 분리되어 있는가?

Service:
  prompt 구성, mock 응답, 저장용 메시지 생성이 llm_service.py에 분리되어 있는가?

Test:
  python -m pytest -s로 테스트가 통과하는가?
```
