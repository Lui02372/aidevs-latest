# 09 Integrated Deployment and Operations

`06`의 보안 정책, `07`의 평가·재시도·Trace, `08`의 Observable Service를 하나의
배포 가능한 AI 서비스로 묶는 최종 과정입니다. 새로운 Agent 기능을 늘리는 대신
**이미 만든 Multi-Agent Service를 안전하게 출시하고 복구하는 방법**을 배웁니다.

여행 Multi-Agent는 배포 대상 워크로드로 유지합니다. 실제 OpenAI·Gemini·Ollama Agent와
Open-Meteo MCP Tool을 사용하며 Provider 또는 Network 오류를 Mock 성공으로 바꾸지 않습니다.

## 학습 목표

- API, Worker, Frontend, MCP Server의 배포 경계를 설명합니다.
- 하나의 Image를 여러 실행 명령으로 재사용합니다.
- Liveness와 Readiness를 구분하고 Auto Healing 조건을 정합니다.
- Retry, Backoff, Fallback의 적용 범위를 구분합니다.
- GitHub Actions 검증 단계와 AWS 배포 단계를 연결합니다.
- Dashboard와 Trace를 이용해 장애를 탐지하고 Rollback합니다.

## 전체 흐름

```text
사용자 → Frontend → API → Redis Queue → Worker
                                    ├─ 실제 AI Agent
                                    ├─ HTTP MCP :8010
                                    └─ PostgreSQL 실행 이력

GitHub Actions → 검사 → Image Build → ECR → ECS 배포
                                           ├─ ALB Health Check
                                           ├─ CloudWatch Log/Alarm
                                           └─ Restart·Scale·Rollback
```

## 단계별 Lab

| 순서 | 파일 | 핵심 질문 |
| --- | --- | --- |
| 01 | `01_deployment_boundary.py` | 무엇을 Process와 Container로 나눌까? |
| 02 | `02_release_config.py` | 환경 변수와 비밀값을 어떻게 검증할까? |
| 03 | `03_health_and_restart.py` | 언제 트래픽을 끊고 언제 재시작할까? |
| 04 | `04_retry_and_fallback.py` | 어떤 오류만 재시도·Fallback할까? |
| 05 | `05_release_gate.py` | 무엇을 통과해야 배포할 수 있을까? |
| 06 | `06_deployment_strategy.py` | Canary를 승격·대기·Rollback하는 기준은? |
| 07 | `07_incident_drill.py` | 장애 신호를 보고 어떤 순서로 대응할까? |

각 Python 파일 상단에는 초보자가 먼저 읽을 수 있는 시나리오가 있습니다. Lab은 Cloud 비용
없이 개념을 확인하는 최소 예이고, `deploy/`에서 같은 개념을 실제 설정에 연결합니다.

## 환경 설정

```powershell
cd C:\aidevs\07_multi-agent-service-ops\09_integrated-deployment-and-operations
Copy-Item .env.example .env
```

`.env`에 실제 API Key를 입력합니다. 기본 주소는 앞 과정과 같습니다.

```ini
API_BASE_URL=http://127.0.0.1:8000
TRAVEL_MCP_URL=http://127.0.0.1:8010/mcp
REDIS_URL=redis://127.0.0.1:6379/0
DATABASE_URL=postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db
GEMINI_MODEL=gemini-3.5-flash
```

## 1. 작은 Lab 실행

```powershell
python .\01_deployment_boundary.py
python .\02_release_config.py
python .\03_health_and_restart.py
python .\04_retry_and_fallback.py
python .\05_release_gate.py
python .\06_deployment_strategy.py
python .\07_incident_drill.py
```

## 2. 기존 Redis·PostgreSQL을 이용한 Docker 실행

Docker Desktop에서 Redis `6379`, PostgreSQL `5433`이 이미 실행 중인 학습 환경에 맞춘
방법입니다. Application Container는 `host.docker.internal`로 두 저장소에 접속합니다.

```powershell
docker compose -f .\deploy\compose.yaml build
docker compose -f .\deploy\compose.yaml up -d
docker compose -f .\deploy\compose.yaml ps
docker compose -f .\deploy\compose.yaml logs -f worker
```

- API: `http://127.0.0.1:8000`
- API 문서: `http://127.0.0.1:8000/docs`
- MCP: `http://127.0.0.1:8010/mcp`
- Frontend: `http://127.0.0.1:8501`

종료할 때는 데이터를 지우지 않는 다음 명령을 사용합니다.

```powershell
docker compose -f .\deploy\compose.yaml down
```

`compose.full-stack.yaml`은 공용 저장소가 없는 별도 PC에서 Redis·PostgreSQL을 준비하는
참고 파일입니다. 현재 환경에서는 기존 Container와 Port가 충돌하므로 실행하지 않습니다.

## 3. Health와 Auto Healing 확인

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health/ready
docker compose -f .\deploy\compose.yaml ps
```

- Liveness 실패: Process 재시작 대상입니다.
- Readiness 실패: 살아 있어도 신규 트래픽을 보내지 않습니다.
- `restart: unless-stopped`: 재기동을 돕지만 잘못된 설정을 해결하지는 못합니다.

## 4. AWS로 옮기기

[`deploy/aws/README.md`](./deploy/aws/README.md)에서 ECR·ECS·RDS·ElastiCache·CloudWatch의
대응 관계를 확인합니다. 그 다음
[`ecs-task-definition.example.json`](./deploy/aws/ecs-task-definition.example.json)의 Placeholder를
본인 환경 값으로 교체합니다. API와 Worker는 같은 Image를 쓰지만 ECS Service는 분리합니다.

## 5. CI/CD 구성

[`ci-cd.example.yml`](./deploy/github/ci-cd.example.yml)을 Repository의
`.github/workflows/`로 복사하면 시작할 수 있습니다. 예제는 검증과 Image Build까지 자동화하고,
실제 ECR Push·ECS 변경은 AWS OIDC와 GitHub Environment 승인 정책을 설정한 뒤 추가합니다.

```text
구문·Test·보안·평가 → Image Build → Registry Push
→ 새 Task Definition → Canary → Readiness 확인 → 승격 또는 Rollback
```

## 6. 장애 대응 종합 실습

1. Frontend에서 실제 Task를 실행합니다.
2. `docker compose stop worker`로 Worker 중단 상황을 만듭니다.
3. Queue 적체와 현재 상태를 08 Dashboard에서 확인합니다.
4. Worker를 다시 시작하고 같은 Trace가 이어지는지 확인합니다.
5. [`RUNBOOK.md`](./RUNBOOK.md)에 따라 원인·조치·복구 기준을 기록합니다.

실제 운영에서는 장애를 만들기 전에 별도 개발 환경인지 확인해야 합니다.

## 과정 완료 기준

- Application Process와 Redis·PostgreSQL의 책임을 구분할 수 있습니다.
- API와 Worker를 독립적으로 배포·확장하는 이유를 설명할 수 있습니다.
- Liveness, Readiness, Restart를 같은 개념으로 혼동하지 않습니다.
- 실패 Task와 Trace가 재시작 후에도 사라지지 않는지 확인합니다.
- Release Gate와 Rollback 기준을 수치로 설명할 수 있습니다.
- 실제 비밀값을 Image, Git, Log에 넣지 않습니다.
