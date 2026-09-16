# 01_simple-multi-llm-compose 실행 가이드

이 파일이 실행 순서의 기준입니다. 한 단계씩 실행하고 결과를 확인하세요. player 주석은 버튼에 연결되는 실행 종류이며 임의 셸 명령을 실행하지 않습니다.

## 1. 프로젝트 구조 확인
<!-- player: {"action": "read"} -->

README와 아래 구조를 읽고 실행 단위와 역할을 확인합니다.

- .env
- .env.example
- COMPOSE_EXPLAINED.md
- README.md
- TROUBLESHOOTING.md
- compose.full-stack.yml
- compose.release.yml
- compose.yml
- init_database.py
- backend/Dockerfile
- backend/app.py
- backend/requirements.txt
- backend/services.py
- backend/test_app.py
- database/init.sql
- frontend/Dockerfile
- frontend/app.py
- frontend/requirements.txt

## 2. 환경설정 준비
<!-- player: {"action": "environment"} -->

환경 예제의 누락된 값만 .env에 병합합니다. 기존 값은 보존합니다.

## 3. 프로젝트 실행
<!-- player: {"action": "start"} -->

분석한 실행 계획에 따라 의존성과 서버를 준비합니다. 오류가 있으면 이 단계에서 해결합니다.
Docker Compose · .

## 4. 실행 결과 확인
<!-- player: {"action": "verify"} -->

서버 응답을 확인한 후 브라우저에서 첫 기능을 실습하세요.


<!-- PLAYER_SETUP_GUIDE_BEGIN -->
# 실행 준비 가이드

## 프로젝트와 실행 순서

### 프로젝트 유형과 확인된 구조

이 폴더는 **독립 실행 앱**입니다. Streamlit 화면, FastAPI 서버, PostgreSQL·Redis 연동 코드가 함께 있습니다. 여러 예제를 따로 실행하는 구조가 아니라, 같은 여행 준비 앱을 세 가지 Compose 구성으로 실행합니다.

Multi-Agent 오케스트레이션과 별도 worker는 없습니다. OpenAI·Gemini는 외부 API이며, Ollama는 선택적으로 사용하는 모델 서버입니다.

```text
.
├─ frontend/
│  ├─ app.py                  # Streamlit 화면과 Backend API 요청
│  ├─ requirements.txt
│  └─ Dockerfile
├─ backend/
│  ├─ app.py                  # FastAPI 라우트와 요청 검증
│  ├─ services.py             # PostgreSQL·Redis·LLM 연결
│  ├─ test_app.py             # 가짜 의존성을 사용하는 API 계약 테스트
│  ├─ requirements.txt
│  └─ Dockerfile
├─ database/init.sql          # 전용 스키마·테이블 생성
├─ init_database.py           # 기존 공용 PostgreSQL 초기화 도구
├─ .env.example
├─ compose.yml                # 기존 공용 저장소 + 앱 컨테이너
├─ compose.full-stack.yml     # 저장소 + 앱 + 선택 Ollama
├─ compose.release.yml        # 배포된 앱 이미지 사용
├─ README.md
├─ COMPOSE_EXPLAINED.md
├─ TROUBLESHOOTING.md
└─ guide.md
```

선택한 루트와 위 파일의 존재를 확인했습니다. 실제 `.env`도 존재하지만 **내용과 입력 완료 여부는 확인하지 않았습니다.**

### 권장 진행 순서

이 가이드는 **`compose.full-stack.yml`로 저장소와 앱을 함께 실행하는 경로**를 먼저 설명합니다. README의 기본 경로는 공용 PostgreSQL·Redis가 이미 있다는 전제인데, 현재 공용 서비스의 실행 여부는 미확인입니다.

1. PowerShell에서 작업 폴더와 Docker 준비 상태를 확인합니다.
2. 기존 `.env`를 보존하면서 실행 방식에 맞는 설정을 확인합니다.
3. 앱 이미지를 빌드합니다.
4. PostgreSQL·Redis → Backend → Frontend 순서로 실행합니다.
5. API 키 없이 서비스 상태와 여행 메모를 실습합니다.
6. Ollama 모델 또는 외부 API 키를 준비한 뒤 채팅을 실습합니다.
7. 사용한 Compose 구성으로 종료합니다.
8. 공용 서비스 재사용, 이미지 전달, CI 학습으로 진행합니다.

Project Player의 서버 실행 기능을 사용할 때도 **실제로 사용하는 Compose 파일을 먼저 확인**하세요. 제공된 실행기 분석에는 `compose.yml`만 근거로 표시되어 있으므로 Full Stack 실행을 의미하지 않습니다. Player에서 이미 실행했다면 같은 앱을 PowerShell로 중복 실행하지 말고 확인 단계부터 진행하세요.

### 구성별 접속 주소

| 실행 방식 | 브라우저 화면 | Backend·API 문서 | 저장소 |
| --- | --- | --- | --- |
| 권장 Full Stack | `http://127.0.0.1:8501` | `http://127.0.0.1:8000/docs` | Compose가 생성 |
| 기본 `compose.yml` | **`http://127.0.0.1`** | `http://127.0.0.1:8000/docs` | 기존 공용 서비스 |
| `compose.release.yml` | `http://127.0.0.1:8501` | `http://127.0.0.1:8000/docs` | 기존 공용 서비스 |

**문서와 설정의 차이:** README는 기본 실행의 화면 주소를 8501번으로 설명하지만, 실제 `compose.yml`의 `frontend.ports`는 **`80:8501`**입니다. 기본 구성으로 실행할 때는 80번 주소를 사용합니다.

## PowerShell

### 처음 필요한 도구와 버전

| 도구 | 필요 여부와 근거 | 확인 상태 |
| --- | --- | --- |
| Docker Desktop·Docker Compose | 권장 경로에 필요. Linux 기반 이미지와 `docker compose` 사용 | 설치·엔진 상태·버전 미확인 |
| Python 3.12 | 컨테이너는 두 Dockerfile의 `python:3.12-slim` 사용. Windows Python은 공용 DB 초기화 경로에서만 필요 | 호스트 설치 미확인 |
| pip·venv | 호스트에서 `init_database.py`를 실행할 때 필요 | 루트 `.venv`는 확인 당시 없음 |
| Git | 이미 받은 폴더의 로컬 실행에는 필수 아님. 향후 GitHub 연결에 필요 | 명령 호출 가능, 버전 미확인 |
| Node.js·npm | 해당 없음. `package.json`, npm scripts, Node 의존성이 없음 | 설치할 필요 없음 |

Docker Desktop이 없다면 [공식 Windows 설치 안내](https://docs.docker.com/desktop/setup/install/windows-install/)에 따라 준비하세요. 이 프로젝트는 Linux 컨테이너를 사용합니다. WSL 2 방식을 선택한다면 해당 안내의 Windows·WSL 요구사항을 확인하세요. 설치 후에는 시작 메뉴에서 Docker Desktop을 열고 엔진 시작이 끝날 때까지 기다립니다.

### A창: 작업 폴더와 Docker 준비 확인

**목적:** 모든 상대 경로가 선택한 프로젝트를 기준으로 해석되도록 하고, Docker CLI와 엔진 준비 상태를 구분합니다.

**작업 폴더·창:** 일반 PowerShell 창 하나를 열고 이를 **A창: 실행·확인용**으로 사용합니다.

```powershell
Set-Location -LiteralPath 'C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose'

Test-Path -LiteralPath '.\compose.full-stack.yml'
docker --version
docker compose version
docker version
```

**예상 결과:**

- 파일 확인은 `True`입니다.
- 처음 두 Docker 명령은 CLI·Compose 버전을 보여 줍니다.
- 마지막 명령은 `Client`와 `Server` 정보를 모두 보여 줍니다. CLI 버전만 확인되는 것은 엔진 준비 완료의 증거가 아닙니다.

**실패 시:** 파일이 없으면 작업 폴더를 확인합니다. `docker`를 찾지 못하면 Docker Desktop 설치 후 PowerShell을 다시 엽니다. Server 연결 오류라면 Docker Desktop의 시작 상태와 Linux 컨테이너 모드를 확인합니다.

WSL 2 방식을 사용하는데 엔진이 시작되지 않을 때만 다음을 확인하세요.

```powershell
wsl --version
```

결과가 없거나 지원되지 않는다는 오류가 나면 공식 설치 안내의 WSL 준비 절차를 확인합니다. 이 문서는 관리자 권한이나 전역 실행 정책 변경을 기본 조건으로 요구하지 않습니다.

### 의존성 설치 방식

권장 Full Stack 경로에서는 Docker 빌드가 Python과 의존성을 설치합니다. Windows에 앱용 가상환경을 만들 필요가 없습니다.

실제 명세는 다음과 같습니다.

| 위치 | 의존성 범위 |
| --- | --- |
| `backend/requirements.txt` | `fastapi>=0.115,<1`, `uvicorn>=0.34,<1`, `redis>=5,<9`, `psycopg[binary]>=3.2,<4`, `google-genai>=2,<3`, `openai>=1.68,<3`, `httpx>=0.27,<1` |
| `frontend/requirements.txt` | `streamlit>=1.41,<2`, `httpx>=0.27,<1` |

잠금 파일은 발견하지 못했습니다. 따라서 위 범위 안에서 실제 설치되는 세부 버전은 빌드 시점에 따라 달라질 수 있습니다.

### 선택: 공용 DB 초기화에 필요한 가상환경

이 단계는 뒤의 **Docker → 대체 경로: 기존 공용 서비스 재사용**에서 `init_database.py`를 실행할 때만 필요합니다. Full Stack의 새 DB에는 필요하지 않습니다.

**목적:** DB 초기화 도구의 의존성을 Windows 전역 Python과 분리합니다.

**작업 폴더·창:** 프로젝트 루트, A창.

```powershell
py -3.12 --version

if (-not (Test-Path -LiteralPath '.\.venv')) {
    py -3.12 -m venv '.\.venv'
}

if (-not (Test-Path -LiteralPath '.\.venv\Scripts\python.exe' -PathType Leaf)) {
    throw '가상환경 Python이 없습니다. Python 설치와 .venv 생성 결과를 확인하세요.'
}

& '.\.venv\Scripts\python.exe' --version
```

**예상 결과:** 마지막 출력이 Python 3.12 계열입니다. 기존 `.venv`는 이 프로젝트용이며 같은 Python 버전으로 정상 실행되는 경우에 재사용합니다.

**실패 시:** `py -3.12`를 찾지 못하면 Python 3.12를 준비합니다. 기존 `.venv`가 손상되었거나 다른 프로젝트용이라면 그대로 설치를 진행하지 말고 해당 환경의 출처를 확인하세요.

버전을 확인한 뒤 같은 A창에서 초기화 도구의 의존성을 설치합니다.

```powershell
& '.\.venv\Scripts\python.exe' -m pip install 'psycopg[binary]>=3.2,<4' 'python-dotenv>=1.0,<2'
```

**예상 결과:** 두 패키지의 설치 또는 이미 설치되어 있다는 메시지가 나옵니다.

**실패 시:** 설치 오류의 패키지명, 네트워크·프록시 상태, 가상환경 Python 경로를 확인합니다. `python-dotenv`는 `init_database.py`가 사용하지만 앱의 `backend/requirements.txt`에는 포함되어 있지 않습니다.

가상환경 활성화는 필요하지 않습니다. 이후에도 가상환경 Python을 직접 호출합니다. 앱 서버의 로컬 시작·확인·종료는 다음 Docker 절의 명령을 사용합니다.

## 환경변수

### 기존 `.env`를 보존하며 예제 준비

실제 예제 파일은 루트의 **`.env.example`**이며 복사 목적지는 같은 폴더의 **`.env`**입니다. `ENVEXAMPLE`이라는 별도 파일은 없습니다.

**목적:** 예제를 출발점으로 설정하되 기존 설정을 덮어쓰지 않습니다.

**작업 폴더·창:** 프로젝트 루트, A창.

```powershell
if (-not (Test-Path -LiteralPath '.\.env')) {
    Copy-Item -LiteralPath '.\.env.example' -Destination '.\.env'
} else {
    Write-Output '기존 .env를 유지합니다. 필요한 항목만 편집기에서 확인하세요.'
}

notepad '.\.env'
```

**예상 결과:** `.env`가 없을 때만 복사되고, 편집기에서 설정을 확인할 수 있습니다.

**실패 시:** `.env.example`의 존재와 작업 폴더를 확인합니다. 기존 `.env`는 예제 파일로 교체하지 마세요. 이 명령은 누락된 항목을 자동 병합하지 않습니다.

첫 Full Stack 실습에서는 PostgreSQL 계정 정보를 확인하고 **`OLLAMA_ENABLED=false`**로 시작하세요. 예제 파일에는 `true`가 적혀 있지만 Ollama 프로필 실행과 모델 다운로드는 별도 단계입니다. API 키가 없어도 메모 실습은 가능합니다.

### 변수별 의미와 입력값

아래 `<사용자가 입력할 값>`은 실제 값으로 바꿔야 하는 설명용 자리표시자입니다.

| 변수명 | 근거 파일·설정 키 | 의미·사용 주체 | 기본값 또는 예시 | 필수·선택 | 사용자가 준비할 값 |
| --- | --- | --- | --- | --- | --- |
| `POSTGRES_USER` | `.env.example`, Full Stack의 `database.environment` | 새 PostgreSQL 계정과 Backend 접속 사용자 | 개발 예시 `agent_user` | Full Stack에서 유효한 값 필요 | 기존 볼륨이면 최초 생성 시 사용자 |
| `POSTGRES_PASSWORD` | 같은 위치, `backend.environment.DATABASE_URL` | 새 DB 비밀번호와 Backend 접속 인증 | `<사용자가 입력할 값>` | Full Stack에서 필요 | 새 DB용 개발 비밀번호 또는 기존 DB와 일치하는 값 |
| `POSTGRES_DB` | `.env.example`, Full Stack의 `database.environment` | 사용할 데이터베이스 이름 | 개발 예시 `agent_db` | Full Stack에서 필요 | 기존 볼륨이면 실제 DB 이름 |
| `DATABASE_URL` | 기본·Release Compose, `PostgresRepository.__init__` | Backend의 PostgreSQL 접속 문자열 | 기본 구성의 호스트 부분은 `host.docker.internal:5433` | 기본·Release에서 실제 DB와 일치해야 함 | DB 사용자·비밀번호·DB 이름을 포함한 URL |
| `HOST_DATABASE_URL` | `.env.example`, `init_database.py:host_database_url()` | Windows에서 초기화 도구가 접속할 DB 주소 | 호스트 부분 `127.0.0.1:5433` | 초기화 시 선택, 지정하면 우선 사용 | 공용 DB의 Host용 접속 URL |
| `REDIS_URL` | 기본·Release Compose, `RedisSessionStore.__init__` | Backend의 Redis 접속 주소 | `redis://host.docker.internal:6379/0` | 저장소 기능에 필요 | 공용 Redis가 다르면 실제 주소·인증 |
| `OPENAI_API_KEY` | Compose의 Backend 환경, `configured()`·`reply()` | OpenAI API 인증 | 비워 둠 | OpenAI 선택 시 필수 | 사용자가 별도로 발급한 API 키 |
| `OPENAI_MODEL` | `.env.example`, `MultiLLMChatService.model()` | OpenAI 요청 모델 | 소스 기본값 `gpt-4.1-mini` | OpenAI 사용 시 | 계정에서 사용 가능한 모델 이름 |
| `GEMINI_API_KEY` | Compose의 Backend 환경, `configured()`·`reply()` | Gemini API 인증 | 비워 둠 | Gemini 선택 시 필수 | 사용자가 별도로 발급한 API 키 |
| `GEMINI_MODEL` | `.env.example`, `MultiLLMChatService.model()` | Gemini 요청 모델 | 소스 기본값 `gemini-3.5-flash` | Gemini 사용 시 | 계정에서 사용 가능한 모델 이름 |
| `OLLAMA_ENABLED` | `.env.example`, `configured()` | Ollama 선택을 허용할지 결정 | 첫 실습은 `false`, 모델 준비 후 `true` | Ollama 채팅 시 필수 | 실행 단계에 맞는 값 |
| `OLLAMA_BASE_URL` | Compose, `MultiLLMChatService.reply()` | Backend가 요청할 Ollama 주소 | 기본 구성은 `http://host.docker.internal:11434` | Ollama 사용 시 | 공용 Ollama의 실제 주소 |
| `OLLAMA_MODEL` | `.env.example`, `model()` | 화면에서 `llama` 선택 시 사용할 모델 | `llama3.2` | 해당 모델 선택 시 | 실제 다운로드한 모델 태그 |
| `GEMMA_MODEL` | `.env.example`, `model()` | 화면에서 `gemma` 선택 시 사용할 모델 | `gemma3:4b` | 해당 모델 선택 시 | 실제 다운로드한 모델 태그 |
| `BACKEND_URL` | `frontend/app.py`, 각 Compose의 `frontend.environment` | Streamlit 서버가 요청할 Backend 주소 | Compose: `http://backend:8000`; Host 코드 기본값: `http://127.0.0.1:8000` | 연결에 필요하나 Compose가 설정 | 일반 Compose 실습에서는 입력 불필요 |
| `BACKEND_IMAGE` | `.env.example`, Release의 `backend.image` | 내려받을 Backend 이미지 | `<사용자가 입력할 값>` | Release에서만 필수 | 실제 레지스트리·저장소·태그 |
| `FRONTEND_IMAGE` | `.env.example`, Release의 `frontend.image` | 내려받을 Frontend 이미지 | `<사용자가 입력할 값>` | Release에서만 필수 | 실제 레지스트리·저장소·태그 |

Full Stack에서는 다음 주소를 Compose가 직접 지정합니다. `.env`의 공용 서비스 주소로 바뀌지 않습니다.

- Redis: `redis://redis:6379/0`
- PostgreSQL: `database:5432`와 `POSTGRES_*` 값으로 구성
- Ollama: `http://ollama:11434`

`POSTGRES_*`를 바꾸는 것만으로 기존 PostgreSQL 볼륨의 계정과 비밀번호가 변경되지는 않습니다. 기존 볼륨은 최초 생성 당시의 설정과 맞아야 합니다. 비밀번호를 URL에 넣을 때 예약 문자가 있으면 URL 인코딩도 필요합니다.

### 설정이 전달되는 위치

- **루트 `.env`:** Compose의 `${변수명}` 치환에 사용됩니다. 현재 PowerShell에 같은 이름의 환경변수가 있으면 그 값이 우선할 수 있습니다. [Docker 환경변수 치환 문서](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)
- **PowerShell의 `$env:`:** 해당 프로세스와 자식 프로세스에 전달되는 값입니다. `.env` 파일의 내용을 바꾸는 기능이 아닙니다.
- **Compose의 `environment`:** 컨테이너에 실제로 전달할 변수를 명시합니다. 이 프로젝트의 세 Compose 파일에는 `env_file:` 설정이 없습니다.
- **Python의 `.env` 로딩:** `init_database.py`는 루트 `.env`를 읽습니다. Backend·Frontend 앱 코드 자체에는 `.env` 자동 로딩이 없습니다.
- **GitHub Secrets·Variables:** GitHub Actions 실행 환경의 설정입니다. 로컬 `.env`나 컨테이너에 자동 복사되지 않습니다.

Frontend는 Python 서버에서 Backend를 호출합니다. LLM API 키는 Backend에만 전달하며, Frontend 환경변수나 화면에 넣지 않습니다. 특히 `BACKEND_URL`은 사이드바에도 표시되므로 인증값을 포함하면 안 됩니다.

Codex가 사용하는 ChatGPT 로그인·구독 인증 정보는 프로젝트 API 키가 아닙니다. OpenAI·Gemini를 선택하면 사용자가 별도의 API 키를 준비해야 합니다. 키 없는 채팅 경로는 이 프로젝트가 지원하는 Ollama입니다.

## Docker

### 실제 Compose 구성

| 파일·프로젝트 이름 | 서비스 | Windows 공개 포트 | 볼륨·의존성 |
| --- | --- | --- | --- |
| `compose.full-stack.yml` / `simple-multi-llm-full-stack` | `redis`, `database`, `backend`, `frontend`, 선택 `ollama` | Backend `8000:8000`, Frontend `8501:8501` | `redis_data`, `postgres_data`, `ollama_data`; Redis·DB 정상 후 Backend, Backend 정상 후 Frontend |
| `compose.yml` / `simple-multi-llm-app` | `backend`, `frontend` | Backend `8000:8000`, Frontend **`80:8501`** | 앱용 영속 볼륨 없음. 외부 공용 저장소 필요 |
| `compose.release.yml` / `release-simple-multi-llm` | `backend`, `frontend` | Backend `8000:8000`, Frontend `8501:8501` | 빌드 대신 지정한 이미지 사용. 외부 공용 저장소 필요 |

Full Stack의 Redis·PostgreSQL·Ollama에는 Windows로 공개하는 `ports` 설정이 없습니다. 컨테이너 내부 네트워크로 연결합니다.

이미지 명세는 Redis `7-alpine`, PostgreSQL `17-alpine`, Ollama `latest`입니다. Ollama에만 `ollama` 프로필이 있으며 GPU 할당 설정은 없습니다.

주소를 읽을 때는 호출 위치를 구분하세요.

| 호출 위치 | 올바른 주소의 예 |
| --- | --- |
| Windows 브라우저 → Backend | `http://127.0.0.1:8000` |
| Frontend 컨테이너 → Backend 컨테이너 | `http://backend:8000` |
| 기본 Backend 컨테이너 → Windows의 공용 DB | `host.docker.internal:5433` |
| Full Stack Backend → 같은 구성의 DB | `database:5432` |

컨테이너 안의 `localhost`는 그 컨테이너 자신입니다. Windows의 `localhost`와 다릅니다.

### D1. 권장 경로: 설정 검사와 이미지 빌드

**목적:** 저장소를 실행하기 전에 Compose 문법과 앱 이미지 빌드를 확인합니다.

**작업 폴더·창:** 프로젝트 루트, A창. 환경변수 절의 준비를 먼저 마칩니다.

```powershell
docker compose -f '.\compose.full-stack.yml' config --quiet
```

**예상 결과:** 오류 없이 종료하며 정상일 때 상세 설정은 출력하지 않습니다.

**실패 시:** YAML 오류와 `.env`의 변수 형식을 확인합니다. 값을 노출하는 전체 `config` 출력 대신 `--quiet`를 사용하세요.

검사가 성공한 뒤 빌드합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' build backend frontend
```

**예상 결과:** 두 Dockerfile의 `requirements.txt` 설치와 소스 복사가 완료됩니다.

**실패 시:** 실패한 서비스의 Dockerfile과 requirements 파일, 이미지·패키지 다운로드 연결을 확인합니다. 빌드가 성공하기 전에는 다음 단계로 넘어가지 않습니다.

### D2. PostgreSQL·Redis 시작

**목적:** 앱의 저장소를 먼저 준비합니다.

**작업 폴더·창:** 프로젝트 루트, A창.

```powershell
docker compose -f '.\compose.full-stack.yml' up -d redis database
docker compose -f '.\compose.full-stack.yml' ps
```

**예상 결과:** `redis`, `database`가 실행되고 잠시 후 `healthy`가 됩니다. 새 PostgreSQL 데이터 볼륨이면 `database/init.sql`이 자동 실행됩니다.

두 서비스가 준비된 뒤 Redis 응답을 확인합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' exec redis redis-cli ping
```

**예상 결과:** `PONG`입니다.

**실패 시:** 다음 로그를 확인합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' logs --tail 60 redis database
```

DB 인증 오류는 `.env`의 `POSTGRES_*`와 기존 볼륨 생성 당시의 값이 일치하는지 확인합니다. 기존 데이터 볼륨에서는 초기화 SQL이 자동 재실행되지 않습니다.

### D3. Backend·Frontend 시작

**목적:** 준비된 저장소에 Backend를 연결하고 화면을 시작합니다.

**작업 폴더·창:** 프로젝트 루트, A창.

```powershell
docker compose -f '.\compose.full-stack.yml' up -d backend frontend
docker compose -f '.\compose.full-stack.yml' ps
```

Compose가 `depends_on.condition: service_healthy`에 따라 순서를 처리합니다.

- Backend: `uvicorn app:app --host 0.0.0.0 --port 8000`
- Frontend: `streamlit run app.py --server.address=0.0.0.0 --server.port=8501`

위 명령은 각 Dockerfile의 컨테이너 진입점 설명입니다. 별도 Windows 서버 창에서 다시 실행하지 않습니다.

**예상 결과:** Backend는 `healthy`, Frontend는 실행 상태입니다. Frontend 자체의 healthcheck는 정의되어 있지 않습니다.

**실패 시:** Backend의 `/health/ready`가 실패하면 Frontend 시작도 막힐 수 있습니다. Backend 로그와 다음 D4의 `/health`를 먼저 확인합니다.

### D4. 응답과 화면 확인

**목적:** 프로세스 생존, 저장소 준비, 화면 응답을 각각 확인합니다.

**작업 폴더·창:** 프로젝트 루트, A창.

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/live'

Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health' |
    ConvertTo-Json -Depth 6

Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready' |
    ConvertTo-Json -Depth 6

Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8501' |
    Select-Object StatusCode
```

**예상 결과:**

- `/health/live`: `status: ok`, `service: backend`
- `/health`: `status: ok`, `checks.redis`, `checks.database`, `checks.database_schema`가 모두 `true`
- `/health/ready`: 저장소 준비가 완료되면 HTTP 200, 실패하면 HTTP 503
- 화면 요청: HTTP 200

API 키가 없고 Ollama를 비활성화했으면 `checks.providers`의 값이 모두 `false`여도 저장소가 정상이면 readiness는 성공합니다. Provider의 `true`는 설정 여부이며 실제 인증·모델 응답 성공을 검사한 결과가 아닙니다.

브라우저에서 `http://127.0.0.1:8501`을 열고 **예제 학습 → E1**로 진행합니다.

**실패 시:** `검증과 문제 해결` 절에서 포트, DB 스키마, Frontend API 주소 순서로 확인합니다.

### D5. 로그 관찰과 종료

**목적:** 실행 중 오류를 관찰하고, 실습 후 이 Compose 프로젝트를 종료합니다.

로그를 계속 보려면 **B창: 로그용**을 별도로 열어 다음을 실행합니다.

```powershell
Set-Location -LiteralPath 'C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose'

docker compose -f '.\compose.full-stack.yml' logs --follow --tail 60 backend frontend
```

**예상 결과:** 새 로그가 계속 표시됩니다. B창의 **Ctrl+C는 로그 관찰만 종료**하며 앱 컨테이너는 계속 실행됩니다.

전체 실습이 끝나면 프로젝트 루트의 A창에서 종료합니다. 뒤에서 Ollama 프로필을 사용한 경우까지 포함하는 명령입니다.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama down
docker compose -f '.\compose.full-stack.yml' --profile ollama ps -a
```

**예상 결과:** 해당 프로젝트의 컨테이너가 제거되고 목록이 비어 있습니다. DB·Redis 데이터와 다운로드한 모델의 named volume은 유지됩니다.

**실패 시:** 종료할 때도 시작한 Compose 파일과 프로젝트 이름이 같은지 확인합니다. 기본 종료에는 볼륨 삭제 옵션을 붙이지 않습니다.

### 대체 경로: 기존 공용 서비스 재사용

이 경로는 README의 기본 수업 구성입니다. Full Stack 실행을 끝낸 뒤 선택하세요.

**선행 조건:**

- Windows의 `127.0.0.1:5433`에서 PostgreSQL에 접근할 수 있어야 합니다.
- `127.0.0.1:6379`에서 Redis에 접근할 수 있어야 합니다.
- PostgreSQL의 계정과 DB는 미리 존재해야 합니다.
- `.env`의 `DATABASE_URL`, `HOST_DATABASE_URL`, `REDIS_URL`이 해당 서비스와 맞아야 합니다.
- 공용 Ollama는 Ollama 채팅을 할 때만 필요합니다.

**목적·창:** 프로젝트 루트의 A창에서 공용 서비스 접근 가능 여부를 확인합니다.

```powershell
Test-NetConnection -ComputerName '127.0.0.1' -Port 5433
Test-NetConnection -ComputerName '127.0.0.1' -Port 6379
```

**예상 결과:** 둘 다 `TcpTestSucceeded: True`입니다. 이 결과는 포트 접근만 확인하며 DB 인증 성공까지 의미하지는 않습니다.

**실패 시:** 이 폴더에는 공용 서비스의 별도 시작 구성이 없습니다. 수업 환경의 서비스 준비 절차를 확인하거나 Full Stack 경로를 사용합니다.

PowerShell 절의 초기화용 `.venv` 준비를 마친 뒤, 같은 A창에서 전용 스키마를 준비합니다.

```powershell
& '.\.venv\Scripts\python.exe' '.\init_database.py'
```

**예상 결과:** 초기화 완료 메시지와 다음 테이블명이 출력됩니다.

```text
simple_multi_llm.chat_messages
simple_multi_llm.notes
```

이 스크립트는 DB나 로그인 계정을 생성하지 않습니다. 지정한 DB에 `CREATE ... IF NOT EXISTS` SQL을 적용하며, 이미 존재하는 테이블 구조를 변경하는 migration도 아닙니다.

**실패 시:** `HOST_DATABASE_URL`의 주소·인증과 스키마 생성 권한을 확인합니다. 이 값이 없으면 스크립트는 `DATABASE_URL`의 `host.docker.internal`을 `127.0.0.1`로 바꿔 사용합니다.

이후 앱을 실행합니다.

```powershell
docker compose -f '.\compose.yml' config --quiet
```

검사가 성공한 뒤 다음을 실행합니다.

```powershell
docker compose -f '.\compose.yml' up --build -d
docker compose -f '.\compose.yml' ps
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready'
```

**예상 결과:** Backend가 준비된 후 Frontend가 실행됩니다. 브라우저 주소는 **`http://127.0.0.1`**입니다. E1의 화면 실습은 동일합니다.

**실패 시:** `docker compose -f '.\compose.yml' logs --tail 60 backend frontend`로 앱 로그를 확인합니다. 컨테이너의 DB·Redis 주소가 `host.docker.internal`을 사용하는지도 확인하세요.

종료는 같은 A창에서 다음과 같이 합니다.

```powershell
docker compose -f '.\compose.yml' down
docker compose -f '.\compose.yml' ps -a
```

**예상 결과:** 이 구성의 앱 컨테이너만 종료됩니다. 기존 공용 PostgreSQL·Redis·Ollama는 이 Compose의 관리 대상이 아닙니다.

## GitHub Actions

### 현재 확인된 workflow와 저장소 관계

**해당 없음:** 선택 폴더에는 `.github/workflows`와 workflow YAML이 없습니다. Git의 저장소 루트 확인도 “Git 저장소가 아님”으로 끝났습니다.

따라서 다음 항목은 현재 설정으로 확인할 수 없습니다.

| 항목 | 확인 결과 |
| --- | --- |
| 정확한 workflow 경로 | 발견하지 못함 |
| `on`, 브랜치·`paths` 조건 | 정의된 workflow 없음 |
| 수동 실행 `workflow_dispatch` | 확인된 정의 없음 |
| job 이름·순서·`needs` | 확인된 정의 없음 |
| runner·`working-directory` | 확인된 정의 없음 |
| 자동 검사·이미지 빌드·배포 | 이 폴더에서 확인된 자동화 없음 |
| 연결된 원격 저장소 | 미확인. 원격 URL·인증 설정은 읽지 않음 |

상위의 실제 Git 저장소 루트를 확인하지 못했으므로 상위 README나 workflow를 이 프로젝트의 CI 근거로 사용하지 않았습니다. 원본 저장소에 별도 CI가 있는지는 사용자가 원본 checkout에서 확인해야 합니다.

### 향후 연결 대상과 사용자 준비 사항

아래는 **제안**이며 현재 구성되어 있다는 뜻이 아닙니다.

| 연결할 대상 | 필요한 권한 | Secret·Variable 이름 | 설정 위치 | 사용 job | 사용자가 준비할 값 |
| --- | --- | --- | --- | --- | --- |
| 사용자의 GitHub 저장소 | 소스 등록·workflow 추가 권한 | 현재 정의 없음 | 저장소와 `.github/workflows` | 현재 없음 | 사용할 저장소, 실제 프로젝트 상대 경로 |
| GitHub Actions 실행 | 조직·저장소의 Actions 허용 및 실행 권한 | 현재 정의 없음 | 저장소 Settings의 Actions 설정 | 향후 검사·빌드 job | 허용할 Actions 정책 |
| 선택한 이미지 레지스트리 | 게시 대상에 대한 이미지 쓰기 권한 | 인증용 이름은 향후 workflow에서 정해야 함 | Actions Secrets·Variables | 향후 이미지 게시 job | 레지스트리 계정, 저장소, 인증 방식 |
| 외부 LLM API | 해당 API 사용 권한 | 현재 workflow 참조 없음 | 실제 통합 테스트를 추가할 때만 검토 | 현재 없음 | API 키·사용 가능 모델 |
| 수신자 PC | Docker 실행과 공용 저장소 접근 | `.env`의 `BACKEND_IMAGE`, `FRONTEND_IMAGE` 등 | 수신자 프로젝트 폴더 | Actions job과 무관 | 전달받은 이미지 주소와 DB 접속 정보 |

`BACKEND_IMAGE`와 `FRONTEND_IMAGE`는 현재 로컬 Compose 변수입니다. 자동으로 GitHub Variables가 되는 것은 아닙니다.

### 권장 CI 학습 순서

로컬 서버 실행에 GitHub나 Actions는 필수가 아닙니다. 먼저 E1·E2를 완료한 뒤 다음 순서로 학습하세요.

1. 원본 Git 저장소 또는 사용자가 관리할 저장소를 정합니다. 업로드 전에 실제 `.env`가 포함되지 않도록 사용자가 제외 설정을 확인합니다.
2. `backend/test_app.py`를 읽습니다. Redis·DB·LLM을 Fake 객체로 바꾸므로 실제 API 키 없이 API 계약을 검사하는 구조입니다.
3. 향후 검사 workflow에서는 Python 3.12, Backend 의존성, 테스트 도구를 준비하도록 설계합니다. 현재 requirements에는 `pytest`가 없으므로 테스트 의존성 관리가 추가로 필요합니다.
4. 테스트 파일의 `from app import ...`가 해석되도록 테스트 작업 경로를 실제 프로젝트의 `backend`로 맞춥니다. 저장소 루트 기준 전체 상대 경로는 원본 checkout에서 확인해야 합니다.
5. 검사 성공 후 Backend·Frontend Docker 빌드를 연결합니다. 이후 게시 job을 추가한다면 앞선 job 성공을 `needs`로 연결할 수 있습니다.
6. 이미지 게시와 실제 배포는 계정·대상·인증이 준비된 다음 별도 단계로 구성합니다.

저장소 연결, Secrets·Variables 생성, 권한 승인, push, 수동 workflow 실행과 배포는 모두 사용자가 이후 수행할 작업입니다. 이번 문서 작성 중에는 수행하지 않았습니다.

### Actions 실패를 읽는 순서

향후 workflow를 만든 뒤에는 **Actions → 해당 run → 실패한 job → 실패 step → 로그** 순서로 확인합니다.

- 인증 실패: 선택한 레지스트리와 계정 권한, YAML에서 참조하는 Secret 이름을 대조합니다.
- 버전 실패: Python 설정과 실제 requirements 범위를 대조합니다.
- 경로 실패: checkout 이후의 `working-directory`, requirements 경로, Docker build context를 확인합니다.
- 테스트 실패: `backend/test_app.py`의 실패 assertion과 Fake 의존성을 확인합니다.
- Docker 실패: `backend`·`frontend` 중 어느 빌드에서 어떤 `COPY` 또는 패키지 설치가 실패했는지 확인합니다.

현재는 workflow가 없으므로 특정 job이나 자동 배포가 성공한다고 판단할 근거가 없습니다.

## 예제 학습

### 같은 앱에서 학습 범위 확장하기

별도 앱 폴더로 바꾸지 않고 다음 순서로 진행합니다. README의 실행 구성 비교 → 실제 LLM 설정 → 상태·저장소 확인 → 이미지 전달 내용을 실습 단계로 나눈 것입니다.

| 순서 | 예제 경로 | 배울 내용 | 선행 조건 | 실행·확인 절차 |
| --- | --- | --- | --- | --- |
| 1 | `frontend/app.py`, `backend/app.py`, `database/init.sql` | 화면·API·영속 저장 | Docker D1~D4 | 아래 E1 |
| 2 | `compose.full-stack.yml`, `backend/services.py` | API 키 없는 Ollama 채팅 | 정상 Full Stack, 모델 다운로드 공간·자원 | 아래 E2 |
| 3 | `.env.example`, `backend/services.py` | 외부 Provider 선택 | 사용자의 API 키·모델 권한 | 아래 E3 |
| 4 | `compose.release.yml`, 두 Dockerfile | 이미지 빌드·전달·수신 | 레지스트리 계정, 수신자의 공용 서비스 | 아래 E4 |
| 5 | `COMPOSE_EXPLAINED.md`, `TROUBLESHOOTING.md` | 연결 구조와 장애별 영향 | 정상 동작 이해 | 검증과 문제 해결 절 |

### E1. API 키 없이 메모 저장하기

**목적:** Frontend → Backend → PostgreSQL·Redis 연결을 확인합니다.

**작업 폴더·창:** 브라우저는 Full Stack의 `http://127.0.0.1:8501`, 확인 명령은 프로젝트 루트의 A창입니다.

1. 화면에 **“Multi-LLM 여행 준비 Chat2 0914”** 제목이 표시되는지 확인합니다.
2. **서비스 상태 → Health 확인**을 누릅니다.
3. `status: ok`와 Redis·DB·DB 스키마의 `true`를 확인합니다.
4. **여행 메모** 탭에서 이름은 `연습 사용자`, 메모는 `부산 2박 3일, 대중교통 이용`으로 입력합니다.
5. **메모 저장**을 누릅니다.
6. 반환 JSON에 `note`가 있고 `warning`이 `null`인지 확인합니다.
7. **메모 조회**를 눌러 방금 저장한 행을 확인합니다.

A창에서 API 결과도 확인합니다.

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/notes' |
    ConvertTo-Json -Depth 6

Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/stats' |
    ConvertTo-Json -Depth 4
```

**예상 결과:** 메모 목록에 입력한 내용이 있고, 통계의 `request_count`가 증가하며 `recent_request`에 메모 내용이 들어갑니다. 기존 데이터가 있으면 시작 횟수는 0이 아닐 수 있습니다.

**실패 시:** 메모 저장·조회 오류는 PostgreSQL부터 확인합니다. 메모는 저장됐지만 `warning`이 있으면 Redis 통계 기록이 실패한 것입니다.

API 키가 없는 상태에서 기본 선택인 `openai`로 채팅하면 503 설정 오류가 예상됩니다. 앱에는 실행용 Mock 성공 대체 경로가 없습니다.

### E2. Ollama로 채팅하고 대화 저장 확인하기

이 절은 **Full Stack 경로**를 기준으로 합니다.

**목적:** 외부 API 키 없이 실제 로컬 모델을 호출합니다.

**작업 폴더·창:** 프로젝트 루트, A창. `.env`에서 `OLLAMA_ENABLED=true`로 설정하고 `GEMMA_MODEL=gemma3:4b`를 확인합니다. 모델 태그를 바꿨다면 아래 다운로드 대상도 같은 값으로 바꿔야 합니다.

먼저 Ollama만 시작합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama up -d ollama
```

**예상 결과:** `ollama` 서비스가 실행됩니다.

**실패 시:** Docker 엔진과 이미지 다운로드 오류를 확인합니다. Full Stack의 Ollama는 Windows에 11434번 포트를 공개하지 않으므로 이 경로에서 Host의 `localhost:11434`로 검사하지 않습니다.

Gemma 모델을 준비합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama exec ollama ollama pull gemma3:4b
docker compose -f '.\compose.full-stack.yml' --profile ollama exec ollama ollama list
```

**예상 결과:** 다운로드가 완료되고 목록에 `gemma3:4b`가 나타납니다.

**실패 시:** Ollama 시작 직후라면 서비스 준비 후 다시 시도합니다. 다운로드 연결, Docker 저장 공간과 메모리를 확인합니다. 이 구성에는 GPU 예약이 없으며, 모델 실행 속도와 필요한 자원은 현재 PC에서 미확인입니다.

변경한 Backend 환경변수를 반영합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama up -d --force-recreate backend frontend

Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready' |
    ConvertTo-Json -Depth 6
```

**예상 결과:** 저장소 준비 상태가 정상이고 `checks.providers.ollama`가 `true`입니다. 실제 모델 호출 확인은 다음 화면 요청으로 합니다.

브라우저에서 다음을 수행합니다.

1. 사이드바의 **실제 LLM Provider**를 `ollama`로 선택합니다.
2. **Ollama Model**을 `gemma`로 선택합니다.
3. **Multi-LLM Chat**에서 `부산 2박 3일 여행 준비물을 세 가지 알려줘`를 전송합니다.
4. 여행 준비 답변과 `Provider: ollama`, 설정한 모델명, `Fallback: False`를 확인합니다.
5. 이어서 `비가 오면 무엇을 추가하면 좋을까?`를 전송해 최근 대화를 활용하는지 살펴봅니다. 답변 문장 자체는 매번 달라질 수 있습니다.

**실패 시:** `OLLAMA_ENABLED`, 다운로드한 모델 태그, Backend·Ollama 로그를 순서대로 확인합니다. 소스의 Ollama 요청 제한 시간은 90초, Frontend의 API 요청 제한 시간은 100초입니다.

저장 이력을 확인하려면 화면 사이드바의 세션 ID를 A창에 입력합니다.

```powershell
$sessionId = Read-Host '화면 사이드바의 session-으로 시작하는 세션 ID를 입력하세요'

Invoke-RestMethod -Uri ('http://127.0.0.1:8000/api/chat/' + $sessionId) |
    ConvertTo-Json -Depth 6
```

**예상 결과:** 성공한 채팅마다 `user`와 `assistant` 메시지가 저장됩니다.

그다음 화면의 **새 대화 시작**을 누르면 새 세션 ID가 표시됩니다. 같은 A창에서 위 이력 조회 명령을 다시 실행하면, 변수에 보관한 이전 세션의 PostgreSQL 이력은 남아 있습니다. 버튼은 이전 Redis 세션을 지우며 PostgreSQL 이력을 삭제하지 않습니다.

다음 모델로 비교하려면 같은 A창에서 Llama를 다운로드합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' --profile ollama exec ollama ollama pull llama3.2
docker compose -f '.\compose.full-stack.yml' --profile ollama exec ollama ollama list
```

**예상 결과:** `llama3.2`가 목록에 추가됩니다. `.env`의 `OLLAMA_MODEL`과 일치하는지 확인한 후 화면에서 `llama`를 선택해 같은 질문을 비교합니다.

실습 종료는 Docker D5의 Full Stack 종료 명령을 사용합니다.

### E3. OpenAI·Gemini로 Provider 비교하기

**목적:** 같은 화면에서 Backend가 다른 외부 모델 제공자를 호출하는 과정을 확인합니다.

**선행 조건:** 선택할 서비스의 API 키와 사용 가능한 모델을 사용자가 준비해야 합니다. 소스의 모델 기본값은 현재 계정의 사용 가능 여부를 보장하지 않습니다.

**작업 폴더·창:** 루트 `.env`를 편집한 뒤 A창에서 반영합니다.

- OpenAI: `OPENAI_API_KEY`, `OPENAI_MODEL`
- Gemini: `GEMINI_API_KEY`, `GEMINI_MODEL`

Full Stack을 사용 중이면 다음 명령을 사용합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' up -d --force-recreate backend frontend
```

**예상 결과:** Backend가 새 환경변수로 다시 생성됩니다. 화면에서 해당 Provider를 선택하고 E2와 같은 질문을 보냅니다. 성공 응답에 선택한 Provider·모델이 표시되어야 합니다.

**실패 시:** `checks.providers`가 `false`면 키 전달부터 확인합니다. `true`인데 요청이 실패하면 실제 API 인증, 모델 이름·접근 권한, 사용 한도와 연결 오류를 확인합니다. Provider 오류를 Mock 답변으로 바꾸지 않습니다.

공용 서비스 경로를 사용 중이라면 위 명령의 Compose 파일을 `compose.yml`로 바꾸고, 종료도 그 파일의 `down`을 사용합니다.

### E4. 이미지를 다른 PC에 전달하기

이 절은 로컬 실행 완료 후의 **선택 배포 실습**입니다. GitHub Actions 자동 배포는 구성되어 있지 않습니다.

#### 운영자: 이미지 게시

**목적:** Backend·Frontend 이미지를 레지스트리에 게시합니다.

**선행 조건:** 사용자가 Docker Hub 계정 또는 조직과 게시 권한을 준비해야 합니다. 아래는 README의 Docker Hub 흐름을 따르는 예시입니다.

**작업 폴더·창:** 프로젝트 루트, A창.

```powershell
docker compose -f '.\compose.yml' build backend frontend
docker image ls
```

**예상 결과:** 기본 Compose 프로젝트 이름에 따른 `simple-multi-llm-app-backend`, `simple-multi-llm-app-frontend` 이미지가 보입니다.

**실패 시:** 빌드 결과와 실제 이미지 이름을 확인합니다. 아래 태그 명령의 원본 이름이 목록과 다르면 실제 이름으로 먼저 수정합니다.

이후 게시 대상 계정을 입력하고 로그인합니다.

```powershell
$registryAccount = Read-Host '게시 권한이 있는 실제 Docker Hub 사용자명 또는 조직명을 입력하세요'
docker login
```

**예상 결과:** 사용자가 선택한 계정으로 로그인됩니다. 이메일 주소가 아니라 이미지 경로에 사용할 사용자명·조직명을 입력합니다.

로그인과 대상 권한을 확인한 뒤 게시합니다.

```powershell
docker tag 'simple-multi-llm-app-backend:latest' "$registryAccount/simple-multi-llm-backend:1.0.0"
docker tag 'simple-multi-llm-app-frontend:latest' "$registryAccount/simple-multi-llm-frontend:1.0.0"

docker push "$registryAccount/simple-multi-llm-backend:1.0.0"
docker push "$registryAccount/simple-multi-llm-frontend:1.0.0"
```

**예상 결과:** 두 이미지의 업로드가 완료됩니다.

**실패 시:** 원본 이미지 존재 여부, 로그인 계정과 게시 대상의 일치 여부, 저장소 쓰기 권한을 확인합니다. `.env`와 API 키는 전달하지 않습니다.

#### 수신자: 배포 이미지 실행

**목적:** 소스 빌드 없이 전달받은 앱 이미지를 실행합니다.

**선행 조건:**

- 실제 게시된 두 이미지 주소와 태그를 전달받아야 합니다.
- 공용 PostgreSQL·Redis와 전용 스키마가 준비되어 있어야 합니다.
- Ollama를 사용할 경우 수신자 측 공용 Ollama와 모델도 별도로 필요합니다.
- 다른 구성으로 같은 앱을 실행 중이면 그 구성의 종료 절차를 먼저 수행합니다.

루트 `.env`에서 `BACKEND_IMAGE`, `FRONTEND_IMAGE`에 실제 이미지 주소를 입력합니다. 예제의 `<REGISTRY_ACCOUNT>`를 그대로 두면 안 됩니다. 비공개 이미지라면 수신자도 읽기 권한이 있는 계정으로 해당 레지스트리에 로그인해야 합니다.

**작업 폴더·창:** 이 프로젝트 파일들이 있는 폴더, A창.

```powershell
docker compose -f '.\compose.release.yml' config --quiet
```

검사가 성공하면 내려받고 실행합니다.

```powershell
docker compose -f '.\compose.release.yml' pull
```

`pull`이 성공한 뒤 다음을 실행합니다.

```powershell
docker compose -f '.\compose.release.yml' up -d
docker compose -f '.\compose.release.yml' ps
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready'
```

**예상 결과:** 전달된 이미지가 이 소스와 같은 계약을 구현했다면 readiness가 성공하고 `http://127.0.0.1:8501`에서 E1 실습을 할 수 있습니다. 실제 레지스트리 이미지의 존재와 내용은 이번 확인 범위 밖입니다.

**실패 시:** 이미지 주소·태그·읽기 권한 → 공용 저장소 연결 → 스키마 순서로 확인합니다.

종료는 같은 A창에서 수행합니다.

```powershell
docker compose -f '.\compose.release.yml' down
docker compose -f '.\compose.release.yml' ps -a
```

**예상 결과:** Release 구성의 앱 컨테이너가 종료됩니다. 공용 저장소는 유지됩니다.

## 검증과 문제 해결

### 구성 요소별 완료 기준

| 확인 대상 | 확인 방법 | 기대 결과와 해석 |
| --- | --- | --- |
| Backend 프로세스 | `GET /health/live` | `status: ok`. DB·LLM 성공을 의미하지 않음 |
| Redis·DB·스키마 | `GET /health/ready` | HTTP 200과 관련 checks `true` |
| 상세 상태 | `GET /health` | 저장소 문제 시 `status: degraded`; 이 경로 자체는 HTTP 200을 반환할 수 있음 |
| Frontend | 구성에 맞는 브라우저 주소 | 세 탭과 Provider 선택 화면 표시 |
| 메모 저장 | E1의 저장·조회 | PostgreSQL에 행 저장, 정상 Redis이면 통계 증가 |
| 모델 호출 | E2 또는 E3의 질문 | 실제 답변과 Provider·모델 표시 |
| 채팅 이력 | `GET /api/chat/{session_id}` | 성공한 대화의 user·assistant 메시지 |
| 세션 초기화 | 화면의 새 대화 시작 | 새 ID 생성, 이전 PostgreSQL 이력 유지 |
| 종료 | 사용한 Compose 파일의 `down`, `ps -a` | 해당 프로젝트의 컨테이너 없음 |

`backend/test_app.py`는 Provider 상태, 선택한 Provider·대화 저장 계약, 미설정 Provider의 503 응답을 검사합니다. 테스트의 Fake 클래스는 실제 앱의 키 없는 채팅 모드가 아닙니다. 테스트 파일을 읽었지만 실행하지 않았습니다.

### 증상별 해결 순서

| 증상 | 원인 후보 | 확인 위치·다음 행동 |
| --- | --- | --- |
| Docker 명령을 찾지 못함 | 설치 또는 PATH 준비 문제 | Docker Desktop 설치 확인 후 PowerShell 다시 열기 |
| Docker Server 연결 실패 | 엔진 미시작, Linux 컨테이너 환경 미준비 | Docker Desktop 상태, 선택한 WSL 2 환경 확인 |
| 포트 사용 중 오류 | 다른 앱 또는 다른 Compose 경로와 중복 실행 | 아래 포트 확인 후 자신이 시작한 구성만 정상 종료 |
| 기본 구성에서 8501 화면이 안 열림 | README와 실제 포트 차이 | `compose.yml`은 `http://127.0.0.1` 사용 |
| Frontend가 생성되지 않음 | Backend healthcheck 실패 | Backend `/health`와 DB·Redis 로그부터 확인 |
| `database=false` | 잘못된 주소·계정·비밀번호·DB 이름 | 실행 구성에 맞는 URL, 기존 볼륨의 최초 인증값 확인 |
| `database=true`, `database_schema=false` | 기존 DB에 전용 테이블이 없음 | 공용 구성은 `init_database.py`, Full Stack은 아래 SQL 복구 절차 |
| `redis=false` | Redis 미실행 또는 주소 오류 | Full Stack의 `redis` 서비스와 `REDIS_URL` 확인 |
| 화면은 열리지만 API 연결 실패 | `BACKEND_URL` 오류 또는 Backend 미실행 | Compose에서는 `http://backend:8000`; `API_BASE_URL`은 사용하지 않음 |
| `ModuleNotFoundError: dotenv` 또는 `psycopg` | 초기화용 venv 의존성 누락 | PowerShell 절의 venv Python으로 의존성 설치 |
| venv를 만들었는데 다른 Python 사용 | 전역 Python 호출 또는 잘못된 경로 | `& '.\.venv\Scripts\python.exe'` 직접 호출 |
| Provider 미설정 503 | 키 누락 또는 Ollama 비활성화 | `.env`, Compose의 Backend 환경, `checks.providers` 확인 |
| Ollama 모델 없음·시간 초과 | 다운로드 태그 불일치, 모델 미준비, 자원 부족 | 모델 목록, `GEMMA_MODEL`·`OLLAMA_MODEL`, Backend·Ollama 로그 |
| `.env` 변경이 반영되지 않음 | 기존 컨테이너 환경 유지 | 사용한 Compose 파일로 `up -d --force-recreate backend frontend` |
| 소스 변경이 반영되지 않음 | 소스가 이미지에 복사되는 구조 | 사용한 Compose 파일로 `up -d --build --force-recreate backend frontend` |
| 메모는 보이는데 요청이 오류였음 | DB 저장 후 Redis 단계 실패 | 응답의 `warning`과 Redis 상태 확인 |

채팅도 단계별로 DB에 기록합니다. 모델 호출이나 후속 Redis 처리가 실패하면 사용자 메시지 등 일부 기록이 남을 수 있습니다. 오류 후 재전송하기 전에 현재 세션 이력을 확인하세요.

### 포트 충돌 확인

**목적:** 어떤 프로세스가 앱 포트를 사용 중인지 확인합니다.

**작업 폴더·창:** 프로젝트 루트, A창.

```powershell
Get-NetTCPConnection -State Listen |
    Where-Object { $_.LocalPort -in @(80, 8000, 8501) } |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

**예상 결과:** 사용 중인 포트와 PID가 표시됩니다. 결과가 없으면 해당 포트에서 대기하는 연결이 발견되지 않은 것입니다.

**실패 시·다음 행동:** Docker의 `ps` 결과와 함께 자신이 실행한 앱인지 확인합니다. Project Player에서 시작한 앱은 Player의 종료 기능을 사용하거나, 실제 사용한 Compose 구성으로 종료합니다. 다른 프로세스를 일괄 종료하지 않습니다.

### 기존 Full Stack DB의 스키마 누락 복구

**목적:** 데이터 볼륨을 삭제하지 않고 이 앱의 누락된 스키마·테이블을 생성합니다.

**선행 조건:** `/health`에서 DB 연결은 성공하지만 `database_schema=false`이며, 적용할 DB가 이 실습 대상임을 확인해야 합니다.

**작업 폴더·창:** 프로젝트 루트, A창. 아래 `agent_user`, `agent_db`는 제안한 개발 이름입니다. 실제 `.env`의 사용자·DB 이름이 다르면 **명령을 먼저 수정**하세요.

```powershell
Get-Content -LiteralPath '.\database\init.sql' -Raw |
    docker compose -f '.\compose.full-stack.yml' exec -T database psql -U agent_user -d agent_db -v ON_ERROR_STOP=1
```

**예상 결과:** 스키마·테이블·인덱스 생성 결과 또는 이미 존재한다는 안내가 나옵니다. 현재 SQL은 `CREATE ... IF NOT EXISTS`로 구성되어 있습니다.

성공한 뒤 앱 시작과 준비 상태를 다시 확인합니다.

```powershell
docker compose -f '.\compose.full-stack.yml' up -d backend frontend
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health/ready'
```

**실패 시:** 사용자·DB 이름, 스키마 생성 권한과 SQL 오류를 확인합니다. 기존 테이블의 열 구조가 다르면 이 초기화 SQL만으로 수정되지 않으므로 별도 구조 검토가 필요합니다.

### 장애 사례를 읽는 다음 순서

정상 실습 후 `COMPOSE_EXPLAINED.md`에서 서비스 주소와 초기화 시점을 정리하고, `TROUBLESHOOTING.md`를 읽습니다. 이 읽기 단계는 실행 불필요입니다.

코드상 장애 영향은 다음과 같습니다.

- Redis 장애: 기존 PostgreSQL 메모·채팅 이력 조회는 가능하지만 새 채팅과 통계는 실패할 수 있습니다.
- PostgreSQL 장애: 메모·영구 이력·새 채팅이 실패하고 Redis 통계는 조회될 수 있습니다.
- Backend 장애: Streamlit 화면이 열려도 API 동작은 연결 오류가 됩니다.

공용 저장소를 장애 실습 목적으로 중단하지 않습니다. 장애 재현을 추가로 진행한다면 해당 문서가 지정한 독립 Full Stack 구성을 사용합니다.

## 근거와 미확인 사항

### 주요 실행 근거

| 내용 | 실제 상대 경로·심벌 또는 설정 키 |
| --- | --- |
| 기본 구성의 앱 전용 실행·화면 80번 | `compose.yml`: `name`, `services`, `frontend.ports` |
| 전체 서비스·프로필·의존 순서 | `compose.full-stack.yml`: `profiles`, `depends_on`, `healthcheck` |
| DB 초기화·영속 저장 | `compose.full-stack.yml`: `database.volumes`, 최상위 `volumes`; `database/init.sql` |
| Release 이미지 필수 입력 | `compose.release.yml`: `backend.image`, `frontend.image`의 `${...:?}` |
| Python 버전·서버 진입점 | `backend/Dockerfile`, `frontend/Dockerfile`: `FROM`, `CMD` |
| 패키지 설치 범위 | `backend/requirements.txt`, `frontend/requirements.txt` |
| 환경변수 예제 | `.env.example`; 민감한 값은 인용하지 않음 |
| Host DB 주소 결정 | `init_database.py`: `host_database_url()`, `load_dotenv(ENV_PATH)` |
| Frontend → Backend 연결 | `frontend/app.py`: `BACKEND_URL`, `api()` |
| 화면에서 호출하는 API | `frontend/app.py`: `/health`, `/api/notes`, `/api/chat`, `/api/chat/{session_id}`, `/api/sessions/{session_id}` |
| 상태 응답·503 판정 | `backend/app.py`: `live()`, `health()`, `ready()` |
| DB·Redis 사용 | `backend/services.py`: `PostgresRepository`, `RedisSessionStore` |
| Provider 선택·실제 호출 | `backend/services.py`: `configured()`, `model()`, `reply()` |
| 테스트 범위 | `backend/test_app.py`: Fake 의존성과 세 테스트 함수 |
| 구성 설명·학습 순서 | `README.md`, `COMPOSE_EXPLAINED.md`, `TROUBLESHOOTING.md` |
| 기존 사용자 안내 | `guide.md` |
| GitHub Actions | 선택 폴더의 `.github/workflows` 없음. 실제 Git 저장소 루트 확인 실패 |

### 관찰한 사실과 정적 분석의 구분

**파일 확인으로 관찰한 사실:**

- 선택한 프로젝트 루트와 위 소스·문서·설정 파일이 존재합니다.
- `.env`는 존재하며 루트 `.venv`는 확인 당시 없었습니다.
- 선택 폴더와 확인한 상위 경로에서 적용할 로컬 `AGENTS.md` 파일은 발견하지 못했습니다. 대화로 제공된 작업 지침을 적용했습니다.
- 별도 `SETUP.md`, `package.json`, 확인 대상 잠금 파일, workflow는 발견하지 못했습니다.

**설정과 코드에서 확인한 예상 동작:**

- 기본 Compose의 화면 포트는 80번이며 Full Stack·Release는 8501번입니다.
- Full Stack은 내부 서비스 이름으로 저장소에 연결합니다.
- readiness는 Redis·DB·스키마를 검사하며 실제 LLM 호출은 검사하지 않습니다.
- API 키 없는 메모 실습과 Ollama를 사용하는 키 없는 채팅 경로가 있습니다.
- 시작·종료 명령과 기대 응답은 정적 분석에 근거하며 실제 실행 결과가 아닙니다.

### 미실행 사항과 남은 사용자 입력

이번 문서 작성에서는 파일을 생성·수정하지 않았고, 앱 import, 패키지 설치, Python 스크립트·테스트, Docker 명령, 서버 시작·종료, DB 변경, 이미지 게시, workflow 실행과 배포를 수행하지 않았습니다.

실제 `.env` 내용, 인증 저장소, 토큰·개인키, 사용자 데이터와 `debug.log` 등 로그는 읽지 않았습니다. 제외 대상 디렉터리의 내용과 확인 범위 밖의 형제 프로젝트 소스도 읽지 않았습니다.

사용자가 다음으로 준비하거나 확인할 항목은 다음과 같습니다.

- Docker Desktop·엔진과 필요한 경우 Python 3.12
- Player가 실행할 실제 Compose 파일
- 새 PostgreSQL용 설정 또는 기존 공용 DB·Redis의 정확한 접속 정보
- Ollama 모델을 실행할 저장 공간·메모리와 다운로드한 태그
- 외부 Provider를 사용할 경우 본인의 API 키와 사용 가능한 모델
- 이미지 전달을 할 경우 실제 레지스트리 주소·태그·권한
- CI를 학습할 경우 원본 Git 저장소와 workflow를 둘 정확한 경로

현재 폴더에서 E1 → E2 → 종료까지 완료한 뒤 구성 비교와 이미지 전달로 진행하면 됩니다. 다음 번호의 형제 프로젝트 경로는 이 폴더의 확인한 문서에 명시되어 있지 않아 **미확인**입니다. Project Player에서 상위 과정 목록을 확인하고, 다음 프로젝트를 선택한 뒤 그 폴더의 소스와 실행 지침을 새로 확인하세요.

**이 가이드는 실행 준비 문서이며 서버 구동 성공이나 CI 통과를 보고하는 문서가 아닙니다.**
<!-- PLAYER_SETUP_GUIDE_END -->
