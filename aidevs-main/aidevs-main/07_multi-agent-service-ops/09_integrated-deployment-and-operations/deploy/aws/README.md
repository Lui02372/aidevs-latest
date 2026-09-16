# AWS 배포 설계

교육 실습의 권장 대응 관계입니다.

| Local | AWS |
| --- | --- |
| Docker Image | ECR Image |
| API Container | ECS Fargate Service + ALB |
| Worker Container | ECS Fargate Service (외부 Port 없음) |
| Frontend Container | ECS Fargate Service 또는 별도 정적 Hosting |
| PostgreSQL | RDS PostgreSQL |
| Redis | ElastiCache for Redis |
| `.env` 비밀값 | Secrets Manager |
| 구조화 Log | CloudWatch Logs |
| Health Check | ALB Target Health + ECS Container Health |

`ecs-task-definition.example.json`은 복사 가능한 학습용 골격입니다. Account ID, Region,
Repository URI, Secret ARN을 실제 값으로 바꾼 뒤 사용합니다. 실습에서는 먼저 API 하나를
배포하고 Readiness를 확인한 다음 Worker를 별도 Service로 배포합니다.

운영에서는 RDS와 ElastiCache를 Public Subnet에 노출하지 않고 Private Subnet에 둡니다.
Security Group은 API/Worker Task에서 오는 연결만 허용합니다.
