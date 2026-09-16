# 03. Auto Healing Scenario Guide

Auto Healing은 장애를 자동으로 “마법처럼 해결”하는 기능이 아닙니다. 장애를 감지하고, 가능한 복구 전략을 선택하고, 결과를 검증하는 운영 흐름입니다.

## 기본 흐름

```text
장애 감지
-> 장애 유형 분류
-> 복구 전략 선택
-> 복구 실행 또는 시뮬레이션
-> Health Check
-> 성공/실패 기록
-> 실패 시 재시도 또는 fallback
```

## 장애 유형별 감지 기준

| 장애 유형 | 감지 기준 예시 | 복구 전략 예시 |
| --- | --- | --- |
| 네트워크 | timeout, connection refused | retry, backoff, fallback URL |
| DB | connection error, slow query | reconnect, pool size 점검, 쿼리 단순화 |
| API | 5xx, 429 rate limit | retry, 대체 API, 캐시 응답 |
| LLM | token limit, empty answer | prompt 축소, 모델 변경, 재요청 |
| Prompt 보안 | injection keyword, tool override 시도 | 입력 차단, tool 권한 제한, 관리자 검토 |

## 복구 결과에 남길 정보

```json
{
  "incident_id": "inc-001",
  "detected_failure": "api_timeout",
  "selected_strategy": "retry_with_backoff",
  "retry_count": 1,
  "recovery_status": "success",
  "validation_result": "health_check_passed",
  "next_action": "monitor for 10 minutes"
}
```

## 보고서에 포함할 내용

- 장애 유형별 감지 기준
- 복구 전략과 선택 이유
- 자동 복구가 성공한 시나리오
- 자동 복구가 실패한 시나리오
- 수동 개입이 필요한 기준
- 복구 성공률 또는 시나리오별 결과
