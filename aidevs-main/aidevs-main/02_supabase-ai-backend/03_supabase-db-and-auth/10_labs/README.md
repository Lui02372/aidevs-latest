# 10_labs

이 폴더는 `03_supabase-db-and-auth`의 `00`부터 `06`까지 배운 내용을 작은 실습 단위로 다시 확인하는 공간입니다.

각 lab은 새로운 기능을 더 만들기보다, 본문 챕터에서 이미 배운 흐름을 다시 실행하고 결과를 확인하는 데 집중합니다.

## 실습 기준

| Lab | 연결 챕터 | 핵심 확인 |
|---|---|---|
| `lab-00_reference-and-schema-map` | `00_references` | 참고 문서와 공통 SQL 파일 위치 확인 |
| `lab-01_supabase-env-check` | `01_supabase-project-and-env` | Supabase 환경변수 준비 상태 확인 |
| `lab-02_supabase-schema-preparation` | `00_references`, `02_supabase-table-and-crud`, `05_conversation-history-and-service-logs` | `learning_notes`, `simple_chat_logs` 테이블 준비 |
| `lab-03_learning-notes-crud` | `02_supabase-table-and-crud` | Python으로 Supabase CRUD 실행 |
| `lab-04_fastapi-supabase-notes-api` | `03_fastapi-supabase-integration` | FastAPI `/notes` API와 Supabase 연결 확인 |
| `lab-05_auth-jwt-bearer-flow` | `04_supabase-auth-and-rls` | Supabase Auth, JWT, Bearer token 흐름 확인 |
| `lab-06_conversation-log-storage` | `05_conversation-history-and-service-logs` | `simple_chat_logs` 저장 흐름 확인 |
| `lab-07_upstash-redis-ttl` | `06_upstash-redis-cache-and-session` | Redis SET/GET/TTL 확인 |
| `lab-08_fastapi-redis-cache` | `06_upstash-redis-cache-and-session` | FastAPI 응답 캐시 확인 |

## 실습 전 준비

백엔드 과정 루트에서 가상환경을 활성화합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Supabase 관련 실습을 진행하려면 `.env`에 아래 값이 필요합니다.

```text
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
```

LLM 로그 저장 실습에서 Gemini를 실제로 호출하려면 아래 값도 필요합니다.

```text
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash-lite
```

Upstash Redis 관련 실습을 진행하려면 아래 값이 필요합니다.

```text
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...
```

실제 key 값은 lab 결과 문서, GitHub, 캡처 화면에 그대로 남기지 않습니다.

## 테이블 준비 기준

아래 파일을 Supabase SQL Editor에서 실행합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
```

현재 필수 확인 테이블:

| 테이블 | 사용하는 챕터 |
|---|---|
| `learning_notes` | 02, 03, lab-03, lab-04 |
| `simple_chat_logs` | 05, lab-06 |

`conversations`, `messages`, `service_logs`는 이후 확장 구조를 이해하기 위한 참고 테이블입니다. 초반 lab의 필수 실행 대상은 아닙니다.

## 실습 결과 정리 방법

각 lab을 진행한 뒤 아래 내용을 짧게 기록합니다.

```text
1. 실행한 파일 또는 접속한 URL
2. 정상 실행 결과
3. 발생한 오류 메시지
4. 오류를 해결한 방법
5. Supabase 또는 Redis에서 확인한 데이터
```

## 제외한 내용

현재 `00`~`06` 기준에서는 아래 내용을 필수 lab으로 진행하지 않습니다.

| 제외한 내용 | 이유 |
|---|---|
| RLS 정책 SQL 작성 | 04에서는 Auth/JWT/Bearer 흐름까지만 다룹니다. |
| Redis rate limit 구현 | 06에서는 TTL 캐시만 최소 예제로 확인합니다. |
| Redis session/cache-aside 구현 | 인증, 사용자 구분, 캐시 갱신 정책까지 필요하므로 뒤 과정에서 확장합니다. |
| Docker PostgreSQL/Redis 운영 | `07_multi-agent-service-ops`에서 다룹니다. |
