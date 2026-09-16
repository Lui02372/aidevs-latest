# 02. Simple Chat Multi-turn Redis

Redis에 대화 내용을 잠시 저장하고, 이전 대화를 Gemini 문맥으로 사용하는 멀티턴 예제입니다.

## DB 기반 예제와 차이

    02_simple-chat-multi-turn
    → Supabase에 영구 저장

    02_simple-chat-multi-turn-redis
    → Redis에 30분만 저장
    → TTL이 만료되면 대화 문맥도 자동 삭제

## 흐름

    POST /chat
    → Redis List에서 이전 메시지 조회
    → 이전 메시지 + 새 질문을 Gemini에 전달
    → 사용자 질문과 Gemini 답변을 Redis List에 저장
    → TTL 30분으로 갱신

## 준비

.env.example을 참고해 같은 폴더에 .env를 만듭니다.

    UPSTASH_REDIS_REST_URL=...
    UPSTASH_REDIS_REST_TOKEN=...
    GEMINI_API_KEY=...
    GEMINI_MODEL=gemini-2.5-flash-lite

## 실행

    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\02_simple-chat-multi-turn-redis
    ..\..\..\.venv\Scripts\Activate.ps1
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8017

Swagger UI: http://127.0.0.1:8017/docs

## API

새 대화를 시작합니다.

    {
      "message": "Redis TTL이 무엇인지 알려줘"
    }

응답의 conversation_id를 다음 요청에 넣으면 같은 대화를 이어 갑니다.

    {
      "conversation_id": "응답에서-받은-UUID",
      "message": "방금 설명을 예시로 다시 알려줘"
    }

대화 조회와 삭제:

    GET    /conversations/{conversation_id}/messages
    DELETE /conversations/{conversation_id}
