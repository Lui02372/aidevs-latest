## 프로젝트와 실행 순서

### 처음 따라갈 순서

1. **이미 실행했는지 먼저 확인합니다.** Project Player의 **9번 서버 실행 기능**으로 시작했다면 다시 서버를 띄우지 말고 [접속과 화면 실습](#화면에서-날씨-조회)으로 이동하세요. 현재 서버 동작 여부는 이 문서 작성 중 확인하지 않았습니다.
2. **Docker 실행 환경을 준비합니다.** [PowerShell](#powershell)에서 작업 폴더와 필요한 도구를 확인합니다. 권장 경로는 Windows에서 Docker로 전체 앱을 실행하는 방식입니다.
3. **프로젝트 설정과 인증을 준비합니다.** [환경변수](#환경변수)에서 `.env.example`을 복사하고 DB 비밀번호를 정합니다. 완성된 날씨 답변까지 확인하려면 Bedrock 인증과 모델 ID가 필요합니다.
4. **인프라부터 앱 순서로 실행합니다.** [Docker](#docker)의 순서대로 PostgreSQL·Redis → MCP·백엔드·프론트엔드를 시작합니다. Project Player로 실행한다면 수동 시작 명령을 중복 실행하지 마세요.
5. **연결과 실제 결과를 확인합니다.** [예제 학습](#예제-학습)에서 MCP 자료 조회 → 날씨 답변 → 캐시 → 실행 이력을 확인합니다. LLM 인증이 없다면 MCP 실습까지만 진행할 수 있습니다.
6. **실습을 종료합니다.** [종료](#종료)에서 앱을 먼저, 인프라를 나중에 종료합니다. 데이터 볼륨은 보존합니다.
7. **자동 검사와 배포를 학습합니다.** 선택 사항인 [로컬 테스트](#선택-로컬-테스트용-가상환경)와 [GitHub Actions](#github-actions)를 진행합니다. AWS 배포는 로컬 실행과 별도 준비가 필요합니다.

아래 명령은 **사용자가 이후 실행할 예시**입니다. 문서 작성 과정에서는 설치, 설정 변경, 서버 실행·종료, 테스트, 배포를 수행하지 않았습니다.

### 폴더 유형과 구성

이 폴더는 **독립 실행 앱**입니다. 여러 예제의 소스를 모아 놓은 폴더가 아니라, 앞선 00~06 단원의 내용을 하나로 통합한 Weather Agent입니다. 배포 교재와 템플릿도 함께 들어 있습니다.

```text
07_integrated-bedrock-mcp/
├─ .env.example
├─ README.md
├─ VALIDATION.md
├─ compose.infrastructure.yml       PostgreSQL·Redis
├─ compose.application.yml          MCP·백엔드·프론트엔드
├─ compose.local-aws.yml            로컬 AWS 임시 인증 전달
├─ backend/
│  ├─ app.py                       FastAPI·작업 상태·LLM 호출
│  ├─ mcp_probe.py                 LLM 없이 MCP 확인
│  ├─ requirements.txt
│  ├─ Dockerfile
│  ├─ test_app.py
│  ├─ test_integration_contracts.py
│  └─ skills/weather-briefing/SKILL.md
├─ frontend/
│  ├─ app.py                       Streamlit 화면
│  ├─ requirements.txt
│  └─ Dockerfile
├─ mcp_server/
│  ├─ server.py                    Open-Meteo tool·resource
│  ├─ requirements.txt
│  └─ Dockerfile
├─ database/init.sql               완료 이력 테이블
└─ deploy/
   ├─ github-actions.yml           07 전용 workflow 템플릿
   ├─ deploy.sh
   ├─ ssm_deploy.py
   └─ iam-policies.md
```

브라우저 → Streamlit → FastAPI → MCP → Open-Meteo 순서로 날씨를 가져옵니다. 백엔드는 날씨 원자료, MCP resource, 로컬 skill 파일을 조합해 Bedrock 또는 선택한 외부 LLM에 전달합니다.

Redis는 진행 상태와 날씨 캐시를, PostgreSQL은 완료 이력을 저장합니다. **별도 worker, 영구 작업 큐, 로컬 모델 서버는 없습니다.** 작업은 FastAPI 프로세스의 `BackgroundTasks`로 실행합니다. Node/npm과 Ollama도 이 앱에는 필요하지 않습니다.

| 접속 위치 | 주소 | 용도 |
| --- | --- | --- |
| Windows 브라우저 | `http://127.0.0.1:8501` | 실습 화면 |
| Windows 브라우저 | `http://127.0.0.1:8000/docs` | API 문서 |
| Windows PowerShell | `http://127.0.0.1:8000/health/ready` | 의존 서비스 준비 상태 |
| 백엔드 컨테이너 내부 | `http://weather-mcp:8010/mcp` | MCP 연결 |
| Docker 내부 | `database:5432`, `redis:6379` | DB·Redis 연결 |

## PowerShell

### 도구와 작업 폴더

**목적:** 프로젝트 루트에서 명령을 실행하고 Docker 엔진 준비 여부를 확인합니다.

**작업 폴더·창:** 새 PowerShell을 열고 **창 A — 실행 관리**로 사용하세요.

```powershell
Set-Location -LiteralPath 'C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\07_integrated-bedrock-mcp'
Test-Path -LiteralPath '.\compose.application.yml'
docker version
docker compose version
```

**예상 결과:** 경로 확인은 `True`, Docker는 Client와 Server 정보가 모두 나옵니다. Compose는 `docker compose` 형태의 v2 명령과 `--wait`를 지원해야 합니다.

**실패 시:** `docker`를 찾지 못하면 Docker Desktop 설치와 PATH를 확인하세요. Client만 나오거나 엔진 연결 오류가 나면 Docker Desktop을 시작하고 Linux 컨테이너 엔진이 준비될 때까지 기다립니다. Windows의 WSL2 기반 설치를 사용하는 경우 WSL2 준비와 재부팅 안내도 완료해야 합니다.

| 도구 | 필요 범위 | 파일 근거와 버전 |
| --- | --- | --- |
| Docker Desktop·Compose v2 | 권장 실행 경로 필수 | Linux 이미지, Compose `--wait` 사용. Desktop 최소 버전은 명시되지 않음 |
| Python | Docker 실행만 하면 호스트 설치 불필요 | Dockerfile은 `python:3.12-slim`; 로컬 테스트는 Python 3.12 권장 |
| AWS CLI v2 | 로컬 Bedrock SSO 인증 시 | README의 `configure sso`, `export-credentials` |
| Git | GitHub 연결 학습 시 | 로컬 Docker 실행에는 필수 아님 |
| Node/npm | 해당 없음 | Python 앱이며 `package.json`·npm scripts 없음 |

도구가 없다면 해당 도구의 공식 배포처에서 설치한 뒤 PowerShell을 새로 여세요. 현재 PC에 설치된 도구와 버전은 **미확인**입니다.

선택 기능에 필요한 도구는 창 A에서 확인합니다.

```powershell
py -3.12 --version
aws --version
git --version
```

Python 3.12, AWS CLI v2, Git 버전이 출력되는 것이 기대 결과입니다. 사용하지 않을 선택 기능의 도구까지 설치할 필요는 없습니다.

### 선택: 로컬 테스트용 가상환경

**목적:** Docker 앱과 별도로 Python 계약 테스트를 학습합니다. 권장 서버 실행 경로에는 호스트 `.venv`가 필요하지 않습니다.

**작업 폴더·창:** 프로젝트 루트, **창 B — 테스트**. 기존 `.venv` 디렉터리의 존재는 확인했지만 내부나 Python 버전은 확인하지 않았습니다. 다음 명령은 없을 때만 생성합니다.

```powershell
Set-Location -LiteralPath 'C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\07_integrated-bedrock-mcp'
if (-not (Test-Path -LiteralPath '.\.venv')) {
    py -3.12 -m venv .venv
}
& '.\.venv\Scripts\python.exe' --version
```

**예상 결과:** `.venv`의 Python 3.12가 출력됩니다. 다른 버전이거나 실행 파일이 없다면 기존 환경을 그대로 재사용하지 말고, 해당 환경의 출처를 확인한 뒤 별도 Python 3.12 환경을 준비하세요. 기존 폴더를 자동 삭제하지 않습니다.

환경이 맞으면 같은 창에서 설치와 테스트를 진행합니다.

```powershell
& '.\.venv\Scripts\python.exe' -m pip install -r '.\backend\requirements.txt' pytest
& '.\.venv\Scripts\python.exe' -m pytest backend -q
```

**예상 결과:** 의존성 설치 후 테스트 성공 요약이 나옵니다. 실패하면 첫 실패 테스트와 설치 오류부터 확인하세요. `VALIDATION.md`에는 과거 9개 통과 기록이 있지만, 현재 환경의 통과 결과는 아닙니다.

활성화는 필요 없습니다. 가상환경 Python을 직접 호출하므로 PowerShell 전역 실행 정책도 변경할 필요가 없습니다. 잠금 파일 없이 각 `requirements.txt`의 버전 범위를 설치하므로 시점에 따라 실제 설치 버전은 달라질 수 있습니다.

### 로컬 서버 실행 방식

이 문서의 “로컬 실행”은 **Windows PC에서 전체 Compose를 실행하는 방식**입니다. 시작·확인·종료 명령은 다음 [Docker](#docker) 절에 있습니다.

기본 인프라 Compose는 DB·Redis 포트를 Windows에 공개하지 않습니다. 따라서 인프라만 실행한 뒤 venv에서 백엔드를 띄우면 소스 기본 주소인 `127.0.0.1:5433`으로 DB에 연결되지 않습니다. 별도 포트 공개 설정이 없는 현재 구성에서는 Docker 전체 실행을 따르세요.

## 환경변수

### ENVEXAMPLE에서 설정 준비

환경 예제의 실제 이름은 루트의 **`.env.example`**, 복사 목적지는 같은 폴더의 **`.env`**입니다. 확인 당시 루트 `.env`는 발견되지 않았으며, 실제 내용이나 인증값은 읽지 않았습니다.

**목적:** Compose가 읽을 개발 설정을 준비합니다.

**작업 폴더·창:** 프로젝트 루트, 창 A.

```powershell
if (-not (Test-Path -LiteralPath '.\.env')) {
    Copy-Item -LiteralPath '.\.env.example' -Destination '.\.env'
}
notepad '.\.env'
```

**예상 결과:** 기존 파일을 덮어쓰지 않고 설정 파일을 엽니다. 편집기에서 DB 비밀번호와 선택한 LLM 설정을 입력한 뒤 저장하세요.

**실패 시:** `.env.example` 존재 여부와 현재 작업 폴더를 확인합니다. 아래 `<사용자가 입력할 값>` 표기는 설명용이므로 파일에 그대로 넣지 마세요.

### 변수별 의미와 입력 위치

| 변수명 | 근거 파일·설정 키 | 의미·사용 주체 | 기본값 또는 예시 | 필수·선택 | 사용자가 준비할 값 |
| --- | --- | --- | --- | --- | --- |
| `POSTGRES_USER` | `.env.example`, 인프라 `database.environment` | DB 계정, 백엔드 URL 조립 | `agent_user` | 필수 설정, 기본값 가능 | 변경할 때만 계정명 |
| `POSTGRES_PASSWORD` | 두 Compose의 DB 설정 | DB 초기 비밀번호·백엔드 인증 | 예제값 교체 | 필수 | 영문·숫자로 정한 개발 비밀번호 |
| `POSTGRES_DB` | 두 Compose의 DB 설정 | 사용할 DB | `agent_db` | 필수 설정, 기본값 가능 | 변경할 때만 DB명 |
| `WEATHER_CACHE_TTL_SECONDS` | 앱 Compose, `backend/app.py:CACHE_TTL` | 날씨 캐시 보존 초 | `600` | 선택 | 양의 정수 |
| `AWS_REGION` | 앱 Compose, `generate_answer()` | Bedrock 호출 리전 | `ap-northeast-2` | Bedrock 사용 시 | 선택 모델의 리전 |
| `BEDROCK_MODEL_ID` | `.env.example`, `generate_answer()` | Converse 모델 또는 추론 프로필 ID | 빈 값 | Bedrock 사용 시 필수 | 계정에서 사용 가능한 실제 ID |
| `AWS_ACCESS_KEY_ID` | `compose.local-aws.yml` | 로컬 임시 AWS 인증 | 기본값 없음 | 로컬 Bedrock 시 필수 | SSO/교육 계정의 임시 값 |
| `AWS_SECRET_ACCESS_KEY` | `compose.local-aws.yml` | 로컬 임시 AWS 인증 | 기본값 없음 | 로컬 Bedrock 시 필수 | 임시 비밀값 |
| `AWS_SESSION_TOKEN` | `compose.local-aws.yml` | 임시 세션 토큰 | 기본값 없음 | 로컬 Bedrock 시 필수 | 임시 토큰 |
| `OPENAI_API_KEY` | 앱 Compose, `generate_answer()` | OpenAI API 인증 | 빈 값 | OpenAI 선택 시 필수 | 사용자 API 키 |
| `OPENAI_MODEL` | `.env.example`, `generate_answer()` | OpenAI 모델 | `gpt-4.1-mini` | OpenAI 선택 시 | 계정에서 사용 가능한 모델 |
| `GEMINI_API_KEY` | 앱 Compose, `generate_answer()` | Gemini API 인증 | 빈 값 | Gemini 선택 시 필수 | 사용자 API 키 |
| `GEMINI_MODEL` | `.env.example`, `generate_answer()` | Gemini 모델 | `gemini-3.5-flash` | Gemini 선택 시 | 계정에서 사용 가능한 모델 |
| `WEATHER_MCP_URL` | 앱 Compose `backend.environment`, `MCP_URL` | 백엔드→MCP | `http://weather-mcp:8010/mcp` | Compose가 설정 | 기본 구성에서는 입력 불필요 |
| `DATABASE_URL` | 앱 Compose `backend.environment` | 백엔드→DB | `database:5432`를 사용하는 URL | Compose가 조립 | 위 DB 변수와 일치 |
| `REDIS_URL` | 앱 Compose `backend.environment` | 백엔드→Redis | `redis://redis:6379/0` | Compose가 설정 | 입력 불필요 |
| `BACKEND_URL` | 앱 Compose `frontend.environment`, `frontend/app.py` | Streamlit 서버→API | `http://backend:8000` | Compose가 설정 | 입력 불필요 |

모델 이름은 **파일에 적힌 기본값**이며 현재 계정에서 호출 가능하다는 보장은 아닙니다. 전체 답변 경로에는 세 provider 중 하나의 외부 인증이 필요합니다. ChatGPT 로그인이나 구독 인증을 프로젝트 API 키로 사용할 수 없습니다.

### 설정이 전달되는 방식

- 루트 `.env`는 Compose의 `${변수}` 치환에 사용됩니다. 이 프로젝트에는 `env_file:` 설정이 없습니다.
- Compose의 `environment:`에 지정된 값만 해당 컨테이너에 전달됩니다. `.env`에 임의의 변수를 추가한다고 모든 컨테이너가 받지는 않습니다.
- PowerShell의 `$env:` 값은 해당 창과 자식 프로세스에 적용됩니다. 같은 이름이면 Compose의 `.env` 값보다 우선할 수 있습니다.
- Python 소스에는 `.env` 자동 로더가 없습니다. venv Python이 루트 `.env`를 자동으로 읽는 구조가 아닙니다.
- GitHub Secrets/Variables는 workflow에서 명시적으로 참조할 때 사용합니다. 로컬 `.env`와 자동 동기화되지 않습니다.
- 프론트엔드의 API 호출은 Streamlit 서버에서 수행됩니다. 프론트엔드 설정이나 브라우저 코드에 LLM 비밀키를 넣지 마세요.

### 권장: Bedrock 인증 준비

**목적:** 로컬 백엔드 컨테이너에 만료되는 AWS 자격 증명을 전달합니다.

먼저 사용자 계정에서 Bedrock Converse 모델 또는 추론 프로필을 정하고, 해당 호출 권한을 준비하세요. `.env`의 `AWS_REGION`, `BEDROCK_MODEL_ID`를 실제 값으로 저장합니다. 계정·리전별 모델 사용 가능 여부는 미확인입니다.

**작업 폴더·창:** 프로젝트 루트, 창 A. 조직의 SSO 시작 URL·리전·계정·역할을 준비한 뒤 진행합니다.

```powershell
aws configure sso --profile weather-lab
aws sso login --profile weather-lab
$weatherCredentials = aws configure export-credentials --profile weather-lab --format process | ConvertFrom-Json
$env:AWS_ACCESS_KEY_ID = $weatherCredentials.AccessKeyId
$env:AWS_SECRET_ACCESS_KEY = $weatherCredentials.SecretAccessKey
$env:AWS_SESSION_TOKEN = $weatherCredentials.SessionToken
```

**예상 결과:** 브라우저 로그인을 완료하고 임시 인증값을 창 A의 환경변수로 보관합니다. `$weatherCredentials`나 비밀 환경변수를 출력하지 마세요. 같은 창에서 Docker를 실행해야 전달됩니다.

**실패 시:** AWS CLI v2, SSO 프로필, 계정 역할을 확인합니다. SSO가 없는 교육 계정은 강사에게 만료되는 STS 자격 증명 전달 방법을 확인하세요. 기본 Compose는 사용자 `.aws` 폴더를 마운트하지 않습니다.

Project Player가 다른 프로세스에서 서버를 시작하면 창 A의 `$env:` 값을 받지 못할 수 있습니다. Player의 인증 환경 전달 방식은 확인하지 않았으므로, Bedrock 실행 전 해당 실행 기능의 설정을 확인하세요.

## Docker

### 실제 Compose 구성

| 파일·프로젝트 이름 | 서비스 | 공개 포트·데이터 |
| --- | --- | --- |
| `compose.infrastructure.yml` / `weather-07-infrastructure` | `database`, `redis` | 호스트 공개 포트 없음. `postgres_data`, `redis_data` 볼륨 |
| `compose.application.yml` / `weather-07-application` | `weather-mcp`, `backend`, `frontend` | 백엔드 `127.0.0.1:8000`, 화면 `127.0.0.1:8501` |
| `compose.local-aws.yml` | 백엔드 환경 설정 추가 | 임시 AWS 인증값 3개 전달 |

Compose profile은 없습니다. 인프라가 `weather-07` 네트워크를 만들고 앱은 이를 외부 네트워크로 사용합니다.

`database/init.sql`은 DB 초기화 디렉터리에 읽기 전용으로 연결됩니다. 빈 DB 볼륨의 첫 초기화에서 `weather_agent.runs`를 만듭니다. 기존 볼륨을 재사용하면 초기화 SQL이나 비밀번호 변경이 자동 재적용되지 않습니다.

컨테이너 내부의 `localhost`는 해당 컨테이너 자신입니다. 백엔드에서 DB를 찾을 때는 `database`, MCP를 찾을 때는 `weather-mcp`를 사용합니다. Windows 브라우저에서 이 서비스 이름을 사용할 수는 없습니다.

### 권장 실행: 전체 Docker와 Bedrock

이미 Project Player로 실행했다면 이 시작 단계를 건너뛰세요.

**1. 목적:** 설정 오류를 확인하고 앱 이미지를 빌드합니다.

**작업 폴더·창:** 프로젝트 루트, 인증을 준비한 창 A.

```powershell
docker compose -f compose.infrastructure.yml config --quiet
docker compose -f compose.application.yml -f compose.local-aws.yml config --quiet
docker compose -f compose.application.yml -f compose.local-aws.yml build
```

**예상 결과:** 설정 검사는 오류 없이 끝나고, 앱 이미지 3개를 빌드합니다. 각 Dockerfile이 Python 의존성을 설치합니다.

**실패 시:** 인증 변수 누락은 [환경변수](#환경변수), 패키지 설치 실패는 해당 서비스의 `requirements.txt`와 빌드 로그를 확인하세요. 각 명령에서 오류가 나면 다음 단계로 넘어가지 마세요. 비밀값이 포함될 수 있으므로 `--quiet` 없는 전체 설정 출력을 공유하지 않습니다.

**2. 목적:** DB·Redis를 먼저 준비합니다.

**작업 폴더·창:** 프로젝트 루트, 창 A.

```powershell
docker compose -f compose.infrastructure.yml up -d --wait --wait-timeout 120
docker compose -f compose.infrastructure.yml ps
```

**예상 결과:** PostgreSQL 17 Alpine과 Redis 7 Alpine이 시작되고 healthcheck가 성공합니다.

**실패 시:** 다음 로그에서 DB 초기화·인증·볼륨 문제를 확인합니다.

```powershell
docker compose -f compose.infrastructure.yml logs --tail=50 database redis
```

**3. 목적:** MCP → 백엔드 → 프론트엔드를 시작합니다.

**작업 폴더·창:** 프로젝트 루트, 창 A.

```powershell
docker compose -f compose.application.yml -f compose.local-aws.yml up -d --wait --wait-timeout 180
docker compose -f compose.application.yml ps
```

**예상 결과:** `weather-mcp`가 준비되면 백엔드, 백엔드 readiness가 성공하면 프론트엔드가 시작됩니다. 프론트엔드에는 별도 Compose healthcheck가 없으므로 브라우저 접속까지 확인해야 합니다.

**실패 시:** `weather-07` 네트워크 오류는 인프라 실행 여부, 백엔드 unhealthy는 readiness 응답과 로그를 확인하세요.

`-d`는 백그라운드 실행입니다. 명령이 끝나도 컨테이너는 계속 동작하며 창 A를 닫는 것으로 종료되지 않습니다.

### 대체 실행: OpenAI·Gemini 또는 인증 없는 기초 실습

이 경로는 위 Bedrock 경로 **대신** 사용합니다. OpenAI·Gemini는 `.env`에 해당 API 키와 모델을 준비합니다. 인증 없이 시작하는 경우에는 화면의 전체 날씨 답변 대신 MCP probe까지만 실습하세요.

**목적:** AWS 인증 override 없이 같은 앱을 실행합니다.

**작업 폴더·창:** 프로젝트 루트, 창 A. 환경 파일 준비 후 다음 순서로 진행합니다.

```powershell
docker compose -f compose.infrastructure.yml config --quiet
docker compose -f compose.application.yml config --quiet
docker compose -f compose.application.yml build
docker compose -f compose.infrastructure.yml up -d --wait --wait-timeout 120
docker compose -f compose.application.yml up -d --wait --wait-timeout 180
```

**예상 결과:** 인프라와 앱이 시작됩니다. readiness 자체는 LLM 인증을 검사하지 않습니다. 인증 없이 화면의 `실제 날씨 조회`를 누르면 LLM 단계에서 실패합니다.

**실패 시:** Docker 및 DB/MCP 연결 문제는 권장 실행과 같은 위치에서 확인합니다.

### 접속 확인

**목적:** 프로세스 생존과 의존 서비스 연결을 구분해 확인합니다.

**작업 폴더·창:** 프로젝트 루트, 창 A 또는 별도 **창 C — 확인**.

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/live'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready'
docker compose -f compose.application.yml ps
docker compose -f compose.application.yml logs --tail=50 backend weather-mcp frontend
```

**예상 결과:** live는 `status: ok`, `service: backend`; ready는 `status: ok`와 모든 check가 `true`입니다. 이후 브라우저에서 `http://127.0.0.1:8501`을 여세요.

**실패 시:** 아래 [검증과 문제 해결](#검증과-문제-해결)의 증상별 순서를 따릅니다. 로그는 사용자가 자신의 PC에서 확인하고, 인증값이나 개인 정보를 제거한 뒤 공유하세요.

### 종료

**목적:** 이 프로젝트의 앱과 인프라를 종료하면서 데이터 볼륨을 보존합니다.

**작업 폴더·창:** 프로젝트 루트, 창 A. 먼저 진행 중 조회가 끝났는지 확인합니다.

```powershell
docker compose -f compose.application.yml down
docker compose -f compose.infrastructure.yml down
docker compose -f compose.application.yml ps
docker compose -f compose.infrastructure.yml ps
```

**예상 결과:** 두 프로젝트의 컨테이너가 제거되고 목록이 비어 있습니다. 종료에는 AWS override가 필요하지 않으므로 임시 인증이 만료돼도 기본 파일로 종료할 수 있습니다.

**실패 시:** 네트워크 사용 중 오류가 나면 앱이 먼저 종료됐는지 확인하세요. 볼륨 삭제 옵션 `-v`는 기본 절차에 넣지 않습니다. Project Player가 시작한 서버는 해당 기능의 종료 절차를 우선 사용하세요.

로그를 `logs -f`로 보고 있었다면 그 창의 `Ctrl+C`는 로그 보기만 끝냅니다. 컨테이너 종료는 별도입니다.

## GitHub Actions

### 발견한 workflow와 적용 대상

상위 workflow 폴더는 선택 루트 기준 `../../../.github/workflows/`입니다. 제공된 파일 3개를 실제로 읽었습니다.

| 파일 | 트리거·경로 조건 | 실제 검사·배포 대상 | 이 프로젝트와 관계 |
| --- | --- | --- | --- |
| [07-runtime-ci.yml](../../../.github/workflows/07-runtime-ci.yml) | 모든 브랜치 push·PR, runtime 폴더 전체와 자기 workflow 경로; 수동 실행 가능 | `01_simple-multi-llm-compose`에서 Python 3.12 테스트·Compose 검사·빌드 | 07 변경으로 실행될 수 있지만 **07 소스를 검사하지 않음** |
| [07-weather-mcp-cicd.yml](../../../.github/workflows/07-weather-mcp-cicd.yml) | 05의 지정 소스·Compose 경로 push·PR; 수동 `deploy` | `05_weather-mcp-deployment-project` | 05 전용, 로컬 07 준비에 불필요 |
| [07-weather-stateful-cicd.yml](../../../.github/workflows/07-weather-stateful-cicd.yml) | 06의 지정 소스·DB·Compose 경로 push·PR; 수동 `deploy` | `06_weather-mcp-stateful-deployment` | 06 전용, 로컬 07 준비에 불필요 |

세 파일 모두 `ubuntu-latest` runner를 사용합니다. Runtime CI는 `test-and-build` 단일 job입니다. 05의 `deploy`, 06의 `deploy-stateful-service`는 각각 `needs: test-and-build`로 검사 후 실행하며, main push 또는 수동 배포 조건을 사용합니다. 이 두 예제의 SSH Secrets를 07의 필수 설정으로 가져오지 마세요.

확인한 상위 workflow 폴더에는 07 통합 앱 전용 파일이 없습니다. 선택 프로젝트의 [deploy/github-actions.yml](deploy/github-actions.yml)은 **템플릿**이며 현재 위치에서는 GitHub가 실행하지 않습니다.

### 07 템플릿의 CI와 CD

템플릿을 활성화한 뒤의 동작은 다음과 같습니다.

| 항목 | YAML에 정의된 동작 |
| --- | --- |
| 트리거 | 모든 PR, main push, 수동 실행. `paths` 필터 없음 |
| 수동 입력 | boolean `deploy`, 기본값 `false` |
| `ci` | Ubuntu runner → checkout → Python 3.12 → 백엔드 테스트 → 두 Compose 검사 → 앱 이미지 빌드 → 소스 archive 업로드 |
| artifact | `weather-07-source`, 보관 7일 |
| `deploy` | `needs: ci`, main에서 push 또는 수동 `deploy=true`일 때 |
| 배포 설정 | `production` Environment, `weather-07-production` 동시 실행 그룹, 취소하지 않음 |
| 배포 흐름 | OIDC 인증 → 소스 archive를 S3 업로드 → `deploy/ssm_deploy.py` → EC2에서 `deploy/deploy.sh` |
| 권한 | 기본 `contents: read`; 배포 job은 `id-token: write` 추가 |
| 시간 제한 | 배포 job 40분 |

배포 스크립트는 EC2에서 이미지를 다시 빌드하고 readiness 성공 후 `/opt/weather-07/current`를 바꿉니다. CI에서 만든 이미지 자체를 배포하거나 ECR에 push하는 구성은 아닙니다. 자동 rollback도 없습니다.

### 저장소 연결 시 먼저 확인할 경로

**목적:** 템플릿의 `PROJECT_DIR`을 실제 저장소 배치에 맞춥니다.

**작업 폴더·창:** 프로젝트 루트, 창 B. GitHub 학습을 시작할 때 사용자가 확인합니다.

```powershell
git rev-parse --show-toplevel
git status --short
```

**예상 결과:** 실제 Git 루트와 변경 목록이 나옵니다.

**실패 시:** ZIP 등으로 받아 Git 저장소가 아니라면 오류가 날 수 있습니다. 로컬 실행에는 영향이 없습니다. 이후 본인 저장소를 준비하고 workflow 경로를 정하세요.

템플릿의 현재 값은 다음과 같습니다.

`aidevs-main/aidevs-main/07_multi-agent-service-ops/00_runtime-and-deployment/07_integrated-bedrock-mcp`

이 값이 맞는지는 실제 Git 루트에 따라 달라집니다.

- Git 루트가 제공된 상위 `.github`의 부모라면 `07_multi-agent-service-ops/00_runtime-and-deployment/07_integrated-bedrock-mcp`로 맞춰야 합니다.
- 선택 폴더 자체가 새 저장소 루트라면 `.`입니다.

사용자는 이후 템플릿을 자기 저장소 루트의 `.github/workflows/07-integrated-bedrock-mcp.yml`로 복사하고 `PROJECT_DIR`을 수정해야 합니다. 이 문서 작성 중에는 복사·수정하지 않았습니다.

### 연결 대상과 사용자 설정

| 연결할 대상 | 필요한 권한 | Secret·Variable 이름 | 설정 위치 | 사용 job | 사용자가 준비할 값 |
| --- | --- | --- | --- | --- | --- |
| GitHub 소스·artifact | `contents: read`, Actions 사용 허용 | 별도 사용자 Secret 없음 | workflow·저장소 Actions 설정 | `ci`, `deploy` | 본인 저장소 |
| AWS OIDC 역할 | 역할 신뢰·S3 업로드·SSM 명령 실행/조회 | Variable `AWS_DEPLOY_ROLE_ARN` | GitHub `production` Variables | `deploy` | 배포 역할 ARN |
| AWS 리전 | 대상 리전 접근 | Variable `AWS_REGION` | 동일 | `deploy` | EC2·S3 리전 |
| S3 | GitHub 역할 쓰기, EC2 역할 읽기 | Variable `ARTIFACT_BUCKET` | 동일 | `deploy` | `s3://` 없는 버킷명 |
| EC2 | SSM 관리 가능 상태 | Variable `EC2_INSTANCE_ID` | 동일 | `deploy` | 실제 `i-...` ID |
| EC2 앱 설정 | 서버 설정 관리 권한 | GitHub Secret으로 전달하지 않음 | `/opt/weather-07/shared/.env` | EC2 배포 스크립트 | DB 설정·리전·모델 ID |
| EC2 Bedrock 호출 | 선택 모델의 호출 권한 | 장기 AWS 키 Secret 없음 | EC2 Instance Profile | 실행 중 백엔드 | SSM·S3 읽기·Bedrock 권한 |

07 템플릿은 `secrets.*`를 참조하지 않습니다. 장기 AWS 키나 SSH 개인키를 GitHub Secrets에 추가하는 방식이 아닙니다. IAM 정책의 구체적인 범위는 [deploy/iam-policies.md](deploy/iam-policies.md)를 자신의 ARN에 맞춰 검토하세요.

### 학습 순서와 실패 로그 확인

1. 로컬 실습 후 [선택: 로컬 테스트용 가상환경](#선택-로컬-테스트용-가상환경)을 진행합니다.
2. 본인 저장소와 workflow 경로를 준비하고 PR에서 CI를 확인합니다. 수동 실행 `deploy=false`도 CI만 수행합니다.
3. AWS 배포는 별도 단계로 진행합니다. [README.md](README.md)의 8~10절에 따라 EC2·네트워크·Docker·SSM·Instance Profile·서버 `.env`를 준비합니다.
4. GitHub `production` Environment, 위 Variables, OIDC trust를 설정합니다. Environment의 배포 브랜치를 main으로 제한하고 필요하면 승인자를 설정합니다.
5. 준비 후 main 병합 또는 main에서 `deploy=true`로 실행합니다. **main push는 템플릿상 배포 조건을 만족합니다.**
6. Actions에서 **workflow → run → job → 실패 step → 로그** 순서로 확인합니다.

경로 실패는 `PROJECT_DIR`, 설치 실패는 Python 3.12와 requirements, 테스트 실패는 첫 assertion, Docker 실패는 해당 이미지 빌드 로그를 봅니다. OIDC 실패는 역할 ARN·trust의 저장소/Environment 조건, SSM 실패는 EC2 Online 상태·대상 ID·S3 권한과 command ID를 확인합니다.

저장소 연결, 설정 생성, 권한 승인, push, workflow 실행과 클라우드 배포는 모두 **사용자가 이후 수행할 작업**입니다. 로컬 서버 실행에 CI/CD는 필수가 아닙니다.

## 예제 학습

### 한 앱 안에서 진행하는 순서

다른 프로젝트를 번갈아 실행하는 구조가 아닙니다. 다음 순서대로 같은 앱을 학습합니다.

| 순서 | 예제 경로 | 배울 내용 | 선행 조건 | 실행·확인 위치 |
| --- | --- | --- | --- | --- |
| 1 | `mcp_server/server.py`, `backend/mcp_probe.py` | tool·resource와 실제 날씨 데이터 | 컨테이너 실행 | 아래 MCP 실습 |
| 2 | `frontend/app.py`, `backend/app.py` | 날씨→LLM 답변 | LLM 인증 | 아래 화면 조회 |
| 3 | `backend/app.py`, `database/init.sql` | 캐시·진행 상태·영구 이력 | 조회 성공 | 아래 캐시·이력 |
| 4 | `backend/test_*.py` | 외부 서비스를 대체한 계약 검사 | Python 테스트 환경 | PowerShell의 로컬 테스트 |
| 5 | `deploy/` | CI→AWS 배포 | 본인 GitHub·AWS 설정 | GitHub Actions |
| 6 | `README.md` 11절 | 재배포·장애·복구 한계 | 앞선 결과 이해 | 아래 다음 학습 |

### LLM 인증 없이 MCP 확인

**목적:** LLM 호출 없이 MCP 연결, resource 내용, 실제 Open-Meteo 응답을 확인합니다.

**작업 폴더·창:** 프로젝트 루트, 창 C. 전체 컨테이너가 실행 중이어야 합니다.

```powershell
docker compose -f compose.application.yml exec backend python mcp_probe.py
docker compose -f compose.application.yml exec backend python mcp_probe.py --city Seoul
```

**예상 결과:**

- tool 목록에 `get_weather`
- resource 목록에 `weather://guide/forecast`
- resource 내용에 기온 단위와 강수 확률 해석
- 두 번째 명령의 tool 결과에 `success: true`, 날짜·최고/최저 기온·강수 확률·`Open-Meteo`

**실패 시:** MCP 연결 실패는 백엔드/MCP 로그와 `WEATHER_MCP_URL`, 도시 검색 실패는 도시 이름, 외부 요청 실패는 DNS·HTTPS 연결을 확인합니다.

이 probe는 LLM을 호출하지 않으며 앱의 완료 이력을 저장하는 전체 경로도 수행하지 않습니다. 키 없는 대안은 이 범위까지입니다.

### 화면에서 날씨 조회

**목적:** 프론트엔드부터 LLM과 DB까지 전체 경로를 확인합니다.

**사용할 화면:** 브라우저 `http://127.0.0.1:8501`. 서버가 이미 실행 중이면 시작 명령 없이 여기서 진행합니다.

1. 왼쪽 **Health Check**를 선택합니다. 준비 성공 메시지와 readiness JSON을 확인합니다.
2. **Weather Agent**로 이동합니다.
3. **도시**에 `Seoul`, **날짜**에 `내일`, **Cloud LLM**에 설정한 provider를 선택합니다. 권장 Bedrock 경로를 준비했다면 `bedrock`입니다.
4. **실제 날씨 조회**를 누릅니다.
5. 진행률이 완료되면 답변, Run ID, provider, model, 캐시 여부를 확인합니다.
6. **실제 Open-Meteo Tool Result**의 `date`, `temperature_min`, `temperature_max`, `precipitation_probability`를 답변과 비교합니다.

**예상 결과:** 실제 날씨를 바탕으로 한국어 답변과 원자료가 표시됩니다. skill은 3문장 이내 브리핑과 Open-Meteo 출처 표기를 지시합니다. 이는 모델에 전달하는 지시이며 출력 형식을 코드가 강제하는 것은 아닙니다.

**실패 시:** `Backend 요청 실패`의 내용을 확인합니다. 모델 ID 누락·키 누락은 환경설정, AWS 권한 오류는 인증, `CITY_NOT_FOUND`는 도시 이름부터 확인하세요. 화면 폴링은 코드상 최대 90회이며 개별 요청 시간까지 포함하므로 정확히 90초 타이머는 아닙니다.

### 캐시와 실행 이력

같은 도시·날짜로 다시 조회합니다. 캐시가 유효하면 화면에 **Redis Cache 사용**이 표시됩니다. 기본 TTL은 600초입니다. 캐시는 날씨 원자료만 재사용하며 **LLM 답변은 다시 생성**합니다.

왼쪽 **실행 이력**을 열면 PostgreSQL에 저장된 최근 완료 결과를 확인할 수 있습니다. 기본 조회 개수는 20개입니다. 실패 작업은 완료 이력 테이블에 저장하지 않습니다.

**목적:** 화면과 같은 이력 API 응답 구조를 확인합니다.

**작업 폴더·창:** 프로젝트 루트, 창 C.

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/runs'
```

**예상 결과:** `runs` 배열이 나옵니다. 아직 성공한 조회가 없다면 빈 배열도 정상입니다.

**실패 시:** DB 연결·스키마 문제는 readiness와 인프라 로그를 확인합니다. 화면에는 성공했는데 이력이 보이지 않으면 동일한 백엔드에 접속했는지 `BACKEND_URL`과 포트를 대조하세요.

### 다음 학습

**구조 이해** 메뉴를 열고 다음 코드 순서로 화면 흐름을 연결해 읽습니다.

`mcp_server/server.py` → `mcp_session()` → `call_weather_tool()` → `read_weather_guide()` → `generate_answer()` → `execute_weather_agent()`

이 구조에서는 백엔드가 tool 호출 순서를 정합니다. LLM이 자율적으로 MCP tool을 선택하는 루프는 구현하지 않았습니다.

그다음 앱을 종료하고 같은 Docker 시작 절차로 다시 실행한 뒤 **실행 이력**이 남아 있는지 확인할 수 있습니다. 진행 중 작업은 재시작으로 유실될 수 있으므로 조회가 완료된 뒤 진행하세요.

README는 00~06을 복습 단원으로 안내합니다. 복습하려면 Project Player에서 다음 폴더를 선택할 수 있습니다.

- MCP 배포: `../05_weather-mcp-deployment-project`
- 상태 보존: `../06_weather-mcp-stateful-deployment`

이 경로는 상위 workflow에서도 참조하지만, **이번 작업에서 두 폴더의 실제 소스 존재와 실행 절차는 확인하지 않았습니다.** 선택한 뒤 해당 폴더 기준 가이드를 새로 확인하세요. 07 실습을 위해 이동할 필요는 없습니다.

## 검증과 문제 해결

### 구성 요소별 완료 기준

| 구성 요소 | 확인 방법 | 설정·코드상 기대 결과 |
| --- | --- | --- |
| PostgreSQL·Redis | 인프라 `ps` | healthcheck 성공 |
| 백엔드 프로세스 | `/health/live` | `status: ok` |
| 내부 의존성 | `/health/ready` | `redis`, `database`, `database_schema`, `mcp`, `resource`, `skill` 모두 true |
| MCP | `mcp_probe.py` | tool·resource 목록과 읽기 성공 |
| Open-Meteo | probe의 `--city Seoul` | 날씨 데이터 `success: true` |
| 프론트엔드 | 브라우저 8501 | 메뉴와 입력 화면 |
| LLM·저장 전체 경로 | 실제 날씨 조회 → 실행 이력 | 답변·원자료·완료 이력 |
| 종료 | 두 Compose의 `ps` | 컨테이너 목록 비어 있음 |

readiness 성공은 **외부 Open-Meteo 호출이나 Bedrock 인증·모델 호출 성공을 의미하지 않습니다.** 전체 완료 판단에는 화면에서 실제 조회가 필요합니다.

### 증상별 해결 순서

| 증상 | 먼저 확인할 곳 | 다음 행동 |
| --- | --- | --- |
| Docker 엔진 연결 실패 | Docker Desktop, `docker version` | Linux 엔진 준비 후 재시도 |
| 8000·8501 포트 충돌 | Player 실행 여부, 기존 앱 | 소유 앱을 확인하고 중복 시작 제거 |
| `weather-07` network 없음 | 인프라 Compose 상태 | 인프라부터 실행 |
| 백엔드 unhealthy | `/health/ready`, 백엔드 로그 | 실패한 check별 DB·Redis·MCP 확인 |
| DB 인증 실패 | 최초 볼륨 생성 때 설정한 비밀번호 | `.env` 변경만으로 기존 DB 비밀번호가 바뀌지 않음. 볼륨 삭제 대신 기존 설정 확인 |
| `database_schema` 실패 | `database/init.sql`, DB 초기화 로그 | 기존 볼륨 상태 확인. 초기화 SQL 자동 재실행을 가정하지 않음 |
| MCP 421 또는 Invalid Host | `server.py`의 `allowed_hosts`, MCP URL | Compose 기본 서비스 이름과 포트 사용 |
| resource·skill 실패 | resource URI, `backend/Dockerfile`의 `COPY skills` | 파일 포함 여부와 이미지 버전 확인 후 앱 빌드 |
| Bedrock 모델 ID 누락 | `.env`의 `BEDROCK_MODEL_ID` | 실제 사용 가능한 ID 입력 후 컨테이너 재생성 |
| AWS 인증 만료 | 창 A의 SSO 세션 | 재로그인·인증 export 후 같은 창에서 앱 재생성 |
| Bedrock AccessDenied | 선택 역할·모델 권한 | 해당 모델·프로필 ARN 접근 권한 확인 |
| Bedrock ValidationException | 리전·모델/추론 프로필 ID | 계정에서 사용 가능한 Converse 설정 확인 |
| OpenAI·Gemini 인증 실패 | 선택 provider와 해당 키·모델 | 사용자 API 인증과 모델 설정 확인 |
| 화면에서 API 연결 실패 | frontend 로그, `BACKEND_URL` | Docker 내부 값은 `http://backend:8000`인지 확인 |
| 진행 상태 404 | `/api/runs/{run_id}/progress` | 상태 TTL 1시간 만료 여부 확인, 완료 이력은 별도로 조회 |
| 작업이 계속 멈춤 | 배포·재시작 여부, backend 로그 | BackgroundTasks는 영구 큐가 아니므로 원인 확인 후 새 조회 |
| `ModuleNotFoundError` | 사용 중 Python 경로 | `.venv` Python으로 해당 requirements 설치 |
| CI 통과 후 CD 실패 | 실패 step, production Variables, SSM | OIDC→S3→SSM 순서로 분리 확인 |

**포트 확인 목적의 명령**은 창 C에서 사용할 수 있습니다.

```powershell
Get-NetTCPConnection -State Listen -LocalPort 8000,8501 -ErrorAction SilentlyContinue |
    Select-Object LocalAddress,LocalPort,OwningProcess
```

리스너가 보이면 사용 중인 포트입니다. 결과가 없다고 앱 전체 상태까지 판단할 수는 없습니다. 표시된 프로세스를 확인 없이 일괄 종료하지 마세요.

### 설정 변경 후 반영

`.env`나 임시 AWS 인증을 변경해도 실행 중 컨테이너 환경은 자동 갱신되지 않습니다.

**목적:** 갱신된 Bedrock 인증·설정을 백엔드에 반영합니다.

**작업 폴더·창:** 프로젝트 루트, 새 인증을 준비한 창 A. 진행 중 작업이 없는 상태에서 실행합니다.

```powershell
docker compose -f compose.application.yml -f compose.local-aws.yml up -d --force-recreate --wait backend
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready'
```

**예상 결과:** 백엔드가 새 환경으로 재생성되고 readiness가 성공합니다.

**실패 시:** override에 필요한 인증값 3개와 인프라/MCP 상태를 확인하세요. OpenAI·Gemini 대체 경로에서는 이 명령의 `-f compose.local-aws.yml`을 제외합니다. 소스를 변경한 경우에는 별도 이미지 재빌드도 필요합니다.

## 근거와 미확인 사항

### 실행 절차의 파일 근거

| 설명·명령 | 근거 |
| --- | --- |
| 독립 통합 앱, 로컬→CI→AWS 학습 순서 | [README.md](README.md) 1·4·6~12절 |
| Python 3.12와 서비스 진입 명령 | 각 서비스의 `Dockerfile` 내 `FROM`, `CMD` |
| 의존성 범위 | `backend/requirements.txt`, `frontend/requirements.txt`, `mcp_server/requirements.txt` |
| 서비스·포트·볼륨·네트워크 | `compose.infrastructure.yml`, `compose.application.yml`의 `name`, `services`, `ports`, `volumes`, `networks` |
| 로컬 임시 AWS 인증 | `compose.local-aws.yml`의 `backend.environment` |
| 환경 예제 | [.env.example](.env.example) |
| 화면→백엔드 경로 | `frontend/app.py`: `BACKEND_URL`, `/api/weather`, `/api/runs/{run_id}/progress`, `/api/runs`, `/health/ready` |
| readiness·상태·캐시·LLM | `backend/app.py`: `ready`, `StateStore`, `generate_answer`, `execute_weather_agent` |
| DB 테이블 | `database/init.sql`: `weather_agent.runs` |
| MCP tool·resource·헬스 | `mcp_server/server.py`: `get_weather`, `forecast_guide`, `health` |
| 키 없는 MCP 실습 | `backend/mcp_probe.py`: `probe`, `--city` |
| 실제 workflow와 템플릿 구분 | 상위 `.github/workflows` 3개, `deploy/github-actions.yml` |
| 배포 방식·권한 | `deploy/ssm_deploy.py`, `deploy/deploy.sh`, `deploy/iam-policies.md` |
| 기존 검증 기록 | [VALIDATION.md](VALIDATION.md) |

### 확인한 범위와 실행하지 않은 항목

선택한 루트의 존재, 주요 소스·설정·문서, `.env.example`, 기존 `.venv` 디렉터리, 제공된 상위 workflow 3개의 파일 존재와 내용을 확인했습니다. 기존 `guide.md`는 발견되지 않았습니다. 확인한 루트·상위 경로 및 주요 하위 폴더에서 추가 `AGENTS.md`는 발견되지 않았으며, 요청에 제공된 작업 지시를 적용했습니다.

실제 `.env`, 인증 저장소, 비밀키, 사용자 데이터·로그, `.git` 내부, `.venv` 내부는 읽지 않았습니다. 원격 저장소 연결 상태와 실제 Git 루트도 확인하지 않았습니다.

프로그램 import, 테스트, Docker 명령, API 요청, 패키지 설치, 서버 실행·종료, GitHub 실행, AWS 배포는 수행하지 않았습니다. 따라서 이 문서는 **정적 파일 근거로 작성한 실행 가이드이며, 현재 서버 구동이나 CI 통과 보고가 아닙니다.**

`VALIDATION.md`의 테스트 통과 기록은 기존 문서의 주장입니다. 해당 문서도 실제 Docker 화면 통합 및 EC2·GitHub CD·Bedrock 검증은 미실행으로 구분합니다.

### 사용자가 마지막으로 준비할 것

전체 화면 실습에는 Docker 엔진, 프로젝트 DB 비밀번호, 선택한 LLM의 실제 인증과 사용 가능한 모델이 필요합니다. 인증이 없다면 MCP probe와 내부 readiness까지 학습할 수 있습니다.

Project Player의 실제 실행 명령·환경변수 전달 방식·현재 서버 상태는 미확인입니다. Player에서 실행 중이라면 먼저 화면과 readiness를 확인하고, 이 가이드의 수동 서버 시작을 중복 수행하지 마세요.

GitHub·AWS 배포를 진행할 때만 본인 저장소, 실제 `PROJECT_DIR`, production Variables, OIDC 역할, S3, SSM Online EC2, 서버 환경 파일을 추가로 준비하세요.