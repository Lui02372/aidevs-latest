# 08 Agent Evaluation and Tracing

이 장에서는 새 Agent나 평가용 애플리케이션을 만들지 않습니다. `mini_agent_st`에서 이미 만든 06과 07 Agent를 실제로 실행하고 결과를 검사합니다.

```text
01 Mini Agent 06 Live 평가
02 Mini Agent 07 Live 평가
```

Scenario JSON, 저장 Fixture와 전체 회귀 Suite는 지금 추가하지 않습니다. 두 Live 평가를 먼저 이해한 뒤 필요할 때 확장합니다.

각 파일의 맨 위에는 `SCENARIO`가 있습니다.

```text
SCENARIO
├─ name: 시험 이름
├─ input: Agent에게 보낼 실제 입력
└─ expected: 기대 상태와 행동
```

따라서 한 파일을 위에서 아래로 읽으면 `Scenario 선언 → Live API 호출 → 실제 결과 → 기대값 비교 → PASS/FAIL` 전체가 보입니다.

## 1. Mini Agent 06 Live 평가

### 평가할 행동

```text
질문: 제주 날씨를 확인하고 비가 오면 실내 관광지를 추천해줘

기대 실행:
get_weather → search_indoor_places → 최종 답변
```

평가 파일의 `SCENARIO`에 질문과 기대값을 선언합니다. 실제 Backend의 `/api/agents/run`을 호출하고 다음 세 가지를 검사합니다.

- `status == completed`
- `termination_reason == model_finished`
- 실행된 Tool 순서가 `get_weather → search_indoor_places`

### 실행

터미널 1에서 Mini Agent 06 MCP Server를 실행합니다.

```powershell
cd C:\mini_agent_st\mini_agent_06_agent_workflow
python .\mcp_server\business_tools_server.py
```

터미널 2에서 Backend를 실행합니다.

```powershell
cd C:\mini_agent_st\mini_agent_06_agent_workflow
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

터미널 3에서 평가합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\08_agent-evaluation-and-tracing
python .\01_evaluate_live_agent_06.py
```

## 2. Mini Agent 07 Live 평가

07의 `SCENARIO`에는 입력, 승인 결정, 승인 전 기대값과 승인 후 기대값이 함께 있습니다. 승인이 필요하므로 두 단계로 평가합니다.

```text
Agent 실행
→ waiting_approval 확인
→ 승인 전 place_order 실행 0회 확인
→ 실제 승인 API 호출
→ completed 확인
→ place_order 실행 1회 확인
```

### 실행

06 서버를 종료한 뒤 터미널 1에서 Mini Agent 07 MCP Server를 실행합니다.

```powershell
cd C:\mini_agent_st\mini_agent_07_human_approval
python .\mcp_server\order_tools_server.py
```

터미널 2에서 Backend를 실행합니다.

```powershell
cd C:\mini_agent_st\mini_agent_07_human_approval
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

터미널 3에서 평가합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\08_agent-evaluation-and-tracing
python .\02_evaluate_live_agent_07.py
```

이 평가는 실제 주문을 생성하므로 Mini Agent 07의 교육용 Mock 주문 환경에서만 실행합니다.

## 환경 변수

Backend 주소가 다르면 환경 변수로 변경할 수 있습니다.

```powershell
$env:MINI_AGENT_06_API_URL = "http://127.0.0.1:8000/api/agents/run"
$env:MINI_AGENT_07_API_URL = "http://127.0.0.1:8000/api/agents"
```

## 파일 구성

| 파일 | 역할 |
| --- | --- |
| `01_evaluate_live_agent_06.py` | Mini Agent 06의 Tool 선택·순서·종료 평가 |
| `02_evaluate_live_agent_07.py` | Mini Agent 07의 승인 전·후 안전 평가 |

다음 단계가 필요해지면 실패 Trace 분석, 저장 Fixture, 여러 Scenario와 회귀 평가를 하나씩 추가합니다.
