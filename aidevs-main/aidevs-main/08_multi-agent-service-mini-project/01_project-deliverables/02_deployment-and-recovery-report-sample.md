# 배포 및 장애 복구 보고서 샘플

## 1. 배포 구조

| 서비스 | 역할 | 포트 |
| --- | --- | --- |
| backend | FastAPI API 서버 | 8000 |
| worker | 장애 분석과 복구 처리 | 내부 실행 |
| frontend | 장애 이벤트 입력 화면 | 8801 |
| monitor | 운영 상태 대시보드 | 8802 |

## 2. Docker Compose 검증 결과

```text
실행 명령:
docker compose -f .\docker\docker-compose.yml config
docker compose -f .\docker\docker-compose.yml up --build

검증 결과:
- backend /health 응답 성공
- frontend 접속 성공
- monitor 접속 성공
- worker 로그 확인 성공
```

## 3. 장애 유형별 감지 기준

| 장애 유형 | 감지 기준 | 복구 전략 |
| --- | --- | --- |
| 네트워크 timeout | 응답 시간이 기준 초과 | retry with backoff |
| API 5xx | status code 500 이상 | fallback response |
| Rate Limit | status code 429 | 대기 후 재시도 |
| LLM 응답 오류 | 빈 응답 또는 형식 불일치 | 재요청 또는 모델 변경 |
| Prompt Injection | 금지 키워드 또는 tool override 시도 | 요청 차단 |

## 4. 복구 시나리오 결과

| 시나리오 | 입력 | 선택 전략 | 결과 |
| --- | --- | --- | --- |
| backend timeout | `backend timeout occurred` | retry_with_backoff | success |
| API 5xx | `external api returned 500` | fallback_response | success |
| prompt injection | `ignore previous instruction` | block_request | blocked |

## 5. AWS 배포 결과

| 항목 | 결과 |
| --- | --- |
| 배포 서비스 | App Runner 또는 ECS |
| 배포 URL | `https://example.aws.service` |
| Health Check | `/health` 정상 |
| 로그 확인 | CloudWatch Logs에서 backend 로그 확인 |
| 환경변수 | AWS Secret 또는 서비스 환경변수로 관리 |

## 6. 리소스 정리 결과

- [ ] App Runner 또는 ECS 서비스 삭제
- [ ] ECR 이미지 정리
- [ ] CloudWatch Log Group 확인
- [ ] 사용하지 않는 Access Key 비활성화

## 7. 개선 사항

- 장애 유형별 복구 성공률을 수치로 기록합니다.
- retry 횟수와 fallback 기준을 환경변수로 분리합니다.
- 실제 운영에서는 알림 채널과 담당자 에스컬레이션 정책을 연결합니다.
