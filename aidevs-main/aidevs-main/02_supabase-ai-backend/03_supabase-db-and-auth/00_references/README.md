# 00_references

이 폴더는 Supabase 중심 DB/인증/로그 실습을 진행할 때 참고하는 문서와 SQL 파일을 모아 둔 곳입니다.

이 과정에서 영구 저장은 Supabase를 사용하고, 짧게 보관할 임시 캐시는 Upstash Redis를 사용합니다. 요청 제한, 세션 저장, cache-aside 구현은 뒤 과정에서 확장합니다.

## 문서 목록

| 파일 | 내용 | 연결되는 챕터 |
|---|---|---|
| `supabase-first-notes.md` | 이 과정에서 Supabase를 먼저 사용하는 이유와 전체 기준 | 전체 |
| `supabase-schema.sql` | `learning_notes`, `simple_chat_logs` 중심 실습용 SQL | 02, 05, 10_labs |
| `env-and-secret-management.md` | `.env`, API key, service role key, Redis token 관리 기준 | 01, 03, 06 |
| `auth-basic-guide.md` | 인증과 접근 제어의 기본 흐름 | 04 |
| `fastapi-db-patterns.md` | FastAPI에서 DB 코드를 나누는 기본 패턴 | 03 |
| `session-patterns.md` | Supabase 저장과 Redis TTL 캐시 구분 기준 | 05, 06 |

## 먼저 볼 순서

```text
1. supabase-first-notes.md
2. env-and-secret-management.md
3. supabase-schema.sql
4. auth-basic-guide.md
5. session-patterns.md
6. fastapi-db-patterns.md
```

## Supabase 테이블 생성 방법

1. Supabase Dashboard에 접속합니다.
2. 실습 프로젝트를 선택합니다.
3. 왼쪽 메뉴에서 `SQL Editor`를 엽니다.
4. `supabase-schema.sql` 내용을 붙여넣고 실행합니다.
5. Table Editor에서 `learning_notes`, `simple_chat_logs`가 생성되었는지 먼저 확인합니다.

`conversations`, `messages`, `service_logs`는 확장 참고용 테이블입니다. 현재 필수 실습은 `learning_notes`와 `simple_chat_logs` 중심으로 진행합니다.

## Upstash Redis 실습 위치

Upstash Redis 실습은 아래 챕터에서 진행합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\06_upstash-redis-cache-and-session
```

이 챕터에서는 Redis TTL 캐시만 필수로 확인합니다. Redis session, rate limit, cache-aside 구현은 뒤 과정에서 확장합니다.

## Docker 자료 안내

`02_supabase-ai-backend`에서는 Supabase와 Upstash Redis 중심으로 진행합니다. Docker 기반 PostgreSQL/Redis 운영은 `C:\aidev\07_multi-agent-service-ops`에서 진행합니다.
