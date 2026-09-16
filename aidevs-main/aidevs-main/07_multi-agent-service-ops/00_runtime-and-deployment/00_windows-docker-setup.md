# Windows Docker 사전 준비

이 문서는 `01_simple-multi-llm-compose`를 시작하기 전에 한 번만 진행합니다. 강의실·회사 PC는
Windows 기능 변경이 제한될 수 있으므로 수업 전에 관리자 권한을 확인합니다.

## 1. 현재 상태 확인

일반 PowerShell에서 실행합니다.

```powershell
docker version
docker compose version
wsl --status
```

| 결과 | 다음 행동 |
| --- | --- |
| Docker Client와 Server가 모두 표시됨 | 01 Simple Compose로 이동 |
| `docker` 명령을 찾지 못함 | WSL 2 확인 후 Docker Desktop 설치 |
| WSL 선택 기능이 필요하다는 메시지 | 아래 Windows 기능 활성화 |
| 회사 정책·관리자 권한 오류 | 임의 우회하지 말고 관리자 또는 강사에게 요청 |

## 2. WSL 2 기능 활성화

PowerShell을 **관리자 권한으로 실행**한 뒤 다음 두 기능을 활성화합니다.

```powershell
dism.exe /online /Enable-Feature /FeatureName:Microsoft-Windows-Subsystem-Linux /All /NoRestart
dism.exe /online /Enable-Feature /FeatureName:VirtualMachinePlatform /All /NoRestart
```

두 명령이 끝나면 Windows를 재시작합니다. 이미 활성화된 기능에 같은 명령을 다시
실행해도 됩니다.

재시작 후 일반 PowerShell:

```powershell
wsl --update
wsl --set-default-version 2
wsl --status
```

## 3. Docker Desktop 설치

[Docker Desktop Windows 공식 설치 안내](https://docs.docker.com/desktop/setup/install/windows-install/)에서
지원 Windows 버전, WSL 요구 사항, 조직의 사용 조건을 확인하고 설치합니다.
설치 화면에서는 Linux Container용 WSL 2 백엔드를 사용합니다.

Docker Desktop을 실행한 뒤 새 PowerShell에서 확인합니다.

```powershell
docker version
docker compose version
docker run --rm hello-world
```

`docker version`에서 Client만 나오고 Server 연결 오류가 보이면 Docker Desktop이
아직 시작 중이거나 실행되지 않은 것입니다.

정상 상태에서는 다음을 확인합니다.

| 명령 | 정상 확인 기준 |
| --- | --- |
| `wsl --status` | 기본 버전이 2이고 오류가 없음 |
| `docker version` | Client와 Server가 모두 표시됨 |
| `docker compose version` | Compose 버전이 표시됨 |
| `docker run --rm hello-world` | 성공 안내 뒤 종료 코드 0 |

## 4. 과정 Port 확인

이 과정은 Host Port `5433`, `6379`, `8000`, `8010`, `8501`, `11434`를 사용합니다.

```powershell
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object LocalPort -In 5433, 6379, 8000, 8010, 8501, 11434 |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

결과가 없다면 현재 듣고 있는 Process가 없는 것입니다. 결과가 있다면 소유 프로그램을
확인하고, 다른 수업 Compose라면 해당 폴더에서 정상 종료합니다. Process를 임의로
강제 종료하지 않습니다.

## 5. 수업 전 체크

```text
[ ] 관리자 권한 또는 담당자 지원이 준비되었다.
[ ] WSL 기본 버전이 2이다.
[ ] Docker Desktop이 실행 중이다.
[ ] docker version에서 Client와 Server를 확인했다.
[ ] docker compose version을 확인했다.
[ ] hello-world Container가 종료 코드 0으로 끝났다.
[ ] 과정에서 사용할 Host Port 충돌 여부를 확인했다.
```

Docker Desktop 설치가 불가능한 PC에서는 01의 코드를 읽고 GitHub Actions의 Linux
Runner 결과를 관찰할 수 있지만, 로컬 Container 실습 완료로 표시하지 않습니다.

## 6. 공통 로컬 서비스 설치

이 과정 앞의 `05_llm-agent-orchestration/00_local-runtime`에서 사용한 환경과 동일하게
PostgreSQL/pgvector, Redis, Ollama를 Docker Container로 준비합니다. 아래 명령은 모두
**일반 PowerShell**에서 실행합니다.

| 서비스 | Container 이름 | Host Port | 데이터 Volume | 주요 용도 |
| --- | --- | --- | --- | --- |
| PostgreSQL/pgvector | `aidevs-pgvector` | `5433` | `aidevs-pgvector-data` | RAG·장기 Memory·실행 이력 |
| Redis | `aidevs-redis` | `6379` | `aidevs-redis-data` | 진행 상태·Cache·짧은 Session |
| Ollama | `aidevs-ollama` | `11434` | `aidevs-ollama-data` | Llama·Gemma Local LLM 실행 |

Named Volume을 사용하므로 Container를 중지하거나 다시 시작해도 Database와 내려받은
Ollama Model이 유지됩니다. 기존 Container가 있다면 새로 만들지 말고 아래의 “기존 환경
다시 시작” 절차를 사용합니다.

### 6-1. 기존 Container 확인

```powershell
docker ps -a --filter "name=aidevs-"
docker volume ls --filter "name=aidevs-"
```

같은 이름의 Container가 이미 있으면 `docker run`을 다시 실행할 때 이름 충돌이 발생합니다.
기존 데이터를 무조건 삭제하지 말고 먼저 `docker start`로 재사용합니다.

### 6-2. PostgreSQL과 pgvector 설치

아래 계정 정보는 외부에 공개하지 않는 로컬 교육 전용 값입니다.

```powershell
docker run -d `
  --name aidevs-pgvector `
  -p 5433:5432 `
  -e POSTGRES_DB=agent_db `
  -e POSTGRES_USER=agent_user `
  -e POSTGRES_PASSWORD=agent_pwd `
  -v aidevs-pgvector-data:/var/lib/postgresql/data `
  pgvector/pgvector:pg16
```

준비 상태와 pgvector Extension을 확인합니다.

```powershell
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
docker exec -it aidevs-pgvector psql -U agent_user -d agent_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
docker exec -it aidevs-pgvector psql -U agent_user -d agent_db -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

첫 명령에 `accepting connections`, 마지막 결과에 `vector`가 표시되면 정상입니다. Host
Python에서 연결할 때 사용하는 기본 주소는 다음과 같습니다.

```ini
DATABASE_URL=postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db
```

### 6-3. Redis 설치

Redis 데이터가 재시작 후에도 유지되도록 AOF와 Named Volume을 함께 설정합니다.

```powershell
docker run -d `
  --name aidevs-redis `
  -p 6379:6379 `
  -v aidevs-redis-data:/data `
  redis:7 `
  redis-server --appendonly yes
```

```powershell
docker exec -it aidevs-redis redis-cli PING
```

`PONG`이 표시되면 정상입니다. Host Application의 기본 연결 주소는 다음과 같습니다.

```ini
REDIS_URL=redis://127.0.0.1:6379/0
```

이 구성에는 Redis 인증이 없으므로 로컬 수업용으로만 사용하고 외부 Network에 공개하지
않습니다.

### 6-4. Ollama 설치

```powershell
docker run -d `
  --name aidevs-ollama `
  -p 11434:11434 `
  -v aidevs-ollama-data:/root/.ollama `
  ollama/ollama:latest
```

Ollama Server가 시작되었는지 확인합니다.

```powershell
docker ps --filter "name=aidevs-ollama"
docker logs --tail 30 aidevs-ollama
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

### 6-5. Llama와 Gemma 3 4B Model 설치

Ollama Container Image에는 Model 파일이 포함되어 있지 않습니다. Container를 만든 뒤 다음
명령으로 두 Model을 각각 내려받아야 합니다.

```powershell
docker exec -it aidevs-ollama ollama pull llama3.2
docker exec -it aidevs-ollama ollama pull gemma3:4b
docker exec -it aidevs-ollama ollama list
```

정확한 Model 이름은 `gemma3:4b`입니다. `gemma 3.4b`, `gemma3.4b` 또는 `gemma:4b`로
입력하지 않습니다. Model 다운로드는 용량이 크므로 네트워크와 PC 사양에 따라 오래 걸릴 수
있습니다. 수업 예제의 환경 변수는 다음처럼 설정합니다.

```ini
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma3:4b
```

Container 안에서 Ollama에 접근하는 Application은 환경에 따라
`http://ollama:11434` 또는 `http://host.docker.internal:11434`를 사용합니다. Host에서 직접
실행하는 Python은 `http://127.0.0.1:11434`를 사용합니다.

Gemma 3 4B가 실제 응답하는지 확인합니다.

```powershell
$body = @{
    model = "gemma3:4b"
    messages = @(
        @{ role = "user"; content = "멀티 에이전트를 한 문장으로 설명해 주세요." }
    )
    stream = $false
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:11434/api/chat `
    -ContentType "application/json" `
    -Body $body
```

메모리 사용량은 다음 명령으로 확인하고 `Ctrl+C`로 관찰 화면만 종료합니다.

```powershell
docker stats aidevs-ollama
```

### 6-6. 기존 환경 다시 시작

최초 설치가 끝난 다음 수업부터는 `docker run`을 반복하지 않습니다.

```powershell
docker start aidevs-pgvector aidevs-redis aidevs-ollama
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
docker exec aidevs-redis redis-cli PING
docker exec aidevs-ollama ollama list
```

### 6-7. 과정용 설치 스크립트 사용

세 Container를 하나씩 만들기 어렵다면 앞 과정의 Script 구조를 적용한 과정용 PowerShell
Script를 실행합니다. Script는 없는 Container만 만들고, 이미 존재하면 시작합니다. pgvector
Extension을 준비하고 `llama3.2`, `gemma3:4b`가 없을 때만 Model도 내려받습니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\00_local-services
.\start-local-services.ps1
```

Script의 PostgreSQL 교육용 비밀번호와 기본 `DATABASE_URL`은 `agent_pwd`로 통일되어 있습니다.
단, 다른 비밀번호로 생성된 기존 `aidevs-pgvector-data` Volume을 재사용하면 최초 생성 시의
비밀번호가 그대로 유지됩니다. 환경 변수 변경만으로 기존 Database 비밀번호가 바뀌지는
않습니다.

수업 종료 시 Container만 중지합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\00_local-services
.\stop-local-services.ps1
```

`docker rm`, `docker volume rm`, `docker compose down -v`는 데이터를 삭제할 수 있으므로 단순
종료 목적으로 사용하지 않습니다.

### 6-8. 최종 확인

```powershell
docker ps --filter "name=aidevs-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
docker exec aidevs-redis redis-cli PING
docker exec aidevs-ollama ollama list
```

```text
[ ] aidevs-pgvector가 실행 중이고 pgvector Extension을 확인했다.
[ ] aidevs-redis에서 PONG을 확인했다.
[ ] aidevs-ollama에서 llama3.2와 gemma3:4b를 확인했다.
[ ] PostgreSQL, Redis, Ollama 데이터가 Named Volume에 저장되는 이유를 설명할 수 있다.
[ ] Container 재설치와 기존 Container 재시작의 차이를 설명할 수 있다.
```
