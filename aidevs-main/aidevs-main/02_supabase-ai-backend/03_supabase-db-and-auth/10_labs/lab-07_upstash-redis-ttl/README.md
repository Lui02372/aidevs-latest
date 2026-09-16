# Lab 07 - Upstash Redis TTL

이 lab은 Upstash Redis에 값을 저장하고, 조회하고, TTL로 자동 만료되는 흐름을 확인합니다.

## 학습 목표

- Redis를 “짧게 저장하는 임시 저장소”로 이해합니다.
- `SET`, `GET`, `TTL` 흐름을 확인합니다.
- Upstash Redis REST URL과 token이 `.env`에 있어야 한다는 것을 이해합니다.

## 실행 방법

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\06_upstash-redis-cache-and-session\01_redis_set_get_ttl.py
```

## 확인 기준

- Redis에 값이 저장됩니다.
- 저장한 값을 다시 조회할 수 있습니다.
- TTL 값이 표시됩니다.
- 일정 시간이 지나면 key가 자동으로 사라진다는 점을 설명할 수 있습니다.

## 정리 질문

- TTL은 무엇의 줄임말인가요?
- Supabase에 저장할 데이터와 Redis에 저장할 데이터는 어떻게 다른가요?
