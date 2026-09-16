# Docker Compose 학습 가이드 (00 ~ 09)

이 문서는 07_multi-agent-service-ops 안에서 각 폴더가 어떤 역할을 하고, 어떤 Compose 파일을 언제 쓰는지 한 번에 이해할 수 있도록 정리한 가이드입니다.

핵심만 먼저 말하면, 이 과정에서 Docker Compose는 단순히 "도커 실행 파일"이 아니라 여러 프로세스가 함께 동작하는 서비스 묶음을 정의하는 문서입니다.

- Frontend는 웹 화면
- Backend는 API 서버
- Redis는 상태와 큐 저장
- PostgreSQL은 영구 기록 저장
- Ollama는 로컬 LLM 서버
- MCP는 외부 Tool 서버

이런 요소를 연결해서 함께 실행할 수 있게 만드는 것이 Compose입니다.

---

## 1. Compose를 이해하는 가장 중요한 5개 개념

### 1) service
Compose 안에서 실제로 실행되는 각 프로그램 단위입니다.

예:
- backend
- frontend
- redis
- database
- weather-mcp
- ollama

각 서비스는 각각의 컨테이너로 실행됩니다.

### 2) ports
호스트와 컨테이너의 연결 관계를 정의합니다.

예:
- "8000:8000" = Host의 8000 포트가 Container의 8000 포트로 연결됨

브라우저는 Host의 포트로 접근하고, 컨테이너 내부에서는 보통 자기 자신이 8000번 포트를 사용한다고 생각하면 됩니다.

### 3) depends_on
어떤 서비스가 먼저 시작해야 하는지 지정합니다.

예:
- backend는 database와 redis가 준비된 뒤 시작
- frontend는 backend가 healthy 상태일 때 시작

의존성이 있는 서비스일수록 반드시 순서가 중요합니다.

### 4) healthcheck
서비스가 정상 상태인지 확인하는 조건입니다.

예:
- Redis: `redis-cli ping`
- PostgreSQL: `pg_isready`
- Backend: `http://127.0.0.1:8000/health/ready`

단순히 프로세스가 살아 있는 것과 "실제 요청을 받을 준비가 되었는지"는 다릅니다. healthcheck는 그 차이를 보여 줍니다.

### 5) environment / env_file
컨테이너 안에서 쓸 환경 변수를 넣는 방식입니다.

예:
- OPENAI_API_KEY
- REDIS_URL
- DATABASE_URL
- OLLAMA_BASE_URL

대부분의 실습은 `.env` 파일을 만들고 Compose에서 참조하는 구조입니다.

---

## 2. 가장 많이 헷갈리는 개념

### A. Host 포트와 Container 포트는 다릅니다

```yaml
ports:
  - "8501:8501"
```

이 의미는 다음과 같습니다.

- Host PC의 8501 포트
- Container 안의 8501 포트
- 브라우저는 Host 포트 8501로 접속
- Container 내부에서는 자기 자신 네트워크 안에서 다른 서비스 이름으로 연결

그래서 Container 안에서는 `127.0.0.1`이 자기 자신을 가리키고, 다른 서비스는 `backend`, `redis`, `database`, `weather-mcp` 같은 이름을 사용합니다.

### B. Docker Desktop에서 Host와 Container는 다른 주소 공간입니다

예를 들면:

- Host에서 PostgreSQL은 `127.0.0.1:5433`
- Container 안에서 PostgreSQL은 `host.docker.internal:5433` 또는 `database:5432`

이 차이를 모르고 `localhost`만 쓰면 연결이 실패하는 경우가 많습니다.

### C. 같은 포트를 쓰는 Compose는 동시에 실행하지 않는다

예:
- 8000, 8501, 5433, 6379

동일한 포트를 다른 Compose가 동시에 잡으면 충돌이 납니다.

그래서 보통은 하나의 실습 폴더 안에서 `docker compose up`을 하고, 다른 실습 폴더는 잠깐 멈추는 식으로 진행합니다.

---

## 3. 00 ~ 09 전체 흐름

이 과정은 대체로 이렇게 이해하면 편합니다.

```text
00: 환경 준비
  → Redis, PostgreSQL, Ollama를 시작

01: 앱 구조 연습
  → Frontend + Backend 연결

05: MCP 배포 연습
  → Tool 서버와 Backend 연결

06: 상태 기반 배포 연습
  → Redis + PostgreSQL 역할 분리

08: Observability 연습
  → 실행 상태, Trace, Redis/DB 분리

09: 운영/배포 연습
  → Health Check, Restart, Retry, Rollback
```

즉, 00~06은 점점 서비스 구조가 복잡해지고, 08~09는 운영 관점으로 들어갑니다.

---

## 4. 폴더별로 어떤 Compose를 쓰는지

### 00. 00_local-services

경로:
- 00_runtime-and-deployment/00_local-services/

핵심 파일:
- docker-compose.yml

역할:
- Redis, PostgreSQL, Ollama를 로컬에 준비하는 공용 환경
- 이후 다른 실습들이 이 환경을 재사용

대표 포트:
- Redis: 6379
- PostgreSQL: 5433
- Ollama: 11434

예시:

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\00_local-services
docker compose up -d redis postgres
docker compose ps
```

이 단계는 앱 자체를 띄우는 게 아니라, 다음 실습을 위해 기반 인프라를 준비하는 단계입니다.

---

### 01. 01_simple-multi-llm-compose

경로:
- 00_runtime-and-deployment/01_simple-multi-llm-compose/

핵심 파일:
- compose.yml
- compose.full-stack.yml
- compose.release.yml

역할:
- Frontend와 Backend를 함께 묶어서 실행하는 가장 기본 예제
- 기존 공용 Redis, PostgreSQL, Ollama를 재사용하는 구조

핵심 구조:

```text
Frontend → Backend
Backend → Redis / PostgreSQL / OpenAI / Gemini / Ollama
```

예시:

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose
docker compose up -d --build
docker compose ps
```

이 단계의 핵심은 "앱을 하나의 Compose로 묶는 법"을 배우는 것입니다.

### 01-2. 01_simple-multi-llm-compose2

역할:
- 01의 기본 구조를 더 배포 친화적으로 정리한 버전
- `env_file`과 이미지 태그 등의 설정을 다루는 연습

핵심 차이:
- 01은 실행 중심
- 01-2는 이미지/배포 설정을 더 많이 다룸

### 01-3. 01_simple-multi-llm-compose3

역할:
- 배포 환경과 로컬 환경을 나누는 실습
- 같은 앱을 다른 설정으로 재사용하는 방법을 확인

이 단계는 "실행용 Compose와 배포용 Compose를 구분하는 법"을 배우는 목적이 큽니다.

---

### 05. 05_weather-mcp-deployment-project

경로:
- 00_runtime-and-deployment/05_weather-mcp-deployment-project/

핵심 파일:
- compose.yml

역할:
- MCP(Server Tool) + Backend + Frontend 구조를 연결하는 실전 예제
- 실제 날씨 Tool 서버를 호출하는 형태

핵심 구조:

```text
Browser
→ Frontend
→ Backend
→ Weather MCP
→ Open-Meteo API
```

예시:

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project
docker compose up -d --build
docker compose ps
```

여기서 가장 중요한 포인트는 Container 안에서 `localhost`를 쓰면 자기 자신만 보고, 다른 서비스는 `weather-mcp`처럼 서비스 이름을 써야 한다는 것입니다.

---

### 06. 06_weather-mcp-stateful-deployment

경로:
- 00_runtime-and-deployment/06_weather-mcp-stateful-deployment/

핵심 파일:
- compose.infrastructure.yml
- compose.application.yml

역할:
- Redis와 PostgreSQL을 인프라로 분리해서 관리
- Application만 따로 올리는 구조

핵심 구분:

| 저장소 | 역할 |
| --- | --- |
| Redis | 진행 상태, cache, queue |
| PostgreSQL | 완료 이력과 로그 |

예시:

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment
docker compose -f .\compose.infrastructure.yml up -d
docker compose -f .\compose.application.yml up -d --build
```

이 단계는 가장 중요합니다. 왜냐하면 실제 운영에서 "데이터를 어디에 저장할지"를 엄격하게 나누는 감각을 배우기 때문입니다.

---

### 08. 08_multi-ai-agent-service

경로:
- 08_multi-ai-agent-service/

역할:
- Compose 파일보다 구조 자체를 이해하는 단계
- Backend, Worker, Redis, PostgreSQL의 역할을 분리해서 보는 실습

핵심 구조:

```text
Frontend
→ Backend API
→ Redis Queue
→ Worker
→ PostgreSQL History
```

이 단계는 실제 운영형 서비스 구조를 이해하는 단계입니다.

여기서는 Compose를 직접 띄우기보다는 여러 프로세스를 각각 실행하고 상태를 보며 이해합니다.

---

### 09. 09_integrated-deployment-and-operations

경로:
- 09_integrated-deployment-and-operations/

핵심 파일:
- deploy/compose.yaml

역할:
- 08이 만든 구조를 배포 가능한 형태로 묶고 운영 관점으로 확장
- Health Check, Retry, Restart, Rollback을 다룸

예시:

```powershell
cd C:\aidevs\07_multi-agent-service-ops\09_integrated-deployment-and-operations
docker compose -f .\deploy\compose.yaml up -d
```

핵심은 "앱이 살아 있는지"와 "요청을 받을 준비가 되었는지"를 구분하는 것입니다.

---

## 5. 각 단계에서 어떤 compose를 봐야 하는가?

### 초보자가 가장 먼저 보는 순서

1. 00_local-services/docker-compose.yml
2. 01_simple-multi-llm-compose/compose.yml
3. 05_weather-mcp-deployment-project/compose.yml
4. 06_weather-mcp-stateful-deployment/compose.infrastructure.yml
5. 06_weather-mcp-stateful-deployment/compose.application.yml
6. 09_integrated-deployment-and-operations/deploy/compose.yaml

이 순서로 보면 전체 구조가 가장 쉽게 연결됩니다.

---

## 6. 실무적으로 자주 쓰는 docker compose 명령

### 설정 검증

```powershell
docker compose config --quiet
```

- YAML 문법과 환경 변수 치환이 맞는지 확인
- 실제 실행 전에 가장 많이 쓰는 명령

### 구성 실행

```powershell
docker compose up -d --build
```

- 이미지를 빌드하고 백그라운드에서 서비스 실행
- 코드 수정 후 재실행할 때 자주 사용

### 상태 확인

```powershell
docker compose ps
```

- 각 서비스가 running / exited / restarting인지 확인

### 로그 확인

```powershell
docker compose logs --tail=100 backend
docker compose logs --tail=100 frontend
```

- 어떤 서비스가 실패했는지 확인

### 컨테이너 내부 확인

```powershell
docker compose exec redis redis-cli ping
docker compose exec database psql -U agent_user -d agent_db
```

- Redis와 PostgreSQL이 정상인지 직접 확인

### 종료

```powershell
docker compose down
docker compose down -v
```

- down: 컨테이너와 네트워크 정리, volume 유지
- down -v: volume까지 삭제, 데이터 초기화

> `down -v`는 실습 데이터를 날리는 명령이어서 주의해서 사용해야 합니다.

---

## 7. 가장 중요한 결론

이 과정에서 Docker Compose는 단지 실행 명령이 아니라, 다음을 보여주는 구조 문서입니다.

- 어떤 프로세스가 어떤 역할을 하는가
- 어떤 서비스가 먼저 실행되어야 하는가
- 어떤 데이터는 Redis에 두고 어떤 데이터는 PostgreSQL에 두는가
- 어떤 포트를 Host에 공개하고 어떤 포트는 내부 전용으로 숨기는가
- Liveness와 Readiness가 어떻게 다른지
- 어떤 설정은 `.env`로 분리하는가

즉, Compose를 읽는 핵심은 "서비스 간 연결 구조를 이해하는 것"입니다.

파일을 외우기보다, 네트워크와 의존성, 저장소 역할, 실행 순서를 따라가면 훨씬 이해가 빠릅니다.

---

## 8. 가장 빠르게 체크하는 질문

아래 질문을 스스로 답할 수 있다면, 거의 다 이해한 것입니다.

1. `compose.yml`은 무엇을 묶는 파일인가?
2. `ports`는 무엇을 의미하는가?
3. `depends_on`은 왜 필요한가?
4. `healthcheck`는 어떤 상태를 확인하는가?
5. `127.0.0.1`과 `backend`, `redis`, `database`는 무엇이 다른가?
6. Redis와 PostgreSQL은 각각 어떤 역할을 하는가?
7. `docker compose up`과 `docker compose build`는 어떤 차이가 있는가?
8. `docker compose down`과 `down -v`는 각 어떤 상황에 쓰는가?

---

## 9. 추천 학습 순서

1. 00_local-services
2. 01_simple-multi-llm-compose
3. 05_weather-mcp-deployment-project
4. 06_weather-mcp-stateful-deployment
5. 09_integrated-deployment-and-operations

이 순서로 보면, 00에서 기반을 만들고, 01에서 앱 구조를 연결하고, 05에서 Tool 서버를 연결하고, 06에서 상태를 분리하며, 09에서 운영 구조까지 이어지는 흐름이 자연스럽게 보입니다.

---

이 문서를 보고도 아직 헷갈리면, 가장 좋은 다음 단계는 실제로 각 폴더의 `compose.yml`을 열어서 "서비스 이름, 포트, 의존성, healthcheck"를 한 줄씩 따라보는 것입니다. 그렇게 하면 Compose의 의미가 눈에 보이기 시작합니다.
