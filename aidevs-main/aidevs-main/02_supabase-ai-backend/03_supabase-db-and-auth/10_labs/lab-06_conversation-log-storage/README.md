# Lab 06 - LLM 채팅 로그 저장

이 실습은 AI 챗봇 서비스에서 사용자 질문과 AI 답변을 Supabase에 저장하는 흐름을 확인합니다.

먼저 `01_insert_conversation_and_log.py`로 샘플 로그 저장을 확인하고, 이후 `02_fastapi_llm_chat_log.py`에서 FastAPI endpoint와 Gemini 호출 결과를 같은 테이블에 저장합니다.

## 학습 목표

- `simple_chat_logs` 테이블의 역할을 설명할 수 있습니다.
- 사용자 질문과 AI 답변을 한 행(row)에 저장하는 흐름을 이해합니다.
- FastAPI endpoint에서 LLM 응답과 로그 저장을 연결하는 흐름을 이해합니다.
- 오류가 발생했을 때 `status`, `error_message`에 무엇을 남길지 설명할 수 있습니다.

## 1단계 - 샘플 로그 저장

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\05_conversation-history-and-service-logs\01_insert_conversation_and_log.py
```

## 2단계 - FastAPI + Gemini 로그 저장

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\05_conversation-history-and-service-logs
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
```

Swagger 주소:

```text
http://127.0.0.1:8003/docs
```

## 테이블 오류가 발생할 때

`PGRST205` 또는 `Could not find the table` 오류가 나오면 Supabase SQL Editor에서 아래 파일을 실행합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
```

## 확인 기준

- `simple_chat_logs` 테이블에 사용자 질문이 저장됩니다.
- `simple_chat_logs` 테이블에 AI 답변이 저장됩니다.
- `provider`, `model`, `status`, `error_message` 값을 확인할 수 있습니다.
- `/logs` endpoint로 최근 로그를 조회할 수 있습니다.

## 정리 질문

- 채팅 로그를 왜 Supabase에 저장하나요?
- `status='error'`인 로그는 어떤 상황에서 생기나요?
- 나중에 `conversations`, `messages`, `service_logs`로 테이블을 나눈다면 어떤 장점이 있나요?
