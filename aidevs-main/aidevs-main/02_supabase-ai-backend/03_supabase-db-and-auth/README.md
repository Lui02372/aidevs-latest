# 03_supabase-db-and-auth

이 단원은 FastAPI 백엔드에서 Supabase를 사용해 데이터 저장, 인증, JWT 흐름, 대화 로그 저장, Redis TTL 캐시를 다루는 과정입니다.

`02_supabase-ai-backend`는 Supabase 중심으로 진행합니다. Redis는 Docker로 직접 실행하지 않고, Upstash Redis를 사용해 TTL 기반 임시 캐시만 가볍게 실습합니다. Redis session, rate limit, cache-aside 같은 확장 패턴은 뒤 과정에서 다시 다룹니다. Docker, Docker Compose, 로컬 PostgreSQL/Redis 운영은 `C:\aidev\07_multi-agent-service-ops`에서 본격적으로 학습합니다.

## 학습 목표

- Supabase 프로젝트를 만들고 API URL/key를 설정합니다.
- Supabase Table Editor와 SQL Editor로 테이블을 설계합니다.
- Python Supabase client로 CRUD를 실행합니다.
- FastAPI endpoint에서 Supabase를 호출합니다.
- Supabase Auth, JWT, Bearer token의 흐름을 이해합니다.
- RLS는 사용자별 데이터 접근 제어에 사용하는 기능임을 이해합니다.
- 사용자 질문과 AI 답변을 Supabase 테이블에 저장하는 구조를 이해합니다.
- Upstash Redis로 TTL 기반 캐시의 기본 흐름을 실습합니다.
- Supabase에 저장할 데이터와 Redis에 저장할 데이터를 구분합니다.

## 이 단원에서 만드는 것

| 구분 | 결과물 | 설명 |
|---|---|---|
| Supabase 설정 | `.env` 환경변수 준비 | URL/key가 정확히 들어갔는지 확인합니다. |
| DB 기초 | `learning_notes` CRUD 예제 | Python에서 Supabase 테이블에 생성/조회/수정/삭제를 실행합니다. |
| API 연동 | FastAPI `notes` API | 백엔드 endpoint가 Supabase를 호출하는 구조를 익힙니다. |
| 인증/보안 | Auth/JWT/Bearer token 예제 | 로그인 사용자 확인과 보호 API 호출 흐름을 이해합니다. |
| 로그/이력 | `simple_chat_logs` 저장 예제 | AI 서비스에서 질문/답변/상태를 Supabase에 저장합니다. |
| Redis | Upstash Redis TTL cache 예제 | 오래 저장하지 않아도 되는 임시 값을 Redis에 저장합니다. |
| 실습/과제 | `10_labs`, `20_assignments` | 따라 하기 실습과 제출 과제를 분리해서 진행합니다. |

## 단원 구조

```text
03_supabase-db-and-auth
├─ 00_references
├─ 01_supabase-project-and-env
├─ 02_supabase-table-and-crud
├─ 03_fastapi-supabase-integration
├─ 04_supabase-auth-and-rls
├─ 05_conversation-history-and-service-logs
├─ 06_upstash-redis-cache-and-session
├─ 10_labs
├─ 20_assignments
└─ 90_structured-fastapi-examples
```

## 권장 학습 순서

```text
00_references/README.md
-> 00_references/supabase-first-notes.md
-> 01_supabase-project-and-env
-> 02_supabase-table-and-crud
-> 03_fastapi-supabase-integration
-> 04_supabase-auth-and-rls
-> 05_conversation-history-and-service-logs
-> 06_upstash-redis-cache-and-session
-> 10_labs
-> 20_assignments
```

`90_structured-fastapi-examples`는 위 흐름을 마친 뒤 필요할 때 보는 독립 참고 예제입니다. 처음 학습 순서에 반드시 포함하지 않습니다.

## 먼저 준비할 것

최상위 폴더에서 `.env`를 준비합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
Copy-Item .env.example .env
```

`.env`에 Supabase 값을 입력합니다.

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
UPSTASH_REDIS_REST_URL=https://your-upstash-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-upstash-redis-rest-token
```

위 값은 예시입니다. 실제 실습에서는 Supabase Dashboard와 Upstash Console에서 발급받은 실제 값을 `.env`에 넣어야 합니다. `.env`는 GitHub에 올리지 않습니다.

가상환경을 활성화하고 패키지를 설치합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Supabase 테이블 준비

기본 실습용 SQL은 아래 파일에 있습니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
```

Supabase Dashboard의 SQL Editor에서 실행합니다.

처음에는 `learning_notes` 테이블 하나로 CRUD를 시작하고, 이후 `simple_chat_logs`로 LLM 질문/답변 로그를 한 테이블에 저장합니다. `conversations`, `messages`, `service_logs`는 더 복잡한 서비스 구조로 확장할 때 참고하는 선택 테이블입니다.

## 기본 실행 순서

환경변수 확인:

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
dir .env
```

`.env` 파일을 VS Code에서 열고 `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`가 실제 값으로 입력되어 있는지 확인합니다. key 전체 값은 터미널이나 문서에 출력하지 않습니다.

Supabase CRUD 확인:

```powershell
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\01_create_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\02_list_learning_notes.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\03_get_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\04_update_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\05_delete_learning_note.py
python .\03_supabase-db-and-auth\02_supabase-table-and-crud\06_learning_notes_crud_all.py
```

FastAPI + Supabase 실행:

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\03_fastapi-supabase-integration
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

확인 주소:

```text
http://127.0.0.1:8000/docs
```

Supabase Auth FastAPI/Swagger 확인:

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\04_supabase-auth-and-rls
..\..\.venv\Scripts\Activate.ps1
python -m uvicorn 01_fastapi_supabase_auth:app --reload --host 127.0.0.1 --port 8002
```

확인 주소:

```text
http://127.0.0.1:8002/docs
```

대화 이력과 서비스 로그 저장:

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\05_conversation-history-and-service-logs\01_insert_conversation_and_log.py
```

FastAPI + LLM 채팅 로그 저장:

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\05_conversation-history-and-service-logs
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
```

확인 주소:

```text
http://127.0.0.1:8003/docs
```

Upstash Redis TTL 캐시 실습:

```powershell
python .\03_supabase-db-and-auth\06_upstash-redis-cache-and-session\01_redis_set_get_ttl.py
```

FastAPI + Redis 캐시 실습:

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\06_upstash-redis-cache-and-session
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
```

확인 주소:

```text
http://127.0.0.1:8004/docs
```

## Supabase와 Redis를 함께 보는 기준

가장 자주 헷갈리는 부분은 “어떤 데이터는 Supabase에 넣고, 어떤 데이터는 Redis에 넣어야 하는가”입니다.

| 데이터 예시 | 저장 위치 | 이유 |
|---|---|---|
| 사용자 프로필 | Supabase | 나중에 다시 조회해야 하는 영구 데이터입니다. |
| 대화 이력 | Supabase | 사용자가 과거 대화를 다시 볼 수 있어야 합니다. |
| 서비스 로그 | Supabase | 오류 분석, 사용 기록, 품질 개선에 사용합니다. |
| 30초짜리 검색 결과 캐시 | Upstash Redis | 잠깐만 빠르게 재사용하면 됩니다. |
| 같은 질문에 대한 60초짜리 답변 캐시 | Upstash Redis | 잠깐만 빠르게 재사용하면 됩니다. |

중요한 기준은 다음과 같습니다.

```text
오래 보관해야 한다 -> Supabase
검색/분석/조회가 중요하다 -> Supabase
짧게 보관하고 자동 만료되어도 된다 -> Upstash Redis
TTL이 지나면 사라져도 되는 임시 값이다 -> Upstash Redis
```

## Lab과 Assignment

따라 하기 실습은 아래 폴더에서 진행합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\10_labs
```

제출 과제는 아래 폴더에서 진행합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\20_assignments
```

## Docker 자료 안내

현재 과정에서는 Docker로 PostgreSQL/Redis를 직접 실행하지 않습니다. Docker로 PostgreSQL/Redis를 직접 실행하고 운영하는 방식은 아래 과정에서 다룹니다.

```text
C:\aidev\07_multi-agent-service-ops
```

## 구조화 참고 예제

`90_structured-fastapi-examples`는 본문 `00`~`06`을 마친 뒤 참고하는 독립 예제 모음입니다. 본문 학습 흐름에 필수로 포함하지 않고, 나중에 프로젝트 구조를 다시 보고 싶을 때 참고합니다.

## 자주 만나는 오류

### Supabase 값이 없다고 나오는 경우

`.env`가 있는지 확인합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
dir .env
```

### relation learning_notes does not exist

Supabase SQL Editor에서 `supabase-schema.sql`의 테이블 생성 SQL을 먼저 실행합니다.

### Could not find the table simple_chat_logs

채팅 로그 실습용 테이블이 아직 없다는 뜻입니다. `00_references/supabase-schema.sql`을 Supabase SQL Editor에서 실행한 뒤 다시 시도합니다.

### FastAPI에서 Supabase 연결 실패

확인할 것:

1. `.env`가 최상위 폴더에 있는가?
2. `SUPABASE_URL`이 정확한가?
3. `SUPABASE_SERVICE_ROLE_KEY`가 실제 값인가?
4. Supabase 프로젝트가 paused 상태는 아닌가?

### Upstash Redis 연결 실패

확인할 것:

1. `.env`에 `UPSTASH_REDIS_REST_URL`이 있는가?
2. `.env`에 `UPSTASH_REDIS_REST_TOKEN`이 있는가?
3. Upstash Redis database가 삭제되거나 비활성화되지 않았는가?
4. URL 끝에 불필요한 공백이 들어가지 않았는가?
