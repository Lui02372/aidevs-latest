# 07 Multi AI Agent Orchestration

> 이전 과정의 Single AI Agent를 여러 전문 AI Agent의 협업 구조로 확장하고, 최종적으로
> Docker·GitHub Actions·AWS를 이용해 배포하고 운영하는 초보자 과정입니다.

## 이전 과정에서 이번 과정으로

이전 `05_llm-agent-orchestration` 과정에서는 하나의 AI Agent가 LLM, Tool, MCP, RAG,
Memory, Human Approval을 이용해 업무를 처리하는 방법을 학습했습니다.

이번 과정에서는 하나의 AI Agent가 담당하던 책임을 여러 전문 AI Agent로 분리하고, 이들의
선택·순서·결과 전달·검증·실패·재시도·전체 종료를 통제하는 **Multi AI Agent
Orchestration**을 학습합니다.

```text
이전 과정                              이번 과정

사용자                                 사용자
  ↓                                      ↓
Single AI Agent                        Orchestrator
  ├─ LLM                                 ├─ Weather Agent
  ├─ Tool                                ├─ Place Agent
  ├─ MCP                                 ├─ Budget Agent
  ├─ RAG                                 ├─ Validation Agent
  └─ Memory                              └─ Join → 최종 결과
```

Multi-Agent는 Single Agent보다 무조건 좋은 구조가 아닙니다. 독립 Goal, 전문 지식, Context
격리, Tool 권한, 평가 기준, 병렬 실행, Handoff 같은 분리 근거가 있을 때만 여러 Agent를
선택합니다.

## 과정의 핵심 질문

1. 어떤 책임을 별도의 AI Agent로 분리해야 하는가?
2. Agent별 Goal·Context·Tool 권한·입출력 계약은 무엇인가?
3. 요청과 중간 상태에 따라 어떤 Agent를 선택할 것인가?
4. 독립 작업을 언제 병렬 실행하고 결과를 누가 Join할 것인가?
5. 업무 책임을 다른 Agent에게 어떻게 Handoff할 것인가?
6. 결과를 누가 평가하고 몇 번까지 수정·재시도할 것인가?
7. Prompt Injection과 위험 Tool 실행을 어떻게 제한할 것인가?
8. 상태·Log·Trace·실행 이력을 어떻게 관찰할 것인가?
9. 검증된 서비스를 Docker와 GitHub Actions로 AWS에 어떻게 배포할 것인가?
10. 장애를 감지하고 Retry·Fallback·Restart로 어떻게 복구할 것인가?

## Anthropic 자료로 배우는 기본 Pattern

이 과정은 Anthropic 공식 글
[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)에서
소개하는 단순하고 조합 가능한 Workflow Pattern을 학습 출발점으로 사용합니다.

| Anthropic 공식 명칭 | 이번 과정의 표현 | 핵심 구조 | 실사용 예 |
| --- | --- | --- | --- |
| Prompt chaining | Sequential | A → B → C | 조사 → 작성 → 검토 |
| Routing | Router | Router → Worker 하나 | 배송·환불·기술지원 분류 |
| Parallelization | Parallel + Join | A·B·C → Join | 날씨·장소·예산 → 여행 일정 |
| Orchestrator-workers | Supervisor–Worker | Supervisor ↔ Workers | 중간 결과에 따라 다음 역할 선택 |
| Evaluator-optimizer | Evaluator–Reviser | 생성 → 평가 → 수정 | 정책 기준을 통과할 때까지 제한적으로 개선 |

Anthropic은 미리 정의된 코드 경로로 LLM과 Tool을 조정하는 시스템을 Workflow로, LLM이
실행 과정과 Tool 사용을 동적으로 결정하는 시스템을 Agent로 구분합니다. 또한 단순한
구조에서 시작하고 필요한 경우에만 복잡성을 추가할 것을 권장합니다.

본 과정은 위 기본 Pattern에 실제 Multi-Agent Service에 필요한 다음 내용을 추가합니다.

- Independent Agents와 Orchestration의 차이
- 역할·입출력·권한을 명시하는 Agent Contract
- 책임과 최소 Context를 이전하는 Handoff
- Primary Provider 오류를 기록하는 Failover
- Guardrail·Tool 권한·Role 기반 접근 통제
- Evaluation·Feedback·Retry·Trace
- Redis Queue·Worker·Progress·PostgreSQL 실행 이력
- Health Check·Monitoring·Auto Healing

Pattern 이름부터 선택하지 않습니다. 업무 의존성, 책임, Context, 권한, 실패와 종료 조건을
먼저 그린 뒤 가장 단순한 Pattern을 선택합니다.

## 공통 여행 서비스

```text
Travel Supervisor
├─ Weather Agent
├─ Place Agent
├─ Budget Agent
├─ Itinerary Agent
└─ Validation Agent
```

공통 요청은 부산 2박 3일 여행 계획입니다. 실제 LLM과 실제 날씨·저장소·HTTP MCP 연결을 사용하지만 실제 예약과 결제는 수행하지 않습니다.

## 로컬 실습에서 AWS 운영으로

이전 과정에서는 PostgreSQL/pgvector, Redis, Ollama를 Docker Container로 설치하여 로컬
AI Agent 환경을 구성했습니다.

이번 과정의 최종 목표는 로컬 Python 예제를 실행하는 데서 끝나지 않습니다. Frontend,
Backend API, MCP Server, Redis Queue, Worker, Multi-Agent Orchestrator와 상태 저장소를
서비스로 구성하고 AWS에 배포하여 상태와 장애를 관찰합니다.

```text
로컬 개발
→ Python Test
→ Docker Image Build
→ GitHub Actions CI
→ Pull Request
→ main 병합
→ 배포 승인
→ AWS 배포
→ Health Check
→ Log·Metric·Trace
→ 장애 복구
→ 다음 개선
```

## DevOps와 CI/CD를 배우는 이유

DevOps는 **Development(개발)**와 **Operations(운영)**를 합친 말입니다.

- Development: 기능 설계, 코드 작성, Test, 변경 관리
- Operations: 배포, 실행 환경, Server·Network·Database 관리, Monitoring, 장애 대응

과거에는 개발팀이 코드를 만든 뒤 운영팀에 전달하고, 운영팀이 별도의 절차로 배포하는 경우가
많았습니다. 이 과정에서 환경 차이, 수동 작업, 책임 경계 때문에 배포가 느려지거나 문제가
발생하기 쉬웠습니다. DevOps는 개발과 운영을 하나의 연속된 생명주기로 보고, 두 역할이 같은
목표와 정보를 공유하면서 반복 작업을 자동화하는 문화·업무 방식·기술 실천입니다.

```text
계획 → 개발 → Test → Build → 배포 → 실행 → Monitoring → 개선
  ↑_______________________________________________________|
```

DevOps는 특정 제품 하나를 의미하지 않습니다. Docker나 GitHub Actions를 사용한다고 자동으로
DevOps가 완성되는 것도 아닙니다. 작은 변경을 자동 검증하고, 동일한 방식으로 배포하며,
운영 결과를 다시 개발에 반영하는 전체 협업 방식이 핵심입니다.

### 핵심 목표

- 코드 변경을 빠르고 반복 가능하게 검증합니다.
- 작은 단위로 자주 배포하여 한 번의 변경 위험을 줄입니다.
- 개발 PC와 운영 Server의 실행 환경 차이를 줄입니다.
- 배포 성공 여부를 Health Check로 판단합니다.
- Log·Metric·Trace로 장애 원인을 빠르게 찾습니다.
- Retry·Fallback·Restart로 일시 장애에 대응합니다.
- 변경자, 배포 버전, 실행 결과를 추적할 수 있게 합니다.
- 개발과 운영 사이의 단절을 줄이고 책임과 정보를 공유합니다.

### 개발자가 코드를 Push하면 일어나는 일

이 과정에서 다루는 기본 자동화 흐름은 다음과 같습니다.

```text
개발자가 개인 Branch에 Push
→ GitHub Actions CI 실행
→ Python Test
→ Compose 설정 검사
→ Docker Image Build
→ Pull Request 검토
→ main Branch 병합
→ CI 다시 실행
→ 운영 배포 승인
→ AWS에 Application 배포
→ Health Check
→ Log·상태·실행 이력 Monitoring
→ 장애 발견 시 복구 또는 다음 코드 개선
```

CI가 실패하면 배포하지 않습니다. Container가 시작되었더라도 Readiness가 실패하면 정상
서비스로 판단하지 않습니다. 배포 후의 Log와 Trace도 개발자가 다음 변경을 판단하는 근거로
사용합니다.

### 자주 연결되는 기술

| 영역 | 대표 기술·개념 | 이 과정에서의 역할 |
| --- | --- | --- |
| CI/CD | GitHub Actions | Test·Build·승인·AWS 배포 자동화 |
| Container | Docker, Docker Compose | 같은 실행 환경 구성과 서비스 연결 |
| Cloud | AWS EC2 | Container Application 실행 환경 |
| Monitoring | Health Check, Log, Metric, Trace | 서비스 상태와 Agent 실행 흐름 확인 |
| 자동 복구 | Restart, Retry, Fallback | Process·외부 API의 일시 장애 대응 |
| 상태 저장 | PostgreSQL, Redis | 영구 이력과 임시 진행 상태 분리 |
| IaC | Terraform 등 | Infrastructure 설정을 코드로 관리 |
| Orchestration | Kubernetes 등 | 다수 Container의 배치·확장·복구 관리 |
| Automation | Script, Workflow | 사람이 반복하던 절차를 일관되게 실행 |

이 입문 과정에서는 Docker Compose, GitHub Actions, AWS EC2, Health Check, Log·Trace,
Retry·Fallback을 직접 다룹니다. Kubernetes와 Terraform은 DevOps에서 자주 사용되지만 이
과정의 필수 구현 범위에는 포함하지 않습니다.

### Multi-Agent 서비스에서 DevOps가 더 중요한 이유

일반 Web Service보다 Multi-Agent Service는 LLM, MCP Tool, Redis, PostgreSQL, 외부 API 등
의존 대상이 많습니다. 같은 사용자 요청도 Provider 응답, Tool 상태, Retry 여부에 따라 실행
시간과 결과가 달라질 수 있습니다.

| 운영 질문 | 필요한 방법 |
| --- | --- |
| 어떤 Agent에서 실패했는가? | Agent별 Log와 Trace ID |
| 어떤 Tool을 호출했는가? | MCP 호출 기록과 권한 기록 |
| 왜 재시도했는가? | Retry 횟수와 실패 원인 |
| 어떤 Model이 답했는가? | Provider·Model·Prompt Version 기록 |
| 배포 후 품질이 나빠졌는가? | Evaluation 결과와 배포 Version 비교 |
| Backend는 살아 있지만 준비됐는가? | Liveness와 Readiness 분리 |
| Application 재배포 후 이력이 남는가? | 상태 인프라와 Application 수명 분리 |

따라서 Multi-Agent DevOps는 단순히 Container를 실행하는 것을 넘어 Agent 실행 과정의
관측 가능성, 품질 평가, 권한, 비용, 실패 복구까지 함께 관리해야 합니다.

### DevOps와 SRE의 차이

DevOps가 개발과 운영을 연결하는 넓은 문화와 실천이라면, SRE(Site Reliability
Engineering)는 신뢰성을 공학적으로 관리하는 운영 접근법입니다. SRE에서는 SLI·SLO,
Error Budget, 장애 대응, 자동화 등을 사용해 “얼마나 안정적이어야 하는가”를 측정합니다.

```text
DevOps: 개발과 운영이 빠르고 안전하게 함께 일하는 전체 방식
SRE: 그중 서비스 신뢰성을 측정하고 유지하는 구체적인 공학 실천
```

이 과정의 Health Check, Monitoring, Auto Healing, Retry, 실행 이력은 DevOps 실습이면서
SRE의 기초 개념으로도 이어집니다.

### 한 줄 요약

> DevOps는 개발한 코드를 자동으로 검증·배포하고 운영 결과를 다시 개발에 연결하여, 서비스를
> 빠르고 안전하게 개선하는 협업 방식입니다.

## 전체 환경 준비

이 과정은 Python 가상환경, OpenAI·Gemini, Ollama의 Llama·Gemma, PostgreSQL/pgvector,
Redis, MCP 공통 환경을 사용합니다.

최초 설치부터 `.env`, 모델 다운로드, Port, 서비스 검증까지의 상세 절차는
[SETUP.md](./SETUP.md)를 위에서 아래로 진행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
.\.venv\Scripts\Activate.ps1
docker start aidevs-pgvector aidevs-redis aidevs-ollama
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
docker exec aidevs-redis redis-cli PING
docker exec aidevs-ollama ollama list
```

## 01~09 학습 흐름

| 단계 | 폴더 | 핵심 내용 |
| ---: | --- | --- |
| 00 | `00_runtime-and-deployment` | Multi-LLM 작은 Chat, Docker Compose, GitHub Actions, AWS |
| 01 | `01_single-vs-multi-agent` | 하나의 Agent를 여러 Agent로 나누는 기준 |
| 02 | `02_agent-role-and-contract` | Agent 역할과 Pydantic 입출력 계약 |
| 03 | `03_supervisor-and-routing` | OpenAI·Gemini·Ollama Supervisor Routing |
| 04 | `04_orchestration` | Multi AI Agent 순차·병렬·Join·State·종료, 선택 LangGraph |
| 05 | `05_handoff-and-context` | 구조화 Handoff와 최소 Context |
| 06 | `06_multi-agent-safety` | AI Security와 Guardrails: 입력·응답 Policy, Tool 권한, 승인, Context 격리 |
| 07 | `07_failure-evaluation-and-tracing` | Evaluation·Feedback·Retry·Tracing |
| 08 | `08_multi-ai-agent-service` | 관측 가능한 Multi-Agent Service: 상태·로그·대시보드·이력 |
| 09 | `09_integrated-deployment-and-operations` | Docker·AWS·CI/CD·Auto Healing 통합 배포와 운영 |

## 서비스 확장 흐름

처음에는 한 Process의 작은 예제로 배우고, 08에서 필요한 책임만 Server로 분리합니다.

```text
Frontend
→ Backend API Server
→ Redis Queue와 Worker
→ Multi AI Agent Server
→ HTTP MCP Servers
→ Redis 현재 상태·PostgreSQL Trace
```

Workflow는 Orchestration 내부의 결정적인 순서·검증·Join을 표현하는 보조 개념입니다. Workflow Server는 이를 별도 서비스로 분리할 이유가 있을 때만 사용합니다.

## 공통 실행 원칙

- 기본 실행은 OpenAI·Gemini·Ollama 중 설정한 실제 Provider를 사용합니다.
- 실제 Provider 실패를 Mock 성공으로 숨기지 않습니다.
- 자동 테스트에서만 Fake Client를 사용합니다.
- 실제 Redis·PostgreSQL·HTTP MCP 연결을 단계적으로 사용합니다.
- 날짜·금액·권한·반복 제한과 승인은 Python과 저장소가 보장합니다.
- `20_assignments`는 만들지 않습니다.
- `10_labs`는 여러 Process 통합에 꼭 필요할 때만 만듭니다.
- LangGraph는 Python Orchestrator와 비교하는 선택 예제입니다.

## 최종 도착점

```text
Browser
→ Frontend
→ Backend API
→ Redis Queue
→ Worker
→ Multi AI Agent Orchestrator
   ├─ Supervisor·Router
   ├─ Specialist Agents
   ├─ Evaluator·Guardrail
   └─ Handoff·Join
→ HTTP MCP Servers
→ Redis 현재 상태·PostgreSQL 실행 이력
→ Docker Compose·GitHub Actions·AWS
→ Monitoring·Auto Healing
```

## 완료 기준

- 이전 Single AI Agent 과정과 이번 Multi-Agent 과정의 차이를 설명할 수 있습니다.
- Anthropic의 기본 Workflow Pattern과 과정에서 추가한 운영 Pattern을 구분할 수 있습니다.
- Agent 역할·계약·Context·Tool 권한과 Pattern 선택 근거를 설명할 수 있습니다.
- `SETUP.md`를 따라 Python·Multi-LLM·Docker 공통 환경을 준비할 수 있습니다.
- 결과 평가·Guardrail·Retry·Failover·Trace를 적용할 수 있습니다.
- Queue·Worker·상태 저장소를 가진 서비스를 구성할 수 있습니다.
- CI와 CD를 구분하고 GitHub Actions 결과를 읽을 수 있습니다.
- AWS에 배포하고 Health·Log·Trace와 장애 복구 상태를 확인할 수 있습니다.
