# 07 Multi AI Agent Orchestration · 전체 환경 설정

이 문서는 `07_multi-agent-service-ops`의 01~09 실습에 필요한 Python, LLM Provider,
Docker, PostgreSQL/pgvector, Redis, Ollama, MCP 환경을 준비합니다.

처음 시작할 때는 위에서 아래로 모두 진행하고, 다음 수업부터는 기존 가상환경과 Container를
다시 시작하는 절차만 실행합니다.

> 과정의 목표와 01~09 학습 흐름은 루트 `README.md`에서 먼저 확인합니다.
## 처음부터 준비하기

이 과정의 `01~09` Python 예제는 과정 루트의 가상환경과 `.env`를 공통으로 사용합니다.
처음 수업을 시작할 때 한 번 준비하고, 다음 수업부터는 기존 가상환경과 Docker Container를
다시 시작합니다.

### 1. 과정 루트와 Python 확인

일반 PowerShell에서 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python --version
docker version
docker compose version
```

Python과 Docker Client·Server가 모두 정상이어야 합니다. `docker version`에 Client만 나오고
Server 오류가 보이면 Docker Desktop을 먼저 실행합니다.

### 2. Python 가상환경 최초 생성

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

- `.venv`는 이 과정의 Python Package를 다른 프로젝트와 분리합니다.
- `pip install -r requirements.txt`는 실행에 필요한 Package를 설치합니다.
- 이 과정은 별도의 설치형 Python Package가 아닙니다.
- 예제는 과정 루트에서 실행하며 Python이 루트의 `shared` Module을 직접 찾습니다.
- 가상환경 폴더는 다른 PC로 복사하지 않고 각 PC에서 새로 생성합니다.

PowerShell에서 Script 실행이 차단되면 현재 사용자 범위의 정책을 확인합니다.

```powershell
Get-ExecutionPolicy -List
```

회사·교육기관 PC의 보안 정책을 임의로 우회하지 말고 관리자 또는 강사의 안내를 따릅니다.

다음 수업부터는 새로 만들거나 Package를 매번 설치하지 않고 활성화만 합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
.\.venv\Scripts\Activate.ps1
```

### 3. 과정 공통 `.env` 만들기

```powershell
cd C:\aidevs\07_multi-agent-service-ops
Copy-Item .env.example .env
```

이미 `.env`가 있다면 덮어쓰기 전에 기존 API Key와 개인 설정을 확인합니다. `.env`는 Git에
Commit하지 않습니다.

```powershell
git check-ignore .env
```

### 4. GPT·Gemini·Llama·Gemma 설정

`.env`에 사용할 실제 Provider와 Model을 설정합니다.

```dotenv
LLM_PROVIDER=openai

OPENAI_API_KEY=본인의_OPENAI_API_KEY
OPENAI_MODEL=gpt-4.1-mini

GEMINI_API_KEY=본인의_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash

OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma3:4b
```

GPT와 Gemini는 Cloud LLM이므로 API Key와 인터넷 연결이 필요합니다. Llama와 Gemma는 같은
Ollama Server를 사용하지만 서로 다른 Local Model입니다. 이 과정에서 `ollama`와 `gemma`는
서로 다른 Server 이름이 아니라 어떤 Model을 선택할지 구분하기 위한 논리 Provider 이름입니다.

| 논리 Provider | 실제 실행 위치 | Model |
| --- | --- | --- |
| `openai` | OpenAI Cloud API | `gpt-4.1-mini` |
| `gemini` | Google Cloud API | `gemini-3.5-flash` |
| `ollama` | 로컬 Ollama `11434` | `llama3.2` |
| `gemma` | 같은 로컬 Ollama `11434` | `gemma3:4b` |

Model 이름 `gemma3:4b`에서 `3`은 Gemma 세대이고 `4b`는 모델 규모를 나타냅니다.
`gemma3.4b`, `gemma 3.4b`, `gemma:4b`로 입력하지 않습니다.

### 5. Agent별 Provider 설정

각 AI Agent가 사용할 기본 Provider도 `.env`에서 변경할 수 있습니다.

`ollama`는 Local Server를 막연하게 가리키는 값이 아니라 이 과정에서 `llama3.2`를 선택하는
논리 Provider입니다. `gemma`는 같은 Ollama Server에서 `gemma3:4b`를 선택합니다.

```dotenv
# openai → OpenAI Cloud API · gpt-4.1-mini
SUPERVISOR_PROVIDER=openai

# gemini → Google Gemini Cloud API · gemini-3.5-flash
WEATHER_AGENT_PROVIDER=gemini

# ollama → Local Ollama Server · llama3.2
PLACE_AGENT_PROVIDER=ollama

# openai → OpenAI Cloud API · gpt-4.1-mini
BUDGET_AGENT_PROVIDER=openai

# gemma → Local Ollama Server · gemma3:4b
ITINERARY_AGENT_PROVIDER=gemma
```

이 설정은 하나의 Ollama Server에서 Llama와 Gemma를 동시에 실행한다는 뜻이 아닙니다. 요청할
때 지정한 Model이 필요에 따라 메모리에 적재됩니다. PC 메모리가 부족하면 Local Model을
연속으로 실행하고 `docker stats aidevs-ollama --no-stream`으로 사용량을 확인합니다.

### 6. 공용 Ollama Container 확인

`01~09` 과정 예제는 기본적으로 이미 준비한 공용 `aidevs-ollama` Container의 Host Port
`11434`를 사용합니다.

```powershell
docker ps -a --filter "name=^/aidevs-ollama$"
docker start aidevs-ollama
docker ps --filter "name=^/aidevs-ollama$"
Invoke-RestMethod http://127.0.0.1:11434/api/tags
docker exec aidevs-ollama ollama list
```

목록에 `llama3.2:latest`와 `gemma3:4b`가 없을 때만 Model을 내려받습니다.

```powershell
docker exec -it aidevs-ollama ollama pull llama3.2
docker exec -it aidevs-ollama ollama pull gemma3:4b
docker exec aidevs-ollama ollama list
```

Model 파일은 `aidevs-ollama-data` Named Volume에 저장되므로 Container를 중지해도 유지됩니다.
최초 다운로드는 파일 크기와 Network 속도에 따라 오래 걸릴 수 있습니다.

Ollama가 실제로 답하는지 Gemma 3 4B로 확인합니다.

```powershell
$body = @{
    model = "gemma3:4b"
    messages = @(
        @{ role = "user"; content = "AI Agent를 한 문장으로 설명해 주세요." }
    )
    stream = $false
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:11434/api/chat `
    -ContentType "application/json" `
    -Body $body
```

### 7. PostgreSQL/pgvector와 Redis 확인

뒤 단원의 RAG, 실행 상태, Trace, 실행 이력은 공용 PostgreSQL/pgvector와 Redis를 사용합니다.

```powershell
docker ps -a --filter "name=^/aidevs-pgvector$"
docker ps -a --filter "name=^/aidevs-redis$"
docker start aidevs-pgvector aidevs-redis
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
docker exec aidevs-redis redis-cli PING
```

정상 결과는 PostgreSQL의 `accepting connections`와 Redis의 `PONG`입니다. pgvector Extension도
확인합니다.

```powershell
docker exec -it aidevs-pgvector psql -U agent_user -d agent_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
docker exec -it aidevs-pgvector psql -U agent_user -d agent_db -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

과정 루트 `.env`의 연결 주소는 **Container를 최초 생성할 때 사용한 실제 비밀번호**와 같아야
합니다.

```dotenv
DATABASE_URL=postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db
REDIS_URL=redis://127.0.0.1:6379/0
```

기존 PostgreSQL Volume을 다른 비밀번호로 생성했다면 `DATABASE_URL`도 최초 생성에 사용한
비밀번호와 같아야 합니다. Docker 환경 변수만 바꿔도 기존 Volume의 Database 비밀번호는
자동 변경되지 않습니다.

### 8. MCP·Backend 기본 주소와 실행 제한

```dotenv
MCP_HOST=127.0.0.1
MCP_PORT=8010
MCP_URL=http://127.0.0.1:8010/mcp
API_BASE_URL=http://127.0.0.1:8000
MULTI_AGENT_API_URL=http://127.0.0.1:8000

MAX_ORCHESTRATION_STEPS=8
TASK_TTL_SECONDS=3600
```

- MCP Server는 과정 공통 Host Port `8010`을 사용합니다.
- FastAPI Backend는 `8000`, Streamlit Frontend는 일반적으로 `8501`을 사용합니다.
- 미니 프로젝트가 같은 Port를 사용하므로 여러 프로젝트를 동시에 실행하지 않습니다.
- 최대 단계는 AI Agent의 무제한 실행을 막는 코드 수준의 안전장치입니다.
- Task TTL은 Redis의 임시 실행 상태가 자동 정리되는 시간을 초 단위로 나타냅니다.

### 9. 공용 서비스 전체 확인

```powershell
docker ps --filter "name=aidevs-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
docker exec aidevs-redis redis-cli PING
docker exec aidevs-ollama ollama list
```

예상 Host Port는 다음과 같습니다.

| 서비스 | Host 주소 |
| --- | --- |
| PostgreSQL/pgvector | `127.0.0.1:5433` |
| Redis | `127.0.0.1:6379` |
| Ollama | `127.0.0.1:11434` |
| Backend | `127.0.0.1:8000` |
| MCP | `127.0.0.1:8010` |
| Frontend | `127.0.0.1:8501` |

`00_runtime-and-deployment/00_local-services/docker-compose.yml`은 별도의 독립 실습 환경을 만들기
위한 Compose입니다. 이미 `aidevs-pgvector`, `aidevs-redis`, `aidevs-ollama`가 같은 Host Port로
실행 중이면 두 환경을 동시에 올릴 수 없습니다. 과정 예제를 실행할 때는 어느 환경을 사용할지
하나로 정하고 Container 이름, Port, 비밀번호, Volume을 섞지 않습니다.

### 10. 수업 시작·종료

다음 수업에서 기존 공용 Container를 시작합니다.

```powershell
docker start aidevs-pgvector aidevs-redis aidevs-ollama
cd C:\aidevs\07_multi-agent-service-ops
.\.venv\Scripts\Activate.ps1
```

수업을 마치면 Container만 중지합니다.

```powershell
docker stop aidevs-pgvector aidevs-redis aidevs-ollama
```

단순 종료할 때 `docker rm`, `docker volume rm`, `docker compose down -v`를 사용하지 않습니다.
이 명령들은 Database, Redis 데이터, Ollama Model을 삭제할 수 있습니다.

### 전체 환경 완료 체크

```text
[ ] 과정 루트의 .venv를 만들고 requirements와 과정 Package를 설치했다.
[ ] .env.example을 .env로 복사하고 Git에서 제외되는지 확인했다.
[ ] OpenAI·Gemini API Key와 Model 이름을 확인했다.
[ ] aidevs-ollama에서 llama3.2와 gemma3:4b를 확인했다.
[ ] PostgreSQL이 accepting connections를 반환했다.
[ ] pgvector Extension을 확인했다.
[ ] Redis가 PONG을 반환했다.
[ ] MCP 8010, Backend 8000, Frontend 8501의 역할을 구분할 수 있다.
[ ] 공용 aidevs-* 환경과 독립 Compose 환경을 동시에 실행하지 않는다.
```
## 문제 해결 순서

```text
1. Python 가상환경이 활성화되었는가?
2. 과정 루트의 .env를 읽고 있는가?
3. 선택한 Cloud Provider API Key가 있는가?
4. PostgreSQL·Redis·Ollama Container가 실행 중인가?
5. llama3.2와 gemma3:4b가 설치되었는가?
6. 과정 Port가 다른 Process와 충돌하지 않는가?
7. 오류가 Provider·MCP·Database 중 어느 계층에서 발생했는가?
```

실패를 Mock 성공으로 바꾸지 않습니다. 오류 메시지와 Container Log를 확인하여 실패한
계층부터 복구합니다.
