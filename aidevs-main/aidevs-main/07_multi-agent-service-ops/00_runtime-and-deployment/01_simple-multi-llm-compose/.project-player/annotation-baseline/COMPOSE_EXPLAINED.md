# 두 Docker Compose 구성 이해하기

## 기본 `compose.yml`

현재 수업 PC에 이미 실행 중인 PostgreSQL·Redis·Ollama를 재사용합니다.

```text
frontend Container → backend Container
                         ├─ host.docker.internal:6379 Redis
                         ├─ host.docker.internal:5433 PostgreSQL
                         ├─ host.docker.internal:11434 Ollama
                         ├─ OpenAI HTTPS API
                         └─ Gemini HTTPS API
```

`host.docker.internal`은 Container에서 Windows Host 방향으로 접근하는 이름입니다.
Backend Container에서 `127.0.0.1`은 Backend Container 자기 자신을 뜻합니다.

Frontend가 Backend에 접근할 때 사용하는 환경 변수 이름은 `BACKEND_URL`입니다.

```text
Host에서 Frontend 직접 실행 → 기본값 http://127.0.0.1:8000
Docker Compose 실행        → http://backend:8000
```

이 프로젝트는 `API_BASE_URL`을 사용하지 않습니다.

## 선택 `compose.full-stack.yml`

공용 Container가 없는 PC에서 전체 환경을 별도로 만듭니다.

```text
frontend → backend → redis
                   → database
                   → 선택 ollama
```

같은 Compose Network에서는 `redis`, `database`, `ollama`, `backend` 같은 Service 이름을
DNS 주소로 사용합니다.

## 설정 주소 비교

| 호출 위치 | PostgreSQL | Redis | Ollama |
| --- | --- | --- | --- |
| Host Python | `127.0.0.1:5433` | `127.0.0.1:6379` | `127.0.0.1:11434` |
| 기본 Backend Container | `host.docker.internal:5433` | `host.docker.internal:6379` | `host.docker.internal:11434` |
| Full Stack Backend | `database:5432` | `redis:6379` | `ollama:11434` |

## 환경 변수 역할

```text
POSTGRES_USER·POSTGRES_PASSWORD·POSTGRES_DB
└─ Full Stack PostgreSQL Container 초기 생성

DATABASE_URL
└─ 기본 Backend가 기존 공용 PostgreSQL에 접속

REDIS_URL
└─ 기본 Backend가 기존 공용 Redis에 접속
```

Full Stack Compose는 Backend 주소를 내부 Service 이름으로 명시적으로 바꾸므로 같은
`.env`를 사용해도 Host 주소와 혼동하지 않습니다.

## init.sql 실행 시점

```text
기본 compose.yml
└─ 기존 PostgreSQL 재사용 → init_database.py를 최초 한 번 실행

compose.full-stack.yml
└─ 새 PostgreSQL Volume 생성 → docker-entrypoint-initdb.d가 init.sql 자동 실행
```

`docker-entrypoint-initdb.d`의 SQL은 PostgreSQL 데이터 디렉터리가 비어 있을 때만 자동
실행됩니다. 이미 만들어진 공용 Database에 Application Container만 연결하면 자동으로
실행되지 않습니다.

## Volume

기본 Compose는 Application Container만 만들기 때문에 공용 저장소의 기존 Volume을
변경하지 않습니다. Full Stack Compose는 다음 전용 Volume을 만듭니다.

```text
redis_data    → Redis AOF 데이터
postgres_data → Chat과 여행 메모
ollama_data   → 내려받은 Model
```

일반 `down`은 Volume을 유지하고 `down -v`는 삭제합니다.
