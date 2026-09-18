# 02 GitHub Actions — 처음 CI를 성공시키는 순서

목표는 GitHub에서 **테스트 → Compose 검사 → Docker Build가 초록색으로 끝나는 것**입니다.
이 단계에는 EC2, AWS 키, 실제 LLM 키가 필요 없습니다. CI가 성공해도 서버가 배포되지는 않습니다.

## 1. 내 PC와 GitHub의 역할

| 위치 | 실행하는 것 |
| --- | --- |
| 내 PC PowerShell | launcher, Git 커밋/Push, 로컬 테스트 |
| GitHub Runner | workflow YAML의 run 명령, 테스트, Docker Build |
| EC2 Linux | 나중에 CD로 전달받은 앱 실행 |
| GitHub Actions 화면 | 실행 시작, 진행 상태, 오류 로그 확인 |

Push는 로컬 커밋을 GitHub로 보내는 작업입니다.
Pull Request는 변경 사항을 합치자고 요청하는 것이며 git pull과 다릅니다.
workflow의 job은 작업 묶음, step은 그 안의 실행 순서입니다.

## 2. Workflow를 올바른 위치에 복사

준비된 파일은 [runtime-ci.yml](../runtime-ci.yml)입니다.
지금 이 파일은 수업 예제 위치에 있으므로 자동으로 실행되지 않습니다.
**Git 저장소 최상위의 .github/workflows/runtime-learning-ci.yml**로 복사해야 합니다.
탐색기에서 보이는 프로젝트 폴더가 Git 저장소 루트와 같다고 가정하지 마세요.

아래는 Windows PowerShell에서 00_runtime-and-deployment 폴더를 기준으로 실행합니다.

~~~powershell
$repoRoot = git rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0) { throw 'Git 저장소 안에서 실행하세요.' }
$workflows = Join-Path $repoRoot '.github/workflows'
New-Item -ItemType Directory -Force -Path $workflows | Out-Null
$destination = Join-Path $workflows 'runtime-learning-ci.yml'
if (Test-Path -LiteralPath $destination) { throw '기존 workflow가 있습니다. 내용을 비교한 뒤 수동으로 갱신하세요.' }
Copy-Item -LiteralPath '.\02_github-actions-ci\runtime-ci.yml' -Destination $destination
~~~

예제는 launcher.json 위치를 찾아 실습 경로를 계산하므로 저장소 안에
aidevs-main 폴더가 여러 단계 있어도 동작합니다.
launcher.json이 같은 저장소에 두 개 있으면 잘못된 폴더를 선택하지 않고 실패합니다.
CI는 01·01-2·01-3·05·06·07 각각 별도 Runner에서 테스트하고 Build합니다.

## 3. 커밋하고 GitHub에 보내기

~~~powershell
git status --short
git remote -v
git branch --show-current
~~~

자신이 Push할 수 있는 GitHub 저장소인지 확인합니다. 수업 원본에 권한이 없다면 본인 Fork를 사용합니다.
GitHub Desktop을 사용해도 됩니다. 변경 목록에서 이번 실습 코드와 workflow를 선택하고
커밋한 다음 Push합니다. **.env, .pem, .venvs, 설치 로그는 선택하지 않습니다.**
CLI에서는 아래처럼 추가할 파일을 명시합니다.

~~~powershell
git add -- "$destination"
# 변경 목록에서 확인한 launcher/실습 파일도 필요한 것만 git add 합니다.
git diff --cached --stat
git diff --cached --name-only
git commit -m "Add runtime learning CI"
git push
~~~

현재 브랜치에 upstream이 없다는 안내가 나오면 안내에 표시된
git push --set-upstream origin 브랜치명을 사용합니다.
예제 CI의 Push 트리거는 모든 브랜치에 동작합니다.
수동 Run workflow 버튼은 이 workflow가 저장소 **기본 브랜치**에 있어야 나타납니다.
개발 브랜치에서 먼저 Push CI를 확인한 뒤 PR로 기본 브랜치에 합치면 됩니다.
동일한 기존 CI가 있으면 실행이 둘 생길 수 있으므로 Actions의 이름을 구분하세요.

## 4. GitHub 화면에서 첫 성공 확인

1. GitHub 저장소 → Actions.
2. 왼쪽에서 **Runtime Learning CI** 선택.
3. 최신 실행을 열어 Branch와 Commit이 방금 Push한 것인지 확인.
4. test-and-build의 각 프로젝트 Job을 열기.
5. Checkout → Python → Locate runtime → Install → Test → Compose check and build 순으로 확인.
6. 전부 초록색이면 이번 단계 완료. EC2 서비스가 바뀐 것은 아닙니다.

수동 실행: Actions → Runtime Learning CI → Run workflow → Branch 선택 → Run workflow.
버튼이 없으면 workflow_dispatch, 기본 브랜치의 파일, 저장소 쓰기 권한을 확인합니다.
Fork에서 Actions가 비활성화되어 있으면 안내에 따라 워크플로 실행을 활성화합니다.

## 5. YAML 읽기

| 항목 | 의미 |
| --- | --- |
| on.push / pull_request | Push/PR 때 실행 |
| on.workflow_dispatch | 수동 실행 버튼 제공 |
| permissions.contents: read | 소스 읽기 권한 |
| strategy.matrix.project | 프로젝트별 별도 환경에서 반복 |
| runs-on: ubuntu-latest | 내 PC 대신 GitHub Linux VM 사용 |
| uses | 공개 Action 사용 |
| run | 해당 VM에서 셸 명령 실행 |
| working-directory | 해당 Step의 명령 기준 폴더 |

requirements는 각 실습 backend 파일을 사용합니다.
테스트에서 Provider를 가짜 클라이언트로 바꾸므로 API 키를 Secrets에 등록할 필요 없습니다.
Compose 검사에는 --quiet를 사용해 해석된 환경변수가 로그에 나오지 않도록 합니다.
Build는 이미지를 Runner에 만들고 끝나며 Registry Push나 EC2 배포는 하지 않습니다.

## 6. 빨간색일 때 보는 순서

실패한 실행 → 실패 Job → **가장 먼저 실패한 Step**을 펼칩니다.
오류 위의 실제 실행 명령과 처음 나타난 오류 문장을 같이 읽으세요.

| 실패 | 해결 |
| --- | --- |
| Locate runtime | launcher.json을 포함해 커밋했는지, 중복된 실습 사본이 있는지 확인 |
| Install / No such file | requirements와 코드 경로가 함께 커밋되었는지 확인 |
| ModuleNotFoundError | 해당 실습 requirements와 import 확인 |
| Test / AssertionError | 실패 테스트 이름과 기대값 확인 후 로컬에서도 재현 |
| Compose config | YAML 들여쓰기·누락 파일 확인 |
| Docker Build / COPY | Dockerfile 기준 build context 안에 소스가 있는지 확인 |
| 결제·사용량·Actions 제한 | 저장소 Settings의 Actions 정책과 계정 실행 한도 확인 |

코드를 수정했다면 새 Commit/Push로 다시 실행합니다.
일시적인 다운로드 실패라면 Re-run failed jobs를 사용할 수 있지만 기존 코드 그대로 재실행됩니다.

로컬 재현 예시(00 폴더 기준):

~~~powershell
.\.venvs\compose\Scripts\python.exe -m pytest .\01_simple-multi-llm-compose\backend -q
.\.venvs\weather\Scripts\python.exe -m pytest .\07_integrated-bedrock-mcp\backend -q
.\launcher.cmd -Target 07 -Action check
~~~

## 7. 다음은 CD

CI 초록색 성공 → [03 EC2 연결](../../03_aws-ec2/doc/ConnectGuide.md) →
[04 GitHub Actions CD](../../04_github-actions-aws-deploy/doc/ConnectGuide.md)로 이동합니다.
CI 성공, EC2 접속 성공, CD 성공은 서로 다른 완료 조건입니다.

공식 근거:
[수동 실행](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow),
[실행 이벤트](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).
