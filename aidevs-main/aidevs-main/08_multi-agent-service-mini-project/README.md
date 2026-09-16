# 08_multi-agent-service-mini-project

`08_multi-agent-service-mini-project`는 `07_multi-agent-service-ops`에서 학습한 멀티 에이전트 협업, Docker 기반 서비스 운영, GitHub Actions, AWS 배포, 장애 복구 흐름을 하나의 미니 프로젝트로 정리하는 과정입니다.

이 과정의 주제는 **에러 자가 치유(Auto Healing) 워크플로우**입니다. 장애가 발생했을 때 여러 Agent가 역할을 나누어 원인을 분석하고, 복구 전략을 선택하고, 실행 결과를 검증하고, 배포 및 운영 결과를 문서화합니다.

## 프로젝트 목표

1. 에이전트 협업 시나리오 및 구조를 설계합니다.
2. 장애 유형별 복구 로직과 자동화 파이프라인을 구현합니다.
3. Health Check, Retry, Fallback 기반 장애 대응 흐름을 구현합니다.
4. Docker Compose, GitHub Actions, AWS 배포 결과를 검증합니다.

## 최종 흐름

```text
장애 이벤트 발생
-> Supervisor Agent가 요청 접수
-> Diagnosis Agent가 장애 유형 분류
-> Recovery Agent가 복구 전략 선택
-> Executor/Worker가 복구 실행 또는 시뮬레이션
-> Validation Agent가 Health Check 재검증
-> Reporter Agent가 결과 요약
-> Monitor 대시보드와 보고서에 결과 기록
-> GitHub Actions/AWS 배포 결과 검증
```

## 과정 구조

```text
08_multi-agent-service-mini-project
├─ .vscode
├─ 00_references
├─ 01_project-deliverables
├─ 02_project_structure
├─ .env.example
├─ .gitignore
├─ README.md
├─ requirements.txt
└─ SETUP.md
```

## 폴더별 역할

| 폴더 | 역할 |
| --- | --- |
| `00_references` | Auto Healing 프로젝트 개념, 아키텍처, 배포, 파이프라인, 평가 기준 참고 문서 |
| `01_project-deliverables` | 필수 산출물 3종 샘플 |
| `02_project_structure` | 학생들이 구현할 최종 프로젝트 기본 구조 |

## 필수 산출물

| 산출물 | 샘플 문서 | 핵심 확인 기준 |
| --- | --- | --- |
| 멀티 에이전트 아키텍처 설계서 | `01_project-deliverables/01_multi-agent-architecture-design-sample.md` | Agent 역할, 책임, Handoff, Context 전달 구조가 명확한가 |
| 배포 및 장애 복구 보고서 | `01_project-deliverables/02_deployment-and-recovery-report-sample.md` | 장애 유형, 감지 기준, 복구 전략, 검증 결과가 정리되었는가 |
| 파이프라인 구현 결과 보고서 | `01_project-deliverables/03_pipeline-implementation-result-report-sample.md` | commit, build, test, deploy, notification, 실패 처리 흐름이 문서화되었는가 |

## 필수 구현 범위

```text
backend  : 장애 이벤트 접수 API, Health Check API, 복구 결과 조회 API
worker   : 장애 유형 분류, 복구 전략 선택, 재시도/대체 경로 처리
frontend : 장애 이벤트 입력과 결과 확인 화면
monitor  : 운영 이벤트, 복구 결과, 파이프라인 상태 표시
docker   : Dockerfile, docker-compose.yml
ci/cd    : GitHub Actions 기반 테스트와 빌드 검증
deploy   : AWS 배포 결과 검증과 비용/리소스 정리 기준
```

## 권장 Agent 역할

| Agent | 역할 |
| --- | --- |
| Supervisor Agent | 장애 요청을 접수하고 담당 Agent와 실행 순서를 결정합니다. |
| Diagnosis Agent | 장애 원인과 유형을 분석합니다. |
| Recovery Agent | Retry, Restart, Reconnect, Fallback 등 복구 전략을 선택합니다. |
| Executor Agent | 선택된 복구 전략을 실행하거나 시뮬레이션합니다. |
| Validation Agent | 복구 후 Health Check와 결과를 검증합니다. |
| Reporter Agent | 실행 결과, 실패 원인, 다음 조치를 요약합니다. |
| Guardrail Agent | 위험한 명령, 민감 정보, 정책 위반 가능성을 점검합니다. |

## 진행 순서

1. [SETUP.md](./SETUP.md)를 보고 Python, Docker, GitHub Actions, AWS 준비 상태를 확인합니다.
2. [00_references](./00_references/README.md)에서 프로젝트 기준과 참고 문서를 확인합니다.
3. [01_project-deliverables](./01_project-deliverables/README.md)에서 제출 산출물 샘플을 확인합니다.
4. [02_project_structure](./02_project_structure/README.md)를 기반으로 팀 프로젝트를 구현합니다.
5. Docker Compose로 전체 서비스를 실행하고 `/health`를 확인합니다.
6. GitHub Actions로 테스트와 이미지 빌드 검증을 수행합니다.
7. AWS에 배포하고 외부 URL, 로그, 리소스 정리 결과를 보고서에 남깁니다.

## 빠른 시작

```powershell
cd C:\aidev\08_multi-agent-service-mini-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import sys; print(sys.executable)"
Copy-Item .env.example .env
```

프로젝트 구조 확인:

```powershell
cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
docker compose -f .\docker\docker-compose.yml config
```

서비스 실행:

```powershell
docker compose -f .\docker\docker-compose.yml up --build
```

확인 주소:

```text
Backend health : http://127.0.0.1:8000/health
Frontend       : http://127.0.0.1:8801
Monitor        : http://127.0.0.1:8802
```

## 주의 사항

- `.env`는 GitHub에 올리지 않습니다.
- AWS Access Key, API Key, 비밀번호는 README나 발표 자료에 적지 않습니다.
- AWS 실습은 비용이 발생할 수 있으므로 배포 전 범위와 삭제 계획을 확인합니다.
- GitHub Actions 로그에 비밀 값이 출력되지 않도록 합니다.
- 실습 종료 후 AWS 리소스와 Docker 컨테이너를 정리합니다.
