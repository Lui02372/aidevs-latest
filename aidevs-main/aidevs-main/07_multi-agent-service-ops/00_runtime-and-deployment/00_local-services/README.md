# 00 Local Runtime

## 역할

이 Compose는 이후 01~09 과정과 Mini Project에서 공통으로 사용하는 PostgreSQL·Redis·
Ollama 환경입니다. 과정마다 저장소 Container를 새로 만들지 않고 Schema와 Redis Key
Prefix를 분리합니다.

| 서비스 | 주소 | 용도 |
| --- | --- | --- |
| Ollama | `http://127.0.0.1:11434` | 로컬 Llama·Gemma |
| PostgreSQL | `127.0.0.1:5433` | Task·Trace·평가 이력 |
| Redis | `127.0.0.1:6379` | Queue·진행 상태·TTL |

이 주소는 01~09와 Mini Project의 `.env.example`에서 사용하는 과정 공통 기준입니다.

## 1. 실행 위치 확인

현재 PC의 충돌 해결과 전체 학습 요약은 [summary.md](../summary.md)를 참고하세요.
Redis 공개 포트는 `.env`의 `REDIS_HOST_PORT`로 변경할 수 있습니다(기본 6379).
6380으로 변경하면 Host 앱의 `REDIS_URL`도 6380으로 맞춰야 합니다.
Ollama는 선택 profile이므로 기본 `docker compose up -d`에서는 실행되지 않습니다.
기존 Ollama가 11434에서 실행 중이면 그것을 사용하세요.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\00_local-services
Get-Location
Get-ChildItem -Force
```

출력에 `docker-compose.yml`과 `.env.example`이 보여야 합니다. 다른 폴더에서 실행하면
다른 Compose 프로젝트를 조작할 수 있으므로 위치부터 확인합니다.

## 2. 환경 변수와 Compose 설정 확인

```powershell
Copy-Item .env.example .env
Get-Content .env
docker compose config --quiet
```

`docker compose config --quiet`가 메시지 없이 끝나면 YAML과 환경 변수 해석에 성공한
것입니다. 오류가 나타나면 `up` 전에 누락 변수와 들여쓰기를 수정합니다.

이전 설정인 `postgres/postgres/multi_agent`로 이미 Volume을 만든 경우 `.env`만 바꿔도
기존 PostgreSQL 사용자와 Database는 자동으로 변경되지 않습니다. 학습 데이터가 필요하면
먼저 Backup하고, 초기화가 가능한 새 실습 환경에서만 Volume을 제거한 뒤 다시 생성합니다.
기존 Volume을 확인하지 않고 `down -v`를 실행하지 않습니다.

## 3. 저장소부터 실행

```powershell
docker compose up -d redis postgres
docker compose ps
```

Redis와 PostgreSQL의 상태가 `running` 또는 `healthy`여야 합니다. `exited`이면 먼저
해당 서비스 로그를 확인합니다.

```powershell
docker compose logs --tail=100 redis
docker compose logs --tail=100 postgres
```

## 4. 서비스별 연결 확인

```powershell
docker compose exec redis redis-cli ping
docker compose exec postgres pg_isready -U agent_user -d agent_db
```

Redis는 `PONG`, PostgreSQL은 `accepting connections`를 반환해야 합니다.

```text
Host Python → 127.0.0.1:6379, 127.0.0.1:5433
Compose Service → redis:6379, postgres:5432
```

## 5. 과정 Database 구조 초기화

PostgreSQL Container가 정상이라면 Host PowerShell에서 Python 초기화 프로그램을
실행합니다.

```powershell
python -m pip install "psycopg[binary]>=3.2,<4" "python-dotenv>=1.0,<2"
python .\init_database.py
```

프로그램은 `.env`의 다음 값을 읽습니다.

```ini
DATABASE_URL=postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db
```

`init_database.py`는 같은 폴더의 `init.sql`을 실행하여 `vector` Extension과 과정 공통
Table을 준비합니다. `DROP TABLE`이나 데이터 삭제는 수행하지 않습니다. SQL을 수정한 후
초기화 프로그램을 다시 실행해도 `IF NOT EXISTS`가 적용된 객체는 유지됩니다.

## 6. Ollama 선택 실행

Ollama를 사용할 때 최초 한 번 Model을 받습니다.

```powershell
docker compose up -d ollama
docker compose exec ollama ollama pull llama3.2
docker compose exec ollama ollama pull gemma3:4b
docker compose exec ollama ollama list
```

OpenAI 또는 Gemini만 사용한다면 Ollama를 실행하거나 Model을 받을 필요가 없습니다.

Host Python은 Ollama `127.0.0.1:11434`를 사용하고, Compose 내부 서비스는
`ollama:11434`, `postgres:5432`, `redis:6379`로 연결합니다.

## 7. 종료와 다시 시작

```powershell
docker compose down
docker compose up -d redis postgres
docker compose ps
```

일반 `docker compose down`은 Volume을 유지합니다. `docker compose down -v`는
PostgreSQL·Redis 데이터와 내려받은 Ollama Model을 삭제하므로 현재 Volume과 학습
데이터를 확인한 뒤 완전 초기화가 확실할 때만 사용합니다.

## 8. 완료 체크

```text
[ ] Compose 설정 검사를 통과했다.
[ ] Redis가 PONG을 반환한다.
[ ] PostgreSQL이 accepting connections를 반환한다.
[ ] init_database.py로 과정 공통 Table을 준비했다.
[ ] Host Port와 Container Port의 차이를 설명할 수 있다.
[ ] down과 down -v의 차이를 설명할 수 있다.
```
