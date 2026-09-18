# Windows DB 계정 정리와 pgAdmin 연결

> 현재 프로젝트는 다시 `weather07_db / weather07_user`를 사용합니다.
> 중간에 생성한 `intedb / inteuser`는 보존하며 현재 프로젝트에서는 사용하지 않습니다.

이 문서는 2026-09-16에 이 PC에서 실제 조사한 결과와 07번 전용 설정을 설명합니다.
이제 07번의 Windows 개발에는 **127.0.0.1:5432 / weather07_db / weather07_user**를 사용합니다.
기존 강의 DB와 VectorDB는 별개이며 데이터는 보존했습니다.

## 1. 무엇이 섞여 있었나?

| 대상 | 주소 | DB / 사용자 | 확인 상태 |
| --- | --- | --- | --- |
| Windows PostgreSQL 18.6 | 127.0.0.1:5432 | postgres / postgres | 실행 중, 관리자 비밀번호 재설정 |
| **07 Windows 프로젝트** | **127.0.0.1:5432** | **weather07_db / weather07_user** | 새 DB·로그인 계정·weather_agent.runs 생성 |
| 기존 Windows 강의 DB | 127.0.0.1:5432 | agent_db / agent_user | 기존 DB·계정 보존 |
| VectorDB, pgvector 0.8.6 | 127.0.0.1:15432 | vectordb / vectadmin | 실행 중, 기존 비밀번호로 실제 인증 검증 완료 |
| 기존 공용 강의 Docker DB | 127.0.0.1:5433 | agent_db / agent_user | multi-agent-postgres 중지 상태 |
| Project Player Docker DB | 127.0.0.1:15433 | agent_db / agent_user | project-player-course07-database-1 중지 상태 |

pgAdmin에 있던 `PostgreSQL 18` 두 항목은 같은 Windows 서버를 `localhost`와 `127.0.0.1`로
중복 등록한 것입니다. `VectorDB (pgvector)`는 다른 서버입니다. pgAdmin의 서버 표시 이름만
보고 같은 계정이라고 판단하지 마세요. **host + port + database + username**을 함께 봅니다.

벡터 DB는 별도의 계정 방식이 아니라 PostgreSQL에 vector 확장을 추가한 서버입니다.
현재 VectorDB에는 vector·pg_trgm 확장이 있고, Windows postgres DB에서는 plpgsql만
확인했습니다. 일반 날씨 이력을 저장하는 07 프로젝트에는 vector 확장이 필요하지 않습니다.

## 2. 새 비밀번호를 확인하는 곳

채팅·README·Git에 비밀번호를 기록하지 않았습니다. 아래 두 파일은 `.local/` 아래에 있고
Git에서 제외되며 Windows 파일 권한도 제한되어 있습니다.

- [.local/db-credentials.env](.local/db-credentials.env): 새 Windows 관리자·07 프로젝트 계정.
- [.local/known-legacy-db-credentials.env](.local/known-legacy-db-credentials.env): 기존 Docker 설정에서 확인한 계정. 중지된 Container는 실제 인증 미검증이라고 표시합니다.

VectorDB의 현재 비밀번호는 두 번째 파일의 **VECTOR_PASSWORD**입니다. 기존 실행 앱의
WORLDS_DB 설정과 대조하고 15432 서버에서 실제 로그인에 성공했습니다. 변경하지 않았으므로
그 비밀번호를 사용하는 기존 앱의 설정도 유지됩니다.

첫 파일의 항목:

| 키 | 쓰는 곳 |
| --- | --- |
| WINDOWS_POSTGRES_ADMIN_USER | 관리자 로그인: postgres |
| WINDOWS_POSTGRES_ADMIN_PASSWORD | Windows PostgreSQL 관리자 비밀번호 |
| POSTGRES_USER | 프로젝트 로그인: weather07_user |
| POSTGRES_PASSWORD | 프로젝트 로그인 비밀번호, 07 .env와 동일 |
| POSTGRES_DB | 프로젝트 DB: weather07_db |

이 파일은 현재 PC에만 존재하는 비공개 파일이므로 GitHub에서 README를 읽을 때는 링크가
없을 수 있습니다. 파일 내용을 화면 공유하거나 GitHub에 업로드하지 마세요.
비밀번호를 다시 변경하면 **실제 DB 역할의 비밀번호와 .env를 함께** 변경해야 합니다.

## 3. pgAdmin의 세 가지 비밀번호

| 비밀번호 | 적용 대상 | 변경 효과 |
| --- | --- | --- |
| pgAdmin Master Password | pgAdmin이 저장한 연결 비밀번호 보호 | DB 로그인 비밀번호 자체는 바뀌지 않음 |
| postgres 관리자 비밀번호 | Windows PostgreSQL 서버 관리자 | 관리자 접속에 사용 |
| weather07_user 비밀번호 | 07 프로젝트용 DB 로그인 | 앱과 pgAdmin 프로젝트 연결에 사용 |

Master Password를 DB 접속 Password에 넣으면 안 됩니다. 반대도 마찬가지입니다.
pgAdmin 버전·설정에 따라 Windows 자격 증명 저장소를 사용하여 Master Password 창이
나오지 않을 수도 있습니다. 이 경우 창이 없는 것만으로 오류라고 판단하지 마세요.

Master Password를 잊었다면 입력 창의 **Reset Master Password**로 재설정합니다.
저장된 DB 비밀번호가 지워지고 열린 연결이 닫히지만 PostgreSQL 데이터는 삭제되지 않습니다.
이후 프로젝트 접속에는 위 비공개 파일의 POSTGRES_PASSWORD를 다시 입력합니다.
Master Password 최종 변경은 사용자가 직접 수행하며 자동 완료로 표시하지 않습니다.

## 4. 프로젝트 서버 하나로 접속

등록 이름은 **07 Windows - Project (5432 / weather07_db)**입니다.
공식 import용 파일은 [deploy/pgadmin-windows-servers.json](deploy/pgadmin-windows-servers.json)에
있으며 프로젝트·관리자·기존 VectorDB의 구분된 연결 정의를 제공합니다.
이전에 자동 등록한 `07 Windows - Project (5432 / weather07_db)` 연결을 사용합니다. 아래 값과 일치하는지 확인하세요.

pgAdmin에서 현재 weather07_db 연결을 선택하거나 아래 값으로 등록합니다.
프로젝트 연결을 열 때 비밀번호가 요청되면 `.local/db-credentials.env`의
**POSTGRES_PASSWORD** 값을 입력합니다.

수동으로 등록한다면 Servers 우클릭 → Register → Server에서 다음을 사용합니다.

| 탭 / 항목 | 값 |
| --- | --- |
| General / Name | 07 Windows - Project (5432 / weather07_db) |
| Connection / Host | 127.0.0.1 |
| Connection / Port | 5432 |
| Connection / Maintenance database | weather07_db |
| Connection / Username | weather07_user |
| Connection / Password | 비공개 파일의 POSTGRES_PASSWORD |

연결 후 Query Tool:

```sql
SELECT current_user, current_database();
SELECT * FROM weather_agent.runs ORDER BY created_at DESC LIMIT 10;
```

첫 결과는 `weather07_user / weather07_db`입니다. 아직 앱 요청을 저장하지 않았다면 runs는
비어 있습니다. 프로젝트 역할은 superuser·createdb·createrole 권한을 갖지 않습니다.
관리 작업이 필요할 때만 기존 PostgreSQL 18 연결의 postgres 계정을 사용합니다.

## 5. 지금 변경한 인증 설정과 보존한 것

Windows PostgreSQL의 기존 IPv4 localhost 규칙은 `trust`여서 비밀번호를 검사하지 않았습니다.
이제 그 규칙보다 앞에 **postgres와 weather07_user만 scram-sha-256으로 인증하는 규칙**을
추가했습니다. 두 계정의 올바른 비밀번호는 성공하고 틀린 비밀번호는 실패함을 확인했습니다.
기존 agent_user 등 다른 역할의 인증 규칙은 다른 강의 앱을 끊지 않도록 유지했습니다.
따라서 모든 기존 계정의 trust 설정을 일괄 해제한 상태는 아닙니다.

기존 agent_db, vectordb, Docker Volume과 중지된 Container는 삭제하지 않았습니다.
관리자 암호 재설정 전후로 열린 연결은 유지될 수 있으므로 재접속 시 새 암호를 입력하세요.
기존 설정과 pgAdmin 등록 DB의 백업은 `.local/`에 있습니다.

## 6. 07 앱을 Windows PostgreSQL에 연결

현재 07 `.env`는 아래 구성을 갖습니다. 비밀번호 값은 실제 파일에만 저장했습니다.

```dotenv
POSTGRES_USER=weather07_user
POSTGRES_PASSWORD=<로컬 파일의 실제 값>
POSTGRES_DB=weather07_db
DATABASE_URL=postgresql://weather07_user:<같은 비밀번호>@127.0.0.1:5432/weather07_db
REDIS_URL=redis://127.0.0.1:6379/7
WEATHER_MCP_URL=http://127.0.0.1:8010/mcp
BACKEND_URL=http://127.0.0.1:8000
```

위 코드는 설명용이므로 `<...>`를 실제 `.env`에 덮어쓰지 마세요. `.env`는 이미 맞춰 놓았습니다.
Redis는 기존 6379 서비스를 사용하되 논리 DB 7을 선택했습니다. 이 변경은 기존 Redis 데이터를
초기화하지 않습니다. 계정 준비와 애플리케이션 전체 실행은 별도의 검증 단계입니다.

Windows에서 Python 프로세스로 실행하는 예입니다. 모든 터미널의 현재 폴더를 07로 맞춥니다.
먼저 필요한 패키지를 설치합니다.

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r frontend/requirements.txt
```

터미널 A — MCP 서버:

```powershell
.\.venv\Scripts\python.exe mcp_server/server.py
```

터미널 B — Backend(.env 명시적 로딩):

```powershell
.\.venv\Scripts\python.exe -m uvicorn app:app --app-dir backend --env-file .env --host 127.0.0.1 --port 8000
```

터미널 C — Frontend:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```

`http://127.0.0.1:8000/health/ready`에서 DB·Redis·MCP 상태를 보고 `http://127.0.0.1:8501`을
엽니다. OpenAI 또는 Gemini API 키를 .env에 입력하고 화면에서 해당 provider를 선택합니다.
`.env` 파일은 Python이 자동으로 읽지 않으므로 Backend의 `--env-file .env`를 생략하지 마세요.

**기존 Compose 경로는 별도 Docker PostgreSQL을 만드는 경로입니다.**
Compose는 POSTGRES_USER/PASSWORD/DB로 Container 내부 `database:5432`에 연결하고,
위 DATABASE_URL로 Windows DB에 접속하지 않습니다. 두 경로의 이력이 자동 공유되는 것으로
생각하지 마세요. 현재 정리한 Windows DB를 이용하려면 위 Python 실행 경로를 선택합니다.

## 7. EC2 학습으로 넘어갈 때

Windows `127.0.0.1`과 EC2 `127.0.0.1`은 서로 다른 컴퓨터입니다.
EC2에서는 README의 Compose 배포를 사용해 별도 PostgreSQL과 데이터 Volume을 준비합니다.
서버 전용 `.env`와 비밀번호를 만들고, 로컬 `.local` 디렉터리는 업로드하지 않습니다.
Windows DB 데이터를 이전하려면 별도로 pg_dump/restore를 수행해야 합니다.

pgAdmin으로 EC2 DB를 보려면 EC2의 Infrastructure Compose에 아래 **loopback 바인딩**만
추가합니다. PostgreSQL을 인터넷 전체에 공개하지 않습니다.

```yaml
services:
  database:
    ports:
      - "127.0.0.1:5434:5432"
```

배포 파일로 관리하고 EC2에서 Infrastructure 설정을 적용한 후, Windows PowerShell에서
SSH 터널을 엽니다. SSH의 관리자 IP 허용 등 사전 조건은 README를 따릅니다.

```powershell
ssh -i C:\keys\weather-07.pem -N -L 15435:127.0.0.1:5434 ubuntu@EC2_PUBLIC_IP
```

터널을 켜 둔 상태에서 pgAdmin에 별도 이름 `07 EC2 - Project`를 등록합니다.

| 항목 | 값 |
| --- | --- |
| Host | 127.0.0.1 |
| Port | 15435 |
| Maintenance DB | EC2 .env의 POSTGRES_DB |
| Username / Password | EC2 .env의 POSTGRES_USER / POSTGRES_PASSWORD |

이 구조에서는 PC 5432는 Windows DB, PC 15435는 SSH 터널을 거친 EC2 DB입니다.
GitHub CD의 OIDC 권한, LLM provider의 API 키, PostgreSQL 로그인은 각각 다른 인증입니다.

## 근거

- 실제 pgAdmin 등록 목록, Windows PostgreSQL 역할/DB 조회, Docker ps/inspect, pgvector 확장 조회.
- [pgAdmin Master Password](https://www.pgadmin.org/docs/pgadmin4/latest/master_password.html)
- [pgAdmin 공식 import/export](https://www.pgadmin.org/docs/pgadmin4/latest/import_export_servers.html)
- [PostgreSQL HBA 규칙](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)
