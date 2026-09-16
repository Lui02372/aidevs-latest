# Lab 03 Solution Notes

## Supabase 테이블 오류

`schema.sql`의 테이블명은 `lab03_debug_logs`입니다.

하지만 코드에서는 `lab03_missing_logs`를 조회합니다.

```python
wrong_table_url = f"{supabase_url}/rest/v1/lab03_missing_logs"
```

먼저 테이블명이 SQL과 코드에서 같은지 확인합니다.

## Bearer token 오류

`/debug/me`는 Authorization 헤더가 없으면 401을 반환합니다.

```text
Authorization: Bearer <access_token>
```

Swagger에서 직접 header를 넣거나, 실제 예제에서는 `HTTPBearer`와 Authorize 버튼을 사용할 수 있습니다.

## Redis 오류

Redis 오류는 보통 다음 순서로 확인합니다.

1. `UPSTASH_REDIS_REST_URL`이 있는가?
2. `UPSTASH_REDIS_REST_TOKEN`이 있는가?
3. URL 끝에 `/`가 중복되지 않는가?
4. TTL이 만료되어 key가 사라진 것은 아닌가?

## 좋은 프롬프트 포인트

외부 서비스 오류는 한 번에 묻지 말고 Supabase, Auth, Redis를 나누어 질문합니다.
