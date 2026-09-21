# GitHub Actions CI/CD 실습 가이드

이 리포(`Lui02372/aidevs-latest`)에 들어 있는 워크플로 두 개를 교재 삼아 CI와 CD의 구조를
익히고, 실제 GitHub Actions에서 돌려 보는 것이 목표입니다.

| 파일 | 성격 | 배우는 것 |
|---|---|---|
| `.github/workflows/01-simple-compose-ci.yml` | **CI 전용** | 테스트 → 빌드 → 스택 기동 → readiness → 정리 |
| `.github/workflows/07-weather-mcp-cicd.yml` | **CI + CD** | 위 CI에 더해 SSH로 EC2 배포까지 |

`.github/workflows/09-ec2-ci-cd.yml`은 같은 CD를 서비스 컨테이너·아티팩트·릴리스 패키징까지
확장한 심화 예제입니다. 먼저 01과 07을 이해한 뒤 보는 것을 권합니다.

---

## 0. 가장 먼저 알아야 할 규칙 — 워크플로는 리포 루트에만 둔다

GitHub Actions는 **리포지토리 루트의 `.github/workflows/`만** 읽습니다. 하위 폴더에 있는
`.github/workflows/`는 조용히 무시됩니다. 에러도 안 나고 Actions 탭에 아예 나타나지 않기 때문에
"왜 안 돌지?" 하며 가장 오래 헤매는 지점입니다.

```
aidevs-latest/                                  ← 리포 루트
├── .github/workflows/                          ← 여기 있는 것만 실행된다
│   ├── 01-simple-compose-ci.yml
│   ├── 07-weather-mcp-cicd.yml
│   └── 09-ec2-ci-cd.yml
└── aidevs-main/aidevs-main/
    ├── .github/workflows/                      ← 무시된다 (루트가 아님)
    │   ├── 07-runtime-ci.yml
    │   └── 07-weather-stateful-cicd.yml
    └── 07_multi-agent-service-ops/...
```

여기서 따라오는 두 번째 규칙: 워크플로 안의 **모든 경로는 리포 루트 기준**입니다. 이 리포는
실제 소스가 `aidevs-main/aidevs-main/` 아래에 있으므로 경로마다 이 접두사가 붙어야 합니다.
반복을 줄이려고 두 파일 모두 `env`로 한 번만 정의해 재사용합니다.

```yaml
env:
  PROJECT_DIR: aidevs-main/aidevs-main/07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project
```

---

## 1. 공통 뼈대 — 모든 워크플로가 가지는 4층 구조

```yaml
name: 07 Weather MCP CI CD      # 1) Actions 탭에 표시될 이름

on:                             # 2) 언제 돌릴 것인가 (트리거)
  push:
  pull_request:
  workflow_dispatch:

jobs:                           # 3) 무엇을 할 것인가
  test-and-build:               #    잡(job) = 독립된 가상머신 1대
    runs-on: ubuntu-latest      #    어떤 OS에서
    steps:                      # 4) 그 안에서 순서대로 실행할 명령들
      - uses: actions/checkout@v4
      - run: echo "hello"
```

**잡(job)과 스텝(step)의 차이**가 핵심입니다.

- **잡**은 각각 **완전히 새로운 빈 가상머신**에서 돕니다. 잡끼리는 파일도 설치한 패키지도
  공유하지 않습니다. 기본적으로 **병렬** 실행됩니다.
- **스텝**은 한 잡 안에서 **같은 머신에서 순차** 실행됩니다. 앞 스텝이 설치한 것을 뒤 스텝이
  그대로 씁니다. 하나라도 실패하면 뒤 스텝은 건너뜁니다.

그래서 잡마다 `actions/checkout@v4`를 다시 해야 합니다. 새 머신이라 소스가 없기 때문입니다.

---

## 2. CI 예제 뜯어보기 — `01-simple-compose-ci.yml`

### 2-1. 트리거: `on`

```yaml
on:
  push:
    branches: [main]
    paths:
      - "aidevs-main/aidevs-main/07_multi-agent-service-ops/00_runtime-and-deployment/01_simple-multi-llm-compose/**"
      - ".github/workflows/01-simple-compose-ci.yml"
  pull_request:
    paths:
      - "..."
  workflow_dispatch:
```

| 키 | 뜻 |
|---|---|
| `push.branches` | 이 브랜치에 push될 때만. 없으면 **모든 브랜치** |
| `paths` | 이 경로의 파일이 바뀐 커밋일 때만. **실습에서 "안 돌아요"의 1순위 원인** |
| `pull_request` | PR이 열리거나 갱신될 때 |
| `workflow_dispatch` | Actions 화면의 **Run workflow** 버튼으로 수동 실행 |

`paths`에 **워크플로 파일 자신**을 넣어두면 CI 설정을 고칠 때도 바로 검증됩니다. 안 넣으면
YAML을 고쳐 push해도 트리거되지 않아 오타를 다음 커밋에서야 발견하게 됩니다.

`**`는 하위 전체를 뜻합니다. `paths` 대신 `paths-ignore`로 "이것만 빼고"도 가능합니다.

### 2-2. 권한: `permissions`

```yaml
permissions:
  contents: read
```

워크플로에 주어지는 `GITHUB_TOKEN`의 권한입니다. **읽기만** 주는 것이 기본이고, 코드를
체크아웃하는 CI에는 이것으로 충분합니다. 커밋을 푸시하거나 릴리스를 만들어야 할 때만
`contents: write`로 올립니다. 최소 권한이 원칙입니다.

### 2-3. 잡 나누기와 `needs`

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    ...

  compose:
    needs: test          # test가 성공해야만 시작
    runs-on: ubuntu-latest
```

`needs`가 없으면 두 잡은 동시에 출발합니다. `needs: test`를 붙이면 **직렬**이 되고, `test`가
실패하면 `compose`는 아예 실행되지 않습니다. "빠른 단위 테스트로 먼저 거르고, 느린 Docker
빌드는 통과한 뒤에만" 이라는 의도입니다.

### 2-4. `defaults`로 작업 디렉토리 고정

```yaml
defaults:
  run:
    working-directory: ${{ env.PROJECT_DIR }}
```

이 잡의 모든 `run:` 스텝이 그 폴더에서 실행됩니다. 스텝마다 `cd`를 쓰지 않아도 됩니다.
특정 스텝만 다른 곳에서 돌려야 하면 그 스텝에 `working-directory:`를 따로 적어 덮어씁니다.

> `defaults`는 `run:` 스텝에만 적용됩니다. `uses:`로 부르는 액션에는 적용되지 않아서
> `actions/setup-python`의 `cache-dependency-path` 같은 값은 **루트 기준 전체 경로**를
> 적어야 합니다.

### 2-5. 스텝 읽기

```yaml
steps:
  - name: Checkout
    uses: actions/checkout@v4              # 남이 만든 액션을 가져다 씀

  - name: Set up Python
    uses: actions/setup-python@v5
    with:                                  # 액션에 넘기는 입력값
      python-version: "3.12"
      cache: pip                           # pip 캐시로 설치 시간 단축
      cache-dependency-path: ${{ env.PROJECT_DIR }}/backend/requirements.txt

  - name: Install dependencies
    run: python -m pip install -r backend/requirements.txt pytest   # 셸 명령 직접 실행

  - name: Unit tests
    run: python -m pytest backend -q
```

- `uses:` = 재사용 액션 호출, `with:`로 입력을 넘김
- `run:` = 셸 명령 실행. `|`를 쓰면 여러 줄
- `name:` = 로그에 표시될 이름 (생략 가능하지만 붙이면 실패 지점 찾기 쉬움)
- `@v4`처럼 **버전을 고정**해야 액션이 바뀌어도 CI가 갑자기 깨지지 않음

### 2-6. CI에 `.env`가 없는 문제

```yaml
- name: Prepare .env
  run: cp .env.example .env
```

`.env`는 커밋되지 않으므로 CI 러너에는 없습니다. 예제 파일로 대체합니다.
이 프로젝트는 실제 API 키 없이도 `config`/`build`가 통과하도록 설계돼 있습니다.

### 2-7. 조건부 스텝 — `if`

```yaml
- name: Show logs on failure
  if: failure()                 # 앞 스텝이 실패했을 때만
  run: docker compose logs --tail 100

- name: Tear down
  if: always()                  # 성공하든 실패하든 무조건
  run: docker compose down -v
```

| 함수 | 실행 시점 |
|---|---|
| `success()` | 기본값. 앞이 전부 성공했을 때 |
| `failure()` | 앞에서 실패가 났을 때 — **로그 덤프용** |
| `always()` | 항상 — **정리(clean-up)용** |
| `cancelled()` | 취소됐을 때 |

실패했을 때 로그를 남기고, 무슨 일이 있어도 컨테이너를 정리하는 이 두 줄이 실무 CI의 품질을
가릅니다.

---

## 3. CD 예제 뜯어보기 — `07-weather-mcp-cicd.yml`

01의 구조 위에 **배포**가 얹힌 형태입니다. 차이나는 부분만 봅니다.

### 3-1. 수동 실행에 입력값 받기

```yaml
workflow_dispatch:
  inputs:
    deploy:
      description: "Deploy 05 application to AWS EC2"
      required: true
      type: boolean
      default: false
```

Actions 화면의 **Run workflow** 버튼을 누르면 체크박스가 뜹니다. 값은 `inputs.deploy`로 읽습니다.
"평소엔 CI만, 원할 때만 배포"를 만드는 장치입니다.

### 3-2. 동시 실행 제어 — `concurrency`

```yaml
concurrency:
  group: weather-mcp-${{ github.ref }}
  cancel-in-progress: false
```

같은 `group` 이름을 가진 실행은 **한 번에 하나만** 돕니다. 배포가 겹쳐서 서버 상태가 꼬이는
사고를 막습니다.

- `cancel-in-progress: false` → 앞 실행이 끝날 때까지 **대기** (배포에 적합)
- `cancel-in-progress: true` → 앞 실행을 **취소**하고 새 것 실행 (CI에 적합)

### 3-3. 배포 잡을 여는 조건 — 이 파일의 핵심

```yaml
deploy:
  if: >-
    (github.event_name == 'push' && github.ref == 'refs/heads/main') ||
    (github.event_name == 'workflow_dispatch' && inputs.deploy)
  needs: test-and-build
  environment: production
```

세 가지가 동시에 걸려 있습니다.

1. **`needs: test-and-build`** — 테스트·빌드가 **성공해야만** 배포. CI/CD에서 가장 중요한 한 줄입니다.
2. **`if`** — main 브랜치 push이거나, 수동 실행에서 deploy를 체크했을 때만. 그래서 다른 브랜치에
   push하면 CI만 돌고 배포는 건너뜁니다. **배포 없이 CI만 시험해 보는 방법**이 바로 이것입니다.
3. **`environment: production`** — GitHub의 Environment 기능. 여기에 승인자를 걸면
   **사람이 Approve를 눌러야** 배포가 진행됩니다. Environment 전용 Secret도 여기에 둡니다.

`github.ref`는 브랜치면 `refs/heads/main`, 태그면 `refs/tags/v1.0` 형태입니다.

### 3-4. Secret을 다루는 안전한 방식

```yaml
- name: Configure verified SSH identity
  env:
    SSH_PRIVATE_KEY: ${{ secrets.AWS_SSH_PRIVATE_KEY }}
    AWS_SSH_KNOWN_HOSTS: ${{ secrets.AWS_SSH_KNOWN_HOSTS }}
  run: |
    install -m 700 -d ~/.ssh
    printf '%s' "$SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
    chmod 600 ~/.ssh/id_ed25519
    printf '%s\n' "$AWS_SSH_KNOWN_HOSTS" > ~/.ssh/known_hosts
    chmod 600 ~/.ssh/known_hosts
```

배울 점 네 가지:

1. Secret을 `run:` 본문에 직접 박지 않고 **`env:`로 주입한 뒤 `$VAR`로** 씁니다. 명령줄에
   그대로 쓰면 로그나 프로세스 목록에 노출될 수 있습니다.
2. `echo` 대신 **`printf '%s'`** — 키에 백슬래시가 있어도 변형되지 않습니다.
3. **`chmod 600`** — SSH는 키 파일 권한이 느슨하면 사용을 거부합니다.
4. **`known_hosts`를 미리 심습니다.** 이게 있어야 중간자 공격을 막으면서도 "이 호스트를
   신뢰하시겠습니까?" 프롬프트 없이 자동 접속이 됩니다. CD에서 빠뜨리기 쉬운 부분입니다.

`secrets.*`는 **값이 가려지는 비밀**(키, 비밀번호), `vars.*`는 **가려지지 않는 설정값**
(호스트명, 리전)입니다. 09번 예제는 호스트/유저를 `vars`로 분리해 둔 형태입니다.

### 3-5. 배포와 검증

```yaml
- name: Copy application source
  run: |
    ssh "$AWS_USER@$AWS_HOST" 'mkdir -p ~/weather-mcp-deployment'
    scp -r "$PROJECT_DIR"/. "$AWS_USER@$AWS_HOST:~/weather-mcp-deployment/"

- name: Deploy and verify readiness
  run: |
    ssh "$AWS_USER@$AWS_HOST" 'cd ~/weather-mcp-deployment && test -f .env && docker compose config --quiet && docker compose up -d --build && curl --fail --retry 12 --retry-delay 5 http://127.0.0.1:8000/health/ready'
```

`&&`로 이어 붙여 **앞이 실패하면 뒤를 실행하지 않습니다.**

- `test -f .env` — `.env`는 Git에 없으므로 **EC2에 미리 수동으로 올려둬야** 합니다.
  실습에서 가장 많이 막히는 지점입니다.
- `curl --fail` — HTTP 4xx/5xx면 0이 아닌 종료 코드를 내서 **잡을 실패시킵니다.** 이게 없으면
  앱이 죽었는데도 배포가 초록불로 뜹니다.
- `--retry 12 --retry-delay 5` — 컨테이너가 뜰 때까지 최대 60초 기다립니다.

**"배포했다"가 아니라 "배포 후 살아있음을 확인했다"까지가 CD입니다.**

---

## 4. 두 파일 비교 요약

| 항목 | `01` (CI) | `07` (CI + CD) |
|---|---|---|
| 잡 구성 | `test` → `compose` | `test-and-build` → `deploy` |
| 트리거 | push(main)/PR/수동 | push(전체 브랜치)/PR/수동+입력 |
| `concurrency` | 없음 | 있음 (배포 충돌 방지) |
| `environment` | 없음 | `production` (승인 게이트 가능) |
| Secret | 불필요 | SSH 키 등 4개 |
| 스택 기동 | CI 러너에서 `up` 후 `down -v` | EC2에서 `up -d` (유지) |
| 최종 검증 | `/health/ready` (러너) | `/health/ready` (EC2) |
| 실패 시 | 로그 덤프 + 정리 | 잡 실패 → 배포 중단 |

---

## 5. 실제로 GitHub Actions에서 돌려 보기

### 5-1. push 전에 로컬에서 미리 검증

CI가 하는 일을 그대로 손으로 돌려 보면 빨간불을 미리 막을 수 있습니다.

```powershell
cd "C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project"

# CI 스텝 1 — 의존성 설치 (전역 오염을 피하려면 venv 권장)
python -m venv C:\Temp\venv
C:\Temp\venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt pytest

# CI 스텝 2 — 백엔드 계약 테스트
cd backend
python -m pytest test_app.py -q
cd ..

# CI 스텝 3 — Compose 문법 검증
docker compose config --quiet

# CI 스텝 4 — 이미지 3개 빌드
docker compose build
```

> Windows에서 가상환경 경로가 길면 `DLL load failed ... 너무 깁니다` 오류가 납니다.
> 위처럼 `C:\Temp\venv` 같은 짧은 경로에 만드세요. CI의 Linux 러너에서는 없는 문제입니다.

### 5-2. 배포 없이 CI만 시험하기 (권장 첫 실습)

`deploy` 잡의 `if`가 `refs/heads/main`을 요구하므로, **다른 브랜치로 push하면 CI만 돕니다.**
AWS 준비가 안 됐어도 안전하게 연습할 수 있습니다.

```powershell
cd "C:\수업 보관소\aidevs-latest"
git switch -c ci-practice
git add -A
git commit -m "Practice: trigger CI"
git push -u origin ci-practice
```

그다음 GitHub 리포 → **Actions** 탭 → 왼쪽에서 `07 Weather MCP CI CD` 선택 → 방금 실행 클릭.

확인할 것:

- 잡 이름 옆 상태 아이콘 (노랑 진행 / 초록 성공 / 빨강 실패)
- 스텝을 펼치면 실제 셸 출력이 그대로 보입니다
- `deploy` 잡이 **회색 skipped**로 표시되는지 — `if` 조건이 의도대로 작동한 증거입니다

### 5-3. 수동 실행 연습

Actions 탭 → 워크플로 선택 → 우측 **Run workflow** 버튼 → 브랜치 고르고 실행.
`07`은 `deploy` 체크박스가 함께 뜹니다. 체크를 풀고 실행하면 CI만 돕니다.

`workflow_dispatch`가 선언돼 있어야 이 버튼이 나타납니다. 또한 이 정의가 **기본 브랜치에
존재해야** 버튼이 보이므로, 처음이라면 CI 확인 후 main에 머지하세요.

### 5-4. 배포까지 돌리려면 (AWS 필요)

| 준비물 | 위치 |
|---|---|
| `production` 환경 생성 | Settings → Environments → New environment |
| `AWS_HOST` | Secrets → New repository secret (EC2 퍼블릭 IP/도메인) |
| `AWS_USER` | 같은 곳 (`ubuntu` 또는 `ec2-user`) |
| `AWS_SSH_PRIVATE_KEY` | 같은 곳 (`.pem` 파일 **전체 내용**, `-----BEGIN`부터 `-----END`까지) |
| `AWS_SSH_KNOWN_HOSTS` | 같은 곳 (아래 명령 결과) |

```bash
ssh-keyscan -H <EC2_IP>
```

EC2 쪽 준비:

```bash
# Docker 및 Compose v2 설치 확인
docker compose version

# .env 수동 업로드 (Git에 없으므로 필수)
mkdir -p ~/weather-mcp-deployment
vi ~/weather-mcp-deployment/.env
```

보안 그룹에서 8000(backend)·8501(frontend) 포트를 열어야 브라우저로 접근됩니다.

준비가 끝나면 main에 머지하거나, Run workflow에서 deploy를 체크해 실행합니다.

---

## 6. 안 될 때 확인 순서

| 증상 | 원인 | 해결 |
|---|---|---|
| Actions 탭에 워크플로가 **안 보임** | 파일이 루트 `.github/workflows/`에 없음 | 루트로 이동 |
| push했는데 **아무것도 안 돎** | `paths` 필터에 안 걸림 | 해당 경로 파일을 수정하거나 수동 실행 |
| `Run workflow` 버튼이 **없음** | `workflow_dispatch` 미선언, 또는 기본 브랜치에 없음 | 선언 추가 후 main에 머지 |
| YAML 파싱 에러 | 들여쓰기·따옴표 | 아래 로컬 검증 명령 |
| `No such file or directory` | 경로가 루트 기준이 아님 | `aidevs-main/aidevs-main/` 접두사 확인 |
| `deploy`가 계속 **skipped** | `if` 조건 미충족 | 브랜치가 main인지, deploy 입력을 체크했는지 |
| `deploy`가 **대기(waiting)** 상태 | `environment`에 승인자 설정됨 | Actions 화면에서 Approve |
| `Permission denied (publickey)` | SSH 키·권한 문제 | Secret에 키 전체가 들어갔는지, `chmod 600` |
| `Host key verification failed` | `known_hosts` 누락 | `ssh-keyscan -H <IP>` 결과를 Secret에 등록 |
| 배포는 성공인데 앱이 안 뜸 | `.env` 누락 | EC2의 `~/weather-mcp-deployment/.env` 확인 |

YAML 문법 로컬 검증:

```powershell
python -c "import yaml; yaml.safe_load(open('.github/workflows/07-weather-mcp-cicd.yml', encoding='utf-8')); print('YAML OK')"
```

---

## 7. 직접 해보기

1. `01-simple-compose-ci.yml`을 복사해 새 워크플로를 만들고, `paths`를 이 `practice` 폴더로
   바꿔 아무 파일이나 수정했을 때만 돌게 해보세요.
2. 일부러 테스트를 깨뜨려 push한 뒤, `if: failure()` 스텝이 로그를 남기는지 확인해 보세요.
3. `needs:`를 지우고 push해서 두 잡이 **동시에** 출발하는 것을 Actions 화면에서 눈으로
   확인해 보세요. 그리고 왜 CD에서 `needs`가 필수인지 생각해 보세요.
4. `concurrency.cancel-in-progress`를 `true`로 바꾸고 연속으로 두 번 push해, 앞 실행이
   취소되는지 보세요.

---

## 참고

- 워크플로 문법 전체: <https://docs.github.com/actions/reference/workflow-syntax-for-github-actions>
- 컨텍스트(`github`, `env`, `secrets`, `inputs`): <https://docs.github.com/actions/learn-github-actions/contexts>
- 표현식과 `if` 조건: <https://docs.github.com/actions/learn-github-actions/expressions>
