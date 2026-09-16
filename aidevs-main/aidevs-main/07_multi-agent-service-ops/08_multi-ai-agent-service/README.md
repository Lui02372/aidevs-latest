# 08 Observable Multi-Agent Service

앞 과정에서 만든 Multi-Agent 협업, Guardrail, 평가와 Retry를 실제 서비스 형태로 실행하고 내부 상태를 관찰합니다. 핵심 질문은 다음과 같습니다.

> 사용자 요청 하나가 어느 Agent와 Provider를 거쳤고, 지금 어디까지 실행됐으며, 왜 실패했는가?

## 전체 학습 흐름

```text
01 Structured Logging
→ 02 Trace Context
→ 03 Agent·Provider Status
→ 04 Liveness·Readiness
→ 05 Redis Live State
→ 06 PostgreSQL History
→ 07 Operations Dashboard
```

## 관측 정보의 차이

| 개념 | 답하는 질문 | 예시 |
| --- | --- | --- |
| Log | 어떤 사건이 발생했는가? | `weather_completed` |
| Trace | 한 요청이 어떤 경로를 지났는가? | Backend → Worker → Agent |
| State | 지금 어디까지 실행됐는가? | `running`, 60% |
| Health | 요청을 처리할 준비가 됐는가? | Redis·PostgreSQL 연결 |
| History | 과거 실행에서 무슨 일이 있었는가? | 실패 Task와 전체 Event |
| Metric | 전체적으로 얼마나 자주 발생하는가? | 상태별 Task 수, Agent 실패 수 |

## Lab 구성

| Lab | 파일 | 실제 연결 |
| ---: | --- | --- |
| 01 | `01_structured_logging.py` | Console JSON Log |
| 02 | `02_trace_context.py` | 없음 |
| 03 | `03_agent_provider_status.py` | 환경 변수·Ollama |
| 04 | `04_health_check.py` | Redis·PostgreSQL |
| 05 | `05_live_execution_state.py` | Redis |
| 06 | `06_execution_history.py` | PostgreSQL |
| 07 | `07_operations_dashboard.py` | Redis·PostgreSQL |

모든 Lab 상단에는 등장 주체, 실행 단계, 기대 결과와 학습 포인트를 상세하게 작성했습니다. `assert`, `lambda`, 고정된 Mock 성공 결과를 사용하지 않습니다.

## 실제 서비스 구조

```text
Streamlit :8508
→ FastAPI :8000
   ├─ POST /api/tasks → Redis Queue
   ├─ GET Live State → Redis
   ├─ GET History·Summary → PostgreSQL
   └─ GET Health → Redis·PostgreSQL

Worker
→ Redis Queue에서 Task 수신
→ 실제 Supervisor·Worker LLM 실행
→ Redis 현재 상태 갱신
→ PostgreSQL Task·Trace 영구 저장
```

Backend는 오래 걸리는 LLM을 직접 실행하지 않습니다. `202 Accepted`는 완료가 아니라 Queue에 접수되었다는 뜻입니다.

## Redis와 PostgreSQL의 책임

| Redis | PostgreSQL |
| --- | --- |
| Queue | 완료·실패 Task 이력 |
| 현재 상태와 Progress | 시간순 Trace Event |
| 현재 Agent | 운영 집계의 원본 |
| 멱등성 Key | TTL 이후에도 필요한 감사 이력 |

Redis Key는 `mini08:` Prefix를 사용하고 PostgreSQL은 `mini_multi_agent_08` Schema를 사용합니다.

## 환경 준비

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

공통 `.env`의 주요 설정은 다음과 같습니다.

```dotenv
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
REDIS_URL=redis://127.0.0.1:6379/0
DATABASE_URL=postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db
```

Schema를 최초 한 번 준비합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\08_multi-ai-agent-service
python .\init_database.py
python .\check_environment.py
```

## Lab 실행

과정 루트에서 실행합니다.

```powershell
python .\08_multi-ai-agent-service\01_structured_logging.py
python .\08_multi-ai-agent-service\02_trace_context.py
python .\08_multi-ai-agent-service\03_agent_provider_status.py
python .\08_multi-ai-agent-service\04_health_check.py
python .\08_multi-ai-agent-service\05_live_execution_state.py
python .\08_multi-ai-agent-service\06_execution_history.py
python .\08_multi-ai-agent-service\07_operations_dashboard.py
```

01~02는 외부 연결 없이 실행됩니다. 03은 실제 Provider 설정을, 04~07은 실제 Redis와 PostgreSQL을 확인합니다.

## 세 Process 실행

각각 별도 터미널에서 실행합니다.

터미널 1 · Backend:

```powershell
cd C:\aidevs\07_multi-agent-service-ops
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
uvicorn backend:app --app-dir .\08_multi-ai-agent-service --reload --port 8000
```

터미널 2 · Worker:

```powershell
cd C:\aidevs\07_multi-agent-service-ops
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\08_multi-ai-agent-service\worker.py
```

터미널 3 · Frontend:

```powershell
cd C:\aidevs\07_multi-agent-service-ops
$env:MULTI_AGENT_API_URL='http://127.0.0.1:8000'
streamlit run .\08_multi-ai-agent-service\frontend.py --server.port 8508
```

- 화면: `http://127.0.0.1:8508`
- API 문서: `http://127.0.0.1:8000/docs`

## 주요 API

| Method | Path | 역할 |
| --- | --- | --- |
| GET | `/health` | 전체 의존성 상태 |
| GET | `/health/live` | Backend Process 생존 여부 |
| GET | `/health/ready` | Redis·PostgreSQL 준비 여부 |
| POST | `/api/tasks` | Task Queue 접수 |
| GET | `/api/tasks/{task_id}` | Redis 현재 상태 |
| GET | `/api/tasks/{task_id}/history` | PostgreSQL 영구 Trace |
| POST | `/api/tasks/{task_id}/decision` | 승인 또는 거절 |
| GET | `/api/operations/live` | 현재 Redis Task |
| GET | `/api/operations/history` | 최근 PostgreSQL Task |
| GET | `/api/operations/summary` | 상태·Agent별 운영 집계 |

## 화면 메뉴

```text
과정 안내
Task 실행
Live Executions
Execution History
Operations Dashboard
Health Check
```

Task 실행 화면은 Redis를 1초마다 폴링합니다. 승인 대기, 완료, 거절 또는 실패에 도달하면 폴링을 종료합니다.

## 수업 중 확인할 질문

1. 일반 Log와 Trace는 어떻게 다른가요?
2. Agent마다 새 trace_id를 만들면 어떤 문제가 생기나요?
3. Liveness는 성공하지만 Readiness는 실패할 수 있는 상황은 무엇인가요?
4. 현재 실행 상태는 왜 PostgreSQL보다 Redis에 적합한가요?
5. 완료 후 실행 이력은 왜 PostgreSQL에 보존해야 하나요?
6. Dashboard가 원본 Log 전체를 그대로 보여 주면 어떤 문제가 있나요?

## 완료 기준

- 구조화 Log의 필드를 설명할 수 있습니다.
- 하나의 trace_id로 Multi-Agent 실행 경로를 추적할 수 있습니다.
- Liveness와 Readiness를 구분할 수 있습니다.
- Redis State와 PostgreSQL History의 책임을 설명할 수 있습니다.
- 현재 Task, 과거 Trace, 상태별 집계와 Agent 실패 수를 화면에서 확인할 수 있습니다.
- Provider·Redis·PostgreSQL 실패가 성공으로 숨겨지지 않는 것을 확인할 수 있습니다.
