# Redis TTL Cache Patterns

AI 서비스에서는 모든 데이터를 한 곳에 저장하지 않습니다. 오래 보관해야 하는 데이터는 Supabase에 저장하고, 짧게 쓰고 사라져도 되는 임시 값은 Upstash Redis에 저장합니다.

현재 과정에서는 Redis session이나 rate limit을 구현하지 않고, TTL 기반 캐시만 실습합니다.

## 저장 위치 기준

| 데이터 | 권장 저장 위치 | 이유 |
|---|---|---|
| 사용자 프로필 | Supabase | 나중에 다시 조회해야 하는 영구 데이터입니다. |
| 대화 이력 | Supabase | 사용자가 과거 대화를 다시 볼 수 있어야 합니다. |
| 서비스 로그 | Supabase | 오류 분석과 운영 기록에 필요합니다. |
| 60초짜리 AI 답변 캐시 | Upstash Redis | 잠깐만 빠르게 재사용하면 충분합니다. |
| 중복 요청 방지 key | Upstash Redis | 뒤 과정에서 확장할 수 있는 임시 데이터 예시입니다. |

## Redis Key 예시

```text
cache:answer:{question_hash}
cache:answer:{user_id}:{question_hash}
```

## Cache Hit와 Cache Miss

```text
cache hit:
1. Redis에 값이 있다.
2. Supabase나 LLM API를 다시 호출하지 않는다.
3. Redis 값을 바로 반환한다.

cache miss:
1. Redis에 값이 없다.
2. Supabase나 LLM API를 호출한다.
3. 결과를 Redis에 TTL과 함께 저장한다.
4. 결과를 사용자에게 반환한다.
```

## 원칙

- Redis에는 오래 보관해야 하는 원본 데이터를 저장하지 않습니다.
- Redis key에는 TTL을 설정해 자동 만료되게 합니다.
- 민감한 개인정보나 API key는 Redis에 저장하지 않습니다.
- 영구 보관, 검색, 분석이 필요한 데이터는 Supabase에 저장합니다.

## 현재 과정에서 확인하는 예제

```text
06_upstash-redis-cache-and-session\01_redis_set_get_ttl.py
06_upstash-redis-cache-and-session\02_fastapi_redis_cache.py
```
