# 03 Supervisor and Router Workflow

이 단원은 사용자 요청에 맞는 Worker 하나를 선택하는 Router와, 중간 결과를 확인하며
다음 Worker 또는 종료를 반복 선택하는 Supervisor를 구분하고 구현합니다.

```text
Router
사용자 요청 → 담당 Worker 한 번 선택 → Worker 실행

Supervisor
사용자 요청 + 현재 State → 다음 Worker 선택 → 결과 검증
                         ↑                    ↓
                         └──── 다음 결정 ────┘
```

Router와 Supervisor는 직접 모든 업무를 수행하는 상위 Agent가 아닙니다. 선택과 종료를
담당하며 실제 업무는 권한과 계약이 제한된 Worker가 수행합니다.

## 이전 단원과의 연결

- 01에서는 Router와 Supervisor–Worker Pattern을 작은 예제로 미리 확인했습니다.
- 02에서는 Role, Task, 입력과 역할별 출력 계약을 만들었습니다.
- 03에서는 그 계약을 사용해 누가 Worker를 선택하고 언제 전체 실행을 멈추는지 구현합니다.
- 여러 Worker의 병렬 실행과 결과 Join은 04에서 확장합니다.

## 실행

모든 명령은 과정 루트에서 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
.\.venv\Scripts\Activate.ps1

python .\03_supervisor-and-routing\01_rule_router.py
python .\03_supervisor-and-routing\02_llm_router.py
python .\03_supervisor-and-routing\03_router_contract.py
python .\03_supervisor-and-routing\04_supervisor_decision.py
python .\03_supervisor-and-routing\05_supervisor_worker_loop.py
python .\03_supervisor-and-routing\06_router_vs_supervisor.py
python .\03_supervisor-and-routing\07_multi_llm_supervisor_team.py
```

`01`, `03`, `06`은 API Key 없이 실행할 수 있습니다. 나머지는 실제 LLM을 호출하며
Provider나 계약 오류를 고정된 성공 결과로 바꾸지 않습니다.

## Lab 진행 순서

| Lab | 학습 질문 | 주요 LLM | 예상 호출 |
| --- | --- | --- | ---: |
| `01` | 모든 자연어 분류에 LLM이 필요한가? | 없음 | 0회 |
| `02` | Router 선택과 Worker 실행은 왜 분리하는가? | GPT + 선택 Worker | 최대 2회 |
| `03` | Prompt만으로 Agent 선택 범위를 제한할 수 있는가? | 없음 | 0회 |
| `04` | 현재 State에 따라 다음 행동은 어떻게 달라지는가? | GPT Supervisor | 1회 |
| `05` | 반복 선택과 종료는 누가 통제하는가? | GPT·Gemini·Gemma | 최대 5회 |
| `06` | 어떤 업무에 Router와 Supervisor가 적합한가? | 없음 | 0회 |
| `07` | 네 LLM과 반복 Worker 설정을 어떻게 통제하는가? | GPT·Gemini·Llama·Gemma | 최대 7회 |

## Router와 Supervisor 비교

| 기준 | Router | Supervisor |
| --- | --- | --- |
| 선택 횟수 | 일반적으로 한 번 | 중간 결과를 보며 반복 |
| 입력 | 사용자 요청 | 사용자 요청과 현재 State |
| 출력 | 담당 Worker 또는 정보 요청 | 다음 Worker 또는 `finish` |
| Worker 결과 확인 | 일반적으로 없음 | 다음 결정 전에 확인 |
| 전체 종료 | Worker 선택 후 역할 종료 | 완료·실패·최대 단계로 종료 |
| 적합한 사례 | 배송·환불·기술지원 분류 | 분석→구현→검토 업무 |

Pattern 이름보다 업무의 의존성과 State 필요 여부를 먼저 확인합니다. 한 번 선택하면 되는
업무에 Supervisor Loop를 사용하면 호출 비용과 실패 지점만 늘어날 수 있습니다.

## Rule Router와 LLM Router

명확한 Keyword로 분류할 수 있다면 Python 규칙이 더 단순하고 재현 가능합니다.

```text
배송·택배·도착 → Delivery Agent
환불·취소·반품 → Refund Agent
로그인·오류·비밀번호 → Technical Support Agent
분류 정보 부족 → Request Information
```

표현이 다양하거나 여러 의도가 섞인 문의는 실제 LLM Router가 의미를 해석합니다.

```text
사용자 문의
→ GPT Router Agent
→ SupportRouteDecision 검증
├─ Worker 선택 → 선택된 실제 Worker만 실행
├─ 정보 부족 → 사용자에게 질문
└─ 오류 → Worker 실행 중단
```

| 선택 Worker | Provider | Model |
| --- | --- | --- |
| Delivery Agent | Gemini | `gemini-3.5-flash` |
| Refund Agent | Gemma | `gemma3:4b` |
| Technical Support Agent | Llama | `llama3.2` |

## Routing 계약

`SupportRouteDecision`은 Router의 선택을 `delivery_agent`, `refund_agent`,
`technical_support_agent`, `request_information`으로 제한합니다.

`request_information`을 선택했다면 `missing_information`이 필요하고, 실제 Worker를
선택했다면 이 목록은 비어 있어야 합니다. 형식뿐 아니라 상태 사이의 의미도 검증합니다.

## Supervisor State와 결정 계약

Supervisor는 사용자 요청만 보는 것이 아니라 현재 실행 상태를 함께 읽습니다.

```python
state = {
    "completed_agents": [],
    "outputs": {},
}
```

| State | 의미 |
| --- | --- |
| `completed_agents` | 계약 검증을 통과한 Worker 목록 |
| `outputs` | 다음 결정에 사용할 검증된 Worker 결과 |
| Trace의 `step` 또는 `call` | 현재까지 사용한 LLM 호출 수 |

`SupervisorDecision`은 업무 결과 대신 `next_agent`, `instruction`, `context_keys`,
`reason`을 반환합니다. LLM이 계약을 통과했더라도 현재 단계에서 허용되지 않은 Worker를
선택하면 Python Guard가 `invalid_transition`으로 차단합니다.

## 반복과 종료 Guard

Python은 다음 조건을 최종 통제합니다.

- 허용된 Worker인지 확인
- 앞 단계가 완료됐는지 확인
- 같은 Worker를 불필요하게 반복하지 않는지 확인
- Worker 결과가 계약을 통과했는지 확인
- Supervisor 또는 Worker 오류 시 중단
- 최대 LLM 호출 수 도달 시 종료
- 모든 Worker 완료 후 `finish`인지 확인

05는 다음의 작은 Loop로 Guard를 확인합니다.

```text
GPT Supervisor
→ Gemini Analyst
→ GPT Supervisor
→ Gemma Reviewer
→ GPT Supervisor Finish
```

## 네 LLM Supervisor Team

07은 같은 구조를 네 LLM Team으로 확장하고, 반복되는 Worker 선언을 YAML로 옮깁니다.
앞선 Lab은 흐름을 쉽게 읽도록 Python으로 직접 정의하고, 마지막 Lab에서 운영 규모가
커질 때의 설정 분리를 경험합니다.

| 역할 | 논리 Provider | 실제 Model |
| --- | --- | --- |
| Supervisor Agent | `openai` | `gpt-4.1-mini` |
| Analyst Agent | `gemini` | `gemini-3.5-flash` |
| Developer Agent | `ollama` | `llama3.2` |
| Reviewer Agent | `gemma` | `gemma3:4b` |

```text
GPT Supervisor
→ Gemini Analyst
→ GPT Supervisor
→ Llama Developer
→ GPT Supervisor
→ Gemma Reviewer
→ GPT Supervisor Finish
```

```text
worker_definitions.yaml
        ↓ load_worker_registry()
Python Supervisor Loop → 선택된 Worker의 Provider·Goal·Instructions 사용
```

YAML에는 Worker의 이름, 목표, 지시문, Provider와 출력 계약처럼 반복되는 설정만
둡니다. Worker 순서, 상태 전이, 최대 호출 수, 오류 처리와 종료 조건은 실행 정책이므로
`07_multi_llm_supervisor_team.py`의 Python 코드에 남겨 둡니다. YAML 수정만으로 보안
정책이나 실행 순서가 바뀌게 만들지 않는 것이 핵심입니다.

정상 흐름은 최대 7회 호출합니다. Llama와 Gemma는 같은 `aidevs-ollama` Container를
사용하므로 동시에 실행하지 않고 순차적으로 호출합니다.

## Trace에서 확인할 내용

- Supervisor가 예상한 다음 Worker를 선택했는가?
- Worker 결과가 성공한 뒤에만 State에 추가됐는가?
- 각 Agent가 어떤 Provider와 Model을 사용했는가?
- 실패한 Agent 이후 다른 Worker가 실행되지 않았는가?
- `finish`, `worker_failed`, `supervisor_failed`, `invalid_transition`,
  `max_llm_calls` 중 어떤 이유로 종료됐는가?

## 핵심

- Router는 요청을 보고 담당 Worker를 한 번 선택합니다.
- Supervisor는 현재 State와 중간 결과를 보고 다음 행동을 반복 선택합니다.
- 선택 책임과 실제 Worker의 업무 실행 책임을 분리합니다.
- LLM 결정은 Pydantic 계약과 Python Allowlist로 제한합니다.
- LLM이 계약을 통과해도 업무 의존 순서는 Python이 검증합니다.
- 최대 호출 수와 명시적인 종료 이유가 없는 Supervisor Loop를 만들지 않습니다.
- 여러 Provider를 사용해도 동일한 State와 Trace 규칙을 유지합니다.
- 반복 Worker 선언은 YAML로 관리해도 Workflow 통제는 Python에 유지합니다.

## 완료 기준

- Router와 Supervisor의 차이를 선택 횟수와 State 관점에서 설명할 수 있습니다.
- Rule Router와 LLM Router 중 더 단순한 구조를 선택할 수 있습니다.
- Router 결정과 Worker 실행 결과를 구분할 수 있습니다.
- SupervisorDecision과 Supervisor State를 설명할 수 있습니다.
- 허용 순서, 중복 실행, 최대 호출과 Worker 실패를 Python으로 통제할 수 있습니다.
- GPT·Gemini·Llama·Gemma Team의 실행 Trace와 종료 이유를 읽을 수 있습니다.
- Python 실행 정책과 YAML Worker 설정의 책임을 구분할 수 있습니다.

## 직접 확인하기

- `01_rule_router.py`에 계정 변경 문의를 추가하고 새 Worker가 정말 필요한지 판단하세요.
- `03_router_contract.py`에서 빈 `reason`을 차단하려면 어떤 제약이 필요한지 확인하세요.
- `04_supervisor_decision.py`에서 모든 Worker가 완료된 State를 전달해 `finish`를 확인하세요.
- `05_supervisor_worker_loop.py`의 최대 호출을 4로 줄이고 종료 이유를 확인하세요.
- `07_multi_llm_supervisor_team.py`에서 Worker 순서를 바꿀 때 깨지는 Context 의존성을 확인하세요.
- `worker_definitions.yaml`에서 Analyst의 Provider를 바꾸고 Python Workflow를 수정하지
  않아도 적용되는지 확인하세요.
