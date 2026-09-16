# 03 Simple AWS Deployment

로컬에서 검증한 Docker Compose Application을 AWS EC2 한 대에서 실행하는 공통 절차를
배웁니다. AWS 서비스를 많이 배우는 단계가 아니라 **같은 Container 구성이 다른 컴퓨터에서도
실행되는지** 확인하고, 이후 GitHub Actions 자동 배포에 필요한 서버 기반을 준비하는 단계입니다.

```text
EC2 한 대(Ubuntu 24.04 LTS 권장)
├─ Streamlit Frontend
├─ FastAPI Backend → 선택한 실제 LLM API
├─ Redis
└─ PostgreSQL + Docker Volume
```

사용하는 AWS 리소스는 EC2, Root EBS, Security Group, Key Pair뿐입니다. ECS, ECR,
RDS, ElastiCache, Load Balancer는 사용하지 않습니다. 이 폴더는 수동 실행 원리를 설명하고,
05·06 프로젝트 README가 같은 EC2를 이용한 GitHub Actions 자동 배포를 이어서 설명합니다.

이 EC2 실습은 Container와 Network를 직접 확인하기 위한 초보자용 첫 단계입니다. 완료 후
09에서는 같은 책임을 ECR·ECS·RDS·ElastiCache·CloudWatch에 대응시키며, EC2 Compose를
유일한 운영 정답으로 설명하지 않습니다.

초보자 기본 배포는 OpenAI 또는 Gemini를 사용합니다. Ollama Profile은 Model Disk와 Memory가 추가로 필요하므로 EC2 Instance 사양과 비용을 별도로 검토하는 선택 실습입니다. 작은 실습 Instance에서 Ollama를 기본으로 실행하지 않습니다.

Backend·Redis·PostgreSQL 포트는 인터넷에 공개하지 않습니다. Browser는 8501의
Frontend만 접근합니다. LLM API Key는 EC2의 `.env`에만 저장하며 Git에 올리지 않습니다.

EC2는 새 서버이므로 로컬 수업 PC처럼 공용 PostgreSQL·Redis·Ollama Container가 이미
실행되어 있지 않습니다. 따라서 이 단원에서는 `compose.yml`이 아니라
`compose.full-stack.yml`로 Frontend·Backend·Redis·PostgreSQL을 함께 실행합니다.
Ollama는 기본 실행에서 제외하고 OpenAI 또는 Gemini API를 사용합니다.

## 진행 순서

1. [아키텍처와 비용 범위](./01_architecture-and-cost.md)
2. [EC2 생성과 보안 그룹](./02_create-ec2.md)
3. [Docker 설치와 코드 전송](./03_install-and-transfer.md)
4. [배포와 Health 확인](./04_deploy-and-verify.md)
5. [장애 실습](./05_failure-lab.md)
6. [리소스 정리](./06_cleanup.md)

이 폴더의 명령은 `01_simple-multi-llm-compose`를 기준으로 설명하는 공통 EC2 입문
절차입니다. 프로젝트별 실행 방식은 다음처럼 구분합니다.

| 대상 | 이 문서에서 사용하는 내용 | 프로젝트 README에서 이어갈 내용 |
| --- | --- | --- |
| `01_simple-multi-llm-compose` | EC2 생성부터 수동 Compose 실행까지 전체 | 없음 |
| `05_weather-mcp-deployment-project` | VPC·EC2·보안 그룹·SSH·Docker | 05 README의 환경 파일·CI/CD 자동 배포 |
| `06_weather-mcp-stateful-deployment` | 05에서 만든 EC2를 그대로 재사용 | 06 README의 Workflow 전환·상태 보존 배포 |

05·06에서는 Ubuntu Server 24.04 LTS, `t3.small`, `16 GiB gp3`를 기본값으로 사용합니다.
05를 완료한 뒤 EC2를 삭제하지 않고 Application만 중지하여 06에서 재사용합니다.

## 수업 전 체크

```text
[ ] 로컬 Compose 네 서비스가 정상이다.
[ ] AWS 계정·Region·예산 정책을 확인했다.
[ ] SSH Key를 Git 밖에 보관한다.
[ ] LLM API Key를 소스에 넣지 않았다.
[ ] 종료 전에 EC2·EBS·Security Group 정리 시간을 확보했다.
```

