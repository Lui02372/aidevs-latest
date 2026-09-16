# 01 Simple Multi-LLM Docker Compose

하나의 여행 준비 Chat으로 Frontend와 Backend Container 연결을 배웁니다. Multi-Agent와
Orchestration은 아직 넣지 않습니다. 현재 수업 PC에는 PostgreSQL·Redis·Ollama Container가
이미 있으므로 기본 실행에서는 Application Container 두 개만 생성합니다.

## 두 실행 방식을 구분하세요

| 파일 | 실행 대상 | 사용하는 경우 |
| --- | --- | --- |
| `compose.yml` | Frontend·Backend | 현재 수업 환경, 기본 권장 |
| `compose.full-stack.yml` | Frontend·Backend·Redis·PostgreSQL·선택 Ollama | 공용 Container가 없는 별도 PC |

두 Compose를 동시에 실행하지 않습니다. 같은 Host Port를 사용하므로 충돌할 수 있습니다.

## 1. 기본 실행: 기존 공용 Container 사용

```text
기존 공용 Container
├─ PostgreSQL :5433
├─ Redis      :6379
└─ Ollama     :11434

이번 Compose
├─ Backend    :8000
└─ Frontend   :8501
```

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose
Copy-Item .env.example .env
docker compose config --quiet
docker compose up --build -d
docker compose ps
```

Backend도 Container이므로 Host의 공용 서비스에는 `127.0.0.1`이 아니라
`host.docker.internal`로 접근합니다.

```ini
DATABASE_URL=postgresql://agent_user:agent_pwd@host.docker.internal:5433/agent_db
REDIS_URL=redis://host.docker.internal:6379/0
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

### 코드·환경 설정을 수정한 뒤 반영하기

`backend/`, `frontend/`, `compose.yml`, 또는 `.env`를 수정해도 이미 실행 중인
Container는 자동으로 바뀌지 않습니다. 예를 들어 `GEMMA_MODEL=gemma3:4b`로 바꾼 뒤에는
아래 명령으로 Backend와 Frontend Image를 다시 빌드하고 Container를 새로 만듭니다.

```powershell
docker compose up -d --build --force-recreate backend frontend
```

전체 실행 방식을 사용했다면 다음처럼 실행합니다.

```powershell
docker compose -f .\compose.full-stack.yml up -d --build --force-recreate backend frontend
```

공용 PostgreSQL은 이 폴더의 `database/init.sql`을 자동 실행하지 않으므로 최초 한 번
전용 Schema와 Table을 준비합니다.

```powershell
python -m pip install "psycopg[binary]>=3.2,<4" "python-dotenv>=1.0,<2"
python .\init_database.py
```

정상 출력:

```text
Database 초기화가 완료되었습니다.
- simple_multi_llm.chat_messages
- simple_multi_llm.notes
```

이미 Backend가 실행 중이었다면 Table 생성 후 다시 요청하면 됩니다. 다만 코드 또는
환경 설정도 수정했다면 바로 앞의 **코드·환경 설정을 수정한 뒤 반영하기** 명령을 실행합니다.

## 2. 전체 실행: 공용 Container가 없는 PC

이 방식은 자체 Network 안에 저장소를 생성합니다.

```powershell
docker compose -f .\compose.full-stack.yml config --quiet
docker compose -f .\compose.full-stack.yml up --build -d
docker compose -f .\compose.full-stack.yml ps
docker compose -f .\compose.full-stack.yml exec redis redis-cli ping
docker compose -f .\compose.full-stack.yml exec database pg_isready -U agent_user -d agent_db
```

Full Stack 내부에서는 Compose Service 이름을 사용합니다.

```text
Backend → redis:6379
Backend → database:5432
Backend → 선택 Ollama: ollama:11434
```

Full Stack 방식은 새 PostgreSQL Volume을 만들 때 `database/init.sql`을 자동 실행하므로
별도로 `init_database.py`를 실행하지 않습니다.

## 3. 실제 LLM 설정

`.env`에 OpenAI 또는 Gemini Key를 입력합니다.

```ini
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
```

기존 공용 Ollama를 사용할 때:

```ini
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma3:4b
```

화면에서는 Provider로 `ollama`를 선택한 뒤 Model을 다시 선택합니다.

```text
ollama + gemma → GEMMA_MODEL=gemma3:4b
ollama + llama → OLLAMA_MODEL=llama3.2
```

API 요청 계약은 다음과 같습니다.

```json
{
  "session_id": "travel-01",
  "message": "부산 여행 준비를 알려줘",
  "provider": "ollama",
  "ollama_model": "gemma"
}
```

`ollama_model`을 `llama`로 바꾸면 같은 Ollama Server에서 Llama를 호출합니다.

Full Stack이 Ollama까지 새로 만들 때만 Profile을 사용합니다.

```powershell
docker compose -f .\compose.full-stack.yml --profile ollama up --build -d
docker compose -f .\compose.full-stack.yml --profile ollama exec ollama ollama pull llama3.2
docker compose -f .\compose.full-stack.yml --profile ollama exec ollama ollama pull gemma3:4b
docker compose -f .\compose.full-stack.yml --profile ollama exec ollama ollama list
```

## 4. 실행 확인

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

| 확인 대상 | 주소 |
| --- | --- |
| Streamlit | `http://127.0.0.1:8501` |
| FastAPI 문서 | `http://127.0.0.1:8000/docs` |
| Liveness | `http://127.0.0.1:8000/health/live` |
| Readiness | `http://127.0.0.1:8000/health/ready` |

- Liveness: Backend Process가 살아 있는지 확인합니다.
- Readiness: PostgreSQL과 Redis를 포함해 요청을 받을 준비가 됐는지 확인합니다.
- 설정하지 않은 Provider 오류는 Mock 성공으로 바꾸지 않습니다.

### Gemini `client has been closed` 오류

Gemini Client를 임시 객체로 한 줄에서 생성하면 요청 전에 Client가 정리될 수 있습니다.
Backend는 Client를 지역 변수로 유지한 뒤 `generate_content()`를 호출하도록 구성했습니다.
이 수정은 Backend Image를 다시 Build해야 반영됩니다.

## 5. 저장소 역할

| 서비스 | 저장 내용 | 기본 실행에서 관리 위치 |
| --- | --- | --- |
| Redis | 최근 대화·Session·요청 횟수 | 기존 공용 Redis Container |
| PostgreSQL | 전체 Chat 이력·여행 메모 | 기존 공용 PostgreSQL Container |
| Ollama | Llama·Gemma Model | 기존 공용 Ollama Container |

Full Stack 방식에서는 이 폴더의 `redis_data`, `postgres_data`, `ollama_data` Volume을
사용합니다.

## 6. 만든 이미지를 다른 PC에 전달하기

수강생 또는 다른 개발자에게 전달할 때는 실제 `.env` 파일을 포함하지 않습니다. API Key가
들어갈 수 있으므로 `.env.example`만 전달하고, 받는 사람이 자신의 `.env`를 만들게 합니다.
Ollama Model도 Backend·Frontend Image와 별개이므로 실행 후 별도로 준비해야 합니다.

### Container Registry로 배포하기

이 절에서는 수신자 PC에 공용 PostgreSQL·Redis·Ollama Container와 Llama·Gemma Model이
이미 준비되어 있다고 가정합니다. 따라서 운영자는 수업 Application인 Backend·Frontend
Image만 올리고, 수신자는 두 Image만 내려받아 실행합니다.

#### 1. 운영자: Backend·Frontend Image 올리기

먼저 현재 수업 Compose로 Image를 만듭니다.

```powershell
docker compose build backend frontend
docker image ls
```

`<DOCKER_HUB_ID>`는 이메일 주소가 아니라 Docker Hub 사용자명 또는 조직명입니다.
예를 들어 사용자명이 `my-course`라면 `my-course/simple-multi-llm-backend:1.0.0` 형식을
사용합니다.

```powershell
docker login
docker tag simple-multi-llm-app-backend:latest <DOCKER_HUB_ID>/simple-multi-llm-backend:1.0.0
docker tag simple-multi-llm-app-frontend:latest <DOCKER_HUB_ID>/simple-multi-llm-frontend:1.0.0
docker push <DOCKER_HUB_ID>/simple-multi-llm-backend:1.0.0
docker push <DOCKER_HUB_ID>/simple-multi-llm-frontend:1.0.0
```

`simple-multi-llm-app-backend:latest` 등의 앞부분은 `docker image ls`에서 보이는 실제
Image 이름을 사용합니다. `push access denied`가 나오면 로그인한 Docker Hub 사용자명과
`<DOCKER_HUB_ID>`가 같은지 확인합니다.

#### 2. 수신자: 공용 서비스 확인하기

수신자는 먼저 PostgreSQL·Redis·Ollama가 실행 중인지 확인합니다. 이 서비스들은 이번
배포에서 새로 만들지 않습니다.

```powershell
docker ps
```

Host Port는 아래와 같아야 합니다.

| 서비스 | Host 주소 | 용도 |
| --- | --- | --- |
| PostgreSQL | `127.0.0.1:5433` | 대화·메모 저장 |
| Redis | `127.0.0.1:6379` | Session·Cache |
| Ollama | `127.0.0.1:11434` | Llama·Gemma 실행 |

#### 3. 수신자: 배포 Image를 받아 Application 실행하기

운영자가 전달한 `compose.release.yml`과 `.env.example`을 같은 폴더에 둡니다. `.env`를
만들고 Image 주소를 실제 Docker Hub 사용자명과 버전으로 바꿉니다.

```powershell
Copy-Item .env.example .env
```

```ini
BACKEND_IMAGE=<DOCKER_HUB_ID>/simple-multi-llm-backend:1.0.0
FRONTEND_IMAGE=<DOCKER_HUB_ID>/simple-multi-llm-frontend:1.0.0
```

그 다음 `pull`로 Image를 받고, `up`으로 Backend·Frontend Container를 실행합니다.

```powershell
docker compose -f .\compose.release.yml pull
docker compose -f .\compose.release.yml up -d
docker compose -f .\compose.release.yml ps
```

`compose.release.yml`에는 다음이 미리 설정되어 있습니다.

| Container | Compose 서비스 이름 | Host Port | 공용 서비스 연결 |
| --- | --- | --- | --- |
| Frontend | `frontend` | `8501` | `http://backend:8000` |
| Backend | `backend` | `8000` | PostgreSQL·Redis·Ollama를 `host.docker.internal`로 연결 |

실행 후 Browser에서 `http://127.0.0.1:8501`을 열고, API 상태는
`http://127.0.0.1:8000/health/ready`에서 확인합니다.

## 7. 종료

기본 Application만 종료:

```powershell
docker compose down
```

이 명령은 기존 공용 PostgreSQL·Redis·Ollama를 중단하지 않습니다.

Full Stack 종료:

```powershell
docker compose -f .\compose.full-stack.yml down
```

`down -v`는 PostgreSQL 데이터와 Ollama Model을 삭제합니다. 학습 데이터가 필요 없는지
확인하지 않았다면 실행하지 않습니다.

## 완료 체크

```text
[ ] 기본 Compose가 Frontend와 Backend만 생성하는 것을 확인했다.
[ ] host.docker.internal과 localhost의 차이를 설명할 수 있다.
[ ] Full Stack Compose를 언제 사용하는지 설명할 수 있다.
[ ] 공용 PostgreSQL·Redis·Ollama를 재사용하는 Registry 배포 흐름을 설명할 수 있다.
[ ] Liveness와 Readiness를 구분할 수 있다.
[ ] 실제 Provider 오류가 성공으로 표시되지 않음을 확인했다.
```
