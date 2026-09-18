# 04 GitHub Actions CD 연결 가이드

**처음에는 02 CI부터 성공시킨 후 배포를 수동으로 한 번 실행하세요.**
CI는 검증이고 CD는 EC2에서 실행 중인 서비스를 바꾸는 단계입니다.
이 문서는 로컬 PowerShell, GitHub 설정 화면, EC2 bash를 구분해서 안내합니다.

## 어떤 배포 방식을 선택하나요?

| 학습 대상 | 방식 | 설정 |
| --- | --- | --- |
| 01 Compose를 이미 EC2에서 수동 실행함 | 기존 SSH 배포 예제 | AWS_HOST 등 Secret 4개 |
| 07 통합 실습 | OIDC → S3 → SSM | AWS 역할 + GitHub Variable 4개 |

둘 중 하나를 선택합니다. 07을 배포할 때 01 SSH workflow를 쓰지 마세요.
05·06의 SSH 방식은 각 폴더 deploy/README.md에서 소스/배포 위치를 확인합니다.
GitHub Runner는 내 PC가 아니므로 EC2 SSH가 내 IP에만 열려 있으면 Runner는 접속하지 못합니다.
그때 SSH 포트를 전체 공개하는 대신 SSM 경로 또는 승인된 내부 Runner를 사용합니다.

## 07 OIDC/SSM 배포 (권장)

### A. AWS를 먼저 준비

1. 07 [README의 EC2·VPC 준비](../../07_integrated-bedrock-mcp/README.md)를 따라
   EC2에 Docker, Compose, AWS CLI, SSM Agent를 준비합니다.
2. 소스 보관용 비공개 S3 버킷을 만들고 퍼블릭 액세스 차단을 유지합니다.
3. [IAM 정책 템플릿](../../07_integrated-bedrock-mcp/deploy/iam-policies.md)의
   ACCOUNT_ID, REGION, BUCKET, INSTANCE_ID, OWNER/REPO를 자신의 값으로 바꿉니다.
4. EC2 IAM 역할에 AmazonSSMManagedInstanceCore와 해당 버킷 weather-07/* 읽기 권한을 연결합니다.
5. IAM의 OIDC Provider에 token.actions.githubusercontent.com, Audience sts.amazonaws.com을 등록합니다.
6. GitHub 배포 역할의 trust를 repo:OWNER/REPO:environment:production으로 제한하고,
   템플릿의 S3 업로드·SSM 실행/조회 권한을 부여합니다.
7. Systems Manager에서 대상 EC2가 Online인지 확인합니다.
   Offline이면 Agent, 인스턴스 역할, HTTPS 아웃바운드/SSM endpoint 연결부터 확인합니다.

EC2의 S3 읽기 역할과 GitHub의 배포 역할은 서로 다릅니다.
장기 AWS Access Key와 PEM은 이 workflow에 필요 없습니다.
OpenAI/Gemini API 키는 AWS IAM 인증과 별개입니다.

### B. EC2에서 .env 준비

**EC2 bash**에서 실행합니다.

~~~bash
sudo install -d -m 700 /opt/weather-07/shared
sudo touch /opt/weather-07/shared/.env
sudo chmod 600 /opt/weather-07/shared/.env
sudo nano /opt/weather-07/shared/.env
~~~

07/.env.example의 항목을 참고하여 실제 키 하나와 DB 설정을 입력합니다.
기존 파일이 있으면 필요한 항목만 편집합니다. 내용을 로그에 출력하지 않습니다.
배포 스크립트는 이 파일이 비어 있으면 실패하며 GitHub에서 덮어쓰지 않습니다.
EC2에서 aws --version, docker compose version이 동작해야 합니다.
이미 다른 실습이 8000/8501을 사용하면 해당 앱을 중지합니다.

### C. GitHub Environment 연결

GitHub 저장소 → Settings → Environments → New environment → **production**을 만듭니다.
배포 가능 브랜치는 main으로 제한합니다.
계정/저장소에서 지원하면 Required reviewers를 설정합니다.
승인은 Environment 보호 규칙을 설정한 경우에만 나타납니다.

production의 **Environment variables**에 다음 네 개를 등록합니다.

| 이름 | 실제 입력값 예 |
| --- | --- |
| AWS_REGION | ap-northeast-2 등 실제 EC2 Region |
| ARTIFACT_BUCKET | 생성한 S3 버킷 이름만, s3:// 제외 |
| EC2_INSTANCE_ID | i-로 시작하는 대상 인스턴스 ID |
| AWS_DEPLOY_ROLE_ARN | GitHub OIDC 배포 역할의 전체 ARN |

이 workflow는 vars를 읽습니다. Secrets에만 등록하면 값이 비어 실패합니다.
LLM 키는 EC2 .env에만 둡니다.

### D. Workflow 복사와 경로 설정

**Windows PowerShell, 00_runtime-and-deployment 폴더**에서 실행합니다.

~~~powershell
$repoRoot = git rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0) { throw 'Git 저장소를 찾지 못했습니다.' }
$source = '.\07_integrated-bedrock-mcp\deploy\github-actions.yml'
$destination = Join-Path $repoRoot '.github/workflows/07-integrated-bedrock-mcp.yml'
New-Item -ItemType Directory -Force (Split-Path $destination) | Out-Null
if (Test-Path -LiteralPath $destination) { throw '기존 workflow를 먼저 비교하세요. 자동으로 덮어쓰지 않습니다.' }
Copy-Item -LiteralPath $source -Destination $destination
git ls-files --full-name -- '07_integrated-bedrock-mcp/compose.application.yml'
notepad $destination
~~~

git ls-files 출력에서 /compose.application.yml을 뺀 경로가 YAML의 PROJECT_DIR입니다.
출력이 없으면 해당 소스가 아직 Git에 추가되지 않은 상태입니다.
git rev-parse --show-toplevel과 실제 소스 위치를 비교해 Git 루트 기준 상대 경로를 입력하세요.
Windows의 C:\... 절대 경로는 GitHub Linux Runner에서 사용할 수 없습니다.

**첫 Push 전에** 복사한 workflow의 deploy Job if를 다음 한 줄로 바꿉니다.
이렇게 해야 CI 설정 중 main Push가 서버를 배포하지 않습니다.

~~~yaml
    if: github.ref == 'refs/heads/main' && github.event_name == 'workflow_dispatch' && inputs.deploy
~~~

기존 템플릿은 main Push 시 CI 후 배포하도록 작성되어 있으므로 이 차이를 꼭 확인합니다.
기본 브랜치가 main이 아니라면 workflow의 push.branches, if, Environment 브랜치 제한을 함께 맞춥니다.
변경한 workflow와 07 소스를 검토 후 Commit/Push하고 기본 브랜치에 반영합니다.
구형 배포 workflow가 동일 EC2를 대상으로 하면 중복 실행되지 않도록 비활성화합니다.

### E. Actions에서 실행하기

1. Actions → **07 Integrated Weather MCP** → Run workflow.
2. Branch main, deploy를 체크하지 않고 실행: ci만 성공, deploy는 skipped여야 합니다.
3. 다시 Run workflow → Branch main → deploy 체크 → 실행.
4. ci가 초록색인지 확인. 실패하면 needs: ci 때문에 deploy는 시작하지 않습니다.
5. production 승인이 설정되어 있으면 Review deployments에서 지정된 검토자가 승인.
6. deploy에서 AWS 인증 → S3 업로드 → SSM 실행 결과 대기를 확인.
7. deploy까지 초록색이면 EC2의 readiness 검사가 통과한 것입니다.
8. [03의 SSH 터널](../../03_aws-ec2/doc/ConnectGuide.md)로 화면에 접속하고 실제 요청을 보냅니다.

실행마다 같은 Commit의 소스 artifact를 EC2에 전달합니다.
SSM 명령을 접수했다고 성공으로 끝내지 않고 명령 종료 결과까지 기다립니다.
처음 수동 배포가 성공한 뒤에만 원본 if( main Push 또는 수동 deploy )로 되돌려
main 병합 → CI → CD 자동화를 켭니다.

### F. 실패를 해석하기

| 실패한 지점 | 확인 |
| --- | --- |
| AssumeRoleWithWebIdentity | OIDC Provider, role ARN, OWNER/REPO, production 이름과 trust sub |
| Region / Bucket / Instance 빈 값 | production Variables에 등록했는지 |
| S3 AccessDenied | GitHub PutObject / EC2 GetObject 권한을 각각 확인 |
| InvalidInstanceId / Offline | 실제 Region·Instance ID, SSM Agent·인스턴스 역할 |
| SSM Failed / .env 없음 | /opt/weather-07/shared/.env 위치와 파일 내용 존재 |
| Docker Build 실패 | EC2 디스크·메모리·인터넷 egress, SSM 명령 출력 |
| health 실패 | EC2에서 Compose ps/logs, DB 자격정보와 최초 스키마 |
| 브라우저 연결 실패 | 07은 loopback 바인딩, SSH 터널 확인 |

SSM 실패 시 workflow 로그의 command_id로 Systems Manager → Run Command에서 해당 실행을 엽니다.
EC2에서 아래 명령은 **성공한 배포가 current 링크를 만든 이후** 사용할 수 있습니다.

~~~bash
cd /opt/weather-07/current
docker compose -f compose.infrastructure.yml ps
docker compose -f compose.application.yml ps
docker compose -f compose.application.yml logs --tail 80 backend
curl --fail http://127.0.0.1:8000/health/ready
~~~

첫 배포 실패 시 /opt/weather-07/releases/실패한_COMMIT_SHA 폴더에서 같은 명령을 실행합니다.
실패 시 자동 롤백은 하지 않습니다. 마지막 정상 Commit의 코드로 복구하는 별도 배포를 수행하고,
DB 스키마 호환성을 확인합니다. DB 볼륨은 삭제하지 않습니다.

## 01 SSH 배포를 선택한 경우

[기존 SSH 예제](../07-runtime-deploy-example.yml)를 Git 루트 .github/workflows에 복사합니다.
복사한 YAML의 scp 소스 경로를 현재 Git 루트 기준 01 폴더 경로로 수정합니다.
02 CI와 03 수동 배포가 성공한 Commit을 선택합니다.
production의 **Environment secrets**에 아래를 등록합니다.

| Secret | 값 |
| --- | --- |
| AWS_HOST | EC2 Public IP/DNS |
| AWS_USER | ubuntu 또는 ec2-user |
| AWS_SSH_PRIVATE_KEY | 배포용 개인 키 전체 |
| AWS_SSH_KNOWN_HOSTS | 지문 확인을 마친 known_hosts의 호스트 공개키 한 줄 |

known_hosts는 [기존 README](../README.md#aws_ssh_known_hosts-생성)의 명령으로 준비합니다.
SHA256 지문 문자열만 넣으면 안 됩니다.
EC2의 ~/aidevs-runtime/01_simple-multi-llm-compose/.env를 미리 설정해야 합니다.
Actions → 07 Runtime Deploy Example → Run workflow로 실행합니다.
이 SSH 예제에는 자동 CI 의존성이 없으므로 동일 Commit의 CI 성공을 직접 확인해야 합니다.
SSH Timeout이면 Runner 네트워크 접근 문제입니다. PC의 SSH 성공과 구분하세요.

## 완료 기준

- CI: 실제 키 없이 테스트·Build 성공
- CD: 같은 Commit의 EC2 배포 및 readiness 성공
- 사용자 확인: 브라우저에서 실제 요청 성공
- 운영 확인: 재배포 후 DB 데이터 유지
