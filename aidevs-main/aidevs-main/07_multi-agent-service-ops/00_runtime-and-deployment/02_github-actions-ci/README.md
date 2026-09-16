# 02 GitHub Actions CI

CI는 **Continuous Integration(지속적 통합)**의 약자입니다. 여러 사람이 변경한 코드를
저장소에 Push하거나 Pull Request로 올릴 때, Test·설정 검사·Image Build를 자동 실행하여
변경이 기존 코드와 함께 정상 동작하는지 확인하는 과정입니다.

Multi-LLM Compose 변경을 Push하거나 Pull Request로 보낼 때 다음을 자동 검사합니다.

```text
Checkout
→ Python 3.12
→ Fake Client 기반 Backend 테스트
→ Compose 문법 검사
→ Frontend·Backend Image Build
```

실제 LLM·Redis·PostgreSQL과 AWS는 CI에서 호출하지 않습니다. 실제 실행 코드는 Provider를 사용하지만 자동 테스트는 비용 없는 Fake Client로 계약만 검사합니다.

실제 Workflow는 저장소 루트 `.github/workflows/07-runtime-ci.yml`에 둡니다.

## CI와 배포의 차이

CI는 변경한 코드가 합쳐질 수 있는 상태인지 자동 검사합니다. 배포는 검증된 코드를
실행 환경에 반영합니다. 이 단계에서는 AWS에 접속하거나 서비스를 변경하지 않습니다.

| 단계 | 확인할 질문 | 외부 환경 변경 |
| --- | --- | --- |
| Test | 계약과 API 동작이 유지되는가? | 없음 |
| Compose 검사 | 설정과 환경 변수 참조가 유효한가? | 없음 |
| Image Build | Dockerfile로 Image를 만들 수 있는가? | CI 내부 Image만 생성 |
| Deploy | 실행 서버에 새 버전을 반영하는가? | 있음, 이 단원에서는 제외 |

## Workflow를 읽는 순서

루트의 `.github/workflows/07-runtime-ci.yml`에서 다음 항목을 순서대로 찾습니다.

1. `name`: Actions 화면에 표시되는 이름
2. `on`: Push와 Pull Request 중 언제 실행하는지
3. `permissions`: Workflow의 최소 저장소 권한
4. `jobs`: 서로 독립적인 검사 묶음
5. `steps`: 로컬 명령을 실행하는 순서

각 Step은 로컬에서 실행한 `pytest`, `docker compose config`, `docker compose build`를
깨끗한 Runner에서 다시 실행하는 과정입니다.

### Runner, Job, Step을 구분하세요

GitHub Actions는 Push한 개발자 PC나 수강생 PC에서 직접 실행되지 않습니다. GitHub가 준비한
새 Linux 가상 머신인 **Runner**에서 실행됩니다. 그래서 내 PC의 `.env`, 실행 중인 Docker
Container, Ollama Model은 CI에 전달되지 않습니다.

```text
GitHub 이벤트(Push 또는 Pull Request)
→ GitHub Runner(ubuntu-latest)를 새로 준비
→ Job: test-and-build 시작
→ Step: Checkout → Python 설정 → 패키지 설치 → Test → Compose 검사 → Image Build
→ 모든 Step 성공: CI 성공 / 하나라도 실패: CI 실패
```

| YAML 항목 | 이 실습의 값 | 의미 |
| --- | --- | --- |
| `runs-on` | `ubuntu-latest` | 매 실행마다 준비되는 Linux Runner |
| `working-directory` | `01_simple-multi-llm-compose` | 이후 `run` 명령이 실행되는 기준 폴더 |
| `uses: actions/checkout@v4` | Checkout Step | 현재 Commit의 소스 코드를 Runner에 내려받음 |
| `uses: actions/setup-python@v5` | Python Step | Python 3.12 설치·선택 |
| `run` | Test·Compose·Build Step | Runner 터미널에서 실제 명령 실행 |

`test-and-build` Job의 Step은 위에서 아래 순서대로 실행됩니다. 예를 들어 Backend Test가
실패하면 Compose 검사와 Image Build는 실행되지 않습니다. 따라서 실패 화면에서는 첫 번째
빨간 Step부터 해결합니다.

### 이 CI가 확인하는 범위와 확인하지 않는 범위

| 항목 | CI에서 하는 일 | CI에서 하지 않는 일 |
| --- | --- | --- |
| Backend Test | Fake Client로 API 계약·입력 검증·예외 처리를 확인 | OpenAI·Gemini·Ollama에 실제 요청을 보내지 않음 |
| Compose | `docker compose config --quiet`로 YAML·환경 변수 참조 확인 | `docker compose up`으로 DB·Redis를 실제 실행하지 않음 |
| Docker Image | Dockerfile Build 성공 여부 확인 | Registry에 `push`하거나 수업 서버를 변경하지 않음 |

즉 이 단원의 CI는 “코드와 배포 설정이 기본적으로 깨지지 않았는지” 빠르게 확인하는
단계입니다. 실제 PostgreSQL·Redis·Ollama까지 연결한 화면 테스트는 수강생 로컬 환경 또는
별도의 통합 테스트 환경에서 `docker compose up`으로 확인합니다.

## 언제 CI가 실행되는가?

`07-runtime-ci.yml`의 `on:`은 Workflow를 시작하는 이벤트(Trigger)를 정의합니다. 이
Workflow는 `main`뿐 아니라 개발자 개인 브랜치에 Push할 때도 실행됩니다. 단,
`07_multi-agent-service-ops/00_runtime-and-deployment/**` 또는 Workflow 파일 자체가
변경된 경우에만 `paths:` 조건을 통과합니다.

| 설정 | 실행 시점 | 실행되지 않는 경우 |
| --- | --- | --- |
| `push` | 개인 브랜치·`main`에 Commit을 `git push`할 때 | 지정한 경로와 관계없는 파일만 변경한 Push |
| `pull_request` | 개인 브랜치에서 `main` 등 대상 브랜치로 Pull Request를 생성하거나, Pull Request에 새 Commit을 Push할 때 | 수강생 PC에서 단순히 `git pull`할 때 |
| `workflow_dispatch` | GitHub Actions 화면에서 **Run workflow**를 눌러 수동 실행할 때 | 버튼을 누르지 않은 경우 |

여기서 `pull_request`는 GitHub의 **병합 요청**입니다. 로컬 PC에서 원격 변경을 내려받는
`git pull` 명령과는 다른 개념이며, `git pull`만으로 GitHub Actions가 실행되지는 않습니다.

협업 흐름은 보통 다음과 같습니다.

```text
개발자 개인 브랜치에 Push
→ CI 실행
→ Pull Request 생성 또는 갱신
→ CI 재실행
→ 통과한 변경을 main에 병합
→ 이후 CD가 배포 환경에 반영
```

## 로컬 확인

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
python -m pip install pytest
python -m pytest backend\test_app.py -q
docker compose config --quiet
docker compose build
```

`.venv`는 이 실습의 Python 패키지를 다른 프로젝트와 분리하는 가상 환경입니다. `pytest`와
Backend 패키지는 가상 환경에 설치합니다. 반면 `docker compose`는 Docker Desktop의 Docker
Daemon에 명령을 보내므로 가상 환경에 설치되는 프로그램이 아닙니다. 가상 환경을 활성화한
터미널에서 그대로 실행해도 되고, `deactivate`한 뒤 실행해도 결과는 같습니다.

위 명령을 모두 통과시킨 뒤 Push합니다. 로컬에서 실패하는 Test를 CI가 고쳐주지는
않습니다.

## GitHub에서 결과 확인

1. 저장소의 `Actions` 탭에서 `07 Runtime CI`를 선택합니다.
2. 최근 실행의 Commit과 Branch가 본인 작업과 일치하는지 확인합니다.
3. 실패한 Job을 열고 빨간색으로 표시된 첫 Step을 찾습니다.
4. Log 마지막 줄만 보지 말고 최초 오류와 실행 명령을 확인합니다.

| 실패 Step | 먼저 확인할 내용 |
| --- | --- |
| Dependency 설치 | requirements 경로·Python 버전·패키지 이름 |
| Backend Test | 첫 Assertion·Import 경로·계약 변경 |
| Compose config | YAML 들여쓰기·누락 환경 변수·파일 경로 |
| Image Build | COPY 경로·requirements·Base Image |

수정 후 새 Commit을 Push하면 새 실행이 만들어집니다. 이전 실패를 성공처럼 취급하지
않습니다.

## 보안 원칙

- Pull Request 테스트에 LLM·AWS Secret을 제공하지 않습니다.
- `.env`를 Commit하지 않습니다.
- Workflow 기본 권한은 `contents: read`입니다.
- 자동 AWS 배포는 수동 EC2 배포를 이해한 뒤 04에서 별도로 구성합니다.

## 완료 체크

```text
[ ] CI와 배포의 차이를 설명할 수 있다.
[ ] Workflow Trigger와 기본 권한을 찾았다.
[ ] 로컬 Test·Compose 검사·Build를 통과했다.
[ ] Actions에서 첫 실패 Step과 오류 문장을 찾을 수 있다.
[ ] CI가 실제 Provider Secret 없이 동작하는 이유를 설명할 수 있다.
```
