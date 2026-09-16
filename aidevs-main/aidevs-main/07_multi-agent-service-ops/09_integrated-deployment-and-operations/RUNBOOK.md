# 장애 대응 Runbook

## 1. 최초 확인

1. 배포 Version, 발생 시각, 영향받은 사용자 범위를 기록합니다.
2. `/health/live`와 `/health/ready`를 각각 확인합니다.
3. Redis Queue 깊이와 Worker 상태를 확인합니다.
4. 같은 `trace_id`의 API·Worker·Agent Log를 모읍니다.

## 2. 증상별 조치

| 증상 | 먼저 확인 | 우선 조치 |
| --- | --- | --- |
| API 응답 없음 | Liveness, Container 종료 코드 | 재시작 후 원인 Log 보존 |
| Readiness 실패 | Redis·PostgreSQL 연결 | 트래픽 제외, 의존성 복구 |
| Queue 지속 증가 | Worker 수와 처리 시간 | Worker 확장, Poison Task 격리 |
| 특정 LLM 오류 증가 | Provider·Model·HTTP 상태 | 제한 재시도, Circuit Breaker, Fallback |
| 배포 직후 오류 증가 | Version별 오류율 | 이전 Image로 Rollback |

## 3. 복구 완료 기준

- Readiness가 연속으로 정상입니다.
- Queue가 지속적으로 감소합니다.
- 오류율과 P95 Latency가 기준 이내입니다.
- 실패 Task가 성공으로 위장되지 않고 이력에 남아 있습니다.
- 임시 조치, 원인, 재발 방지 항목을 운영 기록에 남겼습니다.
