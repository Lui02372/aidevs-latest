# 02_project_structure

이 폴더는 08 최종 미니 프로젝트의 기본 구조입니다. 학생들은 이 구조를 기반으로 Auto Healing 워크플로우를 구현합니다.

## 구조

```text
02_project_structure
├─ backend
│  ├─ app
│  │  ├─ main.py
│  │  ├─ agents
│  │  ├─ core
│  │  ├─ recovery
│  │  ├─ routers
│  │  ├─ schemas
│  │  └─ services
│  └─ tests
├─ frontend
├─ worker
├─ monitor
├─ docker
├─ .github
│  └─ workflows
└─ docs
```

## 실행 준비

```powershell
cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
Copy-Item .env.example .env
```

## 로컬 실행

```powershell
docker compose -f .\docker\docker-compose.yml config
docker compose -f .\docker\docker-compose.yml up --build
```

확인 주소:

```text
Backend health : http://127.0.0.1:8000/health
Frontend       : http://127.0.0.1:8801
Monitor        : http://127.0.0.1:8802
```

## 테스트

```powershell
cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
pytest backend\tests
```

## 구현 시 주의

- 처음에는 장애 유형 2개, 복구 전략 2개 정도로 작게 시작합니다.
- Agent 역할을 코드와 문서에서 같은 이름으로 유지합니다.
- 복구 실행이 위험한 명령이 되지 않도록 먼저 시뮬레이션으로 구현합니다.
- AWS 배포 전에는 로컬 Docker Compose와 GitHub Actions 검증을 먼저 통과시킵니다.
