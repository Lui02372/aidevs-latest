# 06 AI Security and Guardrails

앞 과정에서 여러 Agent가 역할을 나누고 Context와 결과를 전달했습니다. 이제 Agent가 허용된 데이터와 Tool만 사용하고 안전한 응답만 내보내도록 만듭니다.

이 단계는 초보자가 각 보안 경계를 눈으로 확인하도록 작은 결정적 예제로 구성합니다. 실제 LLM은 같은 입력에도 다른 문장을 만들 수 있으므로 핵심 보안 판단에는 사용하지 않습니다. **LLM은 행동을 제안하고 Python Guard가 실행 허용 여부를 결정합니다.**

## 전체 학습 시나리오

```text
사용자 요청
  → Prompt Injection 1차 검사
  → Pydantic 입력 계약 검사
  → Agent별 최소 Context 전달
  → Agent별 Tool 권한 검사
  → 변경 작업의 사용자 승인 검사
  → 멱등성 적용 후 실행
  → 최종 응답 Policy 검사
  → 모든 결정 Audit Log 기록
```

문자열 차단 규칙 하나로 모든 공격을 막을 수는 없습니다. 하나의 완벽한 필터를 만드는 것이 아니라 여러 신뢰 경계에 독립된 방어선을 배치하는 것이 핵심입니다.

## 교육 항목과 Lab

| 교육 항목 | Lab | 확인할 결과 |
| --- | --- | --- |
| Prompt Injection 방어 | `01_prompt_injection_defense.py` | 정상 요청 허용, 의심 요청 차단 |
| 입력 검증과 필터링 | `02_input_validation.py` | 형식·범위 오류 출력 |
| Policy 기반 응답 검증 | `03_policy_response_guard.py` | 허위 실행 주장·민감 정보 차단 |
| Agent와 Tool 권한 | `04_agent_tool_permissions.py` | Weather Agent의 저장 요청 차단 |
| 위험 작업 승인 | `05_approval_boundary.py` | 현재 요청과 일치하는 승인만 허용 |
| Retry 중복 방지 | `06_idempotent_write.py` | 두 요청, 실제 저장 1회 |
| Multi-Agent 접근 제어 | `07_role_context_access_control.py` | 역할별 최소 Context와 사용자 격리 |
| 통합 정책과 감사 추적 | `08_integrated_guardrails.py` | 단계별 Audit Event 출력 |

각 Python 파일 상단에는 등장 Agent, 정상·공격 요청, 기대 결과, 학습 포인트를 포함한 상세 시나리오가 있습니다. 수업에서는 먼저 주석을 읽고 결과를 예상한 다음 코드를 실행합니다.

## Python과 YAML의 책임

`security_policies.yaml`에는 운영 중 바꿀 가능성이 있는 문구, 길이, Context 허용 필드를 둡니다. `security_registry.py`가 정책을 읽고 각 Lab의 Python 코드가 최종 결정을 실행합니다.

| YAML에 두는 것 | Python에 두는 것 |
| --- | --- |
| 차단 문구와 최대 길이 | Pydantic 계약과 범위 검사 |
| 응답 Policy 항목 | Tool 실행 전 권한 강제 |
| Agent별 Context 필드 | 승인 일치와 멱등성 로직 |

YAML을 수정할 수 있다고 실행 권한이 자동으로 생기지는 않습니다. 위험한 행동의 최종 허용 조건은 Python과 서버가 보장해야 합니다.

## 실행

과정 루트에서 순서대로 실행합니다. API Key나 외부 서비스는 필요하지 않습니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python .\06_multi-agent-safety\01_prompt_injection_defense.py
python .\06_multi-agent-safety\02_input_validation.py
python .\06_multi-agent-safety\03_policy_response_guard.py
python .\06_multi-agent-safety\04_agent_tool_permissions.py
python .\06_multi-agent-safety\05_approval_boundary.py
python .\06_multi-agent-safety\06_idempotent_write.py
python .\06_multi-agent-safety\07_role_context_access_control.py
python .\06_multi-agent-safety\08_integrated_guardrails.py
```

`06_idempotent_write.py`의 메모리 Registry는 개념 학습용입니다. 운영 과정에서는 Redis로 교체합니다.

## 수업 중 확인할 질문

1. Prompt Injection 문구 검사만으로 충분하지 않은 이유는 무엇인가요?
2. 숫자 범위를 LLM이 아니라 Python이 검사해야 하는 이유는 무엇인가요?
3. Weather Agent가 일정 저장 Tool을 호출하면 어디에서 차단되나요?
4. 승인과 idempotency key는 각각 어떤 문제를 해결하나요?
5. 모든 Agent에게 전체 Context를 전달하면 어떤 문제가 생길 수 있나요?
6. 차단 결정도 Audit Log에 남겨야 하는 이유는 무엇인가요?

## 완료 기준

- 8개 Lab의 허용·차단 이유를 설명할 수 있습니다.
- Prompt Injection, 입력 검증, Tool 권한, 승인, 멱등성, 응답 검증의 차이를 구분합니다.
- YAML 정책과 Python 강제 로직의 책임 차이를 설명할 수 있습니다.
- Multi-Agent 내부 요청도 신뢰하지 않고 재검증해야 함을 이해합니다.
