# 02 Agent Role, Task and Contract

이 단원은 01에서 분리한 여러 Agent에게 구체적인 역할과 Task를 부여하고, Agent 사이의
입출력을 검증 가능한 계약으로 만드는 방법을 학습합니다.

```text
사용자 요청
→ Role 정의
→ Task 분할
→ Agent 입력 계약
→ 역할별 출력 계약
→ 형식·업무 의미 검증
→ 검증 성공 결과만 다음 Agent에 전달
```

Agent 이름이나 Prompt만 다르게 만드는 것으로는 책임이 분리되지 않습니다. 각 Agent의
Goal, Responsibility, Non-goal, 입력, 출력과 완료 조건을 코드로 표현해야 합니다.

## 01 단원과의 연결

01에서는 Single Agent와 여러 Agent의 차이, 주요 Orchestration Pattern을 작은 예제로
살펴봤습니다. 02에서는 새로운 Pattern을 추가하지 않고 다음 질문에 집중합니다.

- 이 Agent가 맡은 책임은 무엇인가?
- 하나의 사용자 업무를 어떤 Task로 나눌 것인가?
- Agent가 반드시 받아야 하는 입력은 무엇인가?
- 다음 Agent가 사용할 출력은 어떤 구조인가?
- 형식은 맞지만 업무 의미가 잘못된 결과를 어떻게 차단할 것인가?

## 실행 전 준비

모든 명령은 과정 루트에서 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
.\.venv\Scripts\Activate.ps1
```

`01~06`은 API Key 없이 실행할 수 있습니다. `07~08`은 루트 `.env`에 설정한 실제
LLM을 호출합니다.

```dotenv
OPENAI_API_KEY=본인의_API_KEY
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=본인의_API_KEY
GEMINI_MODEL=gemini-3.5-flash
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma3:4b
```

Llama와 Gemma는 실행 중인 공용 Docker Container `aidevs-ollama`를 사용합니다.

```powershell
docker ps --filter "name=aidevs-ollama"
docker exec aidevs-ollama ollama list
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

## Lab 실행

```powershell
python .\02_agent-role-and-contract\01_role_definition.py
python .\02_agent-role-and-contract\02_task_decomposition.py
python .\02_agent-role-and-contract\03_input_output_contract.py
python .\02_agent-role-and-contract\04_role_specific_contracts.py
python .\02_agent-role-and-contract\05_contract_validation.py
python .\02_agent-role-and-contract\06_incomplete_result.py
python .\02_agent-role-and-contract\07_real_multi_llm_contracts.py
python .\02_agent-role-and-contract\08_verified_result_flow.py
```

## Lab 진행 순서

| Lab | 학습 질문 | 확인할 출력 | LLM 호출 |
| --- | --- | --- | ---: |
| `01` | Agent 이름만 다르면 역할이 분리되는가? | Goal·Responsibility·Non-goal | 0회 |
| `02` | 큰 요청을 어떤 책임 단위로 나눌 것인가? | Task 담당자·입력·출력·완료 조건 | 0회 |
| `03` | Agent 사이에서 자연어만 주고받아도 되는가? | 입력·출력 Pydantic 계약 | 0회 |
| `04` | 모든 Agent가 같은 출력 구조를 사용해야 하는가? | Weather와 Budget 전용 계약 | 0회 |
| `05` | 타입이 맞으면 업무 의미도 올바른가? | 누락·역할·합계·상태 오류 차단 | 0회 |
| `06` | 정보 부족과 실행 실패는 같은 상태인가? | `completed`와 `missing_information` | 0회 |
| `07` | Provider가 달라도 계약을 유지할 수 있는가? | 네 LLM의 역할별 결과와 Metadata | 4회 |
| `08` | 어떤 결과를 다음 Agent에게 전달할 수 있는가? | Budget 검증 후 Itinerary 실행 또는 Skip | 2회 |

정상 흐름에서 전체 예상 호출 수는 6회입니다. Gemma 최초 적재 시간과 외부 API 상태에
따라 실행 시간이 길어질 수 있습니다.

## Role과 Task의 차이

```text
Role
└─ Agent가 지속적으로 책임지는 전문 영역

Task
└─ 특정 요청에서 완료해야 하는 작업 단위
```

예를 들어 Budget Agent는 예산 계산이라는 Role을 가집니다. 특정 부산 여행 요청에서는
“60만 원을 교통·숙박·식비·예비비로 분배한다”라는 Task를 받습니다.

Task에는 최소한 다음 내용이 필요합니다.

- `task_id`: 추적할 작업 식별자
- `agent_id`: 작업 책임자
- `required_input`: 실행에 필요한 입력
- `expected_output`: 반환해야 하는 결과
- `completion_condition`: 완료를 판단하는 조건

## 공통 계약과 역할별 계약

모든 Agent가 공통으로 사용하는 Metadata는 협업 상태를 파악하는 데 도움이 됩니다.

```text
agent_id
completed
error
provider
model
latency
```

하지만 실제 업무 결과까지 하나의 `summary`에 넣으면 다음 Agent가 다시 문자열을
해석해야 합니다. 따라서 업무 결과는 역할별 계약으로 분리합니다.

| Agent | 역할별 계약 | 주요 필드 |
| --- | --- | --- |
| Weather Agent | `WeatherResult` | `forecast_summary`, `cautions`, `source_confirmed` |
| Place Agent | `PlaceResult` | `places`, `selection_reason` |
| Budget Agent | `BudgetResult` | `breakdown`, `total`, `currency` |
| Safety Agent | `SafetyResult` | `risks`, `required_actions` |
| Itinerary Agent | `ItineraryResult` | `day_plans`, `applied_constraints` |

## 형식 검증과 업무 의미 검증

```text
Agent JSON 결과
→ 형식 검증
   ├─ 필수 필드가 있는가?
   ├─ 타입이 맞는가?
   └─ 허용된 agent_id인가?
→ 업무 의미 검증
   ├─ 예산 합계가 일치하는가?
   ├─ 음수 금액이 없는가?
   └─ passed 상태와 issues가 모순되지 않는가?
→ 검증 성공 결과만 전달
```

Pydantic 검증 성공은 결과가 사실이라는 의미가 아닙니다. 외부 데이터의 사실성,
최신성, 출처 확인에는 Tool이 필요합니다. 이 폴더의 07 예제는 Tool을 사용하지 않으므로
Weather Agent가 `source_confirmed=False`를 반환하도록 명시하고, Place Agent의 후보도
실제 운영 전에 확인해야 한다고 표시합니다. 실제 날씨와 DB 근거는 아래 미니
프로젝트에서 연결합니다.

## 정보 부족과 실행 실패

| 상태 | 의미 | 다음 행동 |
| --- | --- | --- |
| `completed=True` | 필요한 결과가 준비됨 | 다음 Agent 실행 |
| `completed=False`와 정보 목록 | 사용자 입력이 부족함 | 추가 정보 요청 |
| `error` 존재 | Provider·Network·계약 오류 | 실패 정책 또는 재시도 |

정보가 부족한 상황에서 Agent가 값을 추측해 `completed=True`를 반환하지 않도록 계약과
Prompt를 함께 설계합니다.

## 실제 네 LLM과 역할 계약

`07_real_multi_llm_contracts.py`는 네 Agent를 네 LLM에 하나씩 배정합니다.

| Agent | 논리 Provider | 실제 Model | 출력 계약 |
| --- | --- | --- | --- |
| Weather Agent | `gemini` | `gemini-3.5-flash` | `WeatherResult` |
| Place Agent | `ollama` | `llama3.2` | `PlaceResult` |
| Budget Agent | `openai` | `gpt-4.1-mini` | `BudgetResult` |
| Safety Agent | `gemma` | `gemma3:4b` | `SafetyResult` |

비교 목적은 모델의 문장 품질 순위를 정하는 것이 아닙니다. 서로 다른 Provider의 결과도
같은 방식으로 역할과 계약을 검증할 수 있다는 점을 확인합니다.

## 02 미니 프로젝트로 확장

이 폴더의 코드는 계약 하나씩을 확인하는 최소 강의 예제입니다. 이후
`mini_multi_agent_02_role_task_contract`에서는 같은 개념을 실제 서비스 구조로
확장합니다.

```text
최소 강의 예제                         02 미니 프로젝트
Agent 함수와 Prompt                    agents/*_agent.py의 AgentProfile
shared.travel_llm                      agents/runtime.py + providers/
Pydantic Model 직접 검증               output_contract가 포함된 Agent Registry
Tool 없는 계약 확인                    별도 MCP Server
미확인 날씨                            Open-Meteo 실제 날씨
고정 예산 예제                         PostgreSQL 장소·비용 기준
함수 실행 후 전체 출력                 Redis Trace + 1초 Polling Progress
```

수업에서는 먼저 01~06으로 Role·Task·Contract를 이해하고, 07~08에서 실제 LLM도 같은
계약을 지키는지 확인합니다. 미니 프로젝트에서는 MCP Tool이 근거 데이터를 제공하고
Pydantic이 결과 계약을 검증하는 전체 경계를 관찰합니다.

## 검증된 결과 전달

`08_verified_result_flow.py`는 가장 작은 Agent 연결 경계를 보여 줍니다.

```text
GPT Budget Agent
→ BudgetResult 검증
├─ 성공 → 검증된 Budget를 Gemma Itinerary Agent에 전달
└─ 실패 → Itinerary Agent를 실행하지 않고 Skip 기록
```

이 예제의 Python 코드는 아직 완전한 Orchestrator가 아닙니다. 계약을 통과한 결과만
다음 Agent가 소비한다는 원칙에 집중하며, 동적인 작업 분배는 03에서 학습합니다.

## 오류 확인

실제 Provider가 실패하면 성공 데이터로 바꾸지 않습니다. 출력에서 다음 값을
확인합니다.

- `provider_requested`: 요청한 논리 Provider
- `provider_used`: 실제 성공한 Provider 또는 `None`
- `model`: 호출한 Model
- `latency_ms`: 응답 또는 실패까지 걸린 시간
- `result`: 계약 검증을 통과한 결과 또는 `None`
- `error`: Provider·Network·계약 오류

`08`에서 Budget Agent가 실패하면 Trace에 다음 순서가 남고 Gemma는 호출되지 않습니다.

```text
budget_agent:started
budget_agent:contract_or_provider_failed
itinerary_agent:skipped
```

## 핵심

- Agent를 이름이 아니라 Goal, 책임, Non-goal로 분리합니다.
- Role은 지속적인 책임이고 Task는 특정 요청의 작업 단위입니다.
- Agent의 입력과 출력은 검증 가능한 계약으로 표현합니다.
- 공통 Metadata와 역할별 업무 결과를 구분합니다.
- 형식 검증과 업무 의미 검증은 서로 다른 단계입니다.
- 정보 부족과 실행 오류를 서로 다른 상태로 표현합니다.
- Provider가 달라도 Agent 계약은 유지합니다.
- 검증에 실패한 결과는 다음 Agent에게 전달하지 않습니다.

## 완료 기준

- 하나의 사용자 요청을 책임이 명확한 Task로 분할할 수 있습니다.
- Agent Role Card에 Goal, Responsibility, Non-goal을 작성할 수 있습니다.
- 입력 계약과 역할별 출력 계약을 작성할 수 있습니다.
- 필드 오류, 역할 위장, 업무 의미 오류를 구분할 수 있습니다.
- `completed=False`와 실행 오류의 차이를 설명할 수 있습니다.
- GPT·Gemini·Llama·Gemma 결과에서 Provider Metadata와 계약 결과를 확인할 수 있습니다.
- 앞 Agent의 계약 검증이 실패하면 다음 Agent를 실행하지 않아야 함을 설명할 수 있습니다.

## 직접 확인하기

- `02_task_decomposition.py`에 Safety Agent Task를 추가하고 필요한 입력과 완료 조건을
  작성해 보세요.
- `05_contract_validation.py`에 총예산을 초과한 사례를 추가하려면 어떤 업무 규칙이
  더 필요한지 생각해 보세요.
- `06_incomplete_result.py`에서 숙박 가격이 준비된 경우의 출력을 비교해 보세요.
- `07_real_multi_llm_contracts.py`의 Agent별 Provider 설정을 바꾸고 계약이 유지되는지
  확인해 보세요.
- `08_verified_result_flow.py`에서 잘못된 Budget 결과가 Itinerary Agent로 전달되지
  않는지 Trace를 확인해 보세요.
