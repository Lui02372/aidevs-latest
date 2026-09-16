# 04. Deployment And Recovery Guide

08 프로젝트는 로컬 실행만으로 끝내지 않고, 배포 가능한 서비스 구조를 검증해야 합니다.

## Docker Compose 필수 서비스

| 서비스 | 역할 |
| --- | --- |
| backend | FastAPI API 서버 |
| worker | 장애 분석과 복구 실행 담당 |
| frontend | 사용자 입력 화면 |
| monitor | 운영 상태와 복구 결과 확인 화면 |

## 로컬 검증 명령

```powershell
cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
docker compose -f .\docker\docker-compose.yml config
docker compose -f .\docker\docker-compose.yml up --build
```

## AWS 배포 보고 기준

보고서에는 실제 배포 결과를 아래 기준으로 정리합니다.

| 항목 | 작성 내용 |
| --- | --- |
| 배포 대상 | App Runner, ECS 등 선택한 서비스 |
| 이미지 저장소 | ECR repository 이름 |
| 환경변수 | 민감정보를 제외한 변수 목록 |
| Health Check | `/health` 호출 결과 |
| 로그 확인 | CloudWatch Logs 확인 결과 |
| 장애 복구 확인 | 장애 이벤트 입력 후 복구 흐름 결과 |
| 비용 정리 | 실습 후 삭제한 리소스 목록 |

## 리소스 정리 체크

- App Runner service 또는 ECS service 삭제
- Load Balancer 삭제
- ECR image 정리
- CloudWatch Log Group 정리
- 불필요한 IAM access key 사용 중지

AWS는 비용이 발생할 수 있으므로, 배포 실습 후 삭제 결과까지 제출 자료에 남깁니다.
