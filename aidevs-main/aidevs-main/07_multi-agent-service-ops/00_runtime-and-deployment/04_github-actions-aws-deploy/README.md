# 04 GitHub Actions AWS Deploy · 선택

03에서 EC2에 Compose를 직접 배포한 뒤, 같은 명령을 GitHub Actions가 실행하도록 자동화합니다. 처음부터 자동 배포만 따라 하지 않습니다.

```text
운영자가 CI 성공 Commit 확인
→ production 수동 승인
→ EC2에 새 Source 전달
→ Full Stack Compose Build·실행
→ Readiness Health 확인
```

이 예제는 `workflow_dispatch`만 사용합니다. 즉 CI가 성공했다고 자동 배포되는 구조가
아니라, 운영자가 해당 Commit의 CI 성공을 확인한 뒤 Actions 화면에서 수동으로 실행하는
안전한 첫 단계입니다.

## 초보자 권장 방식

수업에서는 별도 Container Registry와 Cluster를 추가하지 않고 GitHub Actions가 EC2의 배포
명령을 실행하는 최소 구조만 설명합니다. EC2는 새 서버이므로 `compose.full-stack.yml`로
Frontend·Backend·Redis·PostgreSQL을 함께 실행합니다. 운영 환경에서는 장기 AWS Access
Key보다 GitHub OIDC, Image Registry, 배포 이력과 Rollback을 사용해야 합니다.

## 실행 전 필수 조건

1. 03 수동 배포를 먼저 완료하고 EC2의 `~/aidevs-runtime/01_simple-multi-llm-compose/.env`에
   실제 LLM Key를 만들어 둡니다.
2. Repository Settings → Environments에서 `production` Environment를 만들고, 가능하면
   **Required reviewers**와 `main` Branch 제한을 설정합니다.
3. Workflow가 참조하는 Secret을 `production` Environment에 등록합니다.
4. GitHub-hosted Runner가 EC2의 SSH에 연결할 수 있는 네트워크 정책을 사전에 검토합니다.
   03의 기본 Security Group은 SSH를 `My IP`로만 허용하므로 GitHub-hosted Runner는 기본적으로
   접속할 수 없습니다. 문제 해결을 위해 SSH `0.0.0.0/0`을 열면 안 됩니다.

마지막 항목 때문에 이 예제는 운영자가 네트워크 접근을 별도로 승인한 제한된 교육 환경에서만
실행합니다. 실제 운영에서는 SSM, VPN, Bastion, 또는 보안 정책에 맞는 self-hosted Runner를
검토합니다.

## 필요한 GitHub Environment Secret 예시

```text
AWS_HOST
AWS_USER
AWS_SSH_PRIVATE_KEY
AWS_SSH_KNOWN_HOSTS
```

| Secret | 값 | 주의 |
| --- | --- | --- |
| `AWS_HOST` | EC2 Public DNS 또는 IP | 화면·로그에 불필요하게 출력하지 않음 |
| `AWS_USER` | Amazon Linux 기본 사용자 `ec2-user` | 교육 이미지에 맞는 사용자 확인 |
| `AWS_SSH_PRIVATE_KEY` | 배포 전용 SSH Private Key 전체 | `.pem`을 Git에 넣지 않음 |
| `AWS_SSH_KNOWN_HOSTS` | 운영자가 EC2 지문을 확인한 `known_hosts` 한 줄 이상 | 실행 중 `ssh-keyscan`으로 신뢰하지 않음 |

`AWS_SSH_KNOWN_HOSTS`는 신뢰할 수 있는 관리자 네트워크에서 EC2 지문을 확인한 뒤 준비합니다.
지문이 바뀌면 원인을 확인한 뒤에만 Secret을 갱신합니다. LLM API Key는 GitHub Workflow 로그에
출력하지 않고 EC2의 권한 제한된 `.env`에서 관리합니다.

### AWS_SSH_KNOWN_HOSTS 생성

이 단계는 앞의 EC2 실습에서 로컬 PC로 SSH 접속에 성공하여 Host Key가 이미
`$env:USERPROFILE\.ssh\known_hosts`에 저장됐다는 전제로 진행합니다. 서버에 다시 접속하거나
서버의 `.ssh`를 수정하지 않고 로컬 파일을 조회합니다. `SHA256:...` Fingerprint만
Secret에 입력하는 것이 아닙니다.

```powershell
$knownHost = ssh-keygen -F <PUBLIC_IPV4_OR_DNS> `
  -f "$env:USERPROFILE\.ssh\known_hosts" |
  Select-String "ssh-ed25519" |
  ForEach-Object { $_.Line }

$knownHost
$knownHost | Set-Clipboard
```

출력된 `<EC2 주소> ssh-ed25519 <긴 공개 Host Key>` 한 줄 전체를 GitHub
`production → Environment secrets`의 `AWS_SSH_KNOWN_HOSTS` 값으로 붙여 넣습니다. `# Host
... found` 주석은 제외합니다. Windows `ssh-keyscan`에서 `unsupported KEX method`가 나면
위처럼 이미 저장된 `known_hosts`를 조회합니다. EC2 Public IP가 바뀌면 `AWS_HOST`와 함께
갱신합니다.

조회 결과가 없다면 주소 변경 또는 최초 접속을 하지 않은 예외이므로, 이때만 EC2 주소와
Fingerprint를 확인하고 SSH로 한 번 접속한 뒤 다시 조회합니다.

## 배포 안전 조건

1. CI 테스트와 Image Build가 먼저 통과합니다.
2. GitHub `production` Environment 승인을 사용합니다.
3. 동일 EC2에 두 배포가 겹치지 않도록 `concurrency`를 사용합니다.
4. Backend Readiness Health가 실패하면 배포 성공으로 처리하지 않습니다.
5. Workflow는 EC2의 기존 `.env`를 복사·출력·덮어쓰지 않습니다.
6. 학생은 실습 종료 후 EC2·EBS·Security Group을 직접 확인하고 정리합니다.

## 실행 순서

1. `.github/workflows/07-runtime-deploy-example.yml`을 저장소의 `workflows` 폴더로 복사해
   사용하는 경우, 경로·Repository 설정·Secret 이름을 자신의 환경에 맞춥니다.
2. 해당 Workflow 파일을 Commit·Push합니다.
3. 대상 Commit에서 `07 Runtime CI`가 성공했는지 확인합니다.
4. Actions에서 Deploy Workflow를 열고 **Run workflow**를 선택합니다.
5. `production` 승인 대기 상태가 나오면 지정된 검토자가 승인합니다.
6. EC2에서 `docker compose -f compose.full-stack.yml ps`와
   `curl http://127.0.0.1:8000/health/ready`로 결과를 확인합니다.

실제 CD Workflow는 계정·Repository·EC2 설정이 필요한 선택 자료이므로 자동으로 활성화하지 않습니다. `workflow_dispatch` 기반으로 복사해 사용하는 예제만 제공합니다.
