# 01 Single AI Agent와 Multi AI Agent

이 단원은 “Tool이 많으니 Agent를 여러 개 만든다”가 아니라 **독립 Goal·Context·권한·평가 기준이 있는가**를 판단합니다.

```text
Single AI Agent
└─ 하나의 판단 주체가 전체 여행 초안 생성

여러 독립 AI Agent
├─ Weather Agent
├─ Place Agent
├─ Budget Agent
└─ Safety Agent

Multi AI Agent Orchestration
└─ 위 Agent의 선택·순서·결과 전달·실패·전체 종료까지 통제
``` 

## 이 단원에서 먼저 답해야 할 질문 

이 단원은 Agent를 많이 만드는 방법부터 시작하지 않습니다. 다음 질문에 답하면서 하나의
Agent를 유지할지, 여러 Agent로 분리할지, Orchestrator까지 둘지를 결정합니다.

1. 하나의 Goal과 Prompt로 책임을 명확하게 설명할 수 있는가?
2. 모든 작업이 같은 Context와 Tool 권한을 사용해도 안전한가?
3. 작업마다 필요한 전문 지식과 평가 기준이 다른가?
4. 일부 작업을 독립적으로 실행하거나 병렬화할 수 있는가?
5. 업무 책임을 다른 Agent에게 명시적으로 넘겨야 하는가?
6. 중간 결과에 따라 다음 Agent가 달라지는가?
7. 여러 결과를 누가 검증하고 하나의 답으로 합칠 것인가?
8. 실패·재시도·반복·전체 종료를 누가 통제할 것인가?

앞의 질문 대부분이 필요 없다면 Single Agent가 더 적합할 수 있습니다. Multi-Agent는 Single
Agent보다 발전된 정답이 아니라, 책임 경계가 실제로 필요할 때 선택하는 구조입니다.

## Single Agent란 무엇인가

Single Agent는 하나의 판단 주체가 사용자 요청을 이해하고, 필요한 Tool을 선택하고, Context를
관리하며, 최종 답변을 만드는 구조입니다.

```text
사용자 요청
   ↓
Travel Agent
   ├─ Weather Tool
   ├─ Place Tool
   ├─ Budget Tool
   └─ 최종 여행 계획
```

### 장점

- 호출 흐름이 짧고 구현이 단순합니다.
- LLM 호출 수와 운영 비용이 상대적으로 작습니다.
- Context를 다른 Agent에게 전달하는 계약이 필요하지 않습니다.
- 오류가 발생했을 때 확인할 실행 지점이 적습니다.
- 작은 기능은 Prompt 하나를 수정해 빠르게 실험할 수 있습니다.

### 한계

- 역할과 규칙이 늘어나면 System Prompt가 지나치게 커집니다.
- 날씨 조회 Agent가 결제 Tool까지 보는 것처럼 권한이 과도해질 수 있습니다.
- 작성과 검증을 같은 판단 주체가 수행하면 독립적인 평가가 어렵습니다.
- 하나의 Context에 불필요한 개인정보와 업무 데이터가 섞일 수 있습니다.
- 한 영역의 실패가 전체 요청 실패로 이어질 수 있습니다.

Single Agent의 Prompt가 길다는 이유만으로 즉시 분리하지는 않습니다. 먼저 Tool 함수 분리,
Prompt 정리, 결정적인 Python Workflow로 해결할 수 있는지 확인합니다.

## Multi-Agent란 무엇인가

Multi-Agent 구조에서는 독립된 Goal, Instructions, Context, Tool 권한, 평가 기준을 가진 여러
Agent가 각자의 결과를 만듭니다.

```text
Weather Agent → 날씨 근거
Place Agent   → 장소 후보
Budget Agent  → 예상 비용
Safety Agent  → 위험 검토
```

Agent가 여러 개 있다고 자동으로 협업이 되는 것은 아닙니다. 위 네 결과를 각각 출력하고
프로그램이 끝난다면 이는 여러 독립 Agent의 실행입니다. 실행 순서, 결과 전달, Join, 실패,
종료를 통제하는 Orchestrator가 있어야 Multi-Agent Orchestration이라고 부를 수 있습니다.

```text
여러 독립 Agent                   Multi-Agent Orchestration

요청 → Weather Agent → 결과       요청 → Orchestrator
요청 → Place Agent   → 결과                ├→ Weather Agent
요청 → Budget Agent  → 결과                ├→ Place Agent
                                              ├→ Budget Agent
전체 결과·종료를 관리하는 주체 없음          └→ Join Agent → 최종 결과
```

## Single Agent와 Multi-Agent 비교

| 비교 기준 | Single Agent | Multi-Agent |
| --- | --- | --- |
| 판단 주체 | 하나 | 역할별로 여러 개 |
| Goal | 하나의 넓은 Goal | Agent별 좁고 독립적인 Goal |
| Prompt | 커질 수 있지만 한곳에서 관리 | 짧아지지만 Agent별 관리 필요 |
| Context | 한 Agent가 전체 Context 사용 | 필요한 Context만 역할별 전달 가능 |
| Tool 권한 | 한 Agent에 권한이 모이기 쉬움 | Agent별 Allowlist 적용 가능 |
| 평가 | 생성자와 평가자가 같을 수 있음 | Evaluator 역할을 독립시킬 수 있음 |
| 병렬 실행 | 내부 Tool 수준에서 별도 설계 | 독립 Agent 결과를 병렬화하기 쉬움 |
| 호출 비용 | 일반적으로 작음 | Agent·조정·Join 호출만큼 증가 |
| 지연 시간 | 흐름이 짧음 | 순차 단계와 Join 때문에 늘 수 있음 |
| 실패 지점 | 비교적 적음 | Agent·Provider·Handoff·Join마다 증가 |
| 추적 | 한 흐름 | Agent별 Trace와 전체 Correlation 필요 |
| 적합한 상황 | 작고 응집된 업무 | 책임·권한·평가 기준이 실제로 분리된 업무 |

## Agent를 분리할 수 있는 근거

다음 항목 중 하나가 있다고 반드시 분리하는 것은 아니지만, 두 가지 이상이 명확하면
Multi-Agent 후보로 검토합니다.

| 분리 근거 | 예시 |
| --- | --- |
| 독립 Goal | 날씨 조사와 예산 검증의 완료 기준이 다름 |
| 전문 지식 | 법률 검토와 콘텐츠 작성에 서로 다른 지침 필요 |
| Context 격리 | 날씨 Agent에 결제 정보가 필요하지 않음 |
| Tool 권한 격리 | 조회 Agent와 환불 실행 Agent의 권한이 다름 |
| 독립 평가 | 작성 Agent와 보안 Reviewer를 분리해야 함 |
| 병렬 가능 | 날씨·장소·예산 조사가 서로 의존하지 않음 |
| 책임 이전 | 배송 상담에서 환불 담당자에게 업무를 넘김 |
| 장애 격리 | 장소 검색 실패와 예산 계산 성공을 분리해 처리 |

반대로 단순 계산, 형식 변환, 키워드 분류처럼 결과가 결정적인 작업은 새 Agent보다 Python
함수나 Tool이 더 적합합니다. 모든 함수를 Agent라고 부르면 책임 경계가 오히려 흐려집니다.

## Orchestrator가 담당해야 하는 것

AI Agent는 전문 판단과 결과 생성을 담당하고, 결정적으로 통제해야 하는 항목은 Python
Orchestrator가 담당합니다.

| AI Agent가 잘하는 일 | Python Orchestrator가 보장할 일 |
| --- | --- |
| 자연어 분류·요약·초안 작성 | 허용 Agent와 Tool 목록 |
| 비정형 결과 해석 | 실행 순서와 필수 입력 |
| 전문 역할의 의견 생성 | 최대 단계·최대 반복·Timeout |
| 평가 이유와 수정 제안 | Schema 검증·권한·종료 조건 |

LLM에게 “적절히 반복하다 끝내라”라고만 지시하면 무한 반복이나 예측하기 어려운 실행이 생길
수 있습니다. 최대 반복 횟수, 허용 Handoff 대상, 필수 Join 결과, 실패 시 종료 이유는 코드와
계약으로 제한합니다.

## 이번 단원에서 미리 보는 Pattern

| Pattern | 핵심 질문 | 최소 구조 | 사용하지 않아도 되는 경우 | 구체적인 예 |
| --- | --- | --- | --- | --- |
| Independent Agents | Agent가 여러 개면 협업인가? | A, B, C를 각각 실행 | 하나의 결과만 필요할 때 | Weather·Place·Budget Agent가 각각 조사 결과만 출력하고 전체 여행 계획은 만들지 않음 |
| Sequential | 앞 결과가 다음 입력인가? | A → B → C | 작업이 서로 독립적일 때 | Research Agent의 자료를 Writer Agent가 글로 작성하고 Reviewer Agent가 검토함 |
| Parallel + Join | 독립 결과를 모두 합쳐야 하는가? | A·B·C → Join | 일부 결과만 선택하면 될 때 | Weather·Place·Budget Agent가 독립적으로 조사하고 Itinerary Agent가 하나의 여행 일정으로 합침 |
| Router | 요청마다 담당 하나가 다른가? | Router → A 또는 B | 항상 같은 Agent를 실행할 때 | 고객 질문을 분류하여 배송·환불·기술지원 Agent 중 하나만 선택함 |
| Supervisor–Worker | 중간 결과로 다음 역할이 바뀌는가? | Supervisor ↔ Workers | 경로가 고정되어 있을 때 | 코드 분석 결과에 따라 Developer Agent를 호출하고, 수정 후 Reviewer Agent를 추가 호출함 |
| Handoff | 업무 책임 자체가 이동하는가? | A → 책임·Context → B | 결과만 잠깐 요청할 때 | Support Agent가 주문번호와 상담 이유를 전달하며 환불 업무 책임을 Refund Agent에게 넘김 |
| Evaluator–Reviser | 생성과 검증을 반복해야 하는가? | 작성 → 평가 → 수정 | 결정적 규칙으로 한 번 검사 가능할 때 | Writer Agent의 안내문을 Evaluator Agent가 평가하고 실패하면 Reviser Agent가 최대 5회 수정함 |
| Provider Failover | 같은 계약으로 Provider를 바꿀 수 있는가? | Primary 실패 → Secondary | 실패 시 즉시 중단해야 할 때 | Gemma가 Timeout 또는 오류를 반환하면 실패 기록을 남기고 같은 요청을 GPT로 다시 실행함 |

하나의 서비스는 Pattern 하나만 사용하는 것이 아닙니다. 예를 들어 Router가 요청 종류를
선택하고, 선택된 여행 Workflow 안에서는 Weather·Place Agent를 Parallel로 실행한 뒤 Join할
수 있습니다. 중요한 것은 복잡한 Pattern을 많이 쓰는 것이 아니라 각 구간의 의존성과 책임에
맞는 가장 단순한 Pattern을 선택하는 것입니다.

## Pattern을 잘못 선택한 신호

- Agent마다 Prompt 이름만 다르고 Goal·Context·Tool이 사실상 같습니다.
- 모든 Agent가 전체 대화와 모든 Tool을 공유합니다.
- Router가 업무까지 수행하여 Worker와 책임이 겹칩니다.
- Parallel이라고 설명하지만 앞 Agent의 결과를 다음 Agent가 필요로 합니다.
- Join 없이 Agent 결과 목록을 그대로 사용자에게 전달합니다.
- Supervisor가 최대 단계 없이 Worker를 계속 호출합니다.
- Handoff 대상과 전달 Context가 문자열 설명에만 있고 계약이 없습니다.
- Evaluator가 통과 기준 없이 취향에 따라 반복합니다.
- Failover가 첫 오류를 숨겨 정상 Provider처럼 표시합니다.

### 여기서 계약(Contract)이란 무엇인가

이 과정에서 말하는 계약은 법률 계약서가 아니라, **Agent와 Agent 또는 Agent와 Tool 사이에서
무엇을 입력받고 무엇을 반환하며 어떤 조건을 지켜야 하는지 정한 명시적인 규칙**입니다.

```text
보내는 Agent
→ 정해진 입력 형식
→ 받는 Agent
→ 정해진 출력 형식
→ Orchestrator가 검증
```

예를 들어 Support Agent가 Refund Agent에게 업무를 넘긴다면 “환불을 처리해 주세요”라는
문장만 전달하는 것으로는 부족합니다. 최소한 다음 내용이 정해져 있어야 합니다.

| 계약 항목 | 확인할 질문 | 환불 Handoff 예 |
| --- | --- | --- |
| 입력 | 받는 Agent에게 반드시 필요한 값은 무엇인가? | `order_id`, `reason`, `requested_amount` |
| 출력 | 성공과 실패를 어떤 형태로 반환하는가? | `status`, `refund_id`, `error` |
| 자료형 | 문자열·숫자·목록 중 어떤 형식인가? | 금액은 0 이상의 숫자 |
| 필수 여부 | 누락되면 실행을 중단할 값은 무엇인가? | `order_id`는 필수 |
| 허용 값 | 선택 가능한 값의 범위는 무엇인가? | `status`: proposed·approved·rejected |
| 권한 | 어떤 Tool을 실행할 수 있는가? | 정책 조회는 가능, 실제 환불은 승인 후 가능 |
| 책임 | Handoff 후 현재 담당자는 누구인가? | Refund Agent가 환불 검토 책임을 가짐 |
| 종료 조건 | 언제 성공·실패·재시도로 끝나는가? | 정책 검증 실패 시 rejected로 종료 |

### Prompt와 계약의 차이

Prompt는 AI Agent에게 기대하는 행동을 자연어로 설명합니다. 계약은 실제 실행 경계에서
입력과 출력이 규칙을 지키는지 검사합니다.

```text
Prompt
"주문번호와 환불 사유를 확인하고 안전하게 처리하세요."

계약
order_id: 비어 있지 않은 문자열
reason: 필수 문자열
requested_amount: 0 이상의 숫자
status: proposed | approved | rejected 중 하나
```

Prompt만 있으면 AI Agent가 필드를 빠뜨리거나 이름을 다르게 만들 수 있습니다. 계약이 있으면
Orchestrator가 다음 Agent를 실행하기 전에 누락·형식·허용 값 오류를 발견하고 중단할 수
있습니다.

### 문자열 약속과 실행 가능한 계약

다음은 사람이 읽을 수는 있지만 프로그램이 검증하기 어려운 문자열 약속입니다.

```python
handoff_message = "Refund Agent에게 주문번호와 환불 사유를 전달한다."
```

다음처럼 구조화된 Model을 사용하면 필수 값과 허용 범위를 실행 시점에 검사할 수 있습니다.

```python
from typing import Literal

from pydantic import BaseModel, Field


class RefundHandoff(BaseModel):
    from_agent: Literal["support_agent"]
    to_agent: Literal["refund_agent"]
    order_id: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    requested_amount: int = Field(ge=0)
```

이 Model에서 `order_id`가 없거나 `requested_amount`가 음수이면 Handoff를 실행하지 않습니다.
즉, 계약은 문서에만 적어 두는 설명이 아니라 Python과 Pydantic이 확인할 수 있는 실행 규칙이
되어야 합니다.

### Multi-Agent에서 계약이 중요한 이유

Single Agent 안에서는 이전 단계의 결과를 같은 Prompt Context에서 계속 사용할 수 있습니다.
Multi-Agent에서는 결과가 다른 Agent, 다른 Process 또는 다른 Server로 이동하므로 경계마다
정보가 누락되거나 잘못 해석될 가능성이 커집니다.

- Sequential에서는 앞 Agent의 출력이 다음 Agent의 필수 입력 계약이 됩니다.
- Parallel + Join에서는 Join에 필요한 결과가 모두 도착했는지 계약으로 확인합니다.
- Router에서는 선택 결과가 허용된 Worker ID인지 검사합니다.
- Supervisor에서는 다음 Worker와 최대 단계가 계약 범위 안인지 확인합니다.
- Handoff에서는 대상, 이전할 책임, 최소 Context를 계약으로 남깁니다.
- Evaluator에서는 점수, 통과 여부, 수정 Feedback의 형식을 고정합니다.
- Failover에서는 Primary와 Secondary가 같은 출력 계약을 반환해야 합니다.

좋은 계약은 Agent가 자유롭게 생성할 수 있는 내용과 Python이 반드시 통제할 규칙을 분리합니다.
자연어 답변 내용은 AI Agent가 만들 수 있지만, 권한·금액 범위·허용 대상·반복 횟수·종료 상태는
코드가 검증해야 합니다. 이 개념은 다음 단원 `02_agent-role-and-contract`에서 Pydantic 입력·출력
Model로 더 자세히 실습합니다.

## 실행

모든 명령은 과정 루트 `C:\aidevs\07_multi-agent-service-ops`에서 실행합니다. 처음
실행한다면 먼저 Python 환경과 `.env`를 준비합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Copy-Item .env.example .env
```

`.env`에는 다음 네 가지 LLM 설정이 필요합니다. GPT와 Gemini는 API Key가 필요하고,
Llama와 Gemma는 같은 Ollama API를 사용하지만 서로 다른 Model입니다. 이 예제에서
`ollama`와 `gemma`는 서로 다른 서버를 뜻하는 것이 아니라 Llama와 Gemma를 구분하기
위한 논리적인 Provider 이름입니다.

```dotenv
OPENAI_API_KEY=본인의_API_KEY
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=본인의_API_KEY
GEMINI_MODEL=gemini-3.5-flash
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma3:4b
```

이 과정은 이미 실행 중인 공용 Docker Container `aidevs-ollama`를 사용합니다.

```powershell
docker ps --filter "name=aidevs-ollama"
docker exec aidevs-ollama ollama list
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

목록에 `llama3.2:latest`와 `gemma3:4b`가 표시되어야 합니다. 01 과정에서 별도의
Ollama Container를 만들지 않습니다. Model이 없다면 실행 중인 공용 Container 안에
추가합니다.

```powershell
docker exec aidevs-ollama ollama pull llama3.2
docker exec aidevs-ollama ollama pull gemma3:4b
```

| Agent | 논리 Provider | 실제 Model |
| --- | --- | --- |
| Budget/Writer Agent | `openai` | GPT (`gpt-4.1-mini`) |
| Weather/Evaluator Agent | `gemini` | Gemini (`gemini-3.5-flash`) |
| Place/Developer Agent | `ollama` | Llama (`llama3.2`) |
| Safety/Reviewer Agent | `gemma` | Gemma (`gemma3:4b`) |

> `00_runtime-and-deployment/00_local-services/docker-compose.yml`의 Ollama는 독립적인
> 실습 환경이며 Host Port `11435`를 사용합니다. 현재 01 실습은 이미 실행 중인
> `aidevs-ollama`의 `11434`를 사용하므로 두 실행 방법을 섞지 않습니다.

```powershell
python .\01_single-vs-multi-agent\01_single_ai_agent.py
python .\01_single-vs-multi-agent\02_independent_specialists.py
python .\01_single-vs-multi-agent\03_split_decision.py
python .\01_single-vs-multi-agent\04_compare_architectures.py
python .\01_single-vs-multi-agent\05_context_and_permission_boundaries.py
python .\01_single-vs-multi-agent\06_orchestration_preview.py
python .\01_single-vs-multi-agent\07_sequential_orchestration.py
python .\01_single-vs-multi-agent\08_parallel_and_join.py
python .\01_single-vs-multi-agent\09_router_orchestration.py
python .\01_single-vs-multi-agent\10_supervisor_worker.py
python .\01_single-vs-multi-agent\11_handoff_preview.py
python .\01_single-vs-multi-agent\12_evaluator_reviser.py
python .\01_single-vs-multi-agent\13_provider_failover.py
```

`01`, `02`, `06~13`은 실제 LLM을 호출합니다. 특히 `02`와 `08`은 네 Agent를 네 LLM에 하나씩
배정합니다. 실패를 Mock 성공으로 바꾸지 않고 Metadata의
`error`에 표시합니다. `03~05`는 API Key 없이 분리 기준·구조적 비용·권한 경계를 비교합니다.

## 실행 전 확인과 예상 호출 수

실제 LLM Lab은 호출 비용과 로컬 실행 시간이 발생합니다. 아래 횟수는 정상 흐름의
대략적인 값이며 Evaluator 반복과 Failover 여부에 따라 달라집니다.

| Lab | 필요한 실행 환경 | 예상 LLM 호출 |
| --- | --- | ---: |
| `01` | 선택한 Provider 하나 | 2회 |
| `02` | GPT·Gemini·Llama·Gemma | 4회 |
| `03~05` | 없음 | 0회 |
| `06` | GPT·Gemini | 4회: 독립 실행 2회 + 조정 실행 2회 |
| `07` | Gemini·GPT·Gemma | 최대 3회 |
| `08` | 네 LLM | 최대 4회 |
| `09` | GPT와 선택 Worker Provider | 예제 3건 기준 최대 6회 |
| `10` | Gemini·Llama·Gemma | 최대 3회 |
| `11` | Gemini·Gemma | 최대 2회 |
| `12` | GPT·Gemini, 최대 5회 반복 | 2~10회 |
| `13` | Gemma, 실패 시 GPT | 1~2회 |

네 모델을 모두 준비하지 못했다면 먼저 `03~05`를 실행할 수 있습니다. 실제 LLM Lab의
실패는 성공 결과로 바꾸지 않으며 출력의 `error`, `provider_used`, `model`을 확인합니다.

로컬 Model은 최초 호출 때 메모리에 적재되어 응답이 늦을 수 있습니다. 특히 Gemma가
90초 안에 응답하지 못하면 예제는 `ReadTimeout`을 오류로 출력합니다. 이때 고정된 성공
결과로 대체하지 말고 다음 순서로 상태를 확인합니다.

```powershell
docker stats aidevs-ollama --no-stream
docker logs --tail 50 aidevs-ollama
docker exec aidevs-ollama ollama ps
```

수업에서는 먼저 `03~05`로 개념을 확인한 뒤 `01~02`, 마지막으로 `06~13`의 패턴을
실행하면 개념과 실제 LLM 호출을 분리해 관찰하기 쉽습니다.

## Lab 진행 순서

| Lab | 질문 | 확인할 출력 |
| --- | --- | --- |
| `01` | 하나의 Agent로 어디까지 처리할 수 있는가? | 제약 추가 전후 결과와 Provider Metadata |
| `02` | 독립 Specialist가 있으면 바로 Orchestration인가? | Agent별 성공·실패와 전체 종료 부재 |
| `03` | 어떤 근거가 있을 때 역할을 분리하는가? | 사례별 판정과 구체적인 분리 근거 |
| `04` | 분리하면 어떤 비용과 실패 지점이 늘어나는가? | 호출 수·Context 복사·실패 지점 비교 |
| `05` | Context와 Tool 권한은 왜 Agent별로 나누는가? | 전달 Key와 Tool allowlist 차이 |
| `06` | 여러 Agent와 Orchestration은 무엇이 다른가? | 선택·결과·Trace·전체 종료 유무 |
| `07` | 앞 결과가 다음 입력이면 어떻게 실행하는가? | Sequential 결과 전달과 중간 실패 |
| `08` | 독립 결과는 언제 합칠 수 있는가? | Parallel 개념과 필수 Join 결과 |
| `09` | 요청마다 필요한 Agent가 다르면 어떻게 선택하는가? | Router의 단일 선택과 Worker 실행 |
| `10` | 결과를 보며 다음 Agent를 선택하려면? | Python Supervisor의 반복과 최대 단계 |
| `11` | 실행 책임을 다른 Agent에게 어떻게 넘기는가? | Handoff 대상·책임·최소 Context |
| `12` | 생성과 평가를 분리하고 어떻게 반복하는가? | Evaluator–Reviser와 최대 반복 |
| `13` | Primary LLM 실패를 어떻게 투명하게 복구하는가? | 시도 순서·오류·최종 Provider |

`01`에서 Provider 오류가 나면 먼저 `.env`를 확인합니다. 개념 학습을 계속하려면
`03`, `04`를 먼저 실행할 수 있지만 실제 호출이 성공한 것처럼 간주하지 않습니다.

## 강의 예제와 미니 프로젝트의 구조 차이

이 폴더의 파일은 Pattern 하나를 한 화면에서 읽고 실행하는 최소 강의 예제입니다.
따라서 `weather_agent()`처럼 함수 이름으로 Agent 역할을 드러내고, 같은 파일 안에서
작은 Orchestrator와 출력 확인 코드를 함께 보여 줍니다.

미니 프로젝트 `mini_multi_agent_01_patterns`에서는 다음 단계로 구조를 확장합니다.

```text
최소 강의 예제                         미니 프로젝트
weather_agent() 함수                  agents/weather_agent.py의 AgentProfile
run_learning_agent()                  agents/runtime.py
AGENTS 또는 WORKER_AGENTS             agents/registry.py
orchestrator_agent() 함수             orchestration/engine.py
외부 Tool 없음                        MCP Client와 별도 MCP Server
```

두 방식은 서로 경쟁하는 구현이 아닙니다. 강의에서는 Pattern의 핵심 흐름을 먼저 확인하고,
미니 프로젝트에서는 Agent 정의·실행·협업·Tool을 분리하여 실제 애플리케이션 구조로
발전시킵니다. 01 강의 예제를 처음부터 여러 디렉터리로 나누지 않는 이유는 초보자가
Pattern보다 파일 탐색에 더 많은 시간을 쓰지 않게 하기 위해서입니다.

## 다른 업무에도 적용하기

여행은 전체 과정을 연결하는 주제이고, `03`과 `05`에서는 같은 기준을 다른 업무에
적용합니다.

| 업무 | 구분할 질문 |
| --- | --- |
| 고객지원과 환불 | 조회 Agent와 실제 환불 Agent의 권한을 분리해야 하는가? |
| 코드 생성과 보안 검토 | 작성자와 검토자의 독립 평가 기준이 필요한가? |
| 콘텐츠 맞춤법 검사 | Agent보다 결정적인 Workflow나 Tool로 충분한가? |
| 장애 분석과 서버 재시작 | 분석 Context와 운영 변경 권한을 격리해야 하는가? |

주제가 달라져도 Agent 수가 아니라 Goal·Context·권한·평가·종료 기준으로 판단합니다.

## Orchestration Pattern 지도

`01~02`에서는 Single과 여러 독립 AI Agent를 비교하고, `03~05`에서는 호출 없이
분리 기준을 정리합니다. `06~12`에서는 실제 AI Agent로 패턴을 실행하고 `13`에서는
Failover를 확인합니다. Python Orchestrator가 허용 Agent·필수 결과·최대 반복·종료를
통제하며, LLM은 전문 결과 생성·분류·검토·수정을 담당합니다.

### 1. Sequential

```text
Research Agent → Writer Agent → Reviewer Agent
```

앞 결과가 다음 단계의 필수 입력일 때 사용합니다. 순서가 명확하지만 앞 단계가 늦거나
실패하면 뒤 단계도 기다리거나 중단됩니다. `07_sequential_orchestration.py`에서
결과 전달과 중간 실패 경계를 확인합니다.

### 2. Parallel + Join

```text
Weather Agent ─┐
Place Agent   ─┼→ Join → Itinerary Agent
Budget Agent  ─┘
```

서로 의존하지 않는 조사는 병렬로 실행할 수 있습니다. 이 입문 예제는 아직 Thread나
비동기를 사용하지 않고 독립 Agent를 순서대로 호출하여 구조와 Join 경계만 확인합니다.
실제 병렬 처리와 부분 실패는 04 단원에서 확장합니다.

### 3. Router

```text
요청 → Router ─┬→ Delivery Agent
               ├→ Refund Agent
               └→ Technical Support Agent
```

요청마다 필요한 역할 하나가 달라질 때 적합합니다. Router는 직접 업무를 수행하지 않고
허용된 Agent를 선택합니다. 한 번 선택하고 끝나는 구조라는 점이 Supervisor와 다릅니다.

### 4. Supervisor–Worker

```text
Supervisor → Worker 선택 → 결과 확인 → 다음 Worker 또는 종료
```

한 번의 Routing으로 끝나지 않고 중간 결과에 따라 다음 작업을 정할 때 사용합니다.
최대 단계와 완료 조건을 Python이 보장해야 하며 Supervisor에게 무제한 반복 권한을
주지 않습니다. 이 입문 예제의 Supervisor는 Python으로 순서를 통제하고 Worker만 실제
LLM을 사용합니다. 결과를 보고 다음 역할을 동적으로 선택하는 LLM 기반 Supervisor는 03
단원에서 확장합니다.

### 5. Handoff

```text
Support Agent ── 책임과 최소 Context ──→ Refund Agent
```

단순 계산을 요청하고 결과를 돌려받는 호출과 달리 현재 업무의 책임 주체가 바뀝니다.
누가 누구에게 어떤 책임을 넘겼는지가 계약에 남아야 합니다. 상세 Guard는 05에서
학습합니다.

### 6. Evaluator–Reviser

```text
Writer → Evaluator ── 통과 → 종료
             └─ 실패 → Reviser → 재평가
```

생성과 평가에 독립 기준이 필요할 때 적합합니다. 평가가 실패할 때 무한 수정하지 않도록
최대 5회 반복과 종료 이유를 기록하며, 기준을 통과하면 즉시 조기 종료합니다.

### 7. Provider Failover

```text
Gemma Primary ── 실패 → GPT Secondary
```

동일한 출력 계약을 유지한 채 다른 실제 Provider를 시도합니다. 첫 실패를 숨기지 않고
`attempts`에 모델과 오류를 남깁니다. 수업에서는 Gemma가 정상인 경우를 먼저 실행한 뒤,
`GEMMA_MODEL`을 존재하지 않는 이름으로 잠시 바꿔 Failover를 관찰하고 즉시 복원합니다.

## 어떤 Pattern을 선택할까요?

| 상황 | 먼저 검토할 Pattern | 실사용 예 |
| --- | --- | --- |
| 앞 결과가 다음 입력에 반드시 필요 | Sequential | ① Research Agent의 조사 결과로 Writer Agent가 보고서 작성<br>② 요구사항 분석 후 Developer Agent가 코드를 생성하고 Reviewer Agent가 검토 |
| 여러 작업이 독립적이고 결과를 모두 사용 | Parallel + Join | ① 날씨·장소·예산을 동시에 조사한 뒤 여행 일정으로 통합<br>② 여러 문서의 요약을 독립적으로 만든 뒤 하나의 종합 보고서로 통합 |
| 요청마다 담당 Agent 하나가 다름 | Router | ① 고객 문의를 배송·환불·기술지원 Agent 중 하나에게 전달<br>② 질문을 재무·법률·인사 Agent 중 적합한 담당자에게 전달 |
| 중간 결과에 따라 다음 역할이 달라짐 | Supervisor–Worker | ① 장애 분석 결과에 따라 Database·Network·Application Agent 중 다음 담당자를 선택<br>② 코드 분석 결과에 따라 Developer를 호출하거나 바로 Reviewer에게 전달 |
| 업무 책임 자체를 다른 Agent에게 이전 | Handoff | ① 배송 상담 중 환불 요청이 확인되면 Refund Agent에게 주문 Context와 책임 이전<br>② 일반 상담에서 보안 사고가 확인되면 Security Agent에게 사건 처리 책임 이전 |
| 생성 결과를 독립 기준으로 반복 개선 | Evaluator–Reviser | ① Writer의 안내문을 Policy Evaluator가 검사하고 실패 항목을 Reviser가 수정<br>② 생성된 SQL을 Safety Evaluator가 검토하고 위험 Query면 제한 횟수 안에서 다시 작성 |

Pattern 이름부터 선택하지 않습니다. 의존성, 책임, Context, 권한, 실패와 종료 조건을
먼저 그린 뒤 가장 단순한 구조를 선택합니다.

## 이후 단원과 연결

| 01에서 미리 본 내용 | 상세 단원 |
| --- | --- |
| Agent별 입출력과 역할 | 02 Agent Role and Contract |
| Router와 실제 LLM Supervisor | 03 Supervisor and Routing |
| Sequential·Parallel·Join·Supervisor Loop | 04 Orchestration |
| 책임 이전과 최소 Context | 05 Handoff and Context |
| Agent별 권한과 승인 | 06 Multi-Agent Safety |
| 결과 평가·Feedback·Retry·Trace | 07 Evaluation, Feedback, Retry and Tracing |

## 핵심

- Agent 수가 아니라 판단 주체와 책임 경계를 봅니다.
- 여러 Agent가 존재하는 것과 Orchestration은 다릅니다.
- 처음에는 Single AI Agent로 시작하고 분리 근거가 생길 때 Multi AI Agent를 검토합니다.

## 완료 기준

- Tool이 여러 개라는 이유만으로 Multi-Agent를 선택하지 않습니다.
- 여러 독립 Agent와 Multi-Agent Orchestration의 차이를 설명할 수 있습니다.
- 권한 격리가 필요할 때 얻는 이점과 늘어나는 호출·실패 지점을 함께 말할 수 있습니다.
- Agent별 Context와 Tool 권한이 실제 경계라는 것을 코드에서 확인할 수 있습니다.
- 여러 독립 Agent 실행과 Orchestration을 구분할 수 있습니다.
- GPT·Gemini·Llama·Gemma의 실제 결과와 Provider 오류 Metadata를 구분해 읽을 수 있습니다.
- 각 Pattern의 최대 단계·최대 반복·중간 실패 종료 조건을 출력에서 확인할 수 있습니다.

## 직접 확인하기

- 네 Specialist의 Goal을 하나로 합쳤을 때 Prompt와 결과가 어떻게 복잡해지는지 비교하세요.
- Place Agent와 Budget Agent가 서로 다른 Context 권한을 가져야 하는 사례를 적어 보세요.

## 마지막 단계: Mini Multi-Agent 01로 확장

13개의 강의 파일을 실행한 뒤 `C:\mini_multi_agent_st\mini_multi_agent_01_patterns`에서 같은
개념을 하나의 Web Application으로 연결합니다. 강의 파일을 버리고 새로 만드는 것이 아니라,
각 파일에 있던 책임을 Application 계층별로 옮기는 단계입니다.

### 강의 예제가 미니 프로젝트로 이동하는 방법

| 강의 파일의 표현 | 미니 프로젝트의 위치 | 확장되는 책임 |
| --- | --- | --- |
| `weather_agent()` 같은 함수 | `backend/app/agents/*_agent.py` | Agent별 Goal·지시문·Tool 권한 선언 |
| 파일 안의 Agent 목록 | `backend/app/agents/registry.py` | Agent ID 등록과 조회 |
| 한 Agent의 LLM 호출 | `backend/app/agents/runtime.py` | Provider·MCP Tool·출력 계약 공통 실행 |
| Pattern 실행 함수 | `backend/app/orchestration/engine.py` | 순서·분기·Join·반복·종료 통제 |
| Provider별 호출 코드 | `backend/app/providers/registry.py` | GPT·Gemini·Llama·Gemma 호출 방식 통일 |
| 출력용 `dict` | `backend/app/schemas/runs.py` | HTTP 요청·응답 Pydantic 검증 |
| 직접 함수 Tool | `backend/app/mcp/client.py` | HTTP MCP Server 호출 |
| Tool 구현과 데이터 | `mcp_server/tools`, `database`, `weather` | JSON·PostgreSQL·실제 날씨 Source 분리 |
| `print()` 결과 | `frontend/app.py` | 왼쪽 메뉴·Agent 결과·Trace 시각화 |

### 화면 메뉴와 강의 Lab 연결

| 미니 프로젝트 메뉴 | 연결되는 강의 파일 | 화면에서 확인할 것 |
| --- | --- | --- |
| 01 Single AI Agent | `01_single_ai_agent.py` | 하나의 Agent와 선택 Provider |
| 02 Independent Agents | `02_independent_specialists.py` | 네 Agent 결과와 전체 Join 부재 |
| 03 Agent 분리 판단 | `03_split_decision.py` | Goal·권한·평가 근거 Check |
| 04 아키텍처 비용 비교 | `04_compare_architectures.py` | 호출 수와 실패 지점 증가 |
| 05 Context와 Tool 권한 | `05_context_and_permission_boundaries.py` | Agent별 전달 Key와 Tool Allowlist |
| 06 Orchestration 비교 | `06_orchestration_preview.py` | 독립 실행과 조정 실행의 Trace 차이 |
| 07 Sequential | `07_sequential_orchestration.py` | 앞 출력이 다음 입력으로 전달되는 과정 |
| 08 Parallel + Join | `08_parallel_and_join.py` | Specialist 결과와 최종 Join |
| 09 Router | `09_router_orchestration.py` | 선택된 Worker 하나와 선택 이유 |
| 10 Supervisor–Worker | `10_supervisor_worker.py` | 중간 상태·다음 Worker·최대 단계 |
| 11 Handoff | `11_handoff_preview.py` | 이전 책임·대상·최소 Context |
| 12 Evaluator–Reviser | `12_evaluator_reviser.py` | 평가 결과·수정 Feedback·최대 5회 종료 |
| 13 Provider Failover | `13_provider_failover.py` | Primary 오류와 Secondary 시도 기록 |

### 미니 프로젝트에서 추가로 배우는 것

강의 파일은 Pattern의 핵심만 읽기 쉽게 한 파일에 둡니다. 미니 프로젝트에서는 다음과 같은
실제 Application 경계를 추가합니다.

```text
사용자
→ Streamlit Frontend :8501
→ FastAPI Backend :8000
→ Pattern Engine
   ├→ Agent Registry와 Runtime
   ├→ GPT·Gemini·Llama·Gemma
   └→ MCP Client
→ Learning MCP Server :8010
   ├→ 여행 Tool
   ├→ 고객지원 Tool
   └→ 콘텐츠 Tool
```

- Agent Profile과 API Schema를 분리합니다.
- Agent 실행과 Orchestration 실행을 분리합니다.
- Tool 구현을 Backend에서 분리해 MCP Server로 실행합니다.
- 네 LLM Provider가 같은 Agent 계약을 사용하게 합니다.
- 최종 답변뿐 아니라 단계별 Trace, Provider, Model, 오류, 종료 이유를 화면에 표시합니다.
- JSON 데이터에서 실제 Open-Meteo 또는 PostgreSQL로 Source를 바꿀 수 있게 합니다.

### 권장 연결 실습

1. 강의 파일 `01~05`로 Single/Multi 분리 기준을 먼저 설명합니다.
2. 강의 파일 `06~13`을 하나씩 실행해 Pattern의 입력과 출력을 확인합니다.
3. 미니 프로젝트에서 같은 번호의 왼쪽 메뉴를 실행합니다.
4. 강의 파일의 함수가 미니 프로젝트의 어떤 Module로 이동했는지 표를 따라 찾습니다.
5. 화면 Trace와 터미널 `print()` 결과가 같은 실행 단계를 표현하는지 비교합니다.
6. Agent별 Provider를 바꾸어도 Pattern 계약이 유지되는지 확인합니다.
7. `WEATHER_DATA_SOURCE=live`로 실제 날씨 Tool을 연결합니다.
8. 준비된 PostgreSQL 환경에서는 `SUPPORT_DATA_SOURCE=postgresql`로 고객지원 조회를 연결합니다.

### 이 단원의 최종 도착점

```text
Single Agent를 무조건 Multi-Agent로 바꾸는 것          X
많은 Agent와 복잡한 Pattern을 사용하는 것              X

분리 근거가 없으면 Single Agent를 유지하고,
책임·Context·권한·평가 기준이 달라질 때 Agent를 분리하며,
의존성·실패·종료 조건에 맞는 최소 Orchestration을 선택한다. O
```

미니 프로젝트를 실행할 수 있다는 것만으로 완료하지 않습니다. 화면에서 각 Pattern의 선택
이유, 증가한 비용과 실패 지점, Python이 통제하는 종료 조건을 설명할 수 있어야 01 과정이
완료됩니다.
