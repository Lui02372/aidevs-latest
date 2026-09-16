# 멀티 에이전트 아키텍처 설계서 샘플

## 1. 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 프로젝트명 | Auto Healing Workflow Service |
| 목표 | 장애 이벤트를 분석하고 Agent 협업으로 복구 전략을 선택한다. |
| 핵심 기능 | 장애 접수, 유형 분류, 복구 전략 선택, 실행 결과 검증, 운영 로그 기록 |

## 2. 아키텍처 선택 근거

이 프로젝트는 중앙 제어형 멀티 에이전트 구조를 사용합니다. 장애 대응 과정에서는 실행 순서와 책임이 명확해야 하므로, Supervisor Agent가 전체 흐름을 제어하고 각 전문 Agent에게 작업을 전달하는 방식이 적합합니다.

선택 근거:

- 응답 속도: Supervisor가 필요한 Agent만 호출해 불필요한 반복을 줄입니다.
- 결정 일관성: 장애 분류와 복구 전략 선택 기준을 중앙 상태로 관리합니다.
- 장애 격리: Diagnosis, Recovery, Validation 역할을 분리해 특정 단계 실패를 추적하기 쉽습니다.

## 3. Agent 역할 정의

| Agent | 책임 | 입력 | 출력 |
| --- | --- | --- | --- |
| Supervisor Agent | 전체 실행 순서 결정 | 장애 이벤트 | 다음 Agent와 실행 계획 |
| Diagnosis Agent | 장애 유형 분류 | 장애 메시지, 서비스명 | failure_type, severity |
| Recovery Agent | 복구 전략 선택 | failure_type, retry_count | recovery_strategy |
| Executor Agent | 복구 실행 또는 시뮬레이션 | recovery_strategy | execution_result |
| Validation Agent | Health Check 검증 | execution_result | validation_result |
| Reporter Agent | 결과 요약 | 전체 상태 | 보고 메시지 |
| Guardrail Agent | 위험 작업 차단 | 요청 작업, tool 목록 | 허용/차단 판단 |

## 4. Handoff Context

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

## 5. 실행 흐름

```text
사용자 장애 이벤트 입력
-> Supervisor Agent
-> Diagnosis Agent
-> Guardrail Agent
-> Recovery Agent
-> Executor Agent
-> Validation Agent
-> Reporter Agent
-> Monitor 기록
```

## 6. 예외 흐름

| 상황 | 처리 방식 |
| --- | --- |
| 장애 유형을 분류하지 못함 | unknown_failure로 표시하고 수동 확인 요청 |
| retry_count 초과 | fallback 전략으로 전환 |
| 위험 작업 요청 | Guardrail Agent가 차단 |
| Health Check 실패 | Recovery Agent로 다시 전달 |

## 7. 상태 필드

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| incident_id | string | 장애 이벤트 식별자 |
| service_name | string | 장애가 발생한 서비스 |
| failure_type | string | 장애 유형 |
| severity | string | 심각도 |
| retry_count | int | 현재 재시도 횟수 |
| recovery_strategy | string | 선택된 복구 전략 |
| validation_result | string | 검증 결과 |
| final_status | string | 최종 상태 |
