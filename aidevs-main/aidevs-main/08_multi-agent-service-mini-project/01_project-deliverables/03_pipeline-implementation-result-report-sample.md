# 파이프라인 구현 결과 보고서 샘플

## 1. 파이프라인 개요

```text
code commit
-> GitHub Actions
-> install dependencies
-> pytest
-> docker compose config
-> docker build
-> AWS deploy or deployment verification
-> notification
```

## 2. GitHub Actions 단계

| 단계 | 입력 | 출력 | 실패 시 처리 |
| --- | --- | --- | --- |
| checkout | GitHub repository | source code | workflow 중단 |
| install | requirements.txt | installed packages | workflow 중단 |
| test | tests | test result | 배포 차단 |
| compose config | docker-compose.yml | config validation | 배포 차단 |
| docker build | Dockerfile | image build result | 배포 차단 |
| deploy | image, AWS config | service URL | 실패 로그 기록 |

## 3. 테스트 기준

| 테스트 | 기준 |
| --- | --- |
| 단위 테스트 | 장애 분류 함수, 복구 전략 선택 함수 |
| 통합 테스트 | `/health`, `/incidents`, `/recoveries` API |
| Compose 검증 | `docker compose config` 성공 |
| 배포 검증 | 외부 URL `/health` 성공 |

## 4. 알림 기준

| 이벤트 | 알림 대상 | 메시지 내용 |
| --- | --- | --- |
| pipeline success | 팀 채널 | commit id, 배포 URL |
| test failure | 개발 담당자 | 실패 테스트 이름 |
| deploy failure | 운영 담당자 | AWS 로그 위치 |
| repeated failure | 팀장 또는 강사 | 실패 횟수, 조치 필요 |

Slack, Teams, PagerDuty 중 하나를 실제로 연결하거나, 수업 상황에 따라 알림 구조를 보고서에 명확히 설계합니다.

## 5. 실행 결과

```text
GitHub Actions run:
- install: success
- test: success
- compose config: success
- docker build: success
- deploy verification: success
```

## 6. 실패 사례와 개선

| 실패 사례 | 원인 | 수정 |
| --- | --- | --- |
| 테스트 실패 | expected status code 불일치 | 테스트 데이터 수정 |
| Docker build 실패 | requirements 누락 | requirements.txt 보완 |
| AWS health check 실패 | port 설정 오류 | 서비스 포트 수정 |
