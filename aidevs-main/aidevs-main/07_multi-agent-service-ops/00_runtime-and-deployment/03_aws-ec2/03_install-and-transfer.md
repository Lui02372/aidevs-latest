# 03 Docker 설치와 코드 전송

## 1. SSH 접속

로컬 PowerShell에서 실제 Key 경로와 Public DNS로 바꿉니다.

```powershell
ssh -i "C:\Users\<사용자>\.ssh\multi-agent-course.pem" ec2-user@<PUBLIC_DNS>
```

Ubuntu Server 24.04 LTS를 선택했다면 기본 사용자는 `ubuntu`입니다.

```powershell
ssh -i "C:\Users\<사용자>\.ssh\multi-agent-course.pem" ubuntu@<PUBLIC_DNS>
```

첫 연결에서는 서버 지문을 확인하는 질문이 나타날 수 있습니다. 대상 Public DNS가
본인이 만든 인스턴스와 일치하는지 먼저 확인합니다.

`172.31.x.x`, `10.x.x.x`, `192.168.x.x` 형식은 VPC 내부에서 사용하는 Private IP입니다.
인터넷의 수강생 PC에서는 이 주소로 직접 SSH 접속하지 않습니다. EC2 상세 화면의 `Public
IPv4 address` 또는 `Public IPv4 DNS`를 사용합니다.

```powershell
ssh -i "C:\Users\<사용자>\.ssh\multi-agent-course.pem" ubuntu@<PUBLIC_IPV4>
```

Public IPv4가 비어 있다면 다음을 확인합니다.

1. Instance가 Public Subnet에 생성되었는지 확인합니다.
2. Subnet Route Table에 `0.0.0.0/0 → Internet Gateway`가 있는지 확인합니다.
3. 새 Instance를 만들 때 `Auto-assign public IP`를 `Enable`로 설정합니다.
4. 기존 Instance를 유지해야 한다면 Elastic IP 할당·연결을 검토합니다. Elastic IP는 과금
   조건이 있으므로 수업에서는 강사의 지시에 따릅니다.

### Windows에서 `UNPROTECTED PRIVATE KEY FILE`이 표시될 때

PEM 파일을 다른 로컬 사용자나 `BUILTIN\Users` 그룹도 읽을 수 있으면 Windows OpenSSH는
Private Key를 무시합니다. 로컬 PowerShell에서 실제 Key 경로로 다음을 실행합니다.

```powershell
$keyPath = "C:\mini\weather-mcp-key.pem"
icacls $keyPath /inheritance:r
icacls $keyPath /grant:r "$($env:USERNAME):(R)"
icacls $keyPath /remove:g "BUILTIN\Users"
icacls $keyPath
```

`BUILTIN\Users` 제거 명령이 언어 설정 때문에 대상을 찾지 못하면 오류에 표시된 SID를
사용합니다.

```powershell
icacls $keyPath /remove:g '*S-1-5-32-545'
```

현재 사용자에게 `(R)` 권한이 있고 일반 Users 그룹이 제거됐는지 확인한 후 다시
접속합니다. PEM 내용은 열거나 화면에 출력하지 않습니다.

## 2. Docker Engine 설치

### Amazon Linux 2023

EC2 터미널에서 실행합니다.

```bash
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
```

### Ubuntu Server 24.04 LTS

Ubuntu를 선택했다면 다음 명령을 사용합니다.

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git curl
sudo systemctl enable --now docker
sudo usermod -aG docker ubuntu
```

그룹 변경을 적용하려면 SSH 연결을 종료하고 다시 접속합니다.

```bash
exit
```

재접속 후 확인합니다.

```bash
docker info
docker compose version
docker run --rm hello-world
```

`Hello from Docker!`가 출력되면 일반 사용자가 Docker Engine에 연결하여 Image를 받고
Container를 실행할 수 있다는 뜻입니다. `--rm` 때문에 실행이 끝난 Container는 자동으로
삭제되지만 Image는 남을 수 있습니다.

권한 오류가 계속되면 Docker 서비스 상태를 확인하고, 필요하면 교육 담당자의
안내에 따라 인스턴스를 재부팅합니다.

## 3. Docker Compose Plugin

먼저 설치 여부를 확인합니다.

```bash
docker compose version
```

Amazon Linux에서 명령이 없다면 RPM 기반 Linux의 Docker Compose Plugin 설치를 시도합니다.

```bash
sudo yum update -y
sudo yum install -y docker-compose-plugin
docker compose version
```

Ubuntu에서 명령이 없다면 다음을 사용합니다.

```bash
sudo apt update
sudo apt install -y docker-compose-v2
docker compose version
```

패키지를 찾지 못하면 임의 블로그 명령을 실행하지 말고
[Docker 공식 Linux Compose 설치 문서](https://docs.docker.com/compose/install/linux/)를
확인합니다. 수동 설치는 자동 업데이트되지 않으므로 강사가 버전을 지정한 경우에만
사용합니다.

## 4. 코드 전송 방법 A: 공개 교육 저장소

저장소가 공개되어 있고 Secret이 없을 때만 사용합니다.

```bash
git clone <PUBLIC_REPOSITORY_URL> aidevs
cd aidevs/07_multi-agent-service-ops/00_runtime-and-deployment/01_simple-multi-llm-compose
```

Private Repository 인증 Token을 명령이나 Git URL에 직접 넣지 않습니다.

## 5. 코드 전송 방법 B: SCP

저장소 공개가 불가능하면 Simple Compose 폴더만 전송합니다.

프로젝트 폴더 안에 `.venv`, `.env`, `__pycache__`, `.pytest_cache`가 있다면 폴더 전체를
`scp -r`로 보내지 않습니다. `.venv`는 작은 파일이 매우 많아 전송이 오래 걸리고 `.env`에는
Secret이 들어 있습니다. 배포에 필요한 Source·Dockerfile·Compose 파일만 선택하여
전송하거나 프로젝트별 README의 선택 복사 명령을 사용합니다.

로컬 PowerShell:

```powershell
scp -i "C:\Users\<사용자>\.ssh\multi-agent-course.pem" -r `
  "C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose" `
  ec2-user@<PUBLIC_DNS>:~/simple-compose
```

EC2 터미널:

```bash
cd ~/simple-compose
ls
```

다음 파일이 보여야 합니다.

```text
backend
frontend
database
compose.yml
compose.full-stack.yml
README.md
```

## 6. 실제 LLM 환경 변수

EC2 안에서 `.env`를 만들고 Key를 입력합니다.

```bash
cp .env.example .env
nano .env
```

```dotenv
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
OLLAMA_ENABLED=false
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2
```

`.env`를 Git에 추가하거나 `cat .env` 결과를 화면 공유하지 않습니다.

이 EC2 실습은 새 서버에서 Redis와 PostgreSQL도 함께 만들므로 이후 명령은
`compose.full-stack.yml`을 사용합니다. `compose.yml`은 기존 공용 Container가 있는 수업
PC 전용 파일입니다.

## 공식 문서

- [Amazon Linux 2023 EC2에 Docker 설치](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-container-image.html)
- [Docker Compose Plugin 설치](https://docs.docker.com/compose/install/linux/)


