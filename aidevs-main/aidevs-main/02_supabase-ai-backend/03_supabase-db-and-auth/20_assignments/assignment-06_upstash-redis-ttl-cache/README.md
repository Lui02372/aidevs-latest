# Assignment 06 - Upstash Redis TTL Cache

Upstash Redis를 사용해 “짧게 저장했다가 빠르게 꺼내 쓰는 데이터”를 설계하는 과제입니다.

현재 범위에서는 rate limit이나 session 구현까지 요구하지 않습니다. Redis의 기본 역할, TTL, cache hit/cache miss를 설명할 수 있으면 충분합니다.

## 목표

- Supabase와 Redis의 역할을 구분할 수 있습니다.
- TTL이 필요한 데이터를 예로 들 수 있습니다.
- AI API 응답을 캐시했을 때 비용과 응답 속도에 어떤 영향이 있는지 설명할 수 있습니다.

## 제출물

아래 내용을 포함해 Markdown 문서로 작성합니다.

```text
1. Upstash Redis를 사용하는 이유
2. Supabase에 저장할 데이터 목록
3. Redis에 잠깐 저장할 데이터 목록
4. TTL이 필요한 데이터 예시 3개
5. AI 답변 캐시 key 이름 예시
6. cache hit와 cache miss 흐름 설명
7. UPSTASH_REDIS_REST_TOKEN을 GitHub에 올리면 안 되는 이유
8. FastAPI에서 캐시를 적용할 endpoint 후보
9. 캐시 만료 시간이 너무 길거나 너무 짧을 때 생기는 문제
```

## 실행 참고

Redis SET/GET/TTL:

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\06_upstash-redis-cache-and-session\01_redis_set_get_ttl.py
```

FastAPI Redis cache:

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\06_upstash-redis-cache-and-session
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
```

## 확인 기준

- Redis를 영구 데이터베이스처럼 사용하지 않았습니다.
- TTL 설정 이유가 구체적입니다.
- cache hit와 cache miss의 차이를 설명했습니다.
- 실제 token 값을 문서에 적지 않았습니다.
