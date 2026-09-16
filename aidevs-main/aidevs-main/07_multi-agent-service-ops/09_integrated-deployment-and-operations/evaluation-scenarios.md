# 최종 Scenario Evaluation

각 Scenario는 최종 문장뿐 아니라 Redis 상태와 PostgreSQL Trace를 함께 확인합니다.

| ID | 입력·조건 | 기대 상태 | 반드시 확인할 Trace |
| --- | --- | --- | --- |
| T01 | 부산 2박 3일·60만원·알레르기·대중교통 | `waiting_approval` | MCP 호출, 전문 Agent 3개, Handoff 3개, 평가 통과 |
| T02 | T01 승인 | `completed` | 같은 사용자 `approve` 이벤트 |
| T03 | T01 거절 | `rejected` | 실제 예약·결제·저장 없음 |
| T04 | 같은 사용자·같은 idempotency key로 재접수 | 기존 Task 반환 | Queue 중복 없음 |
| T05 | MCP Server 중지 | `failed` | `mcp:get_weather` 이후 연결 오류 |
| T06 | 잘못된 Provider Key | `failed` | 실패한 Agent와 Provider 오류 |
| T07 | Weather Agent가 `save_itinerary` 요청 | `blocked` | allowlist 차단, Tool 실행 없음 |
| T08 | 다른 사용자로 Task 조회·승인 | HTTP `403` | Task 상태 불변 |
| T09 | 알레르기 조건이 최종 결과에서 사라짐 | `failed` | `food_restriction_kept=false` |
| T10 | MCP가 8일 예보 요청 | `failed` | Tool 입력 범위 오류 |

## 회귀 확인 순서

1. T01을 실제 Provider 조합별로 최소 3회 실행합니다.
2. Scenario의 개별 check 통과율을 기록합니다.
3. Prompt·모델·Orchestration을 변경한 뒤 같은 입력을 다시 실행합니다.
4. 평균 문장 점수보다 안전 조건이나 Tool 권한 회귀를 먼저 차단합니다.
5. 실패한 `trace_id`에서 최초 실패 Agent와 직전 Handoff를 찾습니다.

실제 외부 API는 네트워크와 예보 시점에 따라 결과가 달라질 수 있습니다. 따라서 날씨 값 자체를 고정해 비교하지 않고, 출처·계약·필수 필드·오류 처리 경로를 평가합니다.
