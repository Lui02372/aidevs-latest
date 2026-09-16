# 실행 준비 가이드

## 1. 프로젝트와 실행 순서 한눈에 보기

이 폴더는 **여행 준비 채팅과 메모 저장을 제공하는 하나의 앱**입니다. 프론트엔드는 Streamlit, 백엔드는 FastAPI이며 PostgreSQL·Redis·선택한 LLM을 사용합니다. 별도 워커, MCP 서버, 멀티 에이전트 계층은 없습니다.

**권장 실행 경로는 README의 기본 구성인 `compose.yml`입니다.** 기존 공용 PostgreSQL·Redis가 있어야 합니다. 공용 서비스가 없는 PC에서는 **4-7의 전체 Compose 대체 경로**를 선택하세요.

> 아래 명령은 사용자가 이후 실행할 예시입니다. 문서 작성 중 설치·설정 변경·서버 실행은 수행하지 않았습니다. Project Player의 서버 실행 기능으로 시작했다면 수동 시작 명령을 중복 실행하지 마세요. 대체 Compose 파일을 실행기에서 선택할 수 있는지는 미확인입니다.

### 폴더 구조

```text
.
├─ compose.yml                 # 기존 공용 저장소를 사용하는 앱 2개
├─ compose.full-stack.yml      # 앱 + 자체 PostgreSQL·Redis + 선택 Ollama
├─ compose.release.yml         # 게시된 앱 이미지를 내려받아 실행
├─ release.env.example         # 이미지 저장소·태그 예제
├─ init_database.py            # 공용 PostgreSQL의 전용 스키마 초기화
├─ database/
│  └─ init.sql                 # 메모·채팅 테이블
├─ backend/
│  ├─ app.py                   # FastAPI 진입점·HTTP 라우트
│  ├─ services.py              # PostgreSQL·Redis·LLM 연결
│  ├─ test_app.py              # 가짜 의존성을 사용하는 API 테스트
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ .env.example
├─ frontend/
│  ├─ app.py                   # Streamlit 화면·백엔드 요청
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ .env.example
├─ README.md
├─ COMPOSE_EXPLAINED.md
├─ TROUBLESHOOTING.md
└─ guide.md
```

### 역할과 시작 순서

| 구성 요소 | 역할 | 기본 `compose.yml`에서의 위치 |
|---|---|---|
| PostgreSQL | 여행 메모·전체 채팅 이력 저장 | 기존 공용 서비스, 호스트 포트 `5433` |
| Redis | 최근 대화·세션·요청 횟수 저장 | 기존 공용 서비스, 호스트 포트 `6379` |
| Ollama | 선택적인 로컬 모델 실행 | 준비된 공용 서비스, 호스트 포트 `11434` |
| `backend` | API 요청 처리·저장소 및 모델 호출 | 이 프로젝트의 컨테이너, 포트 `8000` |
| `frontend` | 사용자 화면·백엔드 HTTP 요청 | 이 프로젝트의 컨테이너, 포트 `8501` |

**실행 순서:** 도구 확인 → 환경 파일 준비 → 이미지 빌드 → 공용 저장소 확인·DB 초기화 → 백엔드 준비 확인 → 프론트엔드 → 메모 실습 → 모델 준비 후 채팅.

| 접속 목적 | Windows에서 사용할 주소 |
|---|---|
| 앱 화면 | `http://127.0.0.1:8501` |
| API 문서 | `http://127.0.0.1:8000/docs` |
| 백엔드 프로세스 확인 | `http://127.0.0.1:8000/health/live` |
| 저장소 상태 확인 | `http://127.0.0.1:8000/health` |
| 요청 처리 준비 확인 | `http://127.0.0.1:8000/health/ready` |

API 키가 없어도 저장소 상태 확인과 메모 저장·조회를 할 수 있습니다. 실제 채팅에는 **준비된 Ollama 모델 또는 사용자가 발급한 OpenAI/Gemini API 키**가 필요합니다.

## 2. PowerShell

### 2-1. 작업 폴더 열기

**목적:** 상대 경로의 기준을 선택한 프로젝트로 맞춥니다.  
**작업 폴더·창:** 일반 권한 PowerShell을 열고 **창 A — 준비·실행**으로 사용합니다.

```powershell
Set-Location -LiteralPath 'C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose2'

Get-Location
Test-Path -LiteralPath '.\compose.yml'
Test-Path -LiteralPath '.\backend\requirements.txt'
Test-Path -LiteralPath '.\frontend\requirements.txt'
```

**예상 결과:** 지정한 경로와 세 개의 `True`.  
**실패 시:** 경로의 `aidevs-main\aidevs-main`과 마지막 폴더의 `compose2`를 확인하세요.

이후 **루트**는 위 경로입니다. 명령 블록은 한 단계씩 실행하고 결과를 확인한 뒤 다음으로 진행하세요.

### 2-2. 처음 한 번 필요한 도구

| 도구 | 필요 여부·버전 근거 | 확인 상태 |
|---|---|---|
| PowerShell | 명령 예시는 Windows PowerShell 5.1 호환 문법 | 사용자 창의 버전 미확인 |
| Docker Desktop | Linux 컨테이너 실행에 필요 | 설치·엔진 상태 미확인 |
| Docker Compose | `docker compose` 명령 사용. 프로젝트에 세부 버전 고정 없음 | 미확인 |
| Python | 기본 경로의 호스트 DB 초기화에 필요. 두 Dockerfile은 `python:3.12-slim` 사용 | 호스트 설치 미확인 |
| pip·venv | DB 초기화용 Python 환경 관리 | 미확인 |
| Git | 현재 파일로 로컬 실행할 때 필수 아님. GitHub 연결 시 필요 | 명령은 사용 가능했으나 버전 미확인 |
| Node.js·npm | 사용하지 않음. Streamlit 프론트엔드이며 `package.json`·npm scripts 없음 | 설치 불필요 |
| PostgreSQL·Redis 호스트 설치 | 이 가이드는 기존 공용 서비스 또는 전체 Compose 사용 | 직접 설치 불필요 |

**목적:** 필요한 도구의 명령을 확인합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
$PSVersionTable.PSVersion
docker --version
docker compose version
py -3.12 --version
```

**예상 결과:** 도구 버전이 표시되고 Python은 `3.12.x`.  
**실패 시:**

- Docker 명령이 없으면 Docker Desktop을 설치한 뒤 새 PowerShell 창을 여세요.
- `docker compose`가 없으면 Docker Desktop의 Compose 설치 상태를 확인하세요.
- `py -3.12`가 없으면 Python 3.12와 Windows의 `py` 실행기를 준비하세요.
- 전체 Compose 경로만 사용한다면 호스트 Python·venv 단계는 생략합니다.

Docker Desktop은 설치 후 시작 메뉴에서 직접 여세요. 이 프로젝트는 Linux 이미지를 사용합니다. WSL 2 백엔드를 선택했다면 Windows·WSL·가상화 요구 사항을 확인하세요. [Docker Desktop Windows 설치 안내](https://docs.docker.com/desktop/setup/install/windows-install/)

**목적:** Docker Desktop 창이 열린 상태와 엔진이 준비된 상태를 구분합니다.  
**작업 폴더·창:** 창 A·루트, Docker Desktop 시작 후.

```powershell
docker version
docker info --format '{{.OSType}}'
```

**예상 결과:** `Client`와 `Server` 정보가 모두 표시되고 운영체제 유형은 `linux`.  
**실패 시:** Docker Desktop의 엔진 시작 오류를 해결하세요. `Client`만 표시되면 엔진 준비가 끝난 상태가 아닙니다.

WSL 2 백엔드를 사용하는 경우에만 창 A에서 추가로 확인합니다.

```powershell
wsl --version
wsl --status
```

**예상 결과:** WSL 버전·상태 정보.  
**실패 시:** 위 Docker 공식 안내의 WSL 준비 절차를 확인하세요. 관리자 권한이나 시스템 설정 변경은 설치 과정에서 실제로 필요한 경우에만 수행합니다.

### 2-3. 기본 경로의 DB 초기화용 가상환경

Backend·Frontend는 Docker 안에서 실행합니다. 아래 `.venv`는 **`init_database.py`용**이며, 전체 Compose 경로에서는 필요하지 않습니다.

상위 과정 README는 공통 가상환경을 안내하지만, 여기서는 선택 폴더만 실행하기 쉽도록 전용 `.venv`를 사용합니다. 확인 당시 선택 폴더에는 `.venv`가 없었습니다.

**목적:** DB 초기화 도우미를 실행할 Python 환경을 준비합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
if (-not (Test-Path -LiteralPath '.\.venv')) {
    py -3.12 -m venv '.\.venv'
}

if (-not (Test-Path -LiteralPath '.\.venv\Scripts\python.exe')) {
    throw '가상환경 Python이 없습니다. 생성 결과를 확인하세요.'
}

& '.\.venv\Scripts\python.exe' --version
```

**예상 결과:** Python `3.12.x`.  
**실패 시:** Python 설치와 `.venv` 생성 오류를 확인하세요. 기존 환경은 이 프로젝트용이고 Python 3.12가 정상 실행될 때 재사용합니다. 다른 프로젝트의 환경이라면 그대로 설치를 진행하지 마세요.

버전을 확인한 뒤 같은 창에서 README가 지정한 초기화 의존성을 설치합니다.

```powershell
& '.\.venv\Scripts\python.exe' -m pip install 'psycopg[binary]>=3.2,<4' 'python-dotenv>=1.0,<2'
& '.\.venv\Scripts\python.exe' -m pip show psycopg python-dotenv
```

**예상 결과:** 두 패키지의 설치 정보.  
**실패 시:** 첫 설치 오류의 Python 버전·다운로드·인증서 문제를 확인하세요. 이후에도 가상환경 Python을 직접 호출합니다.

활성화는 선택 사항입니다. 창 A에서 원할 때만 실행하세요.

```powershell
& '.\.venv\Scripts\Activate.ps1'
```

**예상 결과:** 활성화된 환경 표시.  
**실패 시:** 실행 정책 오류라면 활성화를 생략하세요. 전역 실행 정책을 변경할 필요가 없습니다.

### 앱 의존성 설치 방식

앱 의존성은 Docker 이미지 빌드 중 각 Dockerfile의 `pip install --no-cache-dir -r requirements.txt`로 설치됩니다.

| 파일 | 명시된 버전 범위 |
|---|---|
| `backend/requirements.txt` | FastAPI `>=0.115,<1`, Uvicorn `>=0.34,<1`, Redis `>=5,<9`, psycopg `>=3.2,<4`, google-genai `>=2,<3`, openai `>=1.68,<3`, httpx `>=0.27,<1`, python-dotenv `>=1.0,<2` |
| `frontend/requirements.txt` | Streamlit `>=1.41,<2`, httpx `>=0.27,<1`, python-dotenv `>=1.0,<2` |

선택 프로젝트에서 잠금 파일은 발견되지 않았습니다. 설치되는 정확한 패키지 버전은 빌드 시점에 따라 달라질 수 있습니다.

## 3. 환경변수

### 3-1. 예제에서 환경 파일 준비

| 실제 예제 경로 | 복사 목적지 | 용도 |
|---|---|---|
| `backend/.env.example` | `backend/.env` | 백엔드 저장소·LLM 설정 |
| `frontend/.env.example` | `frontend/.env` | 프론트엔드의 백엔드 주소 |
| `release.env.example` | `release.env` | 선택적인 게시 이미지 실행 |
| 루트 `.env.example`·`ENVEXAMPLE` | 해당 예제 없음 | 루트 `.env`는 필요한 변수만 직접 준비 |

**목적:** 기존 환경 파일을 덮어쓰지 않고 준비합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
if (-not (Test-Path -LiteralPath '.\backend\.env')) {
    Copy-Item -LiteralPath '.\backend\.env.example' -Destination '.\backend\.env'
}

if (-not (Test-Path -LiteralPath '.\frontend\.env')) {
    Copy-Item -LiteralPath '.\frontend\.env.example' -Destination '.\frontend\.env'
}

Test-Path -LiteralPath '.\backend\.env'
Test-Path -LiteralPath '.\frontend\.env'
```

**예상 결과:** 두 개의 `True`. 기존 파일은 유지됩니다.  
**실패 시:** 작업 폴더·예제 파일·사용자의 쓰기 권한을 확인하세요.

확인 당시 `backend/.env`와 `frontend/.env`는 존재했습니다. **내용, 비밀값, 이미 입력된 값의 유효성은 읽거나 확인하지 않았습니다.** 조건부 복사는 기존 파일에 누락된 변수를 추가하지 않으므로 아래 표와 직접 대조하세요.

### 3-2. 반드시 확인할 설정

**목적:** 실제 실행 위치에 맞는 주소와 사용할 모델을 설정합니다.  
**작업 폴더·창:** 창 A·루트에서 편집기를 엽니다.

```powershell
notepad.exe '.\backend\.env'
notepad.exe '.\frontend\.env'
```

사용자가 편집기에서 확인할 내용:

1. **`frontend/.env`의 `BACKEND_URL`을 `http://backend:8000`으로 설정합니다.**
   - 예제의 `http://127.0.0.1:8000`은 Windows에서 프론트엔드를 직접 실행할 때의 주소입니다.
   - 예제 주석과 달리 기본·전체 Compose에는 이 값을 덮어쓰는 설정이 없습니다.
   - `compose.release.yml`만 `environment.BACKEND_URL`로 덮어씁니다.
2. 기본 경로의 `DATABASE_URL`·`REDIS_URL`을 공용 서비스의 실제 접속 정보와 맞춥니다.
3. 메모 기능부터 학습한다면 사용하지 않는 외부 API 키는 비워 두고 `OLLAMA_ENABLED=false`로 둡니다. Ollama가 준비됐다면 `true`를 사용합니다.

**예상 결과:** 환경 파일이 저장되고 프론트엔드가 컨테이너 이름 `backend`를 사용합니다.  
**실패 시:** 파일이 `.env.txt`로 저장되지 않았는지, 변수 철자가 맞는지 확인하세요. 이 프로젝트는 `API_BASE_URL`을 사용하지 않습니다.

### 3-3. 환경변수 표

아래 개발 기본값은 공개된 소스·예제의 값입니다. 실제 사용자 인증 정보를 확인한 결과가 아닙니다. `<사용자가 입력할 값>`은 사용자가 준비한 값으로 바꿔야 합니다.

| 변수명 | 근거 파일·설정 키 | 의미·사용 주체 | 안전한 기본값 또는 예시 | 필수·선택 | 사용자가 준비할 값 |
|---|---|---|---|---|---|
| `BACKEND_URL` | `frontend/app.py: BACKEND_URL`, `api()` | Streamlit 서버의 API 주소 | Docker: `http://backend:8000` | Docker에서 확인 필수 | 보통 왼쪽 개발 주소 |
| `DATABASE_URL` | `backend/services.py: PostgresRepository.__init__()` | 백엔드의 PostgreSQL 연결 | 기본 경로: `host.docker.internal:5433`, DB `agent_db` | 저장 기능에 필수 | 공용 DB의 실제 접속 문자열 |
| `REDIS_URL` | `RedisSessionStore.__init__()` | 백엔드의 Redis 연결 | `redis://host.docker.internal:6379/0` | readiness·채팅에 필수 | 공용 Redis의 주소·필요한 인증값 |
| `HOST_DATABASE_URL` | `init_database.py: host_database_url()` | Windows에서 DB 초기화 | 호스트 `127.0.0.1`, 포트 `5433`인 PostgreSQL URL | 기본 경로에서 명시 권장 | 루트 `.env`에 공용 DB 접속 문자열 |
| `OPENAI_API_KEY` | `MultiLLMChatService.configured()`, `reply()` | 외부 OpenAI API 인증 | 미사용 시 빈 값 | OpenAI 채팅 시 필수 | `<사용자가 입력할 값>` |
| `OPENAI_MODEL` | `MultiLLMChatService.model()` | OpenAI 모델 식별자 | 소스 기본값 `gpt-4.1-mini` | 선택 | 계정에서 호출 가능한 모델 |
| `GEMINI_API_KEY` | `configured()`, `reply()` | 외부 Gemini API 인증 | 미사용 시 빈 값 | Gemini 채팅 시 필수 | `<사용자가 입력할 값>` |
| `GEMINI_MODEL` | `model()` | Gemini 모델 식별자 | 소스 기본값 `gemini-3.5-flash` | 선택 | 계정에서 호출 가능한 모델 |
| `OLLAMA_ENABLED` | `configured()` | Ollama 사용 허용 | 미준비 시 `false`; 예제는 `true` | Ollama 채팅 시 `true` 필요 | 사용 여부 |
| `OLLAMA_BASE_URL` | `reply()`, 전체 Compose의 `backend.environment` | 백엔드가 접근할 Ollama | 기본: `http://host.docker.internal:11434`; 전체: `http://ollama:11434` | Ollama 사용 시 필수 | 실행 위치에 맞는 주소 |
| `OLLAMA_MODEL` | `model()` | 화면의 `llama` 선택에 대응 | `llama3.2` | 선택 | 설치한 모델 태그 |
| `GEMMA_MODEL` | `model()` | 화면의 `gemma` 선택에 대응 | `gemma3:4b` | 선택 | 설치한 모델 태그 |
| `POSTGRES_USER` | 전체 Compose의 `database.environment`·백엔드 URL 보간 | 자체 DB 사용자 | 공개 개발 기본값 `agent_user` | 전체 경로에서 선택 | 변경한다면 사용자가 정한 이름 |
| `POSTGRES_PASSWORD` | 같은 설정 | 자체 DB 암호 | 공개 실습 기본값 `agent_pwd` | 전체 경로에서 선택 | 실습 외 용도에서는 사용자가 정한 암호 |
| `POSTGRES_DB` | 같은 설정 | 자체 DB 이름 | `agent_db` | 전체 경로에서 선택 | 변경할 DB 이름 |
| `DOCKERHUB_USERNAME` | 각 Compose의 `image`, `release.env.example` | 이미지 저장소 사용자·조직명 | 로컬 빌드는 `local` 기본값 | release 경로에서 필수 | 실제 이미지 게시자 |
| `IMAGE_TAG` | 각 Compose의 `image`, `release.env.example` | 이미지 버전 | Compose 기본 `latest`; 예제 `1.0.0` | release 경로에서 확인 필수 | 실제 게시된 태그 |

`backend/.env.example`의 DB 개발 계정은 `agent_user` / `agent_pwd`, DB는 `agent_db`입니다. 공용 서비스가 이 값으로 준비됐는지는 미확인입니다.

모델 이름은 **소스에 적힌 기본값**입니다. 외부 서비스의 현재 제공 여부나 계정 권한은 검증하지 않았습니다. Codex의 ChatGPT 로그인·구독 인증은 이 앱의 API 키가 아니며 복사해서 사용하지 않습니다.

### 3-4. 기본 경로의 DB 초기화용 루트 `.env`

`init_database.py`는 **루트 `.env`**를 읽습니다. `backend/.env`는 자동으로 읽지 않습니다. Backend 예제에 있는 `HOST_DATABASE_URL`도 해당 파일에만 두면 초기화 도우미에 전달되지 않습니다.

**목적:** 초기화 대상과 백엔드가 사용할 DB를 일치시킵니다.  
**작업 폴더·창:** 창 A·루트. 전체 Compose 경로에서는 생략합니다.

```powershell
notepad.exe '.\.env'
```

사용자가 루트 `.env`에 `HOST_DATABASE_URL=<사용자가 입력할 값>` 한 줄을 작성합니다. 저장하기 전에 자리표시자를 **Windows에서 접속할 실제 PostgreSQL URL 전체**로 바꾸세요.

- 백엔드의 `DATABASE_URL`과 사용자·암호·DB 이름이 같아야 합니다.
- Windows 초기화 주소는 `127.0.0.1:5433`입니다.
- 백엔드 컨테이너 주소는 `host.docker.internal:5433`입니다.
- 암호에 URL 예약 문자가 포함되면 접속 URL에 맞게 인코딩해야 합니다.

**예상 결과:** 루트 `.env`에 초기화용 접속 문자열이 저장됩니다.  
**실패 시:** 공용 DB 담당자에게 접속 정보와 전용 스키마·테이블 생성 권한을 확인하세요.

소스는 `HOST_DATABASE_URL` → `DATABASE_URL`의 호스트명 치환 → 공개 개발 기본 URL 순서로 선택합니다. 의도한 DB를 지정하려면 `HOST_DATABASE_URL`을 명시하는 편이 분명합니다.

### 3-5. 설정 전달 방식의 차이

| 방식 | 이 프로젝트에서의 역할 |
|---|---|
| `backend/.env`, `frontend/.env` | 각 Compose의 `env_file`이 해당 컨테이너에 전달 |
| 루트 `.env` | Compose의 `${변수}` 보간에 사용. 초기화 도우미도 이 파일을 읽음 |
| 현재 PowerShell의 `$env:` | 현재 프로세스와 자식 프로세스의 환경. `.env` 파일을 수정하지 않으며 다른 창과도 별개 |
| Compose `environment` | 같은 변수에 대해 서비스 `env_file`보다 우선 |
| `--env-file '.\release.env'` | release 이미지 이름 등의 Compose 보간값 제공 |
| GitHub Secrets·Variables | workflow가 명시적으로 참조할 때 runner에 전달. 로컬 `.env`로 자동 복사되지 않음 |

- 전체 Compose는 백엔드의 DB·Redis·Ollama 주소를 내부 서비스 주소로 덮어씁니다.
- release Compose는 DB·Redis 주소도 `environment`로 지정합니다. 사용자 지정 주소라면 `release.env`의 보간값까지 맞춰야 합니다.
- 기본 Compose에서 `$env:BACKEND_URL`만 설정해도 `frontend/.env` 대신 컨테이너에 전달되는 것은 아닙니다. `frontend/.env`를 맞추세요.
- 로컬 Python의 `load_dotenv()`는 기본적으로 이미 설정된 프로세스 환경변수를 덮어쓰지 않습니다.
- Streamlit은 서버에서 API를 호출하지만 `BACKEND_URL`은 화면에도 표시합니다. 프론트엔드에 API 키·암호를 넣지 마세요.

## 4. Docker

### 4-1. 실행 구성과 주소

| Compose 파일 | 프로젝트 이름 | 서비스·프로필 | 호스트 포트·볼륨 |
|---|---|---|---|
| `compose.yml` | `simple-multi-llm-app` | `backend`, `frontend`; 프로필 없음 | `8000`, `8501`; 자체 저장소 볼륨 없음 |
| `compose.full-stack.yml` | `simple-multi-llm-full-stack` | `redis`, `database`, `backend`, `frontend`; `ollama`는 `ollama` 프로필 | 앱 포트만 공개. `redis_data`, `postgres_data`, `ollama_data` |
| `compose.release.yml` | `release-simple-multi-llm` | 게시된 `backend`, `frontend` 이미지 | `8000`, `8501`; 자체 저장소 볼륨 없음 |

Compose 상대 경로는 선택한 Compose 파일이 있는 루트를 기준으로 합니다. 모든 예제는 루트에서 실행합니다.

| 호출 위치 | 백엔드 | PostgreSQL | Redis | Ollama |
|---|---|---|---|---|
| Windows 호스트 | `127.0.0.1:8000` | 기본 공용: `127.0.0.1:5433` | 기본 공용: `127.0.0.1:6379` | 기본 공용: `127.0.0.1:11434` |
| 기본 앱 컨테이너 | `backend:8000` | `host.docker.internal:5433` | `host.docker.internal:6379` | `host.docker.internal:11434` |
| 전체 Compose 내부 | `backend:8000` | `database:5432` | `redis:6379` | `ollama:11434` |

컨테이너 안의 `localhost`·`127.0.0.1`은 **그 컨테이너 자신**입니다. 전체 Compose의 저장소·Ollama에는 호스트 포트 매핑이 없으므로 Windows의 `localhost`로 직접 접속하는 구성은 아닙니다.

### 4-2. 권장 경로: 설정 검사와 이미지 빌드

**목적:** 기본 Compose와 환경 파일 참조를 검사하고 앱 의존성을 이미지에 설치합니다.  
**작업 폴더·창:** 창 A·루트. 빌드 중에는 이 창을 유지합니다.

```powershell
docker compose -f '.\compose.yml' config --quiet
```

**예상 결과:** 오류 없이 종료하며 보통 출력이 없습니다.  
**실패 시:** `backend/.env`·`frontend/.env` 존재 여부와 YAML을 확인합니다. 전체 설정을 출력하는 `config` 대신 `config --quiet`를 사용합니다.

검사가 성공한 뒤 빌드합니다.

```powershell
docker compose -f '.\compose.yml' build backend frontend
```

**예상 결과:** 두 이미지 빌드 성공.  
**실패 시:** 처음 실패한 Dockerfile 단계에서 이미지 다운로드, requirements 설치, 네트워크·디스크 공간을 확인하세요.

백엔드 시작 명령은 Dockerfile의 `uvicorn app:app --host 0.0.0.0 --port 8000`, 프론트엔드는 `streamlit run app.py --server.address=0.0.0.0 --server.port=8501`입니다. 호스트에서 별도로 실행하지 않습니다.

### 4-3. 공용 저장소 확인과 DB 초기화

**목적:** 백엔드보다 먼저 필요한 저장소를 확인합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
Test-NetConnection -ComputerName '127.0.0.1' -Port 5433 -InformationLevel Quiet
Test-NetConnection -ComputerName '127.0.0.1' -Port 6379 -InformationLevel Quiet
```

**예상 결과:** 둘 다 `True`. 이는 TCP 연결 확인이며 DB 인증·스키마 정상 여부까지 보장하지 않습니다.  
**실패 시:** 공용 서비스가 준비돼 있는지 담당자·기존 수업 안내에서 확인하세요. 기본 Compose에는 이 서비스를 만드는 정의가 없습니다. 공용 서비스가 없다면 4-7로 이동합니다.

**목적:** 공용 PostgreSQL에 이 앱의 테이블을 준비합니다.  
**작업 폴더·창:** 창 A·루트. 2-3의 venv와 3-4의 루트 `.env` 준비 후 실행합니다.

```powershell
& '.\.venv\Scripts\python.exe' '.\init_database.py'
```

**예상 결과:**

```text
Database 초기화가 완료되었습니다.
- simple_multi_llm.chat_messages
- simple_multi_llm.notes
```

**실패 시:** `init_database.py: host_database_url()`의 설정 위치, DB 주소·인증·생성 권한, `database/init.sql`을 확인하세요.

이 명령은 실제 DB에 스키마·테이블·인덱스를 생성합니다. 현재 SQL은 `CREATE ... IF NOT EXISTS`를 사용하며 기존 데이터를 삭제하지 않습니다.

### 4-4. 백엔드 시작과 준비 확인

**목적:** 저장소가 준비된 뒤 API 서버를 시작합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
docker compose -f '.\compose.yml' up -d backend
docker compose -f '.\compose.yml' ps
```

**예상 결과:** `backend`가 실행되고 잠시 후 `healthy`로 표시됩니다. `-d`는 컨테이너를 백그라운드에서 실행합니다.  
**실패 시:** 아래 로그와 readiness 결과로 원인을 좁히세요.

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/live'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready'
```

**예상 결과:** 첫 응답은 `status: ok`, `service: backend`. 두 번째는 HTTP 200과 `status: ok`.  
**실패 시:** 연결 거부는 컨테이너·포트, HTTP 503은 Redis·DB·스키마를 확인합니다.

`/health/ready`의 성공 조건은 Redis 연결, PostgreSQL 연결, 두 테이블 존재입니다. **LLM 키·모델의 실제 호출 성공은 readiness 조건에 포함되지 않습니다.**

### 4-5. 프론트엔드 시작과 접속

**목적:** 준비된 백엔드에 연결할 화면을 시작합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
docker compose -f '.\compose.yml' up -d frontend
docker compose -f '.\compose.yml' ps
```

**예상 결과:** `backend`는 healthy, `frontend`는 실행 상태. 프론트엔드에는 별도 Compose healthcheck가 없습니다.  
**실패 시:** `depends_on.backend.condition: service_healthy` 때문에 백엔드가 unhealthy이면 프론트엔드 시작이 막힐 수 있습니다.

같은 창에서 화면 응답을 확인합니다.

```powershell
(Invoke-WebRequest -Uri 'http://127.0.0.1:8501' -UseBasicParsing).StatusCode
```

**예상 결과:** `200`. 브라우저에서 `http://127.0.0.1:8501`을 열면 `Multi-LLM 여행 준비 Chat2` 화면이 표시됩니다.  
**실패 시:** 프론트엔드 로그·포트 `8501`을 확인하세요. 화면은 열리는데 API만 실패하면 `frontend/.env`의 `BACKEND_URL`부터 확인합니다.

### 4-6. 로그 확인·설정 반영·종료

**목적:** 실행 중 오류를 관찰합니다.  
**작업 폴더·창:** 새 PowerShell **창 B — 로그 확인**을 열고 루트로 이동합니다.

```powershell
Set-Location -LiteralPath 'C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose2'

docker compose -f '.\compose.yml' logs --tail=100 -f backend frontend
```

**예상 결과:** 두 서비스의 최근 로그와 새 로그가 표시됩니다.  
**실패 시:** 사용한 Compose 파일·프로젝트 이름을 확인하세요. `Ctrl+C`는 이 로그 보기만 끝냅니다. 로그 공유 전에는 키·접속 문자열·사용자 입력을 가리세요.

**설정을 바꾼 경우에만**, 창 A·루트에서 컨테이너를 다시 만듭니다.

```powershell
docker compose -f '.\compose.yml' up -d --build --force-recreate backend frontend
```

**예상 결과:** 변경된 코드·환경 설정으로 앱 컨테이너가 교체됩니다.  
**실패 시:** 빌드의 첫 오류 또는 백엔드 readiness를 확인하세요. 실행 중 컨테이너에는 `.env` 편집이 자동 반영되지 않습니다.

**목적:** 기본 경로로 시작한 이 앱을 종료합니다.  
**작업 폴더·창:** 창 A·루트. Project Player로 시작했다면 해당 실행기의 종료 기능을 사용하세요.

```powershell
docker compose -f '.\compose.yml' down
docker compose -f '.\compose.yml' ps
```

**예상 결과:** 이 프로젝트의 앱 컨테이너가 제거되고 실행 목록이 비어 있습니다. 기존 공용 저장소는 이 Compose의 관리 대상이 아닙니다.  
**실패 시:** 시작할 때 사용한 Compose 파일과 현재 작업 폴더를 확인하세요.

### 4-7. 대체 경로: 공용 서비스가 없는 PC

이 경로는 **4-2~4-6을 대신합니다.** 기본 경로가 실행 중이면 해당 경로의 종료 절차를 먼저 사용하세요. 두 구성은 같은 앱 포트를 사용합니다.

2-1·2-2와 3-1·3-2는 필요하지만 호스트 venv, 루트 `HOST_DATABASE_URL`, `init_database.py`는 생략합니다.

전체 Compose는 다음을 사용합니다.

- Redis: `redis:7-alpine`, AOF 데이터는 `redis_data`
- PostgreSQL: `postgres:17-alpine`, 데이터는 `postgres_data`
- SQL: `database/init.sql`을 초기화 경로에 읽기 전용 마운트
- Ollama: 선택 프로필, 모델은 `ollama_data`
- 백엔드: DB·Redis가 healthy가 된 뒤 시작
- 프론트엔드: 백엔드가 healthy가 된 뒤 시작

#### 검사·빌드

**목적:** 전체 구성을 검사하고 앱 이미지를 빌드합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
docker compose -f '.\compose.full-stack.yml' config --quiet
```

**예상 결과:** 오류 없이 종료.  
**실패 시:** 두 앱의 `.env` 존재 여부를 확인합니다.

성공한 뒤 빌드합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' build backend frontend
```

**예상 결과:** 이미지 빌드 성공.  
**실패 시:** Dockerfile·requirements·다운로드 오류를 확인하세요.

#### 저장소 → 백엔드 → 프론트엔드

**목적:** 자체 저장소부터 시작합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
docker compose -f '.\compose.full-stack.yml' up -d redis database
docker compose -f '.\compose.full-stack.yml' ps
```

**예상 결과:** `redis`·`database`가 잠시 후 healthy.  
**실패 시:** 해당 서비스 로그를 확인하세요.

기본 DB 사용자·이름을 바꾸지 않았다면 같은 창에서 확인합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' exec redis redis-cli ping
docker compose -f '.\compose.full-stack.yml' exec database pg_isready -U agent_user -d agent_db
```

**예상 결과:** `PONG`, `accepting connections`.  
**실패 시:** 사용자·DB 이름을 변경했다면 위 인수를 실제 값으로 맞추세요. `pg_isready`만으로 테이블 존재까지 확인되지는 않습니다.

PostgreSQL은 **데이터 볼륨이 처음 비어 있을 때만** `init.sql`을 자동 실행합니다. 기존 볼륨을 재사용하면 SQL이 다시 실행되지 않습니다.

**목적:** 백엔드의 저장소·스키마 준비를 확인합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
docker compose -f '.\compose.full-stack.yml' up -d backend
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready'
```

**예상 결과:** 준비가 끝난 뒤 HTTP 200과 `status: ok`.  
**실패 시:** 시작 직후라면 잠시 뒤 확인하고, 계속 503이면 DB·Redis·스키마 상태를 확인합니다.

성공한 뒤 프론트엔드를 시작합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' up -d frontend
docker compose -f '.\compose.full-stack.yml' ps
```

**예상 결과:** 앱과 저장소 네 서비스가 실행됩니다. 화면은 `http://127.0.0.1:8501`입니다.  
**실패 시:** `frontend/.env`의 `BACKEND_URL=http://backend:8000`과 백엔드 상태를 확인하세요.

#### 선택: API 키 없는 Ollama 채팅

**목적:** 자체 Ollama에 실제 모델 하나를 준비합니다.  
**작업 폴더·창:** 창 A·루트. 모델 다운로드가 끝날 때까지 창을 유지합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama up -d ollama
docker compose -f '.\compose.full-stack.yml' --profile ollama exec ollama ollama pull llama3.2
docker compose -f '.\compose.full-stack.yml' --profile ollama exec ollama ollama list
```

**예상 결과:** 모델 목록에 `llama3.2`가 표시됩니다.  
**실패 시:** Ollama 시작 로그·네트워크·디스크 및 메모리 여유를 확인하세요. 시작 직후 연결 오류라면 Ollama 준비 후 다운로드를 다시 시도합니다.

사용자가 `backend/.env`에서 `OLLAMA_ENABLED=true`, `OLLAMA_MODEL=llama3.2`를 확인한 뒤 같은 창에서 반영합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama up -d --force-recreate backend frontend
```

**예상 결과:** 화면에서 Provider `ollama`, Model `llama`를 선택해 채팅할 수 있습니다.  
**실패 시:** 실제 모델 태그와 설정값, Ollama 로그를 확인하세요. 화면의 `gemma`를 선택하려면 `GEMMA_MODEL`에 해당하는 모델을 별도로 준비해야 합니다.

#### 전체 구성의 로그·종료

**목적:** 전체 구성의 오류를 확인합니다.  
**작업 폴더·창:** 창 B·루트.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama logs --tail=100 backend frontend database redis ollama
```

**예상 결과:** 생성된 서비스의 최근 로그.  
**실패 시:** 전체 Compose 파일과 실행한 서비스 이름을 확인하세요.

**목적:** 전체 경로로 시작한 서비스를 종료합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama down
docker compose -f '.\compose.full-stack.yml' --profile ollama ps
```

**예상 결과:** 실행 목록이 비고 이름 있는 볼륨은 보존됩니다.  
**실패 시:** 시작한 Compose 프로젝트가 맞는지 확인하세요. 기본 종료 절차에 볼륨 삭제 옵션은 사용하지 않습니다.

### 4-8. 별도 경로: 게시된 이미지 실행

`compose.release.yml`은 운영자가 게시한 앱 이미지를 받는 구성입니다. 공용 저장소·DB 스키마·필요한 모델과 **실제 이미지 게시자·태그**가 먼저 준비돼 있어야 합니다.

**목적:** 게시 이미지의 위치를 설정합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
if (-not (Test-Path -LiteralPath '.\release.env')) {
    Copy-Item -LiteralPath '.\release.env.example' -Destination '.\release.env'
}

notepad.exe '.\release.env'
```

사용자가 `DOCKERHUB_USERNAME`의 예제 자리표시자를 실제 게시자로, `IMAGE_TAG`를 실제 게시된 태그로 바꿉니다. 사용자 지정 공용 DB·Redis라면 `DATABASE_URL`·`REDIS_URL`도 이 파일에 맞춰야 합니다.

**예상 결과:** 실제 이미지와 저장소를 가리키는 설정.  
**실패 시:** 운영자에게 이미지 이름·태그·접근 권한을 확인하세요. 현재 게시 여부는 미확인입니다.

다른 경로의 앱을 종료하고 환경 파일·DB를 준비한 뒤 검사합니다.

```powershell
docker compose --env-file '.\release.env' -f '.\compose.release.yml' config --quiet
```

**예상 결과:** 오류 없이 종료.  
**실패 시:** 필수 이미지 사용자명과 환경 파일 경로를 확인합니다.

검사가 성공한 뒤 시작합니다.

```powershell
docker compose --env-file '.\release.env' -f '.\compose.release.yml' up -d
docker compose --env-file '.\release.env' -f '.\compose.release.yml' ps
```

**예상 결과:** `pull_policy: always`에 따라 지정 이미지를 확인·다운로드하고 앱이 실행됩니다. 접속 주소는 기본 경로와 같습니다.  
**실패 시:** 이미지 이름·태그·Registry 접근 권한 또는 백엔드 readiness를 확인하세요.

같은 창에서 필요할 때 로그 확인과 종료를 각각 수행합니다.

```powershell
docker compose --env-file '.\release.env' -f '.\compose.release.yml' logs --tail=100 backend frontend
```

**예상 결과:** release 앱 로그. **실패 시:** 시작 시 사용한 설정 파일을 확인합니다.

```powershell
docker compose --env-file '.\release.env' -f '.\compose.release.yml' down
docker compose --env-file '.\release.env' -f '.\compose.release.yml' ps
```

**예상 결과:** release 앱 종료. **실패 시:** 프로젝트·환경 파일을 확인합니다.

## 5. GitHub Actions

### 5-1. 발견한 workflow와 이 프로젝트의 관계

선택 폴더에는 `.github`가 없습니다. 세 단계 위 과정 폴더의 `../../../.github/workflows/`에서 실제 YAML 세 개를 확인했습니다.

`git rev-parse --show-toplevel`은 현재 경로를 Git 저장소로 인식하지 못했습니다. **로컬 workflow 파일은 있지만 연결된 GitHub 저장소·활성화 상태·실행 결과는 미확인**입니다. 원격 URL과 인증 정보는 읽지 않았습니다.

로컬 앱 실행에 GitHub Actions는 필수가 아닙니다.

| 실제 workflow 경로 | `on` 트리거·브랜치·경로 조건 | job 순서·runner |
|---|---|---|
| `../../../.github/workflows/07-runtime-ci.yml` | `push`, `pull_request`: `07_multi-agent-service-ops/00_runtime-and-deployment/**` 또는 `.github/workflows/07-runtime-ci.yml` 변경. 브랜치 필터 없음. `workflow_dispatch` 있음 | `test-and-build` 하나, `needs` 없음. `ubuntu-latest` |
| `../../../.github/workflows/07-weather-mcp-cicd.yml` | push·PR: `05_weather-mcp-deployment-project` 아래 `backend/**`, `frontend/**`, `mcp_server/**`, `compose.yml`. 브랜치 필터 없음. 수동 `deploy` 입력 기본 `false` | `test-and-build` → `deploy`, `needs: test-and-build`. 둘 다 `ubuntu-latest` |
| `../../../.github/workflows/07-weather-stateful-cicd.yml` | push·PR: `06_weather-mcp-stateful-deployment` 아래 `backend/**`, `frontend/**`, `mcp_server/**`, `database/**`, `compose.infrastructure.yml`, `compose.application.yml`. 브랜치 필터 없음. 수동 `deploy` 입력 기본 `false` | `test-and-build` → `deploy-stateful-service`, `needs: test-and-build`. 둘 다 `ubuntu-latest` |

05·06의 위 경로는 저장소 기준 `07_multi-agent-service-ops/00_runtime-and-deployment/` 아래입니다. 해당 두 workflow는 자신들의 YAML 변경을 별도 `paths` 항목으로 넣지 않았습니다.

### 5-2. 실제 검사·빌드·배포 범위

**Runtime CI**

`defaults.run.working-directory`는 다음 경로입니다.

`07_multi-agent-service-ops/00_runtime-and-deployment/01_simple-multi-llm-compose`

**끝에 `2`가 없습니다.** 선택 프로젝트의 변경은 트리거할 수 있지만 실제 검사는 형제 프로젝트에서 수행합니다.

한 job 안에서 다음 순서로 실행합니다.

1. `Checkout`: `actions/checkout@v4`
2. `Set up Python`: `actions/setup-python@v5`, Python `3.12`
3. `Install test dependencies`: backend requirements와 `pytest` 설치
4. `Test backend contracts`: `python -m pytest backend/test_app.py -q`
5. `Validate Compose`: `docker compose config --quiet`
6. `Build images`: `docker compose build`

권한은 `contents: read`입니다. 이미지 게시·배포·실제 LLM 통합 확인 단계는 없습니다. **이 CI의 통과를 compose2 검증 결과로 볼 수 없습니다.**

**05 Weather CI/CD**

- 검사 job 작업 폴더: `07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project`
- 테스트 step은 그 아래 `backend`에서 실행합니다.
- Python 3.12 → Fake MCP·LLM 기반 테스트 → Compose 검사 → 세 이미지 빌드 순서입니다.
- 배포 job은 runner의 기본 체크아웃 위치에서 소스를 복사하고, EC2의 `~/weather-mcp-deployment`에서 `.env` 확인 → Compose 검사 → 빌드·실행 → readiness 확인을 수행합니다.

**06 Stateful Weather CI/CD**

- 검사 job 작업 폴더: `07_multi-agent-service-ops/00_runtime-and-deployment/06_weather-mcp-stateful-deployment`
- 테스트 명령은 `backend`로 이동한 뒤 실행합니다.
- Python 3.12 → Fake 저장소 테스트 → 인프라·앱 Compose 검사 → 앱 이미지 빌드 순서입니다.
- 배포 job은 EC2의 `~/weather-stateful`에서 인프라를 먼저 시작하고 앱을 다시 만든 뒤 readiness를 확인합니다.

05·06 배포 job은 선행 검사 성공 후 **`main` push 또는 수동 실행의 `deploy=true`** 조건에서 실행되며 `production` environment를 사용합니다. 두 배포 모두 선택한 compose2의 배포가 아닙니다.

### 5-3. 연결 대상·권한·Secrets

| 연결할 대상 | 필요한 권한 | Secret·Variable 이름 | 설정 위치 | 사용 job | 사용자가 준비할 값 |
|---|---|---|---|---|---|
| Runtime CI용 GitHub 저장소 | 저장소 접근·workflow 관리 및 실행 권한. YAML은 `contents: read` | 사용자 지정 Secret·Variable 없음 | 저장소 Actions 설정 | `test-and-build` | 연결할 저장소·브랜치 |
| 05·06의 EC2 SSH 인증 | 해당 서버 SSH 접속 권한 | `AWS_SSH_PRIVATE_KEY` | 저장소 Settings → Secrets and variables → Actions 또는 `production` environment Secrets | `deploy`, `deploy-stateful-service` | 해당 배포용 개인키 |
| 같은 SSH 서버의 신원 확인 | 검증된 호스트 키 | `AWS_SSH_KNOWN_HOSTS` | 같은 위치 | 같은 배포 job | 검증한 known_hosts 내용 |
| 같은 EC2 주소 | 서버 접근 권한 | `AWS_HOST` | 같은 위치 | 같은 배포 job | 서버 주소 |
| 같은 EC2 로그인 | 원격 배포 명령 실행 권한 | `AWS_USER` | 같은 위치 | 같은 배포 job | SSH 사용자명 |

05·06의 AWS Secrets는 compose2의 로컬 실행이나 Runtime CI에 필요하지 않습니다. 확인한 YAML에는 `vars.*` 참조나 Docker Hub 인증 Secret, compose2 자동 배포 job이 없습니다.

### 5-4. 선택 프로젝트용 CI 준비 제안

다음은 **사용자가 이후 수행할 준비 제안**입니다.

1. 과정 전체를 관리할지 compose2만 별도 저장소로 관리할지 정합니다.
2. 선택한 구조에 맞춰 `working-directory`와 `paths`를 compose2로 조정한 전용 workflow를 준비합니다.
3. Compose 검사 전에 예제에서 CI용 `backend/.env`·`frontend/.env`를 준비하는 step을 넣습니다. 현재 Runtime CI에는 이 단계가 없습니다.
4. `backend/test_app.py`의 Fake Redis·DB·LLM을 사용해 외부 키 없이 계약 테스트를 수행합니다.
5. `.env`·인증 파일·사용자 로그가 커밋 대상에 포함되지 않는지 검토합니다.
6. 필요한 GitHub 권한 승인·저장소 연결·push·수동 실행은 사용자가 수행합니다. 배포는 별도 작업입니다.

**목적:** GitHub 연결 전 로컬 Git 인식 상태를 확인합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
git --version
git rev-parse --show-toplevel
```

**예상 결과:** Git 버전과 저장소 루트. 현재 확인에서는 두 번째 명령이 `not a git repository`로 실패했습니다.  
**실패 시:** 사용할 저장소와 연결 방법을 먼저 정하세요. 이 명령은 저장소를 생성하거나 연결하지 않습니다.

수동 실행에는 기본 브랜치에 있는 `workflow_dispatch` 정의와 저장소 쓰기 권한이 필요합니다. [GitHub 수동 workflow 실행 안내](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)

### 5-5. Actions 오류 찾기

**목적:** 실패한 작업을 step 단위로 좁힙니다.  
**작업 위치·창:** GitHub 웹 브라우저. PowerShell 명령 없이 화면에서 확인합니다.

**순서:** 저장소 → Actions → workflow → 해당 run → 실패한 job → 실패 step → 첫 오류 로그.

| 실패 위치 | 실제 YAML에 맞춰 확인할 사항 |
|---|---|
| 실행 기록 없음 | `on.paths`, 이벤트 종류, Actions 활성화·접근 권한 |
| `Checkout` | 저장소 접근, `contents: read`, 조직의 Actions 허용 설정 |
| `Set up Python` | Python `3.12`, setup-python step 오류 |
| 의존성 설치 | `working-directory`, requirements 경로, 다운로드·버전 충돌 |
| Backend 테스트 | 검사 대상이 compose2인지, import 경로, 첫 실패 assertion |
| `Validate Compose` | 필요한 `.env` 준비 여부·검사 대상 Compose 파일 |
| 이미지 빌드 | build 경로·Dockerfile의 COPY 대상·패키지 및 이미지 다운로드 |
| 05·06 SSH 배포 | 해당 프로젝트 Secrets·호스트 키·원격 `.env`·Docker 준비 |

**예상 결과:** 실패 원인을 특정 step과 파일로 연결할 수 있습니다.  
**다음 행동:** 초록색 run도 실제 검사 작업 폴더를 확인하세요. 외부 인증이 필요한 배포 준비 전까지 로컬 앱과 Fake 기반 CI 학습은 가능합니다.

## 6. 완료 확인

### 6-1. 구성 요소별 확인

**목적:** 화면·백엔드·저장소를 나눠 확인합니다.  
**작업 폴더·창:** 창 A·루트. 어느 Compose 경로로 실행했든 앱 URL은 같습니다.

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/live'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready'
(Invoke-WebRequest -Uri 'http://127.0.0.1:8501' -UseBasicParsing).StatusCode
```

**예상 결과:**

| 대상 | 기대 결과 | 판단 범위 |
|---|---|---|
| `/health/live` | `status=ok`, `service=backend` | 백엔드 프로세스 응답 |
| `/health/ready` | HTTP 200, `status=ok` | Redis·PostgreSQL·두 테이블 준비 |
| 프론트엔드 `/` | HTTP 200 | 화면 서버 응답 |
| 브라우저의 서비스 상태 → Health 확인 | 저장소 항목 `true` | 프론트엔드→백엔드 연결 |
| `checks.providers` | 설정에 따른 `true`·`false` | 키 존재·Ollama 허용 여부만 확인 |

**실패 시:** 다음 문제 해결 표에서 해당 구성 요소부터 점검하세요. Provider의 `true`는 키 유효성·모델 설치·실제 응답 성공을 뜻하지 않습니다.

### 6-2. 첫 사용자 시나리오: 여행 메모 저장

**목적:** 외부 API 키 없이 프론트엔드→백엔드→DB 흐름을 확인합니다.  
**작업 위치·창:** `http://127.0.0.1:8501`을 연 브라우저. 입력 작업은 화면에서 수행합니다.

1. **여행 메모** 탭을 선택합니다.
2. 이름에 `실습사용자`, 메모에 `여행 전 교통편 확인`을 입력합니다.
3. **메모 저장**을 누릅니다.
4. **메모 조회**를 누릅니다.
5. **서비스 상태 → Health 확인**을 누릅니다.

**예상 결과:** 저장 응답에 `note`가 있고 조회 목록에 방금 입력한 내용이 표시됩니다. 정상 Redis 연결이면 저장 응답의 `warning`은 비어 있습니다.

사용자가 원하면 창 A·루트에서 API도 확인할 수 있습니다.

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/notes'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/stats'
```

**예상 결과:** 메모 목록과 Redis 요청 통계.  
**실패 시:** 메모 API는 PostgreSQL, 통계 API는 Redis 연결부터 확인하세요.

### 6-3. 모델 준비 후 채팅

**목적:** 실제 LLM 호출을 확인합니다.  
**작업 위치·창:** 브라우저의 **Multi-LLM Chat** 탭.

1. 준비한 Provider를 선택합니다.
2. Ollama라면 내려받은 모델에 맞춰 `llama` 또는 `gemma`를 선택합니다.
3. `부산 당일 여행 준비물 세 가지를 알려줘`를 입력합니다.

**예상 결과:** 답변과 Provider·Model·`Fallback: False`가 표시됩니다.  
**실패 시:** 키·모델·접속 주소와 백엔드 로그를 확인하세요. 실행 앱은 Provider 실패를 가짜 성공으로 바꾸지 않습니다.

채팅 실패 전에 사용자 메시지가 PostgreSQL에 먼저 저장될 수 있으므로, 오류가 났다고 데이터가 전혀 기록되지 않았다고 판단하지 마세요.

## 7. 문제 해결

| 증상 | 원인·확인 위치 | 해결 순서 |
|---|---|---|
| `8000`·`8501` 포트 사용 오류 | 다른 앱 또는 다른 Compose 경로가 실행 중 | 포트 소유 PID 확인 → 해당 앱 식별 → 그 앱의 정상 종료 절차 사용 |
| venv Python 없음·버전 불일치 | 다른 폴더의 환경 또는 불완전한 생성 | 루트 확인 → `.venv\Scripts\python.exe` 존재·버전 확인 → 올바른 환경 준비 |
| `psycopg`·`dotenv` 모듈 누락 | 초기화 의존성을 다른 Python에 설치 | 2-3의 가상환경 Python으로 pip 설치 |
| Docker 엔진 연결 실패 | Docker Desktop 미시작·엔진 오류 | Desktop 시작 → `docker version`의 Server 확인 → Linux 엔진 확인 |
| 환경 파일을 찾지 못함 | 파일 누락·잘못된 폴더·`.env.txt` | `Test-Path` → 조건부 복사 → 파일 이름 확인 |
| Backend unhealthy·readiness 503 | Redis·DB·스키마 미준비 | `/health` 확인 → 연결 정보 → DB 테이블 순서로 점검 |
| DB는 연결되지만 `database_schema=false` | 전용 테이블 없음 | 기본 경로는 `init_database.py` 실행 대상 확인. 전체 경로는 최초 SQL 초기화 로그 확인 |
| 초기화와 Backend 결과가 다름 | 루트 `.env`와 `backend/.env`가 서로 다른 DB를 지정 | 사용자·DB 이름·포트와 호스트별 주소를 대조 |
| 화면은 열리지만 Backend 연결 실패 | 컨테이너에서 `127.0.0.1:8000` 사용 | `frontend/.env`를 `http://backend:8000`으로 설정 → 앱 컨테이너 재생성 |
| 환경 파일 수정이 반영되지 않음 | 기존 컨테이너 환경 유지 | 선택한 Compose 경로의 재생성 절차 사용 |
| 채팅만 503 | Provider 미설정·인증 오류·모델 없음 | Provider 설정 → 사용 가능한 모델 → 해당 서비스 로그 확인 |
| 전체 구성의 SQL 수정이 반영되지 않음 | 이미 초기화된 DB 볼륨 | 기존 데이터 보존 상태에서 스키마 변경 절차 검토. 볼륨 삭제로 우회하지 않음 |
| CI는 통과했는데 compose2 오류 | Runtime CI가 형제 프로젝트 검사 | `working-directory`와 실제 검사 대상 확인 |

**목적:** 앱 포트를 사용 중인 프로세스 번호만 확인합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
Get-NetTCPConnection -State Listen -LocalPort 8000,8501 -ErrorAction SilentlyContinue |
    Select-Object LocalAddress,LocalPort,OwningProcess
```

**예상 결과:** 사용 중인 포트와 PID. 없으면 출력이 없을 수 있습니다.  
**다음 행동:** PID에 해당하는 앱을 확인한 뒤 해당 앱의 종료 기능을 사용하세요. 다른 프로세스를 일괄 종료하지 않습니다.

**목적:** readiness 실패를 구성 요소별로 확인합니다.  
**작업 폴더·창:** 창 A·루트.

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health' | ConvertTo-Json -Depth 6
```

**예상 결과:** `checks.redis`, `checks.database`, `checks.database_schema`와 오류 정보.  
**다음 행동:** 실패 항목에 해당하는 설정·서비스 로그를 확인하세요. 오류 출력에 접속 정보가 포함될 수 있으므로 그대로 공유하지 않습니다.

## 8. 근거와 검증 범위

### 주요 근거 연결

| 안내 내용 | 실제 상대 파일·심벌 또는 설정 키 |
|---|---|
| 기본 실행 경로·공용 서비스 포트 | `README.md`: 기본 실행, `COMPOSE_EXPLAINED.md`: 설정 주소 비교 |
| 서비스 이름·포트·시작 의존 관계 | `compose.yml`: `services`, `ports`, `depends_on`, `healthcheck` |
| 전체 저장소·볼륨·Ollama 프로필 | `compose.full-stack.yml`: `services`, `environment`, `volumes`, `profiles` |
| 게시 이미지·필수 사용자명·설정 우선값 | `compose.release.yml`: `image`, `pull_policy`, `environment` |
| Python·컨테이너 진입점·의존성 설치 | `backend/Dockerfile`, `frontend/Dockerfile`: `FROM`, `RUN`, `CMD` |
| Python 의존성 범위 | `backend/requirements.txt`, `frontend/requirements.txt` |
| 초기화용 환경 파일 위치·선택 순서 | `init_database.py`: `ENV_PATH`, `host_database_url()`, `initialize_database()` |
| DB 스키마·두 테이블 | `database/init.sql`, `PostgresRepository.schema_ready()` |
| 환경변수 예제 | `backend/.env.example`, `frontend/.env.example`, `release.env.example` |
| 화면에서 Backend로 보내는 요청 | `frontend/app.py`: `BACKEND_URL`, `api()` |
| 메모·채팅·통계·세션 API | `backend/app.py`: `/api/notes`, `/api/chat`, `/api/chat/{session_id}`, `/api/stats`, `/api/sessions/{session_id}` |
| 상태 확인 URL과 readiness 조건 | `backend/app.py`: `live()`, `health()`, `ready()` |
| LLM 설정·모델 이름·실제 호출 | `backend/services.py`: `MultiLLMChatService.configured()`, `model()`, `reply()` |
| 외부 서비스 없는 계약 테스트 | `backend/test_app.py`: `FakeRedis`, `FakeDatabase`, `FakeLLM`, `dependency_overrides` |
| CI의 검사 경로 불일치 | `../../../.github/workflows/07-runtime-ci.yml`: `on.paths`, `defaults.run.working-directory` |
| 다른 프로젝트의 배포·Secrets | `../../../.github/workflows/07-weather-mcp-cicd.yml`, `../../../.github/workflows/07-weather-stateful-cicd.yml`: `needs`, `if`, `environment`, `secrets.*` |
| 기존 사용자 안내·장애 설명 | `guide.md`, `TROUBLESHOOTING.md` |

### 직접 확인한 사항

- 선택한 루트와 위 프로젝트 파일이 존재합니다.
- `backend/.env`·`frontend/.env`는 존재합니다. 내용은 읽지 않았습니다.
- 루트 `.env`, `release.env`, `.venv`는 확인 당시 없었습니다.
- 루트 `.env.example`·`ENVEXAMPLE`, Node 명세·scripts, 패키지 잠금 파일은 발견되지 않았습니다.
- 확인한 경로에서 별도 적용 `AGENTS.md` 파일은 발견되지 않아 요청에 제공된 지침을 적용했습니다.
- 상위 과정 README의 관련 항목과 실제 workflow 세 개를 읽었습니다.
- Git 루트 확인은 실패했으며 원격 저장소 연결 상태는 확인하지 못했습니다.

### 정적 분석으로 판단한 사항

- 기본 Compose는 기존 저장소가 있어야 작동합니다.
- 기본·전체 Compose의 프론트엔드 주소는 환경 파일에서 직접 맞춰야 합니다.
- 초기화 도우미와 앱은 서로 다른 위치의 `.env`를 읽습니다.
- readiness 성공만으로 실제 LLM 호출 성공을 판단할 수 없습니다.
- Runtime CI의 현재 작업 폴더는 선택한 compose2가 아닙니다.

### 수행하지 않은 검증

파일 생성·수정, 실제 `.env`·로그·인증 파일·사용자 데이터 읽기, 앱 import, 테스트, 패키지 설치, Docker 명령, 서버 시작·중지·재시작, DB 초기화, 모델 다운로드, 로컬 API 요청, Git push, workflow 실행, 이미지 게시·클라우드 배포를 수행하지 않았습니다.

### 남은 사용자 준비 사항

- Docker Desktop·Compose와 기본 경로용 Python 3.12
- 공용 PostgreSQL·Redis 접속 정보 또는 전체 Compose 경로 선택
- `frontend/.env`의 컨테이너용 백엔드 주소
- 기본 경로의 루트 `HOST_DATABASE_URL`과 DB 초기화 권한
- 채팅할 경우 실제 API 키·호출 가능한 모델 또는 Ollama 모델
- CI 학습 시 GitHub 저장소 연결과 compose2를 대상으로 하는 workflow 준비

**이 문서는 실행 준비 안내이며 서버 구동 성공·실제 모델 응답·CI 통과를 확인한 보고서가 아닙니다.**