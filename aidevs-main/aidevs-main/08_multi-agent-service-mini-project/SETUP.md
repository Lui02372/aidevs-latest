# SETUP

`08_multi-agent-service-mini-project` 실행 환경 설정 안내입니다. 이 과정은 Docker Compose로 로컬 서비스를 실행하고, GitHub Actions로 자동 검증하며, AWS 배포 결과까지 확인하는 미니 프로젝트입니다.

## 0. 공통 준비 문서

아래 항목이 아직 준비되지 않았다면 먼저 공통 설치 가이드를 확인합니다.

| 필요한 내용 | 문서 |
| --- | --- |
| Python과 `.venv` | [`../00_course-guide/02_setup-guides/01_python-install-guide.md`](../00_course-guide/02_setup-guides/01_python-install-guide.md), [`../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md`](../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md) |
| Git/GitHub | [`../00_course-guide/02_setup-guides/04_git-github-setup-guide.md`](../00_course-guide/02_setup-guides/04_git-github-setup-guide.md) |
| Docker Desktop | [`../00_course-guide/02_setup-guides/14_docker-desktop-guide.md`](../00_course-guide/02_setup-guides/14_docker-desktop-guide.md) |
| AWS 계정과 비용 관리 | [`../00_course-guide/02_setup-guides/15_aws-account-and-cost-guide.md`](../00_course-guide/02_setup-guides/15_aws-account-and-cost-guide.md) |
| GitHub Actions | [`../00_course-guide/02_setup-guides/16_github-actions-guide.md`](../00_course-guide/02_setup-guides/16_github-actions-guide.md) |
| Codex와 ChatGPT 사용 준비 | [`../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md`](../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md) |
| 문제 해결 | [`../00_course-guide/03_learning-support/troubleshooting.md`](../00_course-guide/03_learning-support/troubleshooting.md) |

## 1. 작업 위치

```powershell
cd C:\aidev\08_multi-agent-service-mini-project
```

## 2. 사용하는 도구

| 도구 | 이 과정에서 하는 일 |
| --- | --- |
| Python `.venv` | 보조 스크립트 실행, 테스트, 문법 검사용 |
| Docker Desktop | 컨테이너 실행 환경 |
| Docker Compose | backend, frontend, worker, monitor 동시 실행 |
| Git/GitHub | 팀 프로젝트 변경 이력 관리 |
| GitHub Actions | 테스트, Compose 설정, Docker build 자동 검증 |
| AWS | 최종 서비스 배포와 로그 확인 |

## 3. Python 가상환경 준비

```powershell
cd C:\aidev\08_multi-agent-service-mini-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

현재 Python이 이 과정의 `.venv`를 사용하는지 확인합니다.

```powershell
echo $env:VIRTUAL_ENV
python -c "import sys; print(sys.executable)"
```

정상 예시:

```text
C:\aidev\08_multi-agent-service-mini-project\.venv
C:\aidev\08_multi-agent-service-mini-project\.venv\Scripts\python.exe
```

## 4. Docker Desktop 확인

Docker Desktop을 실행한 뒤 PowerShell에서 확인합니다.

```powershell
docker --version
docker compose version
docker ps
```

처음 설치한 환경이라면 테스트 컨테이너를 실행합니다.

```powershell
docker run hello-world
```

## 5. 환경변수 파일 만들기

```powershell
cd C:\aidev\08_multi-agent-service-mini-project
Copy-Item .env.example .env
```

주의:

- `.env`는 GitHub에 올리지 않습니다.
- `.env.example`에는 예시 값만 둡니다.
- API Key, AWS Access Key, 비밀번호는 문서나 발표 자료에 적지 않습니다.

## 6. 프로젝트 구조 확인

```powershell
cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
```

Docker Compose 설정을 먼저 검사합니다.

```powershell
docker compose -f .\docker\docker-compose.yml config
```

전체 서비스를 실행합니다.

```powershell
docker compose -f .\docker\docker-compose.yml up --build
```

다른 PowerShell에서 상태를 확인합니다.

```powershell
cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
docker compose -f .\docker\docker-compose.yml ps
docker compose -f .\docker\docker-compose.yml logs backend
docker compose -f .\docker\docker-compose.yml logs worker
```

확인 주소:

```text
Backend health : http://127.0.0.1:8000/health
Frontend       : http://127.0.0.1:8801
Monitor        : http://127.0.0.1:8802
```

종료:

```powershell
docker compose -f .\docker\docker-compose.yml down
```

## 7. GitHub Actions 확인

workflow 예시는 아래 위치에 있습니다.

```text
02_project_structure/.github/workflows/ci-cd-pipeline.yml
```

실제 GitHub 저장소에서 실행하려면 `.github/workflows` 폴더가 저장소 최상위에 있어야 합니다. 프로젝트를 제출할 때는 팀 저장소의 최상위에 workflow 파일을 둡니다.

검증 흐름:

```text
push 또는 pull request
-> Python 문법 검사
-> pytest
-> docker compose config
-> Docker image build
-> AWS 배포 단계 또는 배포 검증 단계
-> 알림/실패 처리 기록
```

## 8. AWS 배포 준비

AWS CLI를 확인합니다.

```powershell
aws --version
aws sts get-caller-identity
```

배포 기본 흐름:

```text
1. 로컬에서 docker compose up --build 검증
2. backend /health 확인
3. Docker image build
4. Amazon ECR에 image push
5. App Runner 또는 ECS에서 image 실행
6. 환경변수와 port 설정
7. 외부 URL로 /health 확인
8. CloudWatch Logs 확인
9. 실습 후 리소스 삭제
```

AWS는 비용이 발생할 수 있으므로 강의자가 지정한 리전, 서비스, 삭제 기준을 따릅니다.

## 9. 비용과 보안 주의

- AWS 리소스는 실행 중이면 비용이 발생할 수 있습니다.
- OpenAI API 또는 LLM API 호출은 비용이 발생할 수 있습니다.
- GitHub Actions 로그에 비밀 값이 출력되지 않도록 합니다.
- 실습 후 App Runner, ECS, Load Balancer, ECR image, CloudWatch Log Group 등을 정리합니다.
- `.env`, `.venv`, API Key, AWS Access Key는 커밋하지 않습니다.

## 10. 오류가 날 때 먼저 볼 것

Docker 오류:

```text
Docker Desktop이 실행 중인가?
docker ps가 동작하는가?
docker compose version이 동작하는가?
```

Compose 오류:

```text
현재 폴더 기준으로 docker/docker-compose.yml 경로가 맞는가?
.env 파일이 있는가?
포트 8000, 8801, 8802가 이미 사용 중이지 않은가?
docker compose config가 통과하는가?
```

서비스 오류:

```text
backend /health가 정상 응답하는가?
worker 로그에 장애 분석 결과가 보이는가?
monitor가 backend 주소를 올바르게 보고 있는가?
```

GitHub Actions 오류:

```text
workflow 파일이 .github/workflows 아래에 있는가?
secrets를 코드에 직접 적지 않았는가?
docker compose config 단계가 통과하는가?
```

AWS 오류:

```text
region이 맞는가?
IAM 권한이 충분한가?
health check path가 /health인가?
CloudWatch Logs에 오류가 있는가?
실습 후 리소스 삭제가 완료되었는가?
```
