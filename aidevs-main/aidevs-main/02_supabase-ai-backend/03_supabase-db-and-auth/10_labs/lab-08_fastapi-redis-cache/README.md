# Lab 08 - FastAPI Redis Cache

이 lab은 FastAPI endpoint 응답을 Upstash Redis에 잠깐 저장하고, 같은 질문이 들어왔을 때 캐시를 재사용하는 흐름을 확인합니다.

## 학습 목표

- `cached: false`와 `cached: true`의 차이를 설명할 수 있습니다.
- 같은 요청을 반복할 때 Redis 캐시가 어떻게 재사용되는지 이해합니다.
- AI API 응답을 캐시하면 비용과 응답 속도에 어떤 영향을 주는지 설명할 수 있습니다.

## 실행 방법

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\06_upstash-redis-cache-and-session
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
```

Swagger UI:

```text
http://127.0.0.1:8004/docs
```

## 테스트 순서

```text
1. GET /health를 실행합니다.
2. GET /ai/mock-answer를 질문 하나로 실행합니다.
3. 같은 질문으로 다시 실행합니다.
4. 첫 번째 응답과 두 번째 응답의 cached 값을 비교합니다.
5. DELETE /ai/mock-answer-cache로 캐시를 지운 뒤 다시 호출합니다.
```

## 확인 기준

- 첫 번째 호출은 `cached: false`입니다.
- 같은 질문의 두 번째 호출은 `cached: true`입니다.
- 캐시 삭제 후 다시 호출하면 `cached: false`가 됩니다.

## 정리 질문

- Redis 캐시는 왜 영구 저장소가 아닌가요?
- 캐시 TTL이 너무 길면 어떤 문제가 생길 수 있나요?
