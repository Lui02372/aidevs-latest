# 02. Multi-Agent Architecture Guide

멀티 에이전트 아키텍처 설계서는 “Agent를 몇 개 만들었는가”보다 “왜 그렇게 역할을 나누었는가”를 설명해야 합니다.

## 권장 Agent 구성

| Agent | 책임 |
| --- | --- |
| Supervisor Agent | 장애 요청을 접수하고 전체 실행 순서를 조정합니다. |
| Diagnosis Agent | 장애 유형과 원인을 분류합니다. |
| Recovery Agent | 복구 전략을 선택합니다. |
| Executor Agent | 복구 명령 또는 시뮬레이션을 실행합니다. |
| Validation Agent | 복구 후 Health Check와 결과를 검증합니다. |
| Reporter Agent | 실행 결과와 다음 조치를 요약합니다. |
| Guardrail Agent | 위험한 작업, 민감 정보, 정책 위반 가능성을 확인합니다. |

## Handoff Context

Agent 간 작업 전달 시 아래 정보가 누락되지 않아야 합니다.

```json
{
  "incident_id": "inc-001",
  "service_name": "backend",
  "failure_type": "timeout",
  "severity": "medium",
  "current_agent": "diagnosis",
  "next_agent": "recovery",
  "previous_result": "backend response timeout",
  "allowed_actions": ["retry", "health_check"],
  "blocked_actions": ["delete_resource", "rotate_secret"],
  "retry_count": 0,
  "max_retry_count": 2
}
```

## 설계서에 반드시 들어갈 내용

- 아키텍처 구조 선택 이유
- 각 Agent의 역할과 책임 범위
- Agent 간 의존 관계
- Handoff Context 필드 정의
- 공유 상태와 중간 결과 저장 방식
- 실패 시 fallback 흐름
- 위험 작업 제한 기준

## 초보자가 흔히 빠뜨리는 부분

- Agent 이름만 있고 실제 책임이 겹치는 경우
- 실패했을 때 다음 Agent로 넘어가는 기준이 없는 경우
- Handoff Context에 이전 결과나 retry count가 없는 경우
- 복구 실행과 복구 검증을 같은 Agent가 모두 처리하는 경우
- 위험한 작업을 막는 Guardrail 기준이 없는 경우
