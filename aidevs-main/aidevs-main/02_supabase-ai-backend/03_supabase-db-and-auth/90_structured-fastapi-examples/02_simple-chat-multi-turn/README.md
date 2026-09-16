# 02. Simple Chat Multi-turn API

Supabase에 저장한 이전 질문·답변을 다시 읽어 Gemini에 전달하는 멀티턴 대화 예제입니다.

## 흐름

```text
POST /chat
→ conversation_id의 최근 대화 6턴 조회
→ 이전 대화 + 새 질문을 Gemini에 전달
→ 새 질문·답변을 Supabase에 저장
→ 답변과 conversation_id 반환
```

`conversation_id`를 생략하면 새 대화를 시작합니다. 응답으로 받은 ID를 다음 요청에 다시 보내면 같은 대화를 이어 갑니다.

## 준비

1. Supabase SQL Editor에서 `schema.sql`을 실행합니다.
2. `.env.example`을 참고해 같은 폴더에 `.env`를 만듭니다.

```text
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash-lite
```

## 실행

```powershell
cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\02_simple-chat-multi-turn
..\..\..\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8016
```

Swagger UI: `http://127.0.0.1:8016/docs`

## API 사용

새 대화:

```json
{
  "message": "Redis 캐시를 쉽게 설명해줘"
}
```

응답의 `conversation_id`를 복사합니다.

같은 대화 이어가기:

```json
{
  "conversation_id": "응답에서-받은-UUID",
  "message": "방금 설명을 예시로 다시 알려줘"
}
```

대화 전체 이력은 다음 API로 조회합니다.

```text
GET /conversations/{conversation_id}/messages
```
