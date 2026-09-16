# 05 Handoff and Context

이 단원은 Agent 사이에 결과를 전달하는 것과 **현재 업무 책임을 이전하는 것**을
구분합니다. 최소 Context, 구조화 계약, YAML 경로 Registry, Python Guard, 대상 Agent의
수락과 책임 소유권 변경을 순서대로 학습합니다.

```text
Handoff 제안
→ 계약 검증
→ 경로·사용자·Context Guard
→ 대상 Agent 수락 또는 거절
→ 수락한 경우에만 owner_agent 변경
→ 대상 Agent 완료 또는 실패 기록
```

## 이전 단원과의 연결

- 01에서 Handoff Pattern의 작은 모양을 확인했습니다.
- 02에서 Agent별 입력·출력 계약과 역할 경계를 만들었습니다.
- 03에서 Router와 Supervisor가 다음 Agent를 선택했습니다.
- 04에서 병렬 실행과 Join 사이에 Handoff가 등장했습니다.
- 05에서는 제안 이후의 검증·수락·책임 이전과 실패 상태를 완성합니다.
- Agent별 권한과 승인은 06에서 확장합니다.

## 함수 호출과 Handoff의 차이

함수 호출은 계산을 요청하고 결과를 돌려받는 기술적 동작입니다. Handoff는 현재 Agent가 수행하던 **책임을 다음 Agent에게 명시적으로 넘기는 일**입니다.

```text
Weather Agent
→ 실제 날씨 결과에서 최소 Context 선택
→ Handoff Envelope 생성
→ YAML 경로 + Python Guard
→ Itinerary Agent 수락
→ 책임 소유권 변경
```

좋은 Handoff에는 다음 내용이 있습니다.

- 누가 누구에게 넘기는가
- 어떤 책임을 넘기는가
- 다음 Agent가 꼭 알아야 하는 최소 Context
- 같은 사용자와 Task인지 확인할 ID
- 전체 흐름을 추적할 trace ID
- 반복 인계를 제한할 hop count

대화 전체, API Key, 비밀번호, 내부 프롬프트는 넘기지 않습니다. Context가 많을수록 정확해지는 것이 아니라 비용·정보 유출·잘못된 판단 가능성도 함께 커집니다.

## Lab 진행 순서

| Lab | 확인할 내용 | LLM·외부 연결 |
| --- | --- | --- |
| `01_minimum_context.py` | 전체 State에서 최소 Context 선택 | 없음 |
| `02_handoff_contract.py` | 구조화된 Handoff Envelope | 없음 |
| `03_handoff_guard.py` | YAML 경로와 Python Guard | 없음 |
| `04_ownership_transition.py` | 수락 이후 책임 소유권 변경 | 없음 |
| `05_rejection_and_failure.py` | 거절·중복·잘못된 책임자·실패 | 없음 |
| `06_real_agent_handoff.py` | 실제 Weather→Itinerary Handoff | Open-Meteo·Gemini·Gemma |

## 실행

모든 명령은 과정 루트에서 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path

python .\05_handoff-and-context\01_minimum_context.py
python .\05_handoff-and-context\02_handoff_contract.py
python .\05_handoff-and-context\03_handoff_guard.py
python .\05_handoff-and-context\04_ownership_transition.py
python .\05_handoff-and-context\05_rejection_and_failure.py
python .\05_handoff-and-context\06_real_agent_handoff.py
```

`01`~`05`는 API Key 없이 실행할 수 있습니다. `06`은 Open-Meteo 실제 날씨와 Gemini,
Gemma를 호출하며 외부 오류를 고정 성공 결과로 바꾸지 않습니다.

## Handoff Envelope

| 필드 | 의미 |
| --- | --- |
| `handoff_id` | 중복 인계 방지 ID |
| `task_id` | 같은 업무 실행인지 확인 |
| `trace_id` | 전체 실행 Event 연결 |
| `from_agent`, `to_agent` | 현재 책임자와 인수 대상 |
| `responsibility` | 이전할 업무 책임 |
| `context` | 대상이 꼭 알아야 하는 최소 정보 |
| `context_version` | Context 계약 변경 추적 |
| `user_id` | 다른 사용자 데이터 혼입 방지 |
| `hop_count` | 순환·무한 Handoff 제한 |
| `status` | 제안부터 완료·실패까지의 상태 |

## Python + YAML 책임 분리

`handoff_policies.yaml`에는 반복되는 허용 경로와 Context 목록을 선언합니다.

```yaml
weather_to_itinerary:
  from_agent: weather_agent
  to_agent: itinerary_agent
  required_context: [destination, days, weather_summary]
  optional_context: [weather_cautions, transport, food_restriction]
  max_hops: 3
```

Python Guard는 다음 항목을 최종 통제합니다.

- 현재 사용자와 Handoff 사용자가 같은가?
- 현재 `owner_agent`가 `from_agent`와 같은가?
- YAML Registry에 허용된 경로인가?
- 필수 Context가 모두 있는가?
- 허용되지 않은 값이나 민감정보가 포함되지 않았는가?
- 같은 `handoff_id`를 이미 처리했는가?
- 최대 Hop을 넘지 않았는가?

YAML을 수정했다고 보안 검증이 자동으로 우회되어서는 안 됩니다.

## 책임 상태 전이

```text
proposed → validated → accepted → transferred → completed
                       └→ rejected
                                      └→ failed
```

`validated`는 데이터와 정책이 유효하다는 뜻일 뿐 책임 이전 완료가 아닙니다. 이 Lab은
대상 Agent가 유효한 결과 계약을 반환한 것을 수락으로 보고 그 뒤에 Shared State의
`owner_agent`를 변경합니다. 거절되거나 수락 전에 실패하면 원래 Agent가 책임을 유지합니다.

## Event와 운영 확장

이 과정은 Event를 Python 목록으로 확인합니다. 미니 프로젝트에서는 같은 Event를
Redis Stream과 SSE에 연결할 수 있습니다.

```text
handoff_proposed → handoff_validated → handoff_accepted
→ ownership_transferred → target_agent_completed 또는 target_agent_failed
```

SSE는 Event 전달 수단이며 상태 저장소가 아닙니다. Redis Hash Snapshot이나 영속 저장소가
현재 책임자와 최종 상태를 별도로 보존해야 합니다.

## Handoff와 Multi Agent Orchestration의 관계

Handoff는 Orchestration 전체가 아닙니다. Orchestrator는 어떤 Handoff가 가능한지, 다음 Agent를 실행할지, 실패하면 종료할지, 전체 Task가 끝났는지를 통제합니다. Agent가 “다음 Agent에게 넘기겠다”고 말해도 Python Guard가 허용하지 않으면 실행되지 않습니다.

## 완료 기준

- 함수 호출과 Handoff의 책임 차이를 설명할 수 있습니다.
- 전체 State에서 최소 Context만 선택할 수 있습니다.
- YAML 경로 선언과 Python 보안 검증의 책임을 구분할 수 있습니다.
- 검증과 수락, 소유권 이전의 차이를 설명할 수 있습니다.
- 거절·중복·잘못된 책임자·대상 실패를 안전하게 처리할 수 있습니다.
- 실제 두 LLM Handoff의 Event와 최종 책임자를 확인할 수 있습니다.

## 직접 확인하기

1. Weather Agent의 원문 전체 대신 무엇만 Itinerary Agent에 전달할지 적어 보세요.
2. `task_id`와 `trace_id`의 역할 차이를 설명해 보세요.
3. Agent가 자기 자신에게 계속 Handoff하면 왜 위험한지 설명해 보세요.
4. `04_ownership_transition.py`에서 수락 값을 `False`로 바꾸고 책임자를 확인하세요.
5. `handoff_policies.yaml`에서 필수 Context를 추가하고 Guard 결과를 확인하세요.
6. 동일한 `handoff_id`를 두 번 처리했을 때 차단되는 이유를 설명하세요.
