# Assignment 05 - Simple Chat Log Storage

AI 챗봇 서비스에서 사용자 질문과 AI 답변을 `simple_chat_logs` 테이블에 저장하는 흐름을 설계하고 정리하는 과제입니다.

이번 과제는 `conversations`, `messages`, `service_logs`를 필수로 분리 설계하지 않습니다. 먼저 한 테이블로 질문/답변/상태를 저장하는 최소 흐름을 이해합니다.

## 목표

- 사용자 질문과 AI 답변을 Supabase에 저장하는 이유를 설명할 수 있습니다.
- `simple_chat_logs` 각 컬럼의 역할을 설명할 수 있습니다.
- 성공 로그와 실패 로그를 같은 테이블에 남기는 방식을 설명할 수 있습니다.
- mock 응답과 Gemini SDK 응답을 구분해서 기록하는 기준을 설명할 수 있습니다.

## 제출물

아래 내용을 포함해 작성합니다.

```text
1. simple_chat_logs 테이블 목적
2. 각 컬럼의 의미
3. 01_insert_conversation_and_log.py 실행 결과 요약
4. 02_fastapi_llm_chat_log.py의 endpoint 목록
5. 사용자 질문이 저장되는 순서
6. AI 답변이 저장되는 순서
7. status='success'와 status='error'가 생기는 상황
8. error_message에 남기면 좋은 정보
9. 나중에 conversations/messages/service_logs로 확장할 수 있는 이유
```

## 실행 참고

샘플 로그 저장:

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\05_conversation-history-and-service-logs\01_insert_conversation_and_log.py
```

FastAPI + LLM 로그 저장:

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\05_conversation-history-and-service-logs
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
```

## 확인 기준

- `simple_chat_logs`를 필수 저장 구조로 설명했습니다.
- 사용자 질문, AI 답변, provider, model, status의 의미를 구분했습니다.
- 오류 발생 시 로그를 남겨야 하는 이유를 설명했습니다.
- Redis 캐시와 Supabase 영구 저장의 차이를 설명했습니다.
