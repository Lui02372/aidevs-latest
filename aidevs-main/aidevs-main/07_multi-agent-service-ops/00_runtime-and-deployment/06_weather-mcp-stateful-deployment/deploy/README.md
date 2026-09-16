# Stateful Weather AWS EC2 자동 배포 준비

## 1. EC2 준비

Amazon Linux 2023 EC2에 Docker와 Docker Compose Plugin을 설치합니다. Security Group은 SSH
22와 Frontend 8501만 허용하고, 8000·8010은 인터넷에 공개하지 않습니다.

EC2에 배포 폴더와 Secret 환경 파일을 최초 한 번 준비합니다.

```bash
mkdir -p ~/weather-stateful
cd ~/weather-stateful
nano .env
chmod 600 .env
```

```ini
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=agent_pwd
POSTGRES_DB=agent_db
WEATHER_CACHE_TTL_SECONDS=600
```

Workflow는 이 `.env`를 GitHub에서 복사하거나 로그로 출력하지 않습니다.

프로젝트 파일을 최초 한 번 전송한 뒤 PostgreSQL·Redis를 실행합니다.

```bash
cd ~/weather-stateful
docker compose -f compose.infrastructure.yml up -d
docker compose -f compose.infrastructure.yml ps
```

이후 GitHub Actions는 `compose.application.yml`만 재배포합니다. 인프라 Compose와 Volume을
배포 Workflow에서 내리지 않습니다.

## 2. GitHub production Environment

Repository `Settings → Environments → New environment`에서 `production`을 만듭니다. 가능한
계정에서는 Required reviewers와 `main` Branch 제한을 설정합니다.

다음 Environment Secret을 등록합니다.

| Secret | 내용 |
| --- | --- |
| `AWS_HOST` | EC2 Public DNS 또는 IP |
| `AWS_USER` | Amazon Linux의 `ec2-user` |
| `AWS_SSH_PRIVATE_KEY` | 배포용 Private Key 전체 |
| `AWS_SSH_KNOWN_HOSTS` | 관리자가 지문을 확인한 EC2 known_hosts 항목 |

### AWS_SSH_KNOWN_HOSTS 생성

앞 단계에서 로컬 PC의 SSH 접속이 이미 성공했으므로 Host Key도 Windows 사용자의
`known_hosts`에 저장되어 있습니다. 서버에 다시 접속하거나 서버의 `.ssh`를 수정하지 않고
로컬 PowerShell에서 `ssh-ed25519` 한 줄 전체를 Clipboard에 복사합니다. Fingerprint
`SHA256:...`만 Secret에 넣지 않습니다.

```powershell
$knownHost = ssh-keygen -F <PUBLIC_IPV4_OR_DNS> `
  -f "$env:USERPROFILE\.ssh\known_hosts" |
  Select-String "ssh-ed25519" |
  ForEach-Object { $_.Line }

$knownHost
$knownHost | Set-Clipboard
```

출력 형식은 다음과 같으며 `...`가 아니라 실제 긴 값 전체를 등록합니다.

```text
<PUBLIC_IPV4_OR_DNS> ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA...
```

GitHub `production` Environment에 `Name: AWS_SSH_KNOWN_HOSTS`, `Secret: 복사한 한 줄
전체`로 저장합니다. EC2 Public IP가 바뀌면 `AWS_HOST`와 이 Secret을 함께 갱신합니다.
05와 같은 EC2·주소·`production` Environment를 재사용하면 기존 Secret을 그대로 사용하고
06용으로 다시 등록하지 않습니다. 조회 결과가 없는 예외에만 주소와 Fingerprint를 확인하며
SSH로 한 번 접속한 뒤 다시 조회합니다.

GitHub-hosted Runner에서 EC2 SSH로 접근 가능한 네트워크 정책이 별도로 필요합니다. 이를
해결하기 위해 22번 Port를 `0.0.0.0/0`으로 열지 않습니다. 실제 운영에서는 SSM, VPN,
Bastion 또는 보안 정책에 맞는 self-hosted Runner를 사용합니다.

## 3. 배포 흐름

```text
개인 브랜치 Push 또는 Pull Request
→ Fake MCP·LLM Backend Test
→ Compose 검사
→ Frontend·Backend·MCP Image Build
→ main 병합
→ 같은 CI 재실행·성공
→ production 승인
→ EC2 Source 복사·Application Compose만 실행
→ /health/ready 성공
```

## 4. EC2 확인과 복구

```bash
cd ~/weather-stateful
docker compose -f compose.infrastructure.yml ps
docker compose -f compose.application.yml ps
docker compose -f compose.application.yml logs --tail=100 weather-mcp backend frontend
curl --fail http://127.0.0.1:8000/health/ready
```

배포 후 문제가 있으면 GitHub에서 마지막 정상 Commit으로 되돌린 새 Commit을 만든 뒤 같은
승인 절차로 다시 배포합니다. 이 입문 예제는 Blue/Green이나 자동 Rollback을 구현하지 않습니다.
