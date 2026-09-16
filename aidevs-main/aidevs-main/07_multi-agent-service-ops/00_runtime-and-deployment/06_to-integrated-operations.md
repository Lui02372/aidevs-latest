# 00 Runtime에서 09 통합 배포·운영으로

이 문서는 수업 시작 전에 준비한 Local Runtime이 `09_integrated-deployment-and-operations`에서
어떻게 운영형 구조로 확장되는지 연결합니다.

## 00과 09의 역할 차이

| 구분 | 00 Runtime | 09 Integrated Operations |
| --- | --- | --- |
| 목적 | 실행 환경과 Container 연결 이해 | 실제 Multi-Agent Service 배포·복구 |
| 업무 | 짧은 Multi-LLM Chat | 평가·수정이 포함된 긴 Workflow |
| 실행 주체 | FastAPI가 직접 호출 | Queue Worker가 전체 Workflow 호출 |
| 상태 | Redis Session | Redis Queue·진행률·Trace |
| 이력 | PostgreSQL Chat·메모 | PostgreSQL 실행·평가 회차 |
| 배포 | 단일 PC Compose | Compose 이후 AWS 확장 |

00의 작은 서비스에는 Queue Worker가 없어도 됩니다. Browser, Backend, Redis,
PostgreSQL, 실제 LLM의 연결을 먼저 이해하는 것이 목적입니다. 08~09에서는 실행 시간이
길고 동시 요청을 분리해야 하므로 Worker를 도입합니다.

## Worker가 추가되는 이유

```text
Worker 없음
사용자 → FastAPI → 전체 Workflow 실행 → 완료 후 응답

Worker 사용
사용자 → FastAPI → Redis Queue에 run_id 등록 → 접수 응답
                              ↓
                         Queue Worker
                              ↓
                    미리 구현된 전체 Workflow
```

요청마다 새로운 OS Thread나 Container가 반드시 생성되는 것은 아닙니다. 실행 중인
Worker가 Queue에서 작업을 가져옵니다. Queue가 계속 증가하면 Worker Container 수를
늘릴 수 있습니다.

```powershell
# Local Docker Compose 수동 확장
docker compose up -d --scale worker=3
```

Docker Compose는 수동으로 확장합니다. AWS ECS에서는 CloudWatch Metric과 Service Auto
Scaling을 연결해 Worker Task 수를 자동으로 조절할 수 있습니다.

## Health Check를 구분하기

| 검사 | 질문 | 실패 시 기본 조치 |
| --- | --- | --- |
| Liveness | Process가 살아 있는가? | Container 재시작 검토 |
| Readiness | 의존성을 포함해 요청을 받을 수 있는가? | 트래픽에서 제외 |
| Provider Status | 실제 LLM을 호출할 준비가 됐는가? | 설정 확인·Fallback 검토 |

PostgreSQL 중단으로 Readiness가 실패했다면 API Container를 반복 재시작해도 해결되지
않습니다. 먼저 실패한 의존성을 확인합니다.

## 배포 단계

```text
1. Local Python 실행
2. Docker Image Build
3. Docker Compose 통합 실행
4. 구문·Test·보안·평가 Release Gate
5. Registry에 Version Image Push
6. AWS에 새 Version 배포
7. Readiness와 운영 지표 확인
8. 승격 또는 이전 Image로 Rollback
```

## Local과 AWS 대응 관계

| Local | AWS 운영형 선택 |
| --- | --- |
| Docker Image | ECR |
| API Container | ECS Service + ALB |
| Worker Container | 별도 ECS Service |
| PostgreSQL Container | RDS PostgreSQL |
| Redis Container | ElastiCache for Redis |
| `.env` | Secrets Manager |
| Console JSON Log | CloudWatch Logs |
| `docker compose ps` | ECS Service·Task 상태 |

초보 과정의 첫 AWS 실습은 EC2 한 대에 Compose를 실행하여 구조를 눈으로 확인할 수
있습니다. 운영형 설계에서는 저장소를 Private Network의 관리형 서비스로 분리합니다.

## 배포 전 체크

```text
[ ] API Key와 Database 비밀번호가 Image·Git·Log에 없다.
[ ] API와 Worker가 같은 Image라도 서로 다른 Process로 실행된다.
[ ] Redis·PostgreSQL 주소가 실행 환경에 맞다.
[ ] Liveness와 Readiness가 분리되어 있다.
[ ] 재시도 대상 오류와 최대 횟수가 정해져 있다.
[ ] 실패한 평가가 성공으로 바뀌지 않는다.
[ ] 배포 Version과 Commit을 Trace에서 확인할 수 있다.
[ ] Rollback할 이전 Image Tag가 남아 있다.
```

09의 실제 설정은 다음 폴더에서 확인합니다.

```text
09_integrated-deployment-and-operations/
├─ deploy/Dockerfile
├─ deploy/compose.yaml
├─ deploy/aws/
├─ deploy/github/
└─ RUNBOOK.md
```
