# GitHub Actions CI/CD 강의 — 05 Weather에서 06 Stateful까지

이 강의는 이 프로젝트의 실제 YAML과 Python 코드를 기준으로 작성했다. 먼저 05의 테스트·빌드·EC2 배포를 이해하고, 06에서 데이터 보존 배포로 확장한다. 흐름도는 [02 워크플로우 시각화](02_workflow-visualization.md)를 함께 읽는다.

기준일: 2026-09-21. 파일을 정적으로 확인했으며 GitHub 실행 결과나 EC2 배포 성공을 확인한 기록은 아니다. 아래 명령은 수강생 실습용이다.

## 1. 가장 먼저: 현재 저장소의 루트 찾기

현재 폴더 이름이 중첩되어 있다. Git 루트와 강의 프로젝트 루트를 혼동하면 Actions가 안 뜨거나 `working-directory` 오류가 난다.

```text
C:\수업 보관소\aidevs-latest\                    ← 실제 Git 루트
├─ .github/workflows/07-weather-mcp-cicd.yml    ← 05 실제 실행 대상
└─ aidevs-main/
   └─ aidevs-main/                            ← 강의 프로젝트 루트
      ├─ .githubactionguide/                  ← 이 강의 2개
      ├─ .github/workflows/
      │  ├─ 07-runtime-ci.yml
      │  └─ 07-weather-stateful-cicd.yml       ← 현재는 중첩 폴더의 예제
      └─ 07_multi-agent-service-ops/
         └─ 00_runtime-and-deployment/
            ├─ 02_github-actions-ci/
            ├─ 04_github-actions-aws-deploy/
            ├─ 05_weather-mcp-deployment-project/
            └─ 06_weather-mcp-stateful-deployment/
```

PowerShell에서 먼저 확인한다.

```powershell
Set-Location 'C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main'
git rev-parse --show-toplevel
git status --short
$repoRoot = (git rev-parse --show-toplevel).Trim()
$courseRoot = Join-Path $repoRoot 'aidevs-main/aidevs-main'
$runtimeRoot = Join-Path $courseRoot '07_multi-agent-service-ops/00_runtime-and-deployment'
$weather05 = Join-Path $runtimeRoot '05_weather-mcp-deployment-project'
$weather06 = Join-Path $runtimeRoot '06_weather-mcp-stateful-deployment'
```

GitHub가 읽는 위치는 **Git 저장소 루트의 `.github/workflows/*.yml` 또는 `*.yaml`**이다. `workflow`가 아니라 `workflows`다. 현재 05 파일은 루트로 이동된 작업 상태이며, GitHub에도 커밋·푸시되어야 인식된다. 강의 폴더 안의 `.github`는 현재 저장소 구조에서 자동 검색되지 않는다. [GitHub 공식 YAML 문법](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

다른 PC에서 강의 프로젝트 자체를 Git 루트로 사용한다면 `aidevs-main/aidevs-main/` 접두사를 제거해야 한다. 로컬 절대 경로를 Linux Runner의 YAML에 넣지 않는다.

## 2. CI, CD, GitHub Actions는 각각 무엇인가?

예를 들어 `backend/app.py`의 응답을 수정했다고 하자. 내 PC에서 실행됐다는 사실만으로 팀원이 받아도 테스트가 통과하고 서버에서 실행된다고 보장할 수 없다.

| 개념 | 질문 | 이 프로젝트의 답 |
| --- | --- | --- |
| CI: Continuous Integration | 변경을 합쳐도 기존 계약이 유지되는가? | pytest → Compose 설정 검사 → Docker 이미지 빌드 |
| Continuous Delivery | 검증한 변경을 배포할 준비가 되었는가? | 배포 절차를 자동화하고 필요하면 production 승인 후 실행 |
| Continuous Deployment | 검증 후 실제 서버 반영까지 자동으로 하는가? | main push 후 CI 성공 시 배포 조건 충족; 승인 규칙이 있으면 대기 |
| GitHub Actions | 누가 이 절차를 실행하는가? | GitHub 이벤트를 받아 YAML에 적힌 Job과 Step을 실행하는 플랫폼 |

`git push`는 소스를 GitHub에 올리는 동작이다. `docker compose build`는 이미지를 만드는 동작이다. `docker compose up`은 컨테이너를 실행·갱신하는 동작이다. 세 작업을 구분해야 배포 실패 위치를 찾을 수 있다.

## 3. 읽을 파일과 순서

| 순서 | 파일 | 핵심 |
| --- | --- | --- |
| 1 | [05 README](../07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project/README.md) | 세 서비스와 로컬 실습 |
| 2 | [실제 05 워크플로우](../../../.github/workflows/07-weather-mcp-cicd.yml) | 이번 강의의 기준 YAML |
| 3 | [05 테스트](../07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project/backend/test_app.py) | Fake MCP·LLM과 응답 계약 |
| 4 | [05 Compose](../07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project/compose.yml) | 빌드·환경 변수·포트·기동 의존성 |
| 5 | [06 워크플로우 예제](../.github/workflows/07-weather-stateful-cicd.yml) | CI와 상태 보존 배포 |
| 6 | [06 README](../07_multi-agent-service-ops/00_runtime-and-deployment/06_weather-mcp-stateful-deployment/README.md) | PostgreSQL·Redis 확장 |

02의 `runtime-ci.yml`과 04의 `07-runtime-deploy-example.yml`은 앞선 `01_simple-multi-llm-compose` 학습용이다. 05 전용 파일과 배포 대상 폴더가 다르다. 현재 내부 `07-runtime-ci.yml`도 01을 검사하므로 이것이 성공했다고 Weather 테스트가 통과한 것은 아니다.

기존 README의 축약 YAML보다 실제 05 YAML을 우선한다. 실제 파일에는 중첩 경로, workflow 자체의 `paths`, 수동 배포 조건, pip 캐시가 반영되어 있다. 06의 `deploy/README.md`에는 인프라를 미리 수동 실행하는 설명이 남아 있지만 현재 06 YAML은 배포 과정에서 인프라 `up`도 수행한다.

## 4. YAML을 읽는 순서

YAML은 들여쓰기로 부모·자식 관계를 표현한다. `-`는 목록 항목이고, `|`는 여러 줄 명령을 유지한다. `>-`는 여러 줄 문자열을 한 줄처럼 이어 읽게 한다. `.yml`과 `.yaml`은 같은 용도로 사용한다.

| 키 | 실제 값 또는 역할 | 이해할 점 |
| --- | --- | --- |
| `name` | `07 Weather MCP CI CD` | Actions 목록에 표시되는 이름 |
| `on` | push, pull_request, workflow_dispatch | 시작 조건 |
| `paths` | 05 backend/frontend/mcp_server/compose 및 workflow | 관련 파일 변경만 자동 실행 |
| `permissions` | `contents: read` | checkout에 필요한 저장소 읽기 권한 |
| `env.PROJECT_DIR` | `aidevs-main/aidevs-main/07_.../05_...` | Git 루트 기준 대상 경로 |
| `jobs` | `test-and-build`, `deploy` | 각각 Runner에서 실행할 작업 묶음 |
| `runs-on` | `ubuntu-latest` | 내 Windows PC와 별개인 Linux 실행 환경 |
| `defaults.run.working-directory` | `${{ env.PROJECT_DIR }}` | 해당 Job의 `run` 명령 기준 폴더 |
| `uses` | `actions/checkout@v4` 등 | 기존 Action 호출; 버전은 현재 파일 값 |
| `with` | Python 3.12, pip 캐시 설정 | Action에 전달하는 입력 |
| `run` | pytest, docker, ssh 등 | Runner 셸에서 실행할 명령 |
| `needs` | `test-and-build` | CI 성공 후 배포하도록 의존 관계 연결 |
| `if` | 이벤트·브랜치·입력 조건 | 배포 Job을 실행할지 판단 |
| `environment` | `production` | 배포 환경의 Secret·보호 규칙 적용 |

GitHub 표현식 `${{ secrets.AWS_HOST }}`는 GitHub의 값을 참조한다. Bash의 `$AWS_HOST`는 셸 환경 변수를 읽는다. PowerShell에서는 `$env:AWS_HOST` 형태다. 문서의 PowerShell 명령과 YAML 내부 Linux 명령을 섞지 않는다.

현재 `defaults.run`은 CI Job에만 있다. CD Job은 별도 checkout을 하고 저장소 루트에서 `$PROJECT_DIR`를 scp에 사용한다. CI에서 `cd backend`를 했다고 CD의 폴더가 바뀌지 않는다. 서로 다른 Step 사이에서도 `cd`는 이어지지 않으므로 working-directory를 명시한다.

### 배포 조건을 직접 해석하기

실제 05 YAML의 핵심이다.

```yaml
deploy:
  if: >-
    (github.event_name == 'push' && github.ref == 'refs/heads/main') ||
    (github.event_name == 'workflow_dispatch' && inputs.deploy)
  needs: test-and-build
  runs-on: ubuntu-latest
  environment: production
```

| 상황 | CI | 배포 |
| --- | --- | --- |
| 개인 브랜치에 대상 코드 push | 실행 | 건너뜀 |
| PR 생성·갱신에 대상 코드 포함 | 실행 | 건너뜀 |
| main에 대상 코드 push 또는 PR 병합 | 실행 | CI 성공 후 가능 |
| 수동 실행, deploy=false | 실행 | 건너뜀 |
| 수동 실행, deploy=true | 실행 | CI 성공 후 가능; YAML상 main 제한 없음 |
| README 또는 이 강의만 변경 | 05 자동 실행 안 함 | 실행 안 함 |
| 로컬 git pull 또는 git commit만 수행 | 실행 안 함 | 실행 안 함 |

수동 배포의 브랜치 제한은 이 `if`에 없다. production에서 main만 배포하도록 제한했는지 확인한다. `environment: production`만 쓴다고 승인이 자동으로 생기지는 않는다. Required reviewers 등 실제 보호 규칙을 설정해야 승인 대기가 생긴다.

`concurrency.group: weather-mcp-${{ github.ref }}`는 같은 ref의 실행 간 동시성을 제어한다. `cancel-in-progress: false`는 실행 중 작업을 새 실행 때문에 취소하지 않겠다는 뜻이다. 모든 대기 실행의 FIFO 보장은 아니며, 서로 다른 브랜치의 수동 배포는 같은 EC2에서 겹칠 수 있다. 전체 운영 배포 직렬화가 필요하면 공통 그룹을 사용하는 개선을 검토한다.

## 5. CI는 정확히 무엇을 검사하는가?

현재 05의 Step 순서는 다음과 같다.

1. **Checkout source**: 해당 실행의 소스를 Runner에 내려받는다.
2. **Set up Python**: Python 3.12를 준비한다. pip 캐시는 다운로드 재사용용이며 설치 생략이나 테스트 성공 보장이 아니다.
3. **Install backend test dependencies**: backend requirements와 pytest를 설치한다.
4. **Test backend contract with Fake MCP and LLM**: backend 폴더에서 테스트한다.
5. **Validate Compose**: 컨테이너를 띄우지 않고 Compose 구성을 검사한다.
6. **Build three images**: backend/frontend/weather-mcp 이미지를 만든다.

현재 `test_app.py`에는 `/health/live`의 HTTP 200 검사와 `/api/weather`의 HTTP 200·`get_weather`·도시명·`fake-model` 검사가 있다. `monkeypatch`로 실제 날씨 호출과 LLM 호출 함수를 교체하므로 API Key 없이 계약을 검사한다.

테스트 통과는 실제 Open-Meteo, OpenAI/Gemini, EC2 네트워크의 정상 동작을 보장하지 않는다. `config --quiet`는 네트워크 연결 검사가 아니고, `build`는 컨테이너 기동 검사가 아니다. 현재 CI에는 실제 서비스 통합 테스트나 이미지 Registry push가 없다.

### 실습 A: Windows에서 CI 명령 재현

1절의 PowerShell 경로 변수 설정 후 실행한다. Python 3.12와 실행 중인 Docker Desktop이 필요하다. 가상환경 활성화 대신 실행 파일을 직접 지정한다.

```powershell
Set-Location $weather05
python --version
docker version
docker compose version
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt pytest
Push-Location backend
& ..\.venv\Scripts\python.exe -m pytest test_app.py -q
Pop-Location
docker compose config --quiet
docker compose build
```

명령 하나가 실패하면 다음 명령으로 넘어가기 전에 해결한다. 현재 파일 기준 테스트는 `2 passed`를 기대하며, Compose 검사는 출력 없이 종료 코드 0이면 성공이다. `.env`는 이 Fake 테스트에 필요하지 않다. 실제 서비스 실행에는 별도로 설정한다.

## 6. GitHub에서 실행하고 무엇을 확인할까?

### 실습 B: 배포 없이 수동 CI 실행

워크플로우가 원격 기본 브랜치에 반영되어 있고 Actions 사용 및 실행 권한이 있어야 한다. GitHub 저장소의 `Actions → 07 Weather MCP CI CD → Run workflow`에서 브랜치를 고르고 **deploy 체크를 해제**한다. 기본 브랜치에 workflow_dispatch가 있어야 수동 실행이 가능하다. [공식 수동 실행 안내](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)

GitHub CLI가 설치·인증된 경우에도 실행할 수 있다. `OWNER/REPO`는 실제 원격 저장소로 바꾼다.

```powershell
$repository = 'OWNER/REPO'
gh auth status
gh workflow list --repo $repository
gh workflow run 07-weather-mcp-cicd.yml --repo $repository --ref main -f deploy=false
gh run list --repo $repository --workflow 07-weather-mcp-cicd.yml --limit 5
# 목록에서 이번 실행의 ID를 입력한다.
$runId = Read-Host '이번 실행 ID'
gh run watch $runId --repo $repository --exit-status
gh run view $runId --repo $repository --log-failed
```

`gh workflow run`은 원격 실행을 요청한다. YAML을 내 PC에서 실행하는 명령이 아니다. `--ref`는 실행할 브랜치를, `-f`는 workflow 입력을 지정한다. [GitHub CLI 공식 명령](https://cli.github.com/manual/gh_workflow_run)

### 실습 C: 개인 브랜치 push로 자동 CI 확인

원격에서 인식되는 실제 workflow가 준비된 뒤 진행한다. 학습용 변경을 만든 파일만 stage한다. 현재 다른 작업의 수정·이동이 있으므로 예제를 무조건 전체 stage하는 방식으로 실행하지 않는다.

```powershell
Set-Location $repoRoot
git switch -c lesson/weather-ci
# backend/test_app.py에 테스트 의도를 설명하는 주석 등 학습용 변경 후:
git diff -- aidevs-main/aidevs-main/07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project/backend/test_app.py
git add -- aidevs-main/aidevs-main/07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project/backend/test_app.py
git diff --cached
git commit -m "docs: explain weather backend contract test"
git push -u origin lesson/weather-ci
```

GitHub에서 PR을 만들면 다시 CI가 실행될 수 있다. 같은 커밋에 push 실행과 PR 실행이 함께 보이는 것은 두 이벤트 때문이다. main 병합은 실제 CD 조건을 충족하므로 서버 준비 후 진행한다.

### 실행 결과 읽기

| 화면에서 확인할 것 | 의미 |
| --- | --- |
| Workflow 이름, Event, Branch, Commit SHA | 내가 의도한 코드·이벤트의 실행인가? |
| test-and-build의 최초 실패 Step | 실제 원인을 찾는 시작점 |
| pytest의 실패 assertion과 traceback | 예상 응답과 실제 응답의 차이 |
| Docker Build의 실패 Dockerfile 단계 | COPY 경로·의존성 설치·베이스 이미지 오류 |
| deploy의 Skipped | 조건 미충족 또는 선행 CI 실패 여부 확인 |
| Waiting / 승인 요청 | production 보호 규칙 확인 |
| 마지막 readiness Step | 서버 명령과 건강 상태 검사가 성공했는가? |

수정 후 push하면 새 실행이 만들어진다. 이전 실패 실행의 기록은 그대로다. 재실행은 원래 실행의 코드를 다시 검사하므로 수정한 커밋이 포함된 새 실행인지 확인한다.

## 7. CD: GitHub에서 EC2까지

### 최초 준비

EC2에는 Docker Engine·Compose Plugin, SSH 사용자 권한, `~/weather-mcp-deployment/.env`가 필요하다. `.env.example`의 필요한 값을 참고하여 EC2에 직접 준비한다. Git에 API Key를 올리지 않는다.

GitHub 저장소의 `Settings → Environments → production`에서 필요한 보호 규칙과 다음 Secret을 설정한다.

| Secret | 내용 |
| --- | --- |
| AWS_HOST | EC2 주소 |
| AWS_USER | Ubuntu의 ubuntu 또는 Amazon Linux의 ec2-user 등 실제 사용자 |
| AWS_SSH_PRIVATE_KEY | 배포용 개인 키 전체 |
| AWS_SSH_KNOWN_HOSTS | 서버 지문을 검증한 known_hosts 항목 전체; SHA256 지문만 넣지 않음 |

내 PC에서 SSH가 된다고 GitHub Runner에서도 접속 가능한 것은 아니다. EC2 Security Group이 내 IP만 허용하면 Runner 접속은 실패한다. 수업 환경의 승인된 Runner 접근 경로를 준비한다. backend 8000은 현재 Compose에서 호스트에 매핑되지만 인터넷 공개 여부는 Security Group 등으로 통제하며, MCP 8010은 호스트 포트 매핑이 없다.

### 실제 배포 동작

CI와 별도의 Runner에서 checkout → SSH 키·known_hosts 설정 → 소스를 scp로 복사 → EC2에서 다음 명령을 실행한다. 이해를 위해 실제 SSH 명령 내부를 줄별로 풀었다. 실제 YAML은 `&&`로 연결되어 앞 명령 실패 시 다음 명령을 실행하지 않는다.

```bash
cd ~/weather-mcp-deployment
test -f .env
docker compose config --quiet
docker compose up -d --build
curl --fail --retry 12 --retry-delay 5 http://127.0.0.1:8000/health/ready
```

**CI에서 만든 이미지를 EC2에 전송하는 구조가 아니다.** CI는 이미지가 만들어지는지 검사하고, CD는 소스를 복사하여 EC2에서 다시 빌드한다. 따라서 CI 성공 후에도 EC2의 디스크·메모리·패키지 다운로드 문제로 실패할 수 있다. 버전 범위 의존성이므로 두 빌드가 완전히 동일한 산출물이라는 보장도 없다.

서버 준비가 끝난 뒤 실제 배포 실습에만 아래 명령을 사용한다.

```powershell
gh workflow run 07-weather-mcp-cicd.yml --repo $repository --ref main -f deploy=true
```

### 배포 후 확인: EC2의 Bash에서

```bash
cd ~/weather-mcp-deployment
docker compose ps
docker compose logs --tail=100 weather-mcp backend frontend
curl --fail http://127.0.0.1:8000/health/live
curl --fail http://127.0.0.1:8000/health/ready
```

05 readiness는 MCP 연결과 도구 목록 조회를 확인한다. 현재 코드는 `get_weather`가 목록에 있는지 별도 assertion을 하지 않으며 실제 날씨 API·LLM 호출도 하지 않는다. 따라서 배포 성공 후 브라우저의 `http://EC2주소:8501`에서 실제 요청을 보내 도구 결과와 답변까지 확인한다. 이 요청은 외부 API를 사용한다.

05에는 자동 롤백이 없다. readiness 실패는 배포 Job을 실패로 표시할 뿐 이미 갱신한 컨테이너를 이전 버전으로 되돌리지 않는다. 원인 확인 후 마지막 정상 코드로 되돌리는 새 커밋을 만들어 검증·배포한다.

## 8. 06으로 확장: 데이터는 남기고 앱을 갱신하기

05는 세 앱 컨테이너만 실행한다. 06은 PostgreSQL의 완료 이력과 Redis의 진행 상태·캐시를 추가한다.

| 파일 | 역할 |
| --- | --- |
| compose.infrastructure.yml | database·redis·영속 Volume·weather-stateful 네트워크 |
| compose.application.yml | weather-mcp·backend·frontend; 외부 네트워크 사용 |
| database/init.sql | 최초 DB 초기화 스키마 |
| backend/test_app.py | Fake MCP·LLM·StateStore·Repository로 계약 검사 |

06 YAML을 현재 Git 루트로 옮겨 사용할 때는 `paths`, `working-directory`, `scp`의 소스 경로에 `aidevs-main/aidevs-main/` 접두사를 반영해야 한다. 05의 경로 변수 패턴을 참고한다. 현재 06의 paths에는 workflow 자체가 없으므로 파일만 변경하면 자동 시작되지 않는 점도 확인한다. 이 강의에서는 실제 YAML을 변경하지 않았다.

로컬 CI 재현은 다음과 같다.

```powershell
Set-Location $weather06
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt pytest
Push-Location backend
& ..\.venv\Scripts\python.exe -m pytest test_app.py -q
Pop-Location
docker compose -f compose.infrastructure.yml config --quiet
docker compose -f compose.application.yml config --quiet
docker compose -f compose.application.yml build
```

06의 실제 CD 명령은 인프라를 먼저 `up -d --wait --wait-timeout 120` 하고 앱을 `up -d --build --force-recreate weather-mcp backend frontend`로 갱신한다. 기존 인프라 설정이 같으면 재사용하지만 설정이 바뀌면 Compose가 인프라 컨테이너도 재생성할 수 있다. “절대 재시작하지 않는다”로 이해하면 안 된다.

`down -v`를 하지 않아 Volume을 보존한다. 이것은 백업과 다르다. 기존 DB Volume에는 수정한 init.sql이 자동 재적용되지 않으므로 스키마 변경은 별도 마이그레이션을 계획한다.

EC2에서 배포 전후 이력을 비교한다.

```bash
cd ~/weather-stateful
docker compose -f compose.infrastructure.yml ps
docker compose -f compose.application.yml ps
curl --fail http://127.0.0.1:8000/health/ready
docker compose -f compose.infrastructure.yml exec database psql -U agent_user -d agent_db -c "SELECT run_id, city, created_at FROM weather_agent.runs ORDER BY created_at DESC LIMIT 10;"
```

DB 사용자·DB명을 변경했다면 명령도 맞춘다. 06 readiness는 Redis·DB 연결·DB 스키마·MCP get_weather 도구 존재를 확인한다. 05와 06은 8000·8501 포트가 겹치므로 같은 호스트에서 함께 시작하지 않는다.

## 9. 실패 상황별 진단과 수업 마무리

| 증상 | 먼저 확인 |
| --- | --- |
| Actions에 workflow가 없음 | 실제 Git 루트 위치, 원격 커밋, Actions 활성화 |
| Run workflow 버튼 없음 | 기본 브랜치의 workflow_dispatch, 실행 권한 |
| push했는데 실행 없음 | 변경 경로와 paths, 중첩 폴더 접두사 |
| working directory 없음 | PROJECT_DIR와 checkout 후 파일 구조 |
| ModuleNotFoundError: app | backend에서 pytest를 실행했는지 |
| Compose 검사는 성공, 기동 실패 | 포트 충돌·환경 변수 실제 값·서비스 로그 |
| SSH timeout | Runner→EC2 네트워크, 서버 상태 |
| Permission denied (publickey) | AWS_USER·키 쌍·서버 authorized_keys |
| Host key verification failed | 주소 변경·서버 지문·known_hosts Secret |
| test -f .env 실패 | 해당 EC2 배포 폴더의 .env 존재 |
| readiness 실패 | MCP·backend 로그; 06은 DB·스키마·Redis 추가 |
| CI 성공인데 날씨 요청 실패 | 실제 API Key·외부 API 연결·도구 응답 |

수강생은 다음 질문을 코드와 로그를 보며 설명하면 된다.

- [ ] Git 루트와 강의 루트가 다르면 YAML의 어느 경로가 달라지는가?
- [ ] Fake 테스트, 이미지 빌드, readiness, 실제 날씨 요청은 무엇을 각각 검증하는가?
- [ ] 개인 브랜치 push와 수동 deploy=true는 배포 조건이 어떻게 다른가?
- [ ] CI와 CD에서 checkout을 각각 하는 이유는 무엇인가?
- [ ] production 승인 대기가 생기려면 어떤 설정이 필요한가?
- [ ] 06의 앱 재배포 후 기존 이력이 남는 근거와 백업이 별도로 필요한 이유는 무엇인가?

권장 수업 진행: 개념·경로 15분 → YAML 읽기 20분 → 로컬 CI 20분 → GitHub 실행·로그 20분 → CD·06 확장 25분. 배포 환경이 아직 준비되지 않았다면 수동 CI까지 실행하고 CD는 다음 문서의 흐름도로 추적한다.
