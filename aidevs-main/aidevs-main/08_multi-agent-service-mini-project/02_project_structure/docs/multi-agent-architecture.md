# Multi-Agent Architecture

이 문서에는 팀 프로젝트의 Agent 역할, 책임, Handoff Context, 예외 흐름을 작성합니다.

## Agent 역할

| Agent | 책임 | 입력 | 출력 |
| --- | --- | --- | --- |
| Supervisor |  |  |  |
| Diagnosis |  |  |  |
| Recovery |  |  |  |
| Validation |  |  |  |
| Reporter |  |  |  |

## Handoff Context

```json
{
  "incident_id": "",
  "service_name": "",
  "failure_type": "",
  "retry_count": 0,
  "selected_strategy": ""
}
```
