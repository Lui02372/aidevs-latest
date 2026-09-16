# 05. Pipeline And Notification Guide

파이프라인 구현 결과 보고서는 코드가 어떻게 검증되고 배포되는지 보여 주는 문서입니다.

## 기본 파이프라인

```text
code commit
-> GitHub Actions 실행
-> Python 문법 검사
-> pytest
-> docker compose config
-> Docker image build
-> AWS 배포 또는 배포 검증
-> 알림 전송 또는 알림 구조 기록
```

## GitHub Actions에 포함할 항목

| 단계 | 확인 내용 |
| --- | --- |
| checkout | 저장소 코드를 가져오는가 |
| setup-python | Python 버전을 고정했는가 |
| install | requirements.txt 설치가 되는가 |
| test | pytest가 실행되는가 |
| compose config | docker-compose.yml 문법이 맞는가 |
| docker build | 이미지 빌드가 성공하는가 |
| deploy | AWS 배포 또는 배포 검증 단계가 있는가 |

## 실패 시 처리 기준

- 테스트 실패 시 배포 단계로 넘어가지 않습니다.
- Docker build 실패 시 배포 단계로 넘어가지 않습니다.
- AWS 배포 실패 시 실패 원인과 로그 위치를 보고서에 기록합니다.
- 비밀 값이 로그에 출력되면 즉시 key를 폐기하고 재발급합니다.

## 알림과 에스컬레이션

Slack, Teams, PagerDuty 중 하나를 실제 연동하거나, 수업 상황에 따라 알림 구조를 보고서에 명확히 설계합니다.

보고서에 포함할 내용:

- 어떤 이벤트에서 알림을 보낼 것인가
- 성공/실패/지연을 어떻게 구분할 것인가
- 담당자에게 어떤 정보가 전달되는가
- 장애가 반복될 때 누구에게 에스컬레이션되는가
